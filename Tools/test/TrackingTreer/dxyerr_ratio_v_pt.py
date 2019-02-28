#!/usr/bin/env python

import os, sys
from JMTucker.Tools.ROOTTools import *

set_style()

year = '2017'
ps = plot_saver(plot_dir('dxyerr_v_pt_ratio_%s' % year), size=(600,600), pdf=True, log=False)

eras = ['B', 'C', 'DE', 'F']
if year == '2018':
    eras = ['A', 'B', 'C', 'D']

bkgr = 'background_%s' % year
datasets = ['JetHT%(yr)s%(era)s' % locals() for yr in [year] for era in eras]

hn = 'h_sel_tracks_dxyerr_v_pt'
fn_string = '~/private/mfv_946p1/src/JMTucker/Tools/test/TrackingTreer/%s_higherpt/%s.root' 

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
    ratiohist = ROOT.TH1D('ratio_hist', 'mean dxyerr ratio vs. p_{T} for ultra clean tracks;track p_{T} (GeV);mean dxyerr data/MC ratio', len(binedges)-1, array('d', binedges))
    for bin in range(1, ratio.GetNbinsX()+1):
        err = ratio.GetBinContent(bin) * (div(num.GetBinError(bin), num.GetBinContent(bin))**2 + div(den.GetBinError(bin), den.GetBinContent(bin))**2)**0.5
        ratiohist.SetBinContent(bin, ratio.GetBinContent(bin))
        ratiohist.SetBinError(bin, err)
    return ratiohist

colors = [ROOT.kPink-3, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange+7, ROOT.kViolet-4]

leg1 = ROOT.TLegend(0.5,0.7,0.75,0.9)
for idata, data in enumerate(datasets):
    num = get_profile(fn_string % (year, data), hn)
    den = get_profile(fn_string % (year, bkgr), hn)

    bins = [x for x in range(1,20)]
    bins += [x for x in range(20, 202, 2)]
    bins += [x for x in range(200, 840, 40)]
    bins += [x for x in range(800, 2400, 400)]
    newnum = num.Rebin(len(bins)-1, 'newnum', array('d', bins))
    newden = den.Rebin(len(bins)-1, 'newden', array('d', bins))

    ratio = ratio_hist(newnum, newden)

    ratio.GetYaxis().SetRangeUser(0, 3)
    ratio.GetXaxis().SetRangeUser(1,2000)
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

fitfuncs = {'JetHT2017B':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=18)*pol1(4) + (x>18 && x<=40)*pol1(6) + (x>40 && x<=60)*pol1(8) + (x>60 && x<=200)*pol1(10)',
            'JetHT2017C':'(x<=5)*pol1(0) + (x>5 && x<=8)*pol1(2) + (x>8 && x<=20)*pol3(4) + (x>20 && x<=60)*pol3(8) + (x>60 && x<=200)*pol1(12)',
            'JetHT2017DE':'(x<=5)*pol1(0) + (x>5 && x<=7)*pol1(2) + (x>7 && x<=14)*pol1(4) + (x>14 && x<=20)*pol1(6) + (x>20 && x<=59)*pol3(8) + (x>59 && x<=200)*pol2(12)',
            'JetHT2017F':'(x<=5)*pol1(0) + (x>5 && x<=8)*pol1(2) + (x>8 && x<=11)*pol1(4) + (x>11 && x<=15)*pol1(6) + (x>15 && x<=40)*pol3(8) + (x>40 && x<=200)*pol2(12)',
            }

for idata, data in enumerate(datasets):
    num = get_profile(fn_string % (year, data), hn)
    den = get_profile(fn_string % (year, bkgr), hn)

    bins = [x for x in range(1,20)]
    bins += [x for x in range(20, 202, 2)]
    newnum = num.Rebin(len(bins)-1, 'newnum', array('d', bins))
    newden = den.Rebin(len(bins)-1, 'newden', array('d', bins))

    ratio = ratio_hist(newnum, newden)

    ratio.GetYaxis().SetRangeUser(0,3)
    ratio.GetXaxis().SetRangeUser(1,200)
    ratio.SetLineColor(colors[idata])
    ratio.SetLineWidth(2)
    ratio.SetFillColor(0)
    ratio.SetStats(0)

    fnc = ROOT.TF1('fnc', '%s' % fitfuncs[data], 1, 200)
    ratio.Fit(fnc, 'R')
    ratio.GetYaxis().SetRangeUser(0.9, 1.7)

    tratioplot = ROOT.TRatioPlot(ratio)

    ratio.Draw('hist e')
    ROOT.gStyle.SetOptFit(0)
    fnc.Draw('same')
    tratioplot.SetGraphDrawOpt("P")
    tratioplot.Draw('same')
    ps.save('%s_ratio_fit' % data)
