#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal


filter_hist_dir = ''
di_or_tri = ''
use_presel = False

if use_presel:
    filter_hist_dir = 'mfvFilterHistosPreSel'
else:
    filter_hist_dir = 'mfvFilterHistosNoCuts'

# 0: filters for di-bjet  trigger
# 1: filters for tri-bjet trigger
filter_opt = 1

if filter_opt == 0:
    n_cols = 2
    n_rows = 2
    loop_range  = range(1,5)
    ind_offset  = 0
    rebin = 2
    di_or_tri = 'Di'

if filter_opt == 1:
    n_cols = 4
    n_rows = 3
    loop_range  = range(5,15)
    ind_offset  = 4
    rebin = 2
    di_or_tri = 'Tri'

set_style()
version = 'test'
ps = plot_saver(plot_dir('filter_tocs_%s' % version), size=(1000,600), pdf=False, log=False)

alpha = 1.0 - 0.6827
use_effective = True

#fn = '/uscms_data/d3/shogan/crab_dirs/HistosDFLavV30Tm' + di_or_tri + 'BjetOnly/mfv_neu_tau000300um_M0400_2017.root'    # Black curve
#zn = '/uscms_data/d3/shogan/crab_dirs/HistosDFLavV30Tm' + di_or_tri + 'BjetOnly/ggHToSSTodddd_tau1mm_M40_2017.root'    # Red curve
#an = '/uscms_data/d3/shogan/crab_dirs/HistosDFLavV30Tm' + di_or_tri + 'BjetOnly/ttbar_2017.root'    # Red curve

fn = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetGoofin/mfv_neu_tau000300um_M0400_2017.root'    # Black curve
zn = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetGoofin/ggHToSSTodddd_tau1mm_M40_2017.root'    # Red curve
an = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetGoofin/ttbar_2017.root'    # Red curve

f = ROOT.TFile(fn)
t = f.Get(filter_hist_dir)

if zn != '':
    z = ROOT.TFile(zn)
    v = z.Get(filter_hist_dir)

if an != '':
    a = ROOT.TFile(an)
    b = a.Get(filter_hist_dir)

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

    print(h_n)
    skip_this_hist = False

    for mystr in ['all', 'energy', '5', '6', '7', '8', '9', '10', 'bit', 'idp', 'pt_by_', 'online_offline', 'bsort']:
        if mystr in h_n:
            skip_this_hist = True

    if skip_this_hist:
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

        garbage.append([g, h_den, h_num])  #  python nonsense
    
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
    
            garbage.append([w, y_den, y_num])  #  python nonsense
    
            w.SetLineColor(ROOT.kRed)
            w.Draw("same")

    if an != '':
        c = b.Get(h_n)
        for i in loop_range:
            binx = i
            c1.cd(i-ind_offset)
            if (i != 5):
                c_den = c.ProjectionY("den_pfy", binx, binx)
            if (i == 5):
                c_den = c.ProjectionY("den_pfy", 1, 1)
            c_num = c.ProjectionY("num_pfy", binx+1, binx+1)
            c_den.RebinX(rebin)
            c_num.RebinX(rebin)
        
    
            d = histogram_divide(c_num, c_den, confint_params=(alpha,), use_effective=use_effective)
    
            d.SetTitle('After %s' % (filter_names[i-1]))
            d.GetXaxis().SetTitle(y_num.GetXaxis().GetTitle())
            d.GetYaxis().SetTitle('efficiency')
    
            garbage.append([d, c_den, c_num])  #  python nonsense
    
            d.SetLineColor(ROOT.kBlue)
            d.Draw("same")



    c1.cd()

    ps.save(h_n, other_c=c1)

    c1.Clear()

tot_effs_f = f.Get(filter_hist_dir).Get('h_hlt_calo_jet_eta_0') # choosing a variable that isn't really used, and never has over/underflow
tot_effs_z = z.Get(filter_hist_dir).Get('h_hlt_calo_jet_eta_0')
tot_effs_a = a.Get(filter_hist_dir).Get('h_hlt_calo_jet_eta_0')

for k in loop_range:
    binx = k

    if (k != 5):
        n_den_f = tot_effs_f.ProjectionY("den_pfy_f", binx, binx).GetEntries()
        n_den_z = tot_effs_z.ProjectionY("den_pfy_z", binx, binx).GetEntries()
        n_den_a = tot_effs_a.ProjectionY("den_pfy_a", binx, binx).GetEntries()
        
    else:
        n_den_f = tot_effs_f.ProjectionY("den_pfy_f", 1, 1).GetEntries()
        n_den_z = tot_effs_z.ProjectionY("den_pfy_z", 1, 1).GetEntries()
        n_den_a = tot_effs_a.ProjectionY("den_pfy_a", 1, 1).GetEntries()

    n_num_f= tot_effs_f.ProjectionY("num_pfy_f", binx+1, binx+1).GetEntries()
    n_num_z= tot_effs_z.ProjectionY("num_pfy_z", binx+1, binx+1).GetEntries()
    n_num_a= tot_effs_a.ProjectionY("num_pfy_a", binx+1, binx+1).GetEntries()

    print '\n' + filter_names[k-1]
    print 'eff_f: ', round(n_num_f/n_den_f, 6)
    print 'eff_z: ', round(n_num_z/n_den_z, 6)
    print 'eff_a: ', round(n_num_a/n_den_a, 6)


