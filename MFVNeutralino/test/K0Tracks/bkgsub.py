import sys, os
from JMTucker.Tools.ROOTTools import *
set_style()

batch = sys.argv[1]
in_fn = sys.argv[2]
in_bn = os.path.basename(in_fn)
os.system('mkdir %s' % batch)
out_fn = os.path.join(batch, in_bn)
sample = in_bn.replace('.root', '')

ps = plot_saver(plot_dir('v0bkgsub_%s/%s' % (batch, sample)), size=(600,600))

# fit for s and b using sidebands

in_f = ROOT.TFile(in_fn)
in_f.Get('massall/h_nvtx').Draw()
ps.save('nvtx')

h = in_f.Get('massall/h_mass')

# must keep these numbers in sync
fit_range = 0.420, 0.580
fit_exclude = 0.475, 0.525

npars = 3 # 2 if sample.startswith('ZeroBias') else 3
while 1:
    print 'npars', npars
    def fitfunc(x, p):
        x = x[0]
        if x >= fit_exclude[0] and x <= fit_exclude[1]:
            ROOT.TF1.RejectPoint()
            return 0.
        return sum(p[i] * x**i for i in xrange(npars))

    fcn = ROOT.TF1('fcn', fitfunc, fit_range[0], fit_range[1], npars)

    res = h.Fit(fcn, 'WL R N S Q')
    res.Print()
    print 'Chi2 Prob                 =', res.Prob()

    if npars == 3 and fcn.GetParameter(2) > 0:
        print 'fit wants positive quadratic term, trying again with linear fit'
        npars = 2
    else:
        break

fit_pars = [fcn.GetParameter(i) for i in xrange(npars)]
fit_errs = [fcn.GetParError(i) for i in xrange(npars)]

fdraw = ROOT.TF1('fdraw', 'pol%i' % (npars-1), *fit_range)
fdraw.SetParameters(*fit_pars)

# calc fit residuals

xax = h.GetXaxis()
hbkg = ROOT.TH1F('hbkg', h.GetTitle(), h.GetNbinsX(), xax.GetXmin(), xax.GetXmax())
hres = h.Clone('hres')
xax = hres.GetXaxis()
xax.SetRangeUser(*fit_range)
maxr = 0
for ibin in xrange(xax.FindBin(fit_range[0]), xax.FindBin(fit_range[1])):
    xlo = xax.GetBinLowEdge(ibin)
    xhi = xax.GetBinLowEdge(ibin+1)
    xmd = (xlo + xhi)/2
    w = xhi - xlo
    c  = hres.GetBinContent(ibin)
    ce = hres.GetBinError(ibin)
    i  = fdraw.Integral(xlo, xhi) / w
    ie = fdraw.IntegralError(xlo, xhi) / w
    r = (i - c) / i
    re = ce / i # (ie**2 + ce**2)**0.5 / i
    hbkg.SetBinContent(ibin, i)
    hbkg.SetBinError(ibin, ie)
    if fit_exclude[0] <= xmd <= fit_exclude[1]:
        r, re = 0, 0
    #print i, ie, c, ce, r, re
    maxr = max(maxr, abs(r)+re)
    hres.SetBinContent(ibin, r)
    hres.SetBinError(ibin, re)

h.Draw('hist e')
h.SetStats(0)
h.GetXaxis().SetRangeUser(0.28,1.3)
h.GetYaxis().SetLabelSize(0.025)
h.GetYaxis().SetTitleOffset(1.5)
fdraw.Draw('same')

insert = ROOT.TPad("insert","insert",0.431, 0.671, 0.863, 0.869)
insert.SetRightMargin(0.01)
insert.SetLeftMargin(0.15)
insert.SetTopMargin(0.01)
insert.SetBottomMargin(0.01)
insert.Draw()
insert.cd()
hres.GetYaxis().SetTitle('fit residual')
hres.GetYaxis().SetLabelSize(0.065)
hres.GetXaxis().SetLabelSize(0.065)
hres.GetYaxis().SetTitleSize(0.08)
hres.GetXaxis().SetTitleSize(0.08)
hres.GetYaxis().SetTitleOffset(0.75)
hres.GetYaxis().SetRangeUser(-maxr*1.05, maxr*1.05)
hres.SetStats(0)
hres.Fit('pol1')
ps.c.cd()
ps.save('mass_fit')
del insert

# scan mass window for best yield, purity, and significance z = s/sqrt(b + sigb^2)
# -- but mass window is now fixed in histos to 490-505 MeV, so if you want to change it you have to do it there and rerun hists

xax = h.GetXaxis()
ibinc = xax.FindBin(0.4976)
max_s, max_p, max_z = 0, 0, 0
def do(lo,hi,prnt=False):
    ibinlo = ibinc - lo
    ibinhi = ibinc + hi
    xlo = xax.GetBinLowEdge(ibinlo)
    xhi = xax.GetBinLowEdge(ibinhi+1)
    ne, be = ROOT.Double(), ROOT.Double()
    n = h.IntegralAndError(ibinlo, ibinhi, ne)
    b = hbkg.IntegralAndError(ibinlo, ibinhi, be)
    s = n - b
    se = (ne**2 + be**2)**0.5
    z = s / (b + be**2)**0.5
    p = s/n
    if prnt:
        print '%.3f-%.3f: %10.1f +- %5.1f  %10.1f +- %5.1f  %10.1f +- %5.1f : %5.2f : %5.1f' % (xlo, xhi, n, ne, b, be, s, se, p, z)
    return xlo,xhi,n,ne,b,be,s,se,p,z

