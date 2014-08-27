#!/usr/bin/env python

import sys, os, glob
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.gStyle.SetOptStat(1000000001)
ps = plot_saver('plots/o2t_fit_summary', size=(600,600), log=False)
ROOT.TH1.AddDirectory(0)

def wd(s, i):
    if s > 0:
        return 'plots/o2t_fit/TmpCJ_Ntk5_SigTmp-%i_SigSamn-%ix%s_Sam' % (i, i, s)
    else:
        return 'plots/o2t_fit/TmpCJ_Ntk5_SigTmp-%i_SigSamno_Sam' % i

def file(s, i, n):
    return ROOT.TFile(os.path.join(wd(s, i), n))

def make_h(name):
    return ROOT.TH1D(name, '', 25, 0, 25)

for sig_strength in (0, 1, 5, 10):
    h = make_h('ss%i_nistat3' % sig_strength)
    for i in xrange(1, 25):
        f = file(sig_strength, i, 'h_seed.root')
        hh = f.Get('c0').FindObject('h_seed')
        h.SetBinContent(i, hh.GetEntries())
    h.Draw()
    ps.save(h.GetName())

    for hyp in 'h1 h0'.split():
        for thing in 'mu_sig mu_bkg mu_sig_err mu_bkg_err mu_sig_pull mu_bkg_pull nuis0 nuis0_err nuis1 nuis1_err'.split():
            if hyp == 'h0' and 'sig' in thing:
                continue

            if 'pull' in thing:
                stats = 'mean rms mu sigma'.split()
            else:
                stats = 'mean rms'.split()
            hs = dict((stat, make_h('ss%i_%s_%s_%s' % (sig_strength, hyp, thing, stat))) for stat in stats)

            for i in xrange(1, 25):
                hn ='h_%s_%s' % (hyp, thing)
                f = file(sig_strength, i, hn + '.root')
                h = f.Get('c0').FindObject(hn)

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

            for stat in stats:
                mean = stat in 'mean mu'
                h = hs[stat]
                h.Draw('hist e')
                h.Fit('pol0', 'Q')
                fcn = h.FindObject('pol0')
                fcn.SetLineWidth(1)
                fcn.SetLineColor(2)
                h.SetLineWidth(2)
                h.SetStats(0)
                y = 0 if mean else 1
                l = ROOT.TLine(0, y, 25, y)
                l.SetLineStyle(ROOT.kDashed)
                l.Draw()
#                if mean:
#                    if 'pull' in thing:
#                        h.GetYaxis().SetRangeUser(-3, 3)
#                else:
#                    if 'pull' in thing:
#                        h.GetYaxis().SetRangeUser(0, 6)
                ps.save(h.GetName())

