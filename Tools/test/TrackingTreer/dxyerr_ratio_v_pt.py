#!/usr/bin/env python

import os, sys
from JMTucker.Tools.ROOTTools import *

set_style()

year = '2017'
ps = plot_saver(plot_dir('dxyerr_v_pt_ratio_defaultcuts_etalt1p5_%s' % year), size=(600,600), pdf=True, log=False)

eras = ['B', 'C', 'DE', 'F']# ['B', 'C', 'D', 'E', 'F']
if year == '2018':
    eras = ['A', 'B', 'C', 'D']

bkgr = 'background_%s' % year
datasets = ['JetHT%(yr)s%(era)s' % locals() for yr in [year] for era in eras]

hn = 'h_sel_tracks_dxyerr_v_pt'
fn_string = '/uscms_data/d3/dquach/TrackingTreer/defaultcuts_etalt1p5_%s/%s.root' 

buff = []

def get_profile(fn, hn):
    f = ROOT.TFile(fn)
    h = f.Get(hn)
    profile = h.ProfileX(hn + "pfx")
    profile.SetLineWidth(2)
    profile.SetStats(0)
    buff.append(f)
    return profile

def div(x, y):
    return 0 if y == 0 else x / y

def ratio_hist(num, den):
    ratio = num.Clone('ratio')
    ratio.Divide(den)
    binedges = []
    for bin in range(1, ratio.GetNbinsX()+2):
        binedges.append(ratio.GetBinLowEdge(bin))
    ratiohist = ROOT.TH1D('ratio_hist', 'mean dxyerr ratio vs. p_{T};track p_{T} (GeV);mean dxyerr data/MC ratio', len(binedges)-1, array('d', binedges))
    for bin in range(1, ratio.GetNbinsX()+1):
        err = ratio.GetBinContent(bin) * (div(num.GetBinError(bin), num.GetBinContent(bin))**2 + div(den.GetBinError(bin), den.GetBinContent(bin))**2)**0.5
        ratiohist.SetBinContent(bin, ratio.GetBinContent(bin))
        ratiohist.SetBinError(bin, err)
    return ratiohist

colors = [ROOT.kPink-3, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange+7, ROOT.kViolet-4]

leg1 = ROOT.TLegend(0.65,0.7,0.9,0.9)
for idata, data in enumerate(datasets):
    num = get_profile(fn_string % (year, data), hn)
    den = get_profile(fn_string % (year, bkgr), hn)

#    bins = [x for x in range(1,20,2)]
#    bins += [x for x in range(20, 202, 5)]
#    bins += [x for x in range(200, 840, 40)]
#    bins += [x for x in range(800, 2600, 600)]
#    newnum = num.Rebin(len(bins)-1, 'newnum', array('d', bins))
#    newden = den.Rebin(len(bins)-1, 'newden', array('d', bins))
    newnum = num.Rebin(40)
    newden = den.Rebin(40)

    ratio = ratio_hist(newnum, newden)

    ratio.GetYaxis().SetRangeUser(0, 2)
    ratio.GetXaxis().SetRangeUser(1,200)
    ratio.SetLineColor(colors[idata])
    ratio.SetLineWidth(2)
    ratio.SetFillColor(0)
    ratio.SetStats(0)
    leg1.AddEntry(ratio, '%s' % (datasets[idata]))
    if idata == 0:
        ratio.Draw('hist e')
    else:
        ratio.Draw('sames hist e')
    buff.append(ratio)
leg1.Draw()
ps.save('ratio')

fitfuncs = {'JetHT2017B':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=19)*pol1(4) + (x>19)*pol1(6)',
            'JetHT2017C':'(x<=5)*pol1(0) + (x>5 && x<=8)*pol1(2) + (x>8 && x<=11)*pol1(4) + (x>11)*pol1(6)',
            'JetHT2017DE':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=20)*pol1(4) + (x>20)*pol2(6)',
            'JetHT2017F':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17)*pol2(6)',
            }

for idata, data in enumerate(datasets):
    num = get_profile(fn_string % (year, data), hn)
    den = get_profile(fn_string % (year, bkgr), hn)

    bins = [x for x in range(1,20)]
    bins += [x for x in range(20, 204, 4)]
    newnum = num.Rebin(len(bins)-1, 'newnum', array('d', bins))
    newden = den.Rebin(len(bins)-1, 'newden', array('d', bins))

    ratio = ratio_hist(newnum, newden)

    ratio.GetXaxis().SetRangeUser(1,200)
    ratio.SetLineColor(colors[idata])
    ratio.SetLineWidth(2)
    ratio.SetFillColor(0)
    ratio.SetStats(0)

    fnc = ROOT.TF1('fnc', '%s' % fitfuncs[data], 1, 200)
    ratio.Fit(fnc, 'R')
    ratio.GetYaxis().SetRangeUser(0.8, 1.5)

    tratioplot = ROOT.TRatioPlot(ratio)

    ratio.Draw('hist e')
    ROOT.gStyle.SetOptFit(0)
    fnc.Draw('same')
    tratioplot.SetGraphDrawOpt("P")
    tratioplot.Draw('same')
    ps.save('%s_ratio_fit' % data)
