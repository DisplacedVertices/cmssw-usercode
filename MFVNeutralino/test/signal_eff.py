#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Samples import *

set_style()
ps = plot_saver('plots/mfvsigeff_sig6', size=(600,600))

samples = mfv_signal_samples
samples = [sample for sample in mfv_signal_samples if '0000um' not in sample.name]

per_div = 6
y_range = 1.

def curve(name, root_file_dir, num_path, den_path, color):
    heff = ROOT.TH1F(name, ';;efficiency', len(samples), 0, len(samples))
    xax = heff.GetXaxis()
    for i, sample in enumerate(samples):
        f = ROOT.TFile(os.path.join(root_file_dir, sample.name + '.root'))
        hnum = f.Get(num_path)
        hden = f.Get(den_path)
        num = hnum.Integral(0, hnum.GetNbinsX() + 2)
        den = hden.Integral(0, hden.GetNbinsX() + 2)
        eff = num/float(den)
        if name == 'trig_only':
            eff *= sample.ana_filter_eff
        heff.SetBinContent(i+1, eff)
        heff.SetBinError(i+1, 0)

        mass = sample.name.replace('M0','M').split('M')[1] + ' GeV'
        xax.SetBinLabel(i+1, mass)

    xax.SetLabelSize(0.035)
    xax.SetLabelOffset(0.0035)
    xax.SetLabelFont(62)
    xax.LabelsOption('v')
    heff.GetYaxis().SetTitleOffset(1.1)
    heff.GetYaxis().SetRangeUser(0.0001, y_range)
    heff.SetLineWidth(2)
    heff.SetLineColor(color)
    heff.SetStats(0)
    return heff

#trig_only = curve('trig_only', 'crab/MFVHistosV17_Sig6', 'mfvEventHistosTrigCut/h_bsx', 'mfvEventHistosNoCuts/h_bsx', ROOT.kGreen+2)
#looser = curve('looser', 'crab/MFVHistosV15_looser', 'mfvEventHistos/h_bsx', 'mfvEventHistosNoCuts/h_bsx', ROOT.kGreen+2)
abcd = curve('abcd', 'crab/MFVHistosV17_Sig6', 'mfvEventHistos/h_bsx', 'mfvEventHistosNoCuts/h_bsx', ROOT.kRed)
dreg = curve('dreg', 'crab/MFVHistosV17_Sig6DReg', 'mfvEventHistos/h_bsx', 'mfvEventHistosNoCuts/h_bsx', ROOT.kBlue)

#trig_only.Draw()
#looser.Draw()
abcd.Draw()
dreg.Draw('same')

hmax = abcd.GetYaxis().GetXmax()
print hmax
lines = []
for i in xrange(0, len(samples), per_div):
    if i == 0:
        continue

    l = ROOT.TLine(i, 0, i, y_range)
    l.SetLineWidth(2)
    l.SetLineColor(ROOT.kWhite)
    l.Draw()
    lines.append(l)

    l = ROOT.TLine(i, 0, i, y_range)
    l.SetLineWidth(2)
    l.SetLineStyle(2)
    l.Draw()
    lines.append(l)


leg = ROOT.TLegend(0.151,0.635,0.602,0.858)
#leg.AddEntry(trig_only, 'Trigger+offline jets', 'L')
#leg.AddEntry(looser, 'Preselection', 'L')
leg.AddEntry(abcd, 'Sideband+signal', 'L')
leg.AddEntry(dreg, 'Signal region', 'L')
leg.Draw()


ps.save('sigeff')
