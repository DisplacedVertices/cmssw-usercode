import sys
from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver(plot_dir('v0bkgsub'), size=(600,600))

f = ROOT.TFile(sys.argv[1])
ex = sys.argv[2] if len(sys.argv) >= 3 else ''
h = f.Get('v0eff%s/K0_2pi/h_vtx_mass' % ex)
h.Sumw2()

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
res.Print('V')
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
for lo in [7]: #xrange(50):
    ibinlo = ibinc - lo
    xlo = xax.GetBinLowEdge(ibinlo)
    for hi in [7]: #xrange(50):
        ibinhi = ibinc + hi
        xhi = xax.GetBinLowEdge(ibinhi+1)
        ne, be = ROOT.Double(), ROOT.Double()
        n = h.IntegralAndError(ibinlo, ibinhi, ne)
        b = hbkg.IntegralAndError(ibinlo, ibinhi, be)
        s = n - b
        se = (ne**2 + be**2)**0.5
        z = s / (b + be**2)**0.5
        p = s/n
        if (s > max_s or p > max_p or z > max_z) and p > 0.85:
            print '%.3f-%.3f: %10.1f +- %5.1f  %10.1f +- %5.1f  %10.1f +- %5.1f : %5.2f : %5.1f' % (xlo, xhi, n, ne, b, be, s, se, p, z)
        if s > max_s:
            max_s = s
        if p > max_p:
            max_p = p
        if z > max_z:
            max_z = z

hbkglo = f.Get('v0effbkglo/K0_2pi/h_vtx_rho')
hbkghi = f.Get('v0effbkghi/K0_2pi/h_vtx_rho')
hon = f.Get('v0effon/K0_2pi/h_vtx_rho')
z = hon.GetXaxis().FindBin(1.9)

for i,h in enumerate((hbkghi, hbkglo, hon)):
    h.Scale(1/h.Integral(0,z))
    h.SetLineColor(2+i)
    h.Rebin(10)
    h.SetLineWidth(2)
    if i == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')
ps.save('rhocmp')

hbkghi = f.Get('v0effbkghi/K0_2pi/h_vtx_rho')
hon = f.Get('v0effon/K0_2pi/h_vtx_rho')
z = hon.GetXaxis().FindBin(1.9)

for i,h in enumerate((hbkghi, hon)):
    if h == hbkghi:
        h.Scale(23593./h.Integral(0,z))
    h.SetLineColor(2+i)
    h.Rebin(10)
    h.SetLineWidth(2)
    if i == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')
ps.save('rhocmp')
