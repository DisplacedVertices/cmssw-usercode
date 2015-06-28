#!/usr/bin/env python

import sys, os, glob
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.CRABTools import *

set_style()
ROOT.TH1.AddDirectory(0)
ps = plot_saver('plots/MakeSamples_eff', log=False, size=(700,700))
ps.c.SetBottomMargin(0.2)

tau0s = [0.1*x for x in xrange(1,10)] + [1.*x for x in xrange(1,11)] + range(12,31,2)
tau0s = [int(tau0*1000) for tau0 in tau0s]
ntau0s = len(tau0s)
masses = [400, 1000, 1500]

def denom(tau0, mass):
    if mass == 400:
	if tau0 in (100, 200, 300, 500, 600, 800, 10000):
	    return 499*200
	elif tau0 == 400:
	    return 497*200
	elif tau0 == 6000:
	    return 498*200
    elif mass == 1000 and tau0 == 26000:
	return 499*200
    elif mass == 1500:
	if tau0 == 300:
	    return 498*200
	elif tau0 in (16000, 28000):
	    return 499*200
    return 500*200

def epm(num, den):
    eff, lo, hi = clopper_pearson(num, den)
    return eff, (hi-lo)/2

def curves(mass):
    mass_name = 'M%04i' % mass
    h_one = ROOT.TH1F(mass_name + '_one', '', ntau0s, 0, ntau0s)
    h_two = ROOT.TH1F(mass_name + '_two', '', ntau0s, 0, ntau0s)
    hs = (h_one, h_two)
    for h in hs:
        h.SetLineWidth(2)
        h.SetStats(0)
        h.SetMinimum(0)
        h.SetMaximum(1.03)

    for itau0, tau0 in enumerate(tau0s):
        tau0_name = 'tau%05ium' % tau0
        for h in hs:
            h.GetXaxis().SetBinLabel(itau0+1, tau0_name)

        fn = 'root://cmsxrootd.fnal.gov//store/user/tucker/mfv_sample_scan/1TeVglu/mfv_neutralino_%s_%s.root' % (tau0_name, mass_name)
        f = ROOT.TFile.Open(fn)
        t = f.Get('mfvMiniTree/t')
        den = denom(tau0, mass)
        one, two = 0, 0
        for nvtx, in detree(t, 'nvtx'):
            if nvtx == 1:
                one += 1
            elif nvtx == 2:
                two += 1
            else:
                raise RuntimeError('bad nvtx for %s job %i: %i' % (dir, job, nvtx))
        one_eff, one_eff_e = epm(one, den)
        two_eff, two_eff_e = epm(two, den)
        h_one.SetBinContent(itau0+1, one_eff)
        h_one.SetBinError  (itau0+1, one_eff_e)
        h_two.SetBinContent(itau0+1, two_eff)
        h_two.SetBinError  (itau0+1, two_eff_e)

    return h_one, h_two

if 0:
    f = ROOT.TFile('temp_1TeVglu.root', 'recreate')
    hs = []
    for mass in [400]:
        for h in curves(mass):
            hs.append(h)
            h.SetDirectory(f)
    f.Write()
    f.Close()
elif 0:
    f = ROOT.TFile('temp.root')
    first = True
    leg = ROOT.TLegend(0.619, 0.690, 0.875, 0.872)
    leg.SetBorderSize(0)
    hs = []
    for mass, color in zip(masses, (1,2,4)):
        h = f.Get('M%04i_two' % mass)
        h.SetName('M%04i' % mass)
        h.GetYaxis().SetTitle('two-vertex efficiency')
        h.SetLineColor(color)
        h.GetXaxis().LabelsOption('v')
        hs.append(h)
        if first:
            h.Draw()
            first = False
        else:
            h.Draw('same')
        leg.AddEntry(h, h.GetName(), 'LE')
    leg.Draw()
    ps.save('two')

    assert len(hs) == 3
    h0400, h1000, h1500 = hs
    h_15_10 = h1500.Clone('h_15_10')
    h_15_10.GetYaxis().SetTitle('ratio of effs M1500 / M1000')
    h_15_10.Divide(h1000)
    h_15_10.Draw()
    ps.save('h_15_10')

    h_04_10 = h0400.Clone('h_04_10')
    h_04_10.GetYaxis().SetTitle('ratio of effs M0400 / M1000')
    h_04_10.Divide(h1000)
    h_04_10.Draw()
    ps.save('h_04_10')
else:
    f1 = ROOT.TFile('temp.root')
    f2 = ROOT.TFile('temp_1TeVglu.root')
    h1 = f1.Get('M0400_two')
    h1.SetName('M_{neu} = 400 GeV')
    h2 = f2.Get('M0400_two')
    h2.SetName('M_{neu} = 400 GeV, M_{glu} = 1 TeV')

    hs = [h1,h2]
    first = True
    leg = ROOT.TLegend(0.619, 0.690, 0.875, 0.872)
    leg.SetBorderSize(0)
    for h in hs:
        h.GetXaxis().LabelsOption('v')
        h.GetYaxis().SetTitle('two-vertex efficiency')
        h.SetLineColor(2 if not first else 1)
        if first:
            h.Draw()
            first = False
        else:
            h.Draw('same')
        leg.AddEntry(h, h.GetName(), 'LE')
    leg.Draw()
    ps.save('two')

    h2.Divide(h1)
    h2.GetYaxis().SetTitle('ratio of effs M_{glu} = 1 TeV / M_{glu} = 405 GeV')
    h2.SetMaximum(3)
    h2.Draw()
    ps.save('hrat')
