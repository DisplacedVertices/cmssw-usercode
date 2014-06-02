#!/usr/bin/env python

from math import pi
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.gStyle.SetOptStat(2222222)
ROOT.gStyle.SetOptFit(2222)
ps = plot_saver('plots/one2two', size=(600,600))

f = ROOT.TFile('one2two.root')

####

h2v = f.Get('MFVOne2Two/h_2v_delta_phi')
h1v = f.Get('MFVOne2Two/h_1v_worep_delta_phi')
hfn = f.Get('MFVOne2Two/h_fcn_delta_phi')

h1v.SetLineColor(ROOT.kRed)
hfn.SetLineColor(ROOT.kGreen+2)

h1v.Scale(h2v.Integral()/h1v.Integral())
hfn.Scale(h2v.Integral()/hfn.Integral())

h2v.Draw()
h1v.Draw('sames')
hfn.Draw('sames')
ps.c.Update()
differentiate_stat_box(h1v)
differentiate_stat_box(hfn, 2)
ps.save('deltaphi')

####

h2v = f.Get('MFVOne2Two/h_2v_svdist2d')
h1v = f.Get('MFVOne2Two/h_1v_worep_svdist2d')

h1v.SetLineColor(ROOT.kRed)
h1v.Scale(h2v.Integral()/h1v.Integral())

h2v.Draw()
h1v.Draw('sames')
ps.c.Update()
differentiate_stat_box(h1v)
ps.save('svdist2d')

####

h = f.Get('MFVOne2Two/h_2v_delta_phi')

for i in xrange(2, 17, 2):
    print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%i' % i
    fcn = ROOT.TF1('fcn', '[0]*x**%i' % i, pi, pi)
    res = h.Fit(fcn, 'IQRS')
    ps.save('power_%i' % i)
    #res.Print()


h = f.Get('MFVOne2Two/h_2v_abs_delta_phi')

for i in xrange(2, 17, 2):
    print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%i' % i
    fcn = ROOT.TF1('fcn', '[0]*x**%i' % i, pi, pi)
    res = h.Fit(fcn, 'IQRS')
    ps.save('abs_power_%i' % i)
    #res.Print()


