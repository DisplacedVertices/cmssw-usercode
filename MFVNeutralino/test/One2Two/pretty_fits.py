import sys
from array import array
from JMTucker.Tools.ROOTTools import *
import JMTucker.MFVNeutralino.AnalysisConstants as ac

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
    h = ROOT.TH1D(in_h.GetName(), ';d_{VV} (mm);events', len(bins)-1, bins)
    h.Sumw2()
    h.SetStats(0)
    h.SetLineWidth(2)
    for ibin in xrange(0, nbins+2):
        h.SetBinContent(ibin, in_h.GetBinContent(ibin))
        h.SetBinError  (ibin, in_h.GetBinError  (ibin))

    yax = h.GetYaxis()
    yax.SetTitleOffset(1.15)
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

c = ROOT.TCanvas('c', '', 800, 800)
c.SetTopMargin(0.08)
c.SetRightMargin(0.05)
c.SetLogy()

h_sb_sum.Draw('hist')
h_b_sum.Draw('hist same')
h_data.Draw('P')

leg = ROOT.TLegend(0.431, 0.659, 0.931, 0.902)
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.AddEntry(h_data, 'Data', 'LPE')
leg.AddEntry(h_sb_sum, 'Signal + background fit', 'L')
leg.AddEntry(h_b_sum, 'Background-only fit', 'L')
leg.Draw()
#leg.SetF
cms = write(61, 0.050, 0.099, 0.931, 'CMS')
pre = write(52, 0.040, 0.211, 0.931, 'Preliminary')
sim = write(42, 0.050, 0.631, 0.933, ac.int_lumi_nice)
name = '/uscms/home/tucker/afshome/fit'
c.SaveAs(name + '.pdf')
c.SaveAs(name + '.png')
c.SaveAs(name + '.root')
