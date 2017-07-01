import sys
from JMTucker.Tools.ROOTTools import *
set_style()

fn = sys.argv[1]
ex = '_' + sys.argv[2] if len(sys.argv) >= 3 else ''

ps = plot_saver(plot_dir('v0bkgsub%s' % ex), size=(600,600))

f = ROOT.TFile(fn)
h = f.Get('v0eff/K0_2pi/h_vtx_mass')

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
ps.save('duh')

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

h.Draw('hist e')
hbkg.SetLineColor(ROOT.kOrange+2)
hbkg.Draw('hist same')
ps.save('wbkg')

xax = h.GetXaxis()
ibinc, _ = real_hist_max(h, return_bin=True)
print 'ibinc', ibinc
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
xlo,xhi,n,ne,b,be,s,se,p,z = do(7,7, True)
assert abs(xlo-0.490) < 1e-5 and abs(xhi-0.505) < 1e-5

hbkglo = f.Get('v0effbkglo/K0_2pi/h_vtx_rho')
hbkghi = f.Get('v0effbkghi/K0_2pi/h_vtx_rho')
hon = f.Get('v0effon/K0_2pi/h_vtx_rho')

for i,h in enumerate((hbkglo, hbkghi, hon)):
    h.Rebin(10)
    h.SetLineWidth(2)
    h.SetLineColor(2+i)
    h.SetStats(0)
    h.GetXaxis().SetRangeUser(0,2.5)

hsiglo = hon.Clone('hsiglo')
hsighi = hon.Clone('hsighi')
hsiglo.SetLineColor(2)
hsighi.SetLineColor(3)
hsig = hsiglo, hsighi

for i,h in enumerate((hon, hbkglo, hbkghi)):
    hint = h.Integral(0,h.GetNbinsX()+2)
    if i == 0:
        assert abs(hint - n) < 1e-5
    else:
        h.Scale(b/hint)
        hsig[i-1].Add(h, -1)
 
    if i == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')
ps.save('rhocmp')

hsiglo.Draw('hist e')
hsighi.Draw('hist e same')
ps.save('sig')

fout = ROOT.TFile('bkgsub.root', 'recreate')
for x in hon, hbkglo, hbkghi, hsiglo, hsighi:
    x.Write()
fout.Write()
fout.Close()
