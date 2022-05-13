#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal


# 0: filters for di-bjet  trigger
# 1: filters for tri-bjet trigger
filter_opt = 1

if filter_opt == 0:
    n_cols = 2
    n_rows = 2
    loop_range  = range(1,5)
    ind_offset  = 0
    rebin = 1

if filter_opt == 1:
    n_cols = 4
    n_rows = 3
    loop_range  = range(5,15)
    ind_offset  = 4
    rebin = 2

set_style()
version = 'test'
ps = plot_saver(plot_dir('filter_tocs_%s' % version), size=(1000,600), pdf=True, log=False)

alpha = 1.0 - 0.6827
use_effective = True

fn = '/uscms_data/d3/shogan/crab_dirs/HistosV29Am/mfv_neu_tau00100um_combined.root'    # Black curve
#zn = '/uscms_data/d3/shogan/crab_dirs/HistosDibjetNomVtxV29Am/combined_lowmass_stop.root'    # Red curve
zn = '/uscms_data/d3/shogan/crab_dirs/HistosV29Am/mfv_neu_tau10000um_combined.root'    # Red curve

f = ROOT.TFile(fn)
t = f.Get('mfvFilterHistosNoCuts')

if zn != '':
    z = ROOT.TFile(zn)
    v = z.Get('mfvFilterHistosNoCuts')

hist_names = [h.GetName() for h in t.GetListOfKeys()]

filter_names = ["hltDoubleCaloBJets100eta2p3",
                "hltBTagCalo80x6CSVp0p92DoubleWithMatching",
                "hltDoublePFJets100Eta2p3",
                "hltDoublePFJets100Eta2p3MaxDeta1p6",
                "hltQuadCentralJet30",
                "hltCaloQuadJet30HT300", 
                "hltBTagCaloCSVp05Double", 
                "hltPFCentralJetLooseIDQuad30", 
                "hlt1PFCentralJetLooseID75", 
                "hlt2PFCentralJetLooseID60",
                "hlt3PFCentralJetLooseID45", 
                "hlt4PFCentralJetLooseID40", 
                "hltPFCentralJetsLooseIDQuad30HT300", 
                "hltBTagPFCSVp070Triple",
                ]

garbage = []

for h_n in hist_names:
    if ('all' in h_n) or ('energy' in h_n) or ('10' in h_n):
        continue

    c1 = ROOT.TCanvas('c1', '', 1600,1000)
    c1.Divide(n_cols, n_rows)

    h = t.Get(h_n)

    for i in loop_range:
        binx = i
        c1.cd(i-ind_offset)
        if (i != 5):
            h_den = h.ProjectionY("den_pfy", binx, binx)
        if (i == 5):
            h_den = h.ProjectionY("den_pfy", 1, 1)
        h_num = h.ProjectionY("num_pfy", binx+1, binx+1)
        h_den.RebinX(rebin)
        h_num.RebinX(rebin)
    

        g = histogram_divide(h_num, h_den, confint_params=(alpha,), use_effective=use_effective)

        g.SetTitle('After %s' % (filter_names[i-1]))
        g.GetXaxis().SetTitle(h_num.GetXaxis().GetTitle())
        g.GetYaxis().SetTitle('efficiency')
        g.GetYaxis().SetRangeUser(0.0, 1.05)

        garbage.append([g, h_den, h_num])  # stupid python nonsense
    
        g.Draw()

    if zn != '':
        y = v.Get(h_n)
        for i in loop_range:
            binx = i
            c1.cd(i-ind_offset)
            if (i != 5):
                y_den = y.ProjectionY("den_pfy", binx, binx)
            if (i == 5):
                y_den = y.ProjectionY("den_pfy", 1, 1)
            y_num = y.ProjectionY("num_pfy", binx+1, binx+1)
            y_den.RebinX(rebin)
            y_num.RebinX(rebin)
        
    
            w = histogram_divide(y_num, y_den, confint_params=(alpha,), use_effective=use_effective)
    
            w.SetTitle('After %s' % (filter_names[i-1]))
            w.GetXaxis().SetTitle(y_num.GetXaxis().GetTitle())
            w.GetYaxis().SetTitle('efficiency')
    
            garbage.append([w, y_den, y_num])  # stupid python nonsense
    
            w.SetLineColor(ROOT.kRed)
            w.Draw("same")

    c1.cd()

    ps.save(h_n, other_c=c1)

    c1.Clear()
