#!/usr/bin/env python

import sys, os, glob
from JMTucker.Tools.ROOTTools import *

from JMTucker.Tools.Samples import mfv_signal_samples

special = 'BBv5'

set_style()
ROOT.gStyle.SetOptStat(1000000001)
ROOT.TH1.AddDirectory(0)
ps = plot_saver('plots/o2t_fit_summary_%s' % special, size=(600,600), log=False)

def wd(s, i):
    spec = special + '_' if special else ''
    if s > 0:
        return 'plots/o2t_fit/%sTmpCJ_Ntk5_SigTmp-%i_SigSamn-%ix%s_Sam' % (spec, i, i, s)
    else:
        return 'plots/o2t_fit/%sTmpCJ_Ntk5_SigTmp-%i_SigSamno_Sam' % (spec, i)

def file(s, i, n):
    return ROOT.TFile(os.path.join(wd(s, i), n))

def make_h(name):
    return ROOT.TH1D(name, '', 24, 0, 24)

def draw_h_labels(h, thing, stat, obj_cache=[]):
    mean = stat in 'mean mu'

    y_range = None
    y_label_min = None
    y_label_height = None
    lifetime_pos = None
    mass_pos = None
    yax_title = None
    
    if mean:
        if 'pull' in thing:
            y_range = (-3, 3)
            y_label_min = 2.5
            y_label_height = 0.1
            lifetime_pos = (0.965, 1.757, 3.639, 2.255)
            mass_pos = (-2.129, -3.698, -0.136, -3.108)
            yax_title = '%s mean of pull'
        elif thing == 'mu_sig':
            y_range = (-1, 10)
            y_label_min = 9
            y_label_height = 0.1
    else:
        if 'pull' in thing:
            y_range = (0, 6)
            y_label_min = 5.5
            y_label_height = 0.1
            lifetime_pos = (0.965, 4.757, 3.639, 5.255)
            mass_pos = (-2.129, -0.698, -0.136, -0.108)
            yax_title = '%s width of pull'

    if y_range is None:
        print 'need y_range etc. for thing %s stat %s' % (thing, stat)
        return

    yax_title = yax_title % ('fitted' if stat in 'mu sigma' else 'sample') + (', s' if 'sig' in thing else ', b')

    xax = h.GetXaxis()
    for i, sample in enumerate(mfv_signal_samples):
        mass = sample.name.replace('M0','M').split('M')[1] + ' GeV'
        xax.SetBinLabel(i+1, mass)
    xax.SetLabelSize(0.035)
    xax.SetLabelOffset(0.0035)
    xax.SetLabelFont(62)
    xax.LabelsOption('v')
    xax.SetRangeUser(0, 24)
    yax = h.GetYaxis()
    yax.SetRangeUser(*y_range)
    yax.SetTitle(yax_title)
    
    per_div = 6
    taus = ['100 #mum', '300 #mum', '1 mm', '10 mm']
    y_label_min = [y_label_min]*4
    for i in xrange(2):
        y_label_min[i] -= 0.005 # for the #mu descender
    lines = []
    paves = []
    for i in xrange(0, len(mfv_signal_samples), per_div):
        p = ROOT.TPaveText(i+1, y_label_min[i/per_div], i+per_div-1, y_label_min[i/per_div] + y_label_height)
        p.AddText(taus[i/per_div])
        p.SetTextSize(0.05)
        p.SetBorderSize(0)
        p.Draw()
        paves.append(p)

        if i == 0:
            continue

        l = ROOT.TLine(i, y_range[0], i, y_range[1])
        l.SetLineWidth(2)
        l.SetLineColor(ROOT.kWhite)
        l.Draw()
        lines.append(l)

        l = ROOT.TLine(i, y_range[0], i, y_range[1])
        l.SetLineWidth(2)
        l.SetLineStyle(2)
        l.Draw()
        lines.append(l)

    lifetime = ROOT.TPaveText(*lifetime_pos)
    lifetime.AddText('#tau_{#chi^{0}}')
    lifetime.SetBorderSize(0)
    lifetime.Draw()

    mass = ROOT.TPaveText(*mass_pos)
    mass.AddText('M_{#chi^{0}}')
    mass.SetBorderSize(0)
    mass.Draw()

    h.SetLineWidth(2)
    h.SetStats(0)
    y = 0 if mean else 1
    eyeline = ROOT.TLine(0, y, 24, y)
    eyeline.SetLineStyle(ROOT.kDashed)
    eyeline.Draw()

    obj_cache.extend(lines)
    obj_cache.extend(paves)
    obj_cache.append(lifetime)
    obj_cache.append(mass)
    obj_cache.append(eyeline)

sig_strengths = (0, 1, 5)
sample_nums = range(1, 25)

#sig_strengths = (0, 1, 10)
#sample_nums = (9, 15)

for sig_strength in sig_strengths:
    h = make_h('ss%i_nistat3' % sig_strength)
    for i in sample_nums:
        f = file(sig_strength, i, 'h_seed.root')
        hh = f.Get('c0').FindObject('h_seed')
        h.SetBinContent(i, hh.GetEntries())
    ps.c.cd()
    h.Draw()
    ps.save(h.GetName())

    for hyp in 'h1 h0'.split():
        for thing in 'mu_sig mu_bkg mu_sig_err mu_bkg_err mu_sig_pull mu_bkg_pull nuis0 nuis0_err nuis1 nuis1_err'.split():
            if (thing != 'mu_bkg_pull' and thing != 'mu_sig_pull'):
                continue
            
            if hyp == 'h0' and 'sig' in thing:
                continue

            if 'pull' in thing:
                stats = 'mean rms mu sigma'.split()
            else:
                stats = 'mean rms'.split()
            hs = dict((stat, make_h('ss%i_%s_%s_%s' % (sig_strength, hyp, thing, stat))) for stat in stats)

            for i in sample_nums:
                hn ='h_%s_%s' % (hyp, thing)
                f = file(sig_strength, i, hn + '.root')
                #print f.GetName(), hn
                h = f.Get('c0').FindObject(hn)
                if not h:
                    print 'skip', f.GetName(), hn
                    continue

                hs['mean'].SetBinContent(i, h.GetMean())
                hs['mean'].SetBinError(i, h.GetMeanError())
                hs['rms'].SetBinContent(i, h.GetRMS())
                hs['rms'].SetBinError(i, h.GetRMSError())

                if 'pull' in thing:
                    fcn = h.FindObject('gaus')
                    hs['mu'].SetBinContent(i, fcn.GetParameter(1))
                    hs['mu'].SetBinError(i, fcn.GetParError(1))
                    hs['sigma'].SetBinContent(i, fcn.GetParameter(2))
                    hs['sigma'].SetBinError(i, fcn.GetParError(2))

            ps.c.cd()
            for stat in stats:
                h = hs[stat]
                h.Draw('hist e')
                draw_h_labels(h, thing, stat)
                ps.save(h.GetName())

