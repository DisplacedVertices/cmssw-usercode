import sys
from array import array
from JMTucker.Tools.ROOTTools import *
import JMTucker.MFVNeutralino.AnalysisConstants as ac

set_style()
rainbow_palette()

def arr(l):
    return array('d', l)

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

hs = []

def rebin(in_h):
    bins = arr([0, 0.02, 0.04, 0.06, 0.08, 0.1, 5])
    h = in_h.Rebin(len(bins) - 1, in_h.GetName() + '_rebin', bins)
    hs.append(h)
    return h

def rebook(in_h):
    assert type(in_h) == ROOT.TH1D
    nbins = in_h.GetNbinsX()
    assert nbins == 6
    asses = [None, 0, 0.02, 0.04, 0.06, 0.08, 0.1, 5]
    for ibin in xrange(1, nbins+2):
        assert abs(in_h.GetBinLowEdge(ibin) - asses[ibin]) < 1e-6

    bins = [j*0.2 for j in range(6)] + [2.]
    bins = arr(bins)
    h = ROOT.TH1D(in_h.GetName() + '_rebook', ';d_{VV} (mm);events', len(bins)-1, bins)
    hs.append(h)
    h.Sumw2()
    h.SetStats(0)
    h.SetLineWidth(2)
    print h.GetName()
    for ibin in xrange(0, nbins+2):
        c = in_h.GetBinContent(ibin)
        e = in_h.GetBinError  (ibin)
        print ibin, c, e
        h.SetBinContent(ibin, c)
        h.SetBinError  (ibin, e)

    yax = h.GetYaxis()
    yax.SetTitleOffset(1.15)
    yax.SetRangeUser(0.1, 300)

    return h

f = ROOT.TFile('mfvo2t_forclosure.root')

def up_down(x, s):
    return (round((x + s)/5.)*5,
            round((x - s)/5.)*5)
def imu_isig(mu, sig):
    assert mu  % 5 == 0 and sig % 5 == 0
    imu, isig = mu/5, sig/5
    return 'ClearedJetsTemplater/seed0000_toy0000/templates/imu_%02i/h_template_imu%03i_isig%03i' % (imu, imu, isig)

mu_clear_up,  mu_clear_down  = up_down(293, 36)
sig_clear_up, sig_clear_down = up_down(115, 28)

h_mctoy   = rebook(rebin(f.Get('Fitter/seed00_toy00/fit_results/h_data_b_fit_nobb_nodiv')))
h_central = rebook(rebin(f.Get('Fitter/seed00_toy00/fit_results/h_bkg_b_fit_nobb_nodiv')))
h_up      = rebook(rebin(f.Get(imu_isig(mu_clear_up,   sig_clear_up))))
h_down    = rebook(rebin(f.Get(imu_isig(mu_clear_down, sig_clear_down))))

scale_to = 251.
for h in (h_mctoy, h_central, h_up, h_down):
    h.Scale(scale_to/h.Integral())

x, y, exl, exh, eyl, eyh = [], [], [], [], [], []
xax = h_central.GetXaxis()
def quad(*l):
    return sum(x**2 for x in l)**0.5
nbins = h_central.GetNbinsX()
for ibin in xrange(1, nbins+1):
    ct = xax.GetBinCenter(ibin) + 0.01
    x.append(ct)
    exl.append(ct - xax.GetBinLowEdge(ibin))
    exh.append(xax.GetBinUpEdge(ibin) - ct)
    
    c, e = h_central.GetBinContent(ibin), h_central.GetBinError(ibin)
    y.append(c)
    eyl.append(quad(h_down.GetBinContent(ibin) - c, e/2))
    eyh.append(quad(h_up  .GetBinContent(ibin) - c, e/2))

for l in (x, y, exl, exh, eyl, eyh):
    print l

g_cons = ROOT.TGraphAsymmErrors(nbins, arr(x), arr(y), arr(exl), arr(exh), arr(eyl), arr(eyh))
g_cons.SetTitle(';d_{VV} (mm);events')

h_mctoy.SetLineColor(ROOT.kBlue)
g_cons.SetLineColor(ROOT.kRed)
g_cons.SetFillColor(ROOT.kRed)
g_cons.SetFillStyle(3002)
g_cons.SetLineWidth(2)

c = ROOT.TCanvas('c', '', 800, 800)
c.SetTopMargin(0.08)
c.SetRightMargin(0.05)
c.SetLogy()

h_mctoy.Draw()
g_cons.Draw('e2')
#g_cons.Draw('p')
h_mctoy.GetYaxis().SetRangeUser(0.1, 400)

leg = ROOT.TLegend(0.476, 0.690, 0.931, 0.903)
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.AddEntry(h_mctoy, 'Simulated events', 'LPE')
g_cons.SetLineWidth(0)
g_cons.SetLineColor(ROOT.kWhite)
leg.AddEntry(g_cons, 'Best-fit construction', 'F')
#leg.AddEntry(g_cons, 'Range', 'F')
leg.Draw()

cms = write(61, 0.050, 0.099, 0.931, 'CMS')
pre = write(52, 0.040, 0.211, 0.931, 'Preliminary')
sim = write(42, 0.050, 0.741, 0.933, 'Simulation')
c.SaveAs('/uscms/home/tucker/afshome/closure.pdf')
c.SaveAs('/uscms/home/tucker/afshome/closure.png')
c.SaveAs('/uscms/home/tucker/afshome/closure.root')
del c
