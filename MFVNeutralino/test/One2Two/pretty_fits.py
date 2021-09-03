import sys
from array import array
from DVCode.Tools.ROOTTools import *
import DVCode.MFVNeutralino.AnalysisConstants as ac

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

def rebook(in_h):
    assert type(in_h) == ROOT.TH1D
    nbins = in_h.GetNbinsX()
    assert nbins == 6
    asses = [None, 0, 0.02, 0.04, 0.06, 0.08, 0.1, 5]
    for ibin in xrange(1, nbins+2):
        assert abs(in_h.GetBinLowEdge(ibin) - asses[ibin]) < 1e-6

    bins = [j*0.2 for j in range(6)] + [2.]
    bins = array('d', bins)
    h = ROOT.TH1D(in_h.GetName(), ';d_{VV} (mm);Events', len(bins)-1, bins)
    h.Sumw2()
    h.SetStats(0)
    h.SetLineWidth(2)
    for ibin in xrange(0, nbins+2):
        h.SetBinContent(ibin, in_h.GetBinContent(ibin))
        h.SetBinError  (ibin, in_h.GetBinError  (ibin))

    xax = h.GetXaxis()
    xax.SetTitleSize(0.05)
    xax.SetLabelSize(0.04)
    xax.SetTitleOffset(0.91)

    yax = h.GetYaxis()
    yax.SetTitleOffset(1.)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.04)
    yax.SetRangeUser(0.1, 300)

    return h

def colf(h, color, fill):
    h.SetLineColor(color)
    h.SetFillColor(color)
    h.SetFillStyle(fill)
    
set_style()
rainbow_palette()

f = ROOT.TFile('mfvo2t.root')

t = f.Get('Fitter/t_fit_info')
d = list(detree(t, 't_obs_0__h1_mu_sig:t_obs_0__h1_mu_bkg:t_obs_0__h0_mu_bkg', xform=float))
assert len(d) == 1
sb_sig, sb_bkg, b_bkg = d[0]

sb_sig_unc = 1.9
def bkg_uncert(h):
    bkg_syst = [0,0,0,3.8,1.4,0.1,0.1]
    assert h.GetNbinsX() == 6
    for ibin in xrange(1, 7):
        #print ibin, h.GetBinError(ibin)
        h.SetBinError(ibin, bkg_syst[ibin])
    
h_sb_bkg = rebook(f.Get('Fitter/seed00_toy-1/fit_results/h_bkg_sb_fit_bb_nodiv'))
h_sb_sig = rebook(f.Get('Fitter/seed00_toy-1/fit_results/h_sig_sb_fit_bb_nodiv'))
h_sb_bkg.Scale(sb_bkg)
h_sb_sig.Scale(sb_sig)
#bkg_uncert(h_sb_bkg)

h_sb_sum = h_sb_bkg.Clone('h_sb_sum')
h_sb_sum.Add(h_sb_sig)
h_sb_sum.SetLineColor(ROOT.kRed)
h_sb_sum.SetLineStyle(2)
#h_sb_sum.SetFillStyle(3002)
h_sb_sum.GetYaxis().SetRangeUser(0.1, 300)

h_b_sum = rebook(f.Get('Fitter/seed00_toy-1/fit_results/h_bkg_b_fit_bb_nodiv'))
h_b_sum.Scale(b_bkg)
#bkg_uncert(h_b_sum)
#h_b_sum.SetFillStyle(3002)
#h_b_sum.SetFillColor(ROOT.kBlue)
h_b_sum.SetLineColor(ROOT.kBlue)
h_b_sum.SetLineStyle(3)

h_data = poisson_intervalize(rebook(f.Get('Fitter/seed00_toy-1/fit_results/h_data_b_fit_bb_nodiv')))
h_data.SetLineWidth(2)
h_data.SetMarkerStyle(20)
h_data.SetMarkerSize(1.5)

c = ROOT.TCanvas('c', '', 800, 800)
c.SetBottomMargin(0.12)
c.SetLogy()

h_sb_sum.Draw('hist')
xax = h_sb_sum.GetXaxis()
h_b_sum.Draw('hist same')
h_data.Draw('P')

leg = ROOT.TLegend(0.381, 0.639, 0.871, 0.882)
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.AddEntry(h_data, 'Data', 'LPE')
leg.AddEntry(h_sb_sum, 'Signal + background fit', 'L')
leg.AddEntry(h_b_sum, 'Background-only fit', 'L')
leg.Draw()
#leg.SetF
cms = write(61, 0.050, 0.099, 0.913, 'CMS')
#pre = write(52, 0.040, 0.211, 0.931, 'Preliminary')
lum = write(42, 0.050, 0.586, 0.913, '17.6 fb^{-1} (8 TeV)')


# do a broken x axis. thanks root (throot)

boxcenter = 1.8
boxwidth = 0.02
boxy1 = 0.065
boxy2 = 0.14
box1 = ROOT.TBox(boxcenter-boxwidth, boxy1, boxcenter+boxwidth, 2)
box1.SetLineColor(ROOT.kWhite)
box1.SetFillColor(ROOT.kWhite)
box1.Draw()

box2 = ROOT.TBox(1.74, 0.065, 2.1, 0.095)
box2.SetLineColor(ROOT.kWhite)
box2.SetFillColor(ROOT.kWhite)
box2.Draw()

#lab1 = ROOT.TText(1.714, 0.06989, '49.8')
#lab1.SetTextFont(xax.GetLabelFont())
#lab1.SetTextSize(xax.GetLabelSize())
#lab1.Draw()

lab2 = ROOT.TText(1.914, 0.06989, '50.0')
lab2.SetTextFont(xax.GetLabelFont())
lab2.SetTextSize(xax.GetLabelSize())
lab2.Draw()

lineslantdx = 0.009
lineybackoff = 0.01

line1 = ROOT.TLine(boxcenter-boxwidth-lineslantdx, boxy1+lineybackoff, boxcenter-boxwidth+lineslantdx, boxy2-lineybackoff)
line1.SetLineWidth(2)
line1.Draw()

line2 = ROOT.TLine(boxcenter+boxwidth-lineslantdx, boxy1+lineybackoff, boxcenter+boxwidth+lineslantdx, boxy2-lineybackoff)
line2.SetLineWidth(2)
line2.Draw()

name = 'plots/after_referee/fit'
c.SaveAs(name + '.pdf')
c.SaveAs(name + '.png')
c.SaveAs(name + '.root')
