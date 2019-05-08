#!/usr/bin/env python

import os, sys
from JMTucker.Tools.ROOTTools import *

set_style()

do_fits = True

year = '2018'
cov = ['dxyerr', 'dszerr', 'absdxydszcov']
etabins = ['lt1p5', 'gt1p5']

ps = plot_saver(plot_dir('cov_v_pt_ratio_all_%s' % year), size=(600,600), pdf=True, log=False)

eras = ['B', 'C', 'DE', 'F']
if year == '2018':
    eras = ['A', 'B', 'C', 'D']

bkgr = 'background_%s' % year
datasets = ['JetHT%(yr)s%(era)s' % locals() for yr in [year] for era in eras]

hn = 'h_sel_tracks_%s_v_pt' 
fn_string = '/uscms_data/d3/dquach/crab3dirs/TrackingTreerHistsV23mv3_eta%s/%s.root' 
fn_scale_string = '/uscms_data/d3/dquach/crab3dirs/TrackingTreerHistsV23mv3_eta%s_%sscale/%s.root'

buff = []
colors = [ROOT.kPink-3, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange+7, ROOT.kViolet-4]

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
    ratiohist = ROOT.TH1D('ratio_hist', '', len(binedges)-1, array('d', binedges))
    for bin in range(1, ratio.GetNbinsX()+1):
        err = ratio.GetBinContent(bin) * (div(num.GetBinError(bin), num.GetBinContent(bin))**2 + div(den.GetBinError(bin), den.GetBinContent(bin))**2)**0.5
        ratiohist.SetBinContent(bin, ratio.GetBinContent(bin))
        ratiohist.SetBinError(bin, err)
    ratiohist.GetYaxis().SetRangeUser(0, 1.7)
    ratiohist.GetXaxis().SetRangeUser(1,200)
    ratiohist.SetLineColor(colors[idata])
    ratiohist.SetLineWidth(2)
    ratiohist.SetFillColor(0)
    ratiohist.SetStats(0)
    return ratiohist


names = ['%(yr)s%(era)s Data' % locals() for yr in [year] for era in eras]
for var in cov:
    for etabin in etabins:
        leg1 = ROOT.TLegend(0.65,0.2,0.9,0.4)
        for idata, data in enumerate(datasets):
            num = get_profile(fn_string % (etabin, data), hn % var)
            den = get_profile(fn_string % (etabin, bkgr) if 'dxydszcov' not in var else fn_scale_string % (etabin, data, bkgr), hn % var)

            bins = [x for x in range(0,20,2)]
            bins += [x for x in range(20, 205, 5)]
            #bins += [x for x in range(200, 840, 40)]
            #bins += [x for x in range(800, 2600, 600)]
            newnum = num.Rebin(len(bins)-1, 'newnum', array('d', bins))
            newden = den.Rebin(len(bins)-1, 'newden', array('d', bins))
            #newnum = num.Rebin(40)
            #newden = den.Rebin(40)

            ratio = ratio_hist(newnum, newden)
            ratio.SetTitle('mean %s ratio vs. p_{T};track p_{T} (GeV);mean %s data/MC ratio' % (var, var))

            leg1.AddEntry(ratio, '%s' % (names[idata]))
            if idata == 0:
                ratio.Draw('hist e')
            else:
                ratio.Draw('sames hist e')
            buff.append(ratio)
        leg1.Draw()
        ps.save('%s_ratio_eta%s' % (var, etabin))

