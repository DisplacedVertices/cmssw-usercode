#!/usr/bin/env python

from math import pi
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.gStyle.SetOptStat(2222222)
ROOT.gStyle.SetOptFit(2222)
ps = plot_saver('plots/one2two', size=(600,600))

f = ROOT.TFile('one2two.root')

####

for name in 'h_2v_bs2ddist h_2v_bs2ddist_0 h_2v_bs2ddist_1 h_1v_bs2ddist'.split():
    h = f.Get('MFVOne2Two/%s' % name)
    h.Rebin(2)
    h.SetTitle(';vertex xy distance to beamspot (cm);vertices/20 #mum')
    h.Draw()
    ps.save(name)

for name in 'h_2v_bsdz h_2v_bsdz_0 h_2v_bsdz_1 h_1v_bsdz'.split():
    h = f.Get('MFVOne2Two/%s' % name)
    h.Rebin(2)
    h.SetTitle(';vertex #Delta z to beamspot (cm);vertices/0.4 cm')
    h.Draw()
    ps.save(name)

for name in 'h_2v_bs2ddist_v_bsdz h_2v_bs2ddist_v_bsdz_0 h_2v_bs2ddist_v_bsdz_1 h_1v_bs2ddist_v_bsdz'.split():
    h = f.Get('MFVOne2Two/%s' % name)
    h.SetTitle(';vertex #Delta z to beamspot (cm);vertex xy distance to beamspot (cm)')
    h.SetStats(0)
    h.Draw('colz')
    ps.save(name, logz=True)

for name in 'h_2v_svdz h_1v_svdz h_1v_svdz_all'.split():
    h = f.Get('MFVOne2Two/%s' % name)
    h.SetTitle(';vertex #Delta z (cm);events/100 #mum')
    h.Draw()
    ps.save(name)

for name in 'h_2v_svdz_v_dphi h_1v_svdz_v_dphi'.split():
    h = f.Get('MFVOne2Two/%s' % name)
    h.SetTitle(';vertex #Delta #phi;vertex #Delta z (cm)')
    h.SetStats(0)
    h.Draw('colz')
    ps.save(name, logz=True)

####

h2v = f.Get('MFVOne2Two/h_2v_dphi')
h1v = f.Get('MFVOne2Two/h_1v_dphi')
hfn = f.Get('MFVOne2Two/h_fcn_dphi')

h1v.SetLineColor(ROOT.kRed)
hfn.SetLineColor(ROOT.kGreen+2)

h1v.Scale(h2v.Integral()/h1v.Integral())
hfn.Scale(h2v.Integral()/hfn.Integral())

h2v.SetTitle(';#Delta#phi;events/0.63')
h2v.Draw()
h1v.Draw('sames')
hfn.Draw('sames')
ps.c.Update()
differentiate_stat_box(h2v, (1,0), new_size=(0.25, 0.25))
differentiate_stat_box(h1v, (1,1), new_size=(0.25, 0.25))
differentiate_stat_box(hfn, (1,2), new_size=(0.25, 0.25))
ps.save('deltaphi')

####

for norm_below in (1, 0.024, 0.032, 0.048, 0.052):
    norm_name = ('%.3f' % norm_below).replace('.','p')
    
    h2v = f.Get('MFVOne2Two/h_2v_svdist2d').Clone('h2v')
    h1v = f.Get('MFVOne2Two/h_1v_svdist2d').Clone('h1v')

    h2v.Rebin(4)
    h1v.Rebin(4)

    h2v.SetLineWidth(2)
    h1v.SetLineColor(ROOT.kRed)

    scale = h2v.Integral(1, h2v.FindBin(norm_below))/h1v.Integral(1, h1v.FindBin(norm_below))
    print 'scale factor for norm_below = %f: %f' % (norm_below, scale)
    h1v.Scale(scale)

    h2v.SetTitle(';xy distance between vertex 0 and 1 (cm);events/40 #mum')

    h2v.Draw('e')
    h1v.Draw('sames')
    ps.c.Update()
    differentiate_stat_box(h2v, 0, new_size=(0.3, 0.3))
    differentiate_stat_box(h1v,    new_size=(0.3, 0.3))
    ps.save('svdist2d_norm%s' % norm_name)

    for opt in ('ge', 'le'):
        ch2v = cumulative_histogram(h2v, opt)
        ch1v = cumulative_histogram(h1v, opt)

        ch2v.SetTitle(';x = svdist2d (cm);# events w/ svdist2d #%sq x' % opt)
        ch2v.SetStats(0)
        ch1v.SetStats(0)
        ch2v.SetLineWidth(2)
        ch1v.SetLineColor(ROOT.kRed)
        ch2v.Draw()
        ch1v.Draw('hist same')
        ps.save('svdist2d_norm%s_cumul_%s' % (norm_name, opt))

####

if 0:
    h = f.Get('MFVOne2Two/h_2v_dphi')

    for i in xrange(2, 17, 2):
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%i' % i
        fcn = ROOT.TF1('fcn', '[0]*x**%i' % i, pi, pi)
        res = h.Fit(fcn, 'IQRS')
        ps.save('power_%i' % i)
        #res.Print()

    h = f.Get('MFVOne2Two/h_2v_abs_dphi')

    for i in xrange(2, 17, 2):
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%i' % i
        fcn = ROOT.TF1('fcn', '[0]*x**%i' % i, pi, pi)
        res = h.Fit(fcn, 'IQRS')
        ps.save('abs_power_%i' % i)
        #res.Print()
