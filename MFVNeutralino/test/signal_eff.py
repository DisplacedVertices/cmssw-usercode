#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Samples import *

set_style()
ps = plot_saver(plot_dir('sigeff_v14'), size=(600,600))

samples = [x for x in mfv_signal_samples if not x.name.startswith('my')]
print len(samples)
samples.sort(key=lambda s: s.name)

per_div = 7
assert len(samples) % per_div == 0
y_range = 1.

def curve(name, root_file_dir, num_path, color):
    heff = ROOT.TH1F(name, ';;efficiency', len(samples), 0, len(samples))
    xax = heff.GetXaxis()
    for i, sample in enumerate(samples):
        f = ROOT.TFile(os.path.join(root_file_dir, sample.name + '.root'))
        hnum = f.Get(num_path)
        hden = f.Get('mfvWeight/h_sums')
        num = hnum.Integral(0, hnum.GetNbinsX() + 2)
        den = hden.GetBinContent(1)
        eff = num/float(den)
#        eff *= sample.filter_eff
        heff.SetBinContent(i+1, eff)
        interval = clopper_pearson(num, den)
        error = (interval[2] - interval[1]) / 2
        heff.SetBinError(i+1, error)
        if name == 'two':
            print sample.name, eff, interval
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

two = curve('two', '/uscms_data/d2/tucker/crab_dirs/HistosV14', 'mfvEventHistosFullSel/h_bsx', ROOT.kRed)
two.Draw('hist e')

taus = ['100 #mum', '300 #mum', '1 mm', '10 mm', '30 mm']
#ymin = [0.745, 0.745, 0.75, 0.75]
ymin = [1.00, 1.00, 1.005, 1.005, 1.005]
lines = []
paves = []
for i in xrange(0, len(samples), per_div):
    p = ROOT.TPaveText(i+1,ymin[i/per_div],i+per_div-1,ymin[i/per_div]+0.1)
    p.SetFillColor(ROOT.kWhite)
    p.AddText(taus[i/per_div])
    p.SetTextSize(0.042)
    p.SetBorderSize(0)
    p.Draw()
    paves.append(p)

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


decay = ROOT.TPaveText(0.31, 0.89,6.6,0.97)
decay.AddText('#tilde{N} #rightarrow tbs')
decay.SetFillColor(ROOT.kWhite)
decay.SetBorderSize(0)
decay.Draw()

lifetime = ROOT.TPaveText(-3,1.01,-0.01,1.11)
lifetime.AddText('#tau_{#tilde{N}}')
lifetime.SetFillColor(ROOT.kWhite)
lifetime.SetBorderSize(0)
lifetime.Draw()

mass = ROOT.TPaveText(-3,-0.1,-0.01,-0.01)
mass.SetFillColor(ROOT.kWhite)
mass.AddText('M_{#tilde{N}}')
mass.SetBorderSize(0)
mass.Draw()

ps.save('sigeff')