def fit_func_dict(cov, etabin):
    if cov == 'dxyerr': 
        if etabin == 'lt1p5':
            fitfuncs = {'JetHT2017B':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=19)*pol1(4) + (x>19 && x<=200)*pol1(6)',
                        'JetHT2017C':'(x<=5)*pol1(0) + (x>5 && x<=8)*pol1(2) + (x>8 && x<=11)*pol1(4) + (x>11 && x<=19)*pol1(6) + (x>19 && x<=200)*pol2(8)',
                        'JetHT2017DE':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=20)*pol1(4) + (x>20 && x<=200)*pol2(6)',
                        'JetHT2017F':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)',
                        'JetHT2018A':'(x<=15)*pol1(0) + (x>15 && x<=200)*pol1(2)',
                        'JetHT2018B':'(x<=5)*pol1(0) + (x>5 && x<=20)*pol1(2) + (x>20&&x<=200)*pol1(4)',
                        'JetHT2018C':'(x<=4)*pol1(0) + (x>4 && x<=20)*pol1(2) + (x>4 && x<=200)*pol2(4)',
                        'JetHT2018D':'(x<=3)*pol1(0) + (x>3 && x<=10)*pol1(2) + (x>10 && x<=15)*pol1(4) + (x>15 && x<=200)*pol2(6)'
                        }
        else:
            fitfuncs = {'JetHT2017B':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=19)*pol1(4) + (x>19 && x<=200)*pol1(6)',
                        'JetHT2017C':'(x<=5)*pol1(0) + (x>5 && x<=8)*pol1(2) + (x>8 && x<=19)*pol1(4) + (x>19 && x<=200)*pol2(6)',
                        'JetHT2017DE':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=20)*pol1(4) + (x>20 && x<=200)*pol2(6)',
                        'JetHT2017F':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)',
                        'JetHT2018A':'(x<=4)*pol1(0) + (x>4 && x<=10)*pol1(2) + (x>10 && x<=22)*pol1(4) + (x>22 && x<=200)*pol2(6)',
                        'JetHT2018B':'(x<=5)*pol1(0) + (x>5 && x<=25)*pol1(2) + (x>25 && x<=200)*pol2(4)',
                        'JetHT2018C':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=20)*pol1(4) + (x>20 && x<=200)*pol2(6)',
                        'JetHT2018D':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)'
                        }
    elif cov == 'dszerr':
        if etabin == 'lt1p5':
            fitfuncs = {'JetHT2017B':'(x<=3)*pol1(0) + (x>3 && x<=7)*pol1(2) + (x>7 && x<=11)*pol1(4) + (x>11 && x<=200)*pol3(6)',
                        'JetHT2017C':'(x<=3)*pol1(0) + (x>3 && x<=7)*pol1(2) + (x>7 && x<=12)*pol1(4) + (x>12 && x<=200)*pol4(6)',
                        'JetHT2017DE':'(x<=3)*pol1(0) + (x>3 && x<=8)*pol1(2) + (x>8 && x<=200)*pol3(4)',
                        'JetHT2017F':'(x<=3.5)*pol1(0) + (x>3.5 && x<=6)*pol1(2) + (x>6 && x<=13)*pol1(4) + (x>13 && x<=200)*pol3(6)',
                        'JetHT2018A':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol2(2) + (x>20 && x<=200)*pol1(5)',
                        'JetHT2018B':'(x<=4)*pol1(0) + (x>4 && x<=10)*pol1(2) + (x>10 && x<=20)*pol1(4) + (x>20 && x<=200)*pol2(6)',
                        'JetHT2018C':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)',
                        'JetHT2018D':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)'
                        }
        else:
            fitfuncs = {'JetHT2017B':'(x<=7)*pol1(0) + (x>7 && x<=17)*pol1(2) + (x>17 && x<=200)*pol2(4)',
                        'JetHT2017C':'(x<=5.5)*pol1(0) + (x>5.5 && x<=10)*pol1(2) + (x>10 && x<=19)*pol1(4) + (x>19 && x<=200)*pol4(6)',
                        'JetHT2017DE':'(x<=7)*pol1(0) + (x>7 && x<=13)*pol1(2) + (x>13 && x<=21)*pol1(4) + (x>21 && x<=200)*pol3(6)',
                        'JetHT2017F':'(x<=7)*pol1(0) + (x>7 && x<=16)*pol1(2) + (x>16 && x<=200)*pol3(4)',
                        'JetHT2018A':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=200)*pol3(4)',
                        'JetHT2018B':'(x<=4)*pol1(0) + (x>4 && x<=17)*pol2(2) + (x>17 && x<=200)*pol1(5)',
                        'JetHT2018C':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol1(6)',
                        'JetHT2018D':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)'
                        }
    else: # dxydszcov
        if etabin == 'lt1p5':
            fitfuncs = {'JetHT2017B':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol1(2) + (x>20)*pol0(4)',
                        'JetHT2017C':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol1(2) + (x>20)*pol0(4)',
                        'JetHT2017DE':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol1(2) + (x>20)*pol0(4)',
                        'JetHT2017F':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol1(2) + (x>20 && x<=60)*pol1(4) + (x>60)*pol0(6)',
                        'JetHT2018A':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=25)*pol1(2)+ (x>25 && x<=200)*pol1(4)',
                        'JetHT2018B':'(x<=5)*pol1(0) + (x>5 && x<=20)*pol1(2) + (x>20 && x<=200)*pol2(4)',
                        'JetHT2018C':'(x<=4)*pol1(0) + (x>4 && x<=25)*pol1(2) + (x>25 && x<=200)*pol2(4)',
                        'JetHT2018D':'(x<=5)*pol1(0) + (x>5 && x<=20)*pol1(2) + (x>20 && x<=60)*pol1(4) + (x>60)*pol0(6)'
                        }

        else:
            fitfuncs = {'JetHT2017B':'(x<=5)*pol1(0) + (x>5 && x<=21)*pol1(2) + (x>21)*pol0(4)',
                        'JetHT2017C':'(x<=4.5)*pol1(0) + (x>4.5 && x<=21)*pol1(2) + (x>21)*pol0(4)',
                        'JetHT2017DE':'(x<=5)*pol1(0) + (x>5 && x<=21)*pol1(2) + (x>21)*pol0(4)',
                        'JetHT2017F':'(x<=5)*pol1(0) + (x>5 && x<=21)*pol1(2) + (x>21)*pol0(4)',
                        'JetHT2018A':'(x<=7)*pol1(0) + (x>7 && x<=20)*pol1(2) + (x>20 && x<=60)*pol1(4) + (x>60)*pol0(6)',
                        'JetHT2018B':'(x<=6)*pol1(0) + (x>6 && x<=20)*pol1(2) + (x>20 && x<=200)*pol2(4)',
                        'JetHT2018C':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=40)*pol1(4) + (x>40 && x<=200)*pol1(6)',
                        'JetHT2018D':'(x<=3.5)*pol1(0) + (x>3.5 && x<=15)*pol1(2) + (x>15 && x<=20)*pol1(4) + (x>20 && x<=60)*pol1(6) + (x>60)*pol0(8)'
                        }
    return fitfuncs
        