for lo in xrange(50):
    for hi in xrange(50):
        xlo,xhi,n,ne,b,be,s,se,p,z = do(lo,hi)
        if (s > max_s or p > max_p or z > max_z) and p >= 0.85:
            do(lo,hi,True)
        if s > max_s:
            max_s = s
        if p > max_p:
            max_p = p
        if z > max_z:
            max_z = z
print
xlo,xhi,n,ne,b,be,s,se,p,z = do(1,1, True) # print the one we're using
the_b = b
assert abs(xlo-0.490) < 1e-5 and abs(xhi-0.505) < 1e-5 # check that we're in sync with histos

out_f = ROOT.TFile(out_fn, 'recreate')

def is_th2(h):
    return issubclass(type(h), ROOT.TH2)

def integ(h):
    if is_th2(h):
        return h.Integral(0,h.GetNbinsX()+2,0,h.GetNbinsY()+2)
    else:
        return h.Integral(0,h.GetNbinsX()+2)

# do the bkg subtraction in whatever variables you want as long as the hists exist
# written out to file in folders so the cmp script can do the rest

scans = True
variables = [
    ('h_rho', 1, 1, (0,2), 0),
    ('h_pt', 1, 1, None, 0),
    ('h_eta', 1, 1, None, 0),
    ('h_phi', 1, 1, None, 0),
    ('h_costh3', 1, 1, None, 0),
    ('h_costh2', 1, 1, None, 0),
    ('h_tracks_pt', 2, 1, None, 0),
    ('h_tracks_eta', 2, 1, None, 0),
    ('h_tracks_phi', 2, 1, None, 0),
    ('h_tracks_dxy', 2, 1, None, 0),
    ('h_tracks_absdxy', 2, 1, None, 0),
    ('h_tracks_dz', 2, 1, None, 0),
    ('h_tracks_dzpv', 2, 1, None, 0),
    ('h_tracks_dxyerr', 2, 1, None, 0),
    ('h_tracks_dszerr', 2, 1, None, 0),
    ('h_tracks_nsigmadxy', 2, 1, None, 0),
    ('h_tracks_npxlayers', 2, 1, None, 0),
    ('h_tracks_nstlayers', 2, 1, None, 0),
    ('h_tracks_dxyerr_v_pt', 2, None, (0, 40), 0),
    ]

for hname, integ_factor, rebin, x_range, scan_dir in variables:
    hon = in_f.Get('masson/%s' % hname)
    hbkglo = in_f.Get('masslo/%s' % hname)
    hbkghi = in_f.Get('masshi/%s' % hname)

    d = out_f.mkdir(hname)
    d.cd()
    hon = hon.Clone('hon')
    hbkglo = hbkglo.Clone('hbkglo')
    hbkghi = hbkghi.Clone('hbkghi')
    hbkg = hbkglo.Clone('hbkg')
    hbkg.Add(hbkghi)
    hsig = hon.Clone('hsig')

    if abs(integ(hon) - integ_factor * n) > 1e-5:
        raise ValueError('hint %s n %s' % (hint, n))

    hbkg.Scale(the_b / integ(hbkg))
    hsig.Add(hbkg, -1)
 
    for h,c in zip((hon, hbkg, hsig), (1, 4, 2)):
        h.SetLineColor(c)
        h.SetLineWidth(2)
        h.SetStats(0)
        if rebin:
            h.Rebin(rebin)
        if not is_th2(h) and x_range:
            h.GetXaxis().SetRangeUser(*x_range)

    if is_th2(hon):
        p_hon, p_hbkg, p_hsig = pfs = [h.ProfileX() for h in hon, hbkg, hsig]
        for p in pfs:
            p.SetLineWidth(2)
            p.SetStats(0)
            if x_range:
                p.GetXaxis().SetRangeUser(*x_range)
        p_hon.Draw('hist')
        p_hbkg.Draw('hist same')
        p_hsig.Draw('hist same')
    else:
        hon.Draw('hist e')
        hbkg.Draw('hist e same')
        hsig.Draw('hist e same')

    ps.save(hname)

    if scans and scan_dir:
        hsig_cumu, hbkg_cumu = [cumulative_histogram(h, 'ge' if scan_dir == 1 else 'le') for h in hsig, hbkg] 
        print hname
        max_z = 0
        for ibin in xrange(1, hsig.GetNbinsX()+1):
            s = hsig_cumu.GetBinContent(ibin)
            b = hbkg_cumu.GetBinContent(ibin)
            be = hbkg_cumu.GetBinError(ibin)
            if b > 0:
                p = s/(s+b)
                z = s/(b + be**2)**0.5
                print '%6.3f' % hsig.GetXaxis().GetBinLowEdge(ibin), 's = %10.1f' % s, 'b = %10.1f +- %6.1f' % (b,be), 'p = %.3f' % p, 'z = %4.1f' % z

    for h in hon, hbkg, hsig:
        h.Write()

# copy over normalization hist
h = in_f.Get('mfvWeight/h_sums').Clone('h_sums')
h.SetDirectory(out_f.mkdir('mfvWeight'))

#out_f.Write()
out_f.Close()
