#!/usr/bin/env python

import sys, os, glob
from JMTucker.Tools.ROOTTools import *
from JMTucker.MFVNeutralino.PerSignal import PerSignal
import smallsigscan

set_style()
ROOT.gStyle.SetOptStat(1000000001)
ROOT.TH1.AddDirectory(0)
ps = plot_saver(plot_dir('o2t_fit_summary_run2'), size=(600,600), log=False)

def get_file(s, i, n):
    path = '/publicweb/t/tucker/asdf/plots/o2t_fit_run2/BkgScale1_SigTmp%i_SigSamn' % i
    if s > 0:
        path += '%ix%s' % (i, s)
    else:
        path += 'o'
    return ROOT.TFile(os.path.join(path, n + '.root'))

sig_strengths = (0, 1, 5, 25, 100)

for sig_strength in sig_strengths:
    name = 'ss%i_nistat3' % sig_strength
    per = PerSignal(name, y_range=(480, 520))
    for sample in smallsigscan.samples:
        f = get_file(sig_strength, sample.sample_num, 'h_seed')
        hh = f.Get('c0').FindObject('h_seed')
        sample.y = hh.GetEntries()
    per.add(smallsigscan.samples)
    per.draw(canvas=ps.c)
    ps.save(name)

    for hyp in 'h1 h0'.split():
        for thing in 'mu_sig mu_bkg mu_sig_err mu_bkg_err mu_sig_pull mu_bkg_pull'.split():
            if 'pull' not in thing:
                continue

            if hyp == 'h0' and 'sig' in thing:
                continue

            stats = [
                ('mean', (-2,2)),
                ('rms', (0, 2)),
                ('mu', (-2,2)),
                ('rms', (0,2)),
                ]
                
            for stat, y_range in stats:
                for sample in smallsigscan.samples:
                    hn = 'h_%s_%s' % (hyp, thing)
                    f = get_file(sig_strength, sample.sample_num, hn)
                    hh = f.Get('c0').FindObject(hn)
                    if not hh:
                        continue
                    #print sample, hn, f, hh
                    if 'pull' in thing:
                        fcn = hh.FindObject('gaus')

                    if stat == 'mean':
                        sample.y, sample.ye = hh.GetMean(), hh.GetMeanError()
                    elif stat == 'rms':
                        sample.y, sample.ye = hh.GetRMS(), hh.GetRMSError()
                    elif 'pull' in thing and stat == 'mu':
                        sample.y, sample.ye = fcn.GetParameter(1), fcn.GetParError(1)
                    elif 'pull' in thing and stat == 'sigma':
                        sample.y, sample.ye = fcn.GetParameter(1), fcn.GetParError(1)
                    else:
                        if hasattr(sample, 'y'):
                            del sample.y
                        if hasattr(sample, 'ye'):
                            del sample.ye

                #mn = min(sample.y - sample.ye for sample in smallsigscan.samples)
                #mx = max(sample.y + sample.ye for sample in smallsigscan.samples)

                name = 'ss%i %s %s %s' % (sig_strength, hyp, thing, stat)
                per = PerSignal(name, y_range=y_range)
                per.add(smallsigscan.samples)
                per.draw(canvas=ps.c)
                ps.save(name.replace(' ', '_'))