if do_fits:
    for var in cov:
        for etabin in etabins:
            for idata, data in enumerate(datasets):
                num = get_profile(fn_string % (etabin, data), hn % var)
                den = get_profile(fn_string % (etabin, bkgr) if 'dxydszcov' not in var else fn_scale_string % (etabin, data, bkgr), hn % var)
    
                bins = [x for x in range(1,20)]
                bins += [x for x in range(20, 210, 5)]
                newnum = num.Rebin(len(bins)-1, 'newnum', array('d', bins))
                newden = den.Rebin(len(bins)-1, 'newden', array('d', bins))
    
                ratio = ratio_hist(newnum, newden)
    
                ratio.GetXaxis().SetRangeUser(1,200)
    
                fitfuncs = fit_func_dict(var, etabin)
                fnc = ROOT.TF1('fnc', '%s' % fitfuncs[data], 1, 200)
                ratio.Fit(fnc, 'Rq')
                ratio.GetYaxis().SetRangeUser(0.5, 1.7)
    
                tratioplot = ROOT.TRatioPlot(ratio)
    
                ratio.Draw('hist e')
                ROOT.gStyle.SetOptFit(0)
                fnc.Draw('same')
                tratioplot.SetGraphDrawOpt("P")
                tratioplot.Draw('same')
                ps.save('%s_%s_ratio_eta%s_fit' % (data, var, etabin))
                
                print
                print '****%s %s eta%s****' % (data, var, etabin)
                print fnc.GetExpFormula()
                print [fnc.GetParameter(x) for x in xrange(fnc.GetNpar())]
                print
