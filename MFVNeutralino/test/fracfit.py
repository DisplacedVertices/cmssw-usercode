import sys, os
from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
set_style()
#ps = plot_saver('plots/fracfit_mconly', size=(600,600))
ps = plot_saver('plots/fracfit_dd_nosigcontam_clearover', size=(600,600))

ROOT.TH1.AddDirectory(0)
ROOT.gRandom.SetSeed(19800101)

f_bkg = ROOT.TFile('~jchu/afshome/public_html/plots/ABCD/lifetime_v_mass/h_svdist2d_tkonlymass01/background.root')
h_bkg_lo = f_bkg.Get('c1_n315').FindObject('h_svdist2d_low_tkonlymass01')
h_bkg_hi = f_bkg.Get('c1_n315').FindObject('h_svdist2d_high_tkonlymass01')

# JMTBAD hack to get rid of crap event
if 1:
    h_bkg_lo.SetBinContent(10, 0)
    h_bkg_lo.SetBinError(10, 0)
if 1:
    h_bkg_lo.SetBinContent(11, 0)
    h_bkg_lo.SetBinError(11, 0)

f_sig = ROOT.TFile('~jchu/afshome/public_html/plots/ABCD/lifetime_v_mass/h_svdist2d_tkonlymass01/mfv_neutralino_tau9900um_M1000.root')
h_sig_lo = f_sig.Get('c1_n305').FindObject('h_svdist2d_low_tkonlymass01')
h_sig_hi = f_sig.Get('c1_n305').FindObject('h_svdist2d_high_tkonlymass01')

h_dd_template = h_bkg_lo.Clone('h_dd_template')
h_dd_template.Add(h_sig_lo)

################################################################################

#x_sig, x_bkg = 0.9, 0.1
#n_sig = int(round(n_bkg/x_bkg*x_sig))
n_sig, n_bkg = 150, 100
n_exp = 1000
print n_sig, n_bkg

h_x_1 = ROOT.TH1F('h_x_1', '', 40, 0, 1)
h_x_2 = ROOT.TH1F('h_x_2', '', 40, 0, 1)
h_e_x_1 = ROOT.TH1F('h_e_x_1', '', 40, 0, 0.15)
h_e_x_2 = ROOT.TH1F('h_e_x_2', '', 40, 0, 0.15)
h_p_x_1 = ROOT.TH1F('h_p_x_1', '', 40, -2, 2)
h_p_x_2 = ROOT.TH1F('h_p_x_2', '', 40, -2, 2)

for iexp in xrange(n_exp):
    h_data = ROOT.TH1D('h_data', '', h_bkg_lo.GetNbinsX(), h_bkg_lo.GetBinLowEdge(1), h_bkg_lo.GetBinLowEdge(h_bkg_lo.GetNbinsX()+1))
    n_bkg_hat = ROOT.gRandom.Poisson(n_bkg)
    n_sig_hat = ROOT.gRandom.Poisson(n_sig)
    for i in xrange(n_bkg_hat):
        h_data.Fill(h_bkg_hi.GetRandom())
    for i in xrange(n_sig_hat):
        h_data.Fill(h_sig_hi.GetRandom())

    templates = ROOT.TObjArray(2)
    #templates.Add(h_bkg_hi)
    templates.Add(h_dd_template)
    templates.Add(h_sig_hi)

    fit = ROOT.TFractionFitter(h_data, templates)
    fit.Constrain(1, 0., 1.)
    fit.Constrain(2, 0., 1.)
    print fit.Fit()

    if iexp % 20 == 0:
        h_data.Draw('hist e')
        h_fit = fit.GetPlot()
        h_fit.SetLineColor(ROOT.kRed)
        h_fit.Draw('e same')

    x_1, e_x_1, x_2, e_x_2 = ROOT.Double(), ROOT.Double(), ROOT.Double(), ROOT.Double()
    fit.GetResult(0, x_1, e_x_1)
    fit.GetResult(1, x_2, e_x_2)
    #print x_1, e_x_1
    #print x_2, e_x_2
    h_x_1.Fill(x_1)
    h_x_2.Fill(x_2)
    h_e_x_1.Fill(e_x_1)
    h_e_x_2.Fill(e_x_2)
    h_p_x_1.Fill((x_1 - n_bkg_hat/float(n_sig_hat+n_bkg_hat))/e_x_1)
    h_p_x_2.Fill((x_2 - n_sig_hat/float(n_sig_hat+n_bkg_hat))/e_x_2)

    if iexp % 20 == 0:
        h_1 = fit.GetMCPrediction(0)
        h_1.Scale(x_1)
        h_1.SetLineColor(ROOT.kGreen+2)
        h_1.Draw('e same')

        h_2 = fit.GetMCPrediction(1)
        h_2.Scale(x_2)
        h_2.SetLineColor(ROOT.kBlue)
        h_2.Draw('e same')

        ps.save('fit_%03i' % iexp)

    del fit

h_x_1.Draw()
ps.save('h_x_1')
h_x_2.Draw()
ps.save('h_x_2')
h_e_x_1.Draw()
ps.save('h_e_x_1')
h_e_x_2.Draw()
ps.save('h_e_x_2')
h_p_x_1.Fit('gaus')
ps.save('h_p_x_1')
h_p_x_2.Fit('gaus')
ps.save('h_p_x_2')

