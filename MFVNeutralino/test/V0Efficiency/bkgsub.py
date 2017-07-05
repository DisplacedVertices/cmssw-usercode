import sys, os
from JMTucker.Tools.ROOTTools import *
set_style()

in_fn = sys.argv[1]
ex = sys.argv[2] if len(sys.argv) >= 3 else ''
out_fn = os.path.basename(in_fn)
if in_fn == out_fn or os.path.exists(out_fn):
    raise IOError('refusing to clobber existing file %s' % out_fn)

sample = out_fn.replace('.root', '')

ps = plot_saver(plot_dir('v0bkgsub/' + sample), size=(600,600))

# fit for s and b using sidebands

in_f = ROOT.TFile(in_fn)
h = in_f.Get('v0eff%s/K0_2pi/h_vtx_mass' % ex)

# must keep these numbers in sync with histos!
fit_range = 0.38, 0.6 
fit_exclude = 0.44, 0.55

def fitfunc(x, p):
    x = x[0]
    if x >= fit_exclude[0] and x <= fit_exclude[1]:
        ROOT.TF1.RejectPoint()
        return 0.
    return p[0] + p[1] * x

fcn = ROOT.TF1('fcn', fitfunc, fit_range[0], fit_range[1], 2)

res = h.Fit(fcn, 'WL R N S Q')
res.Print()
print 'Chi2 Prob:', res.Prob()

fit_pars = fcn.GetParameter(0), fcn.GetParameter(1)
fit_errs = fcn.GetParError(0), fcn.GetParError(1)

fdraw = ROOT.TF1('fdraw', 'pol2', *fit_range)
fdraw.SetParameters(*fit_pars)

h.Draw('hist e')
h.SetStats(0)
h.GetXaxis().SetRangeUser(0.28,0.9)
h.GetYaxis().SetLabelSize(0.025)
h.GetYaxis().SetTitleOffset(1.5)
fdraw.Draw('same')
ps.save('mass_fit')

# draw the fit residuals

xax = h.GetXaxis()
hbkg = ROOT.TH1F('hbkg', h.GetTitle(), h.GetNbinsX(), xax.GetXmin(), xax.GetXmax())
hres = h.Clone('hres')
xax = hres.GetXaxis()
xax.SetRangeUser(*fit_range)
for ibin in xrange(xax.FindBin(fit_range[0]), xax.FindBin(fit_range[1])):
    xlo = xax.GetBinLowEdge(ibin)
    xhi = xax.GetBinLowEdge(ibin+1)
    xmd = (xlo + xhi)/2
    w = xhi - xlo
    c  = hres.GetBinContent(ibin)
    ce = hres.GetBinError(ibin)
    i  = fdraw.Integral(xlo, xhi) / w
    ie = (fit_errs[0]**2 + fit_errs[1]**2 * xmd**2)**0.5
    r = (i - c) / i
    re = (ie**2 + ce**2)**0.5 / i
    #print i, ie, c, ce, r
    hbkg.SetBinContent(ibin, i)
    hbkg.SetBinError(ibin, ie)
    if fit_exclude[0] <= xmd <= fit_exclude[1]:
        r, re = 0, 0
    hres.SetBinContent(ibin, r)
    hres.SetBinError(ibin, re)

hres.GetYaxis().SetTitle('fit residual')
hres.Fit('pol1')
ps.save('res', log=False)

# scan mass window for best yield, purity, and significance z = s/sqrt(b + sigb^2)
# -- but mass window is fixed in histos to 490-505 MeV, so if you want to change it you have to do it there and rerun histos

h.Draw('hist e')
hbkg.SetLineColor(ROOT.kOrange+2)
hbkg.Draw('hist same')
ps.save('wbkg')

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
        if (s > max_s or p > max_p or z > max_z) and p > 0.85:
            do(lo,hi,True)
        if s > max_s:
            max_s = s
        if p > max_p:
            max_p = p
        if z > max_z:
            max_z = z
print
xlo,xhi,n,ne,b,be,s,se,p,z = do(7,7, True) # print the one we're using
assert abs(xlo-0.490) < 1e-5 and abs(xhi-0.505) < 1e-5 # check that we're in sync with histos

out_f = ROOT.TFile(out_fn, 'recreate')
integ = lambda h: h.Integral(0,h.GetNbinsX()+2)

# do the bkg subtraction in whatever variables you want as long as the histos exist
# written out to file in folders so the cmp script can do the rest

colors = (2,3,4,6)
variables = [
    ('h_vtx_rho', 1, 10, (0,2)),
    ('h_track_dxybs', 2, 10, (-0.5,0.5)),
    ]

for hname, integ_factor, rebin, x_range in variables:
    hon = in_f.Get('v0effon%s/K0_2pi/' % ex + hname)
    hbkglo = in_f.Get('v0effbkglo%s/K0_2pi/' % ex + hname)
    hbkghi = in_f.Get('v0effbkghi%s/K0_2pi/' % ex + hname)

    d = out_f.mkdir(hname)
    d.cd()
    hon = hon.Clone('hon')
    hbkglo = hbkglo.Clone('hbkglo')
    hbkghi = hbkghi.Clone('hbkghi')
    hbkg = hbkglo.Clone('hbkg')
    hbkg.Add(hbkghi)
    hsig = [hon.Clone(name) for name in 'hsiglo', 'hsighi', 'hsig']
    hoth = [hbkglo, hbkghi, hbkg, hon]

    for i,h in enumerate(hoth + hsig):
        h.Rebin(rebin)
        h.SetLineWidth(2)
        h.SetLineColor(colors[i-len(hoth) if h in hsig else i])
        h.SetStats(0)
        h.GetXaxis().SetRangeUser(*x_range)

    for i,h in enumerate(reversed(hoth)):
        hint = integ(h)
        if i == 0:
            if abs(hint - integ_factor * n) > 1e-5:
                print 'hint', hint, 'n', n
                raise ValueError('duh?')
            h.Draw('hist')
        else:
            h.Scale(b/hint)
            hsig[i-1].Add(h, -1)
            h.Draw('hist same')
    ps.save(hname + '_cmp')

    for i,h in enumerate(hsig):
        h.Draw('hist e' if i == 0 else 'hist e same')
    ps.save(hname + '_sig')

# copy over normalization hist

h = in_f.Get('mfvWeight/h_sums').Clone('h_sums')
h.SetDirectory(out_f.mkdir('mfvWeight'))

out_f.Write()
out_f.Close()
