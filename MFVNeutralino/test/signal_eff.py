#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Samples import *

set_style()
ps = plot_saver('~/plots/mfvlq2sigeff_V6p1_76X', size=(600,600))

samples = mfv_signal_samples_lq2
samples.sort(key=lambda s: s.name)

per_div = 5
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

two = curve('two', '/uscms_data/d1/jchu/crab_dirs/mfv_763p2/HistosV6p1_76x_nstlays3_13', 'mfvEventHistos/h_bsx', 'mfvEventHistosNoCuts/h_bsx', ROOT.kRed)
one = curve('one', '/uscms_data/d1/jchu/crab_dirs/mfv_763p2/HistosV6p1_76x_nstlays3_13/', 'mfvEventHistosOnlyOneVtx/h_bsx', 'mfvEventHistosNoCuts/h_bsx', ROOT.kBlue)
oneormore = two.Clone('oneormore')
oneormore.Add(one)
oneormore.SetLineColor(ROOT.kViolet)

two.Draw('hist e')
one.Draw('hist e same')
oneormore.Draw('hist e same')

hmax = two.GetYaxis().GetXmax()
print hmax

taus = ['100 #mum', '300 #mum', '1 mm', '10 mm']
#ymin = [0.745, 0.745, 0.75, 0.75]
ymin = [1.00, 1.00, 1.005, 1.005]
lines = []
paves = []
for i in xrange(0, len(samples), per_div):
    p = ROOT.TPaveText(i+1,ymin[i/per_div],i+per_div-1,ymin[i/per_div]+0.1)
    p.AddText(taus[i/per_div])
    p.SetTextSize(0.05)
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


leg = ROOT.TLegend(0.1,0.72,0.5,0.80)
leg.AddEntry(two, 'two-or-more-vertex events', 'L')
leg.AddEntry(one, 'exactly-one-vertex events', 'L')
leg.AddEntry(oneormore, 'one-or-more-vertex events', 'L')
leg.Draw()

decay = ROOT.TPaveText(0.7,0.88,4.5,0.96)
decay.AddText('LQ #rightarrow #muc')
decay.SetBorderSize(0)
decay.Draw()

lifetime = ROOT.TPaveText(-3,1.01,-0.01,1.11)
lifetime.AddText('#tau_{LQ}')
lifetime.SetBorderSize(0)
lifetime.Draw()

mass = ROOT.TPaveText(-3,-0.1,-0.01,-0.01)
mass.AddText('M_{LQ}')
mass.SetBorderSize(0)
mass.Draw()

ps.save('sigeff')
