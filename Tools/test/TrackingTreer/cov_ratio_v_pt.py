#!/usr/bin/env python

import os, sys
from JMTucker.Tools.ROOTTools import *

set_style()


do_fits = True
compare_rescaled = False

year = '2018'
#year = '2017'
#cov = ['dxyerr', 'dszerr', 'absdxydszcov']
cov = ['dxyerr', 'dszerr']


etabins = ['lt1p5', 'gt1p5']
#make better bin organization for use 
#eta < 1.5
lep_bins_lt1p5 = [x for x in range(20, 60, 10)]
lep_bins_lt1p5 += [x for x in range(60, 120, 20)]
lep_bins_lt1p5 += [x for x in range(120, 240, 40)]

seltracks_bins_lt1p5 = [x for x in range(0, 10, 2)]
seltracks_bins_lt1p5 += [x for x in range(10, 20, 5)]
seltracks_bins_lt1p5 += [x for x in range(20, 60, 20)]
seltracks_bins_lt1p5 += [x for x in range(60, 140, 40)]
seltracks_bins_lt1p5 += [x for x in range(140,260,60)]

#eta > 1.5 
ele_bins_gt1p5 = [x for x in range(20, 60, 10)]
ele_bins_gt1p5 += [x for x in range(60, 100, 20)]
ele_bins_gt1p5 += [x for x in range(100, 250, 50)]
                    
#good muons 
mu_bins_gt1p5 = [x for x in range(20, 80, 5)]
mu_bins_gt1p5 += [x for x in range(80, 210, 10)]
                    
#sel tracks
seltracks_bins_gt1p5 = [x for x in range(0, 10, 2)]
seltracks_bins_gt1p5 += [x for x in range(10, 20, 5)]
seltracks_bins_gt1p5 += [x for x in range(20, 60, 20)]
seltracks_bins_gt1p5 += [x for x in range(60, 140, 40)]
seltracks_bins_gt1p5 += [x for x in range(140,260,60)]
                    

ps = plot_saver(plot_dir('cov_v_pt_ratio_all_%s' % year), size=(600,600), pdf=True, log=False)

eras = ['B', 'C', 'D', 'E', 'F']
if year == '2018':
    eras = ['A', 'B', 'C', 'D']


bkgr = 'background_leptonpresel_%s' % year
#bkgr = 'bkg_leptonpresel_wqcd_%s' % year
datasets = ['SingleLepton%(yr)s%(era)s' % locals() for yr in [year] for era in eras] 



hn = 'h_pass_muon_tracks_%s_v_pt'
track = 'pass_mu'
# hn = 'h_pass_ele_tracks_%s_v_pt'
# track = 'pass_ele'
#hn_1d = 'h_pass_ele_tracks_pt'
# hn = 'h_sel_nolep_tracks_%s_v_pt'
# track = 'sel_track'
#pt_slices = ['pt_20', 'pt_40', 'pt_60', 'pt_90', 'pt_130', 'pt_200']

is_muon = True
is_ele = False
is_seltracks = False

fn_string = '/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackingTreerULV1_Lepm_cut0_eta%s_2018_wsellep/%s.root'
#fn_scale_string = '/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackingTreerULV1_Lepm_eta%s_era%s_2018/%s.root'
fn_scale_string = ''

buff = []
colors = [ROOT.kPink-3, ROOT.kBlue, ROOT.kGreen+1, ROOT.kOrange+7, ROOT.kViolet-4]


def get_profile(fn, hn):
    f = ROOT.TFile(fn)
    h = f.Get(hn)
    #print h
    profile = h.ProfileX(hn + "pfx")
    profile.SetLineWidth(2)
    profile.SetStats(0)
    buff.append(f)
    return profile

def get_1D(fn, hn) :
    f = ROOT.TFile(fn)
    h = f.Get(hn)
    buff.append(f)
    return h

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


#names = ['%(yr)s%(era)s Data' % locals() for yr in [year] for era in eras]
names = ['%(yr)s%(era)s' % locals() for yr in [year] for era in eras]
if compare_rescaled:
  #idata = 0
  #data = datasets[idata]
  #era = eras[idata]
  var = 'dxyerr'
  for idata, data in enumerate(datasets):
    era = eras[idata]
    for etabin in etabins:
        leg = ROOT.TLegend(0.65,0.7,0.9,0.9)

        if etabin == 'lt1p5':
            if is_muon or is_ele: 
                bins = lep_bins_lt1p5
            else :
                bins = seltracks_bins_lt1p5
        else :
            if is_muon : 
                bins = mu_bins_gt1p5
            elif is_ele :
                bins = ele_bins_gt1p5
            else :
                bins = seltracks_bins_gt1p5

        mc = get_profile(fn_string % (etabin, bkgr), hn % var)
        # print fn_string % (etabin, bkgr)
        #mcrescaled = get_profile(fn_scale_string % (etabin, era, bkgr), hn % var)
        #print fn_scale_string % (etabin, era, bkgr)
        newmc = mc.Rebin(len(bins)-1, 'newmc', array('d', bins))
        newmc.SetLineColor(ROOT.kBlack)
        newmc.SetLineWidth(2)
        newmc.SetFillColor(0)
        newmc.SetStats(0)
        newmc.SetTitle('mean %s vs. p_{T};track p_{T} (GeV);mean %s' % (var, var))
        leg.AddEntry(newmc, 'background MC')
        
        #newmcrescaled = mcrescaled.Rebin(len(bins)-1, 'newmcrescaled', array('d', bins))
        #newmcrescaled.SetLineColor(ROOT.kBlue)
        #newmcrescaled.SetLineWidth(2)
        #newmcrescaled.SetFillColor(0)
        #newmcrescaled.SetStats(0)
        #newmcrescaled.SetTitle('mean %s vs. p_{T};track p_{T} (GeV);mean %s' % (var, var))
        #leg.AddEntry(newmcrescaled, 'background MC rescaled')
        
        d = get_profile(fn_string % (etabin, data), hn % var)
        #print fn_string % (etabin, data)
        newd = d.Rebin(len(bins)-1, 'newd', array('d', bins))
        newd.SetTitle('mean %s vs. p_{T};track p_{T} (GeV);mean %s' % (var, var))
        newd.SetLineColor(colors[idata])
        newd.SetLineWidth(2)
        newd.SetFillColor(0)
        newd.SetStats(0)
        newd.Draw('hist e')
        newmc.Draw('sames hist e')
        #newmcrescaled.Draw('sames hist e')
        leg.AddEntry(newd, '%s' % (names[idata]))
        leg.Draw()
        ps.save('%s_eta%s_rescaled_era%s_%s' % (var, etabin, era, track))


for var in cov:
    for etabin in etabins:

        leg0 = ROOT.TLegend(0.65,0.7,0.9,0.9)

        if etabin == 'lt1p5':
            if is_muon or is_ele: 
                bins = lep_bins_lt1p5
            else :
                bins = seltracks_bins_lt1p5
        else :
            if is_muon : 
                bins = mu_bins_gt1p5
            elif is_ele :
                bins = ele_bins_gt1p5
            else :
                bins = seltracks_bins_gt1p5
        
        #mc = get_profile(fn_string % (etabin, bkgr) if 'absdxydszcov' not in cov else fn_scale_string % (etabin, data, bkgr), hn % var)
        mc = get_profile(fn_string % (etabin, bkgr) if 'absdxydszcov' not in cov else fn_scale_string % (etabin, era, bkgr), hn % var)
        newmc = mc.Rebin(len(bins)-1, 'newmc', array('d', bins))
        newmc.SetLineColor(ROOT.kBlack)
        newmc.SetLineWidth(2)
        newmc.SetFillColor(0)
        newmc.SetStats(0)
        newmc.GetYaxis().SetRangeUser(0, 0.01)
        newmc.SetTitle('mean %s vs. p_{T};track p_{T} (GeV);mean %s' % (var, var))
                   
        newmc.Draw('hist e')
        leg0.AddEntry(newmc, 'background MC')
 
        for idata, data in enumerate(datasets):
            
            d = get_profile(fn_string % (etabin, data), hn % var)
            newd = d.Rebin(len(bins)-1, 'newd', array('d', bins))
            newd.SetTitle('mean %s vs. p_{T};track p_{T} (GeV);mean %s' % (var, var))
            newd.SetLineColor(colors[idata])
            newd.SetLineWidth(2)
            newd.SetFillColor(0)
            newd.SetStats(0)
            newd.Draw('sames hist e')
            leg0.AddEntry(newd, '%s' % (names[idata]))
            
            leg0.Draw()
        ps.save('%s_%s_eta%s' % (track, var, etabin))
 

for var in cov:
    for etabin in etabins:
        leg1 = ROOT.TLegend(0.65,0.2,0.9,0.4)
        for idata, data in enumerate(datasets):
            num = get_profile(fn_string % (etabin, data), hn % var)
            #den = get_profile(fn_string % (etabin, bkgr) if 'absdxydszcov' not in var else fn_scale_string % (etabin, data, bkgr), hn % var)
            den = get_profile(fn_string % (etabin, bkgr) if 'absdxydszcov' not in cov else fn_scale_string % (etabin, eras[idata], bkgr), hn % var)
            if etabin == 'lt1p5':
                if is_muon or is_ele: 
                    bins = lep_bins_lt1p5
                else :
                    bins = seltracks_bins_lt1p5
            else :
                if is_muon : 
                    bins = mu_bins_gt1p5
                elif is_ele :
                    bins = ele_bins_gt1p5
                else :
                    bins = seltracks_bins_gt1p5     
                
            newnum = num.Rebin(len(bins)-1, 'newnum', array('d', bins))
            newden = den.Rebin(len(bins)-1, 'newden', array('d', bins))
            
            
            ratio = ratio_hist(newnum, newden)
            #ratio = ratio_hist(num, den)
            ratio.SetTitle('mean %s ratio vs. p_{T};track p_{T} (GeV);mean %s data/MC ratio' % (var, var))
            #ratio.SetTitle('mean %s ratio vs. eta;track eta;mean %s data/MC ratio' % (var, var))
           
            leg1.AddEntry(ratio, '%s' % (names[idata]))
            if idata == 0:
                ratio.Draw('hist e')
            else:
                ratio.Draw('sames hist e')
            buff.append(ratio)
        leg1.Draw()
        ps.save('%s_%s_ratio_eta%s' % (track, var, etabin))

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
                        'JetHT2018D':'(x<=3)*pol1(0) + (x>3 && x<=10)*pol1(2) + (x>10 && x<=15)*pol1(4) + (x>15 && x<=200)*pol2(6)',

                        # Group A) good electron and Group B) good muon
                        # 'SingleLepton2017B':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017C':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017D':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017E':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017F':'(x>=20 && x<=200)*pol1(0)'
                        
                        #Good Muon
                        # 'SingleLepton2018A':'(x>=20 && x<=60)*pol1(0) + (x>=60 && x<=200)*pol1(2)',
                        # 'SingleLepton2018B':'(x>=20 && x<=60)*pol1(0) + (x>=60 && x<=200)*pol1(2)',
                        # 'SingleLepton2018C':'(x>=20 && x<=60)*pol1(0) + (x>=60 && x<=200)*pol1(2)',
                        # 'SingleLepton2018D':'(x>=20 && x<=60)*pol1(0) + (x>=60 && x<=200)*pol1(2)',
                        
                        'SingleLepton2018A':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018B':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018C':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018D':'(x>=20 && x<=200)*pol1(0)'
                        
                        #Good Electron
                        # 'SingleLepton2018A':'(x>=20 && x<=60)*pol2(0) + (x>=60 && x<=200)*pol1(3)',
                        # 'SingleLepton2018B':'(x>=20 && x<=60)*pol2(0) + (x>=60 && x<=200)*pol1(3)',
                        # 'SingleLepton2018C':'(x>=20 && x<=60)*pol2(0) + (x>=60 && x<=200)*pol1(3)',
                        # 'SingleLepton2018D':'(x>=20 && x<=60)*pol2(0) + (x>=60 && x<=200)*pol1(3)',
                        
                        # # Group C) sel tracks 
                        # 'SingleLepton2017B':'(x<=5)*pol2(0) + (x>5 && x<=40)*pol1(3) + (x>40 && x<=200)*pol1(5)', 
                        # 'SingleLepton2017C':'(x<=5)*pol2(0) + (x>5 && x<=200)*pol1(3)',
                        # 'SingleLepton2017D':'(x<=5)*pol2(0) + (x>5 && x<=200)*pol1(3)',
                        # 'SingleLepton2017E':'(x<=5)*pol2(0) + (x>5 && x<=25)*pol1(3) + (x>25 && x<=200)*pol1(5)',
                        # 'SingleLepton2017F':'(x<=5)*pol2(0) + (x>5 && x<=200)*pol1(3)'
                        # 'SingleLepton2018A':'(x<=4)*pol1(0) + (x>=4 && x<=18)*pol1(2) + (x>=18 && x<=200)*pol2(4)',
                        # 'SingleLepton2018B':'(x<=4)*pol1(0) + (x>=4 && x<=18)*pol1(2) + (x>=18 &&x<=200)*pol2(4)', 
                        # 'SingleLepton2018C':'(x<=4)*pol1(0) + (x>=4 && x<=18)*pol1(2) + (x>=18 && x<=200)*pol2(4)', 
                        # 'SingleLepton2018D':'(x<=4)*pol1(0) + (x>=4 && x<=18)*pol1(2) + (x>=18 && x<=200)*pol2(4)' 

            }
       # dxyerr gt1p5
        else:
            fitfuncs = {'JetHT2017B':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=19)*pol1(4) + (x>19 && x<=200)*pol1(6)',
                        'JetHT2017C':'(x<=5)*pol1(0) + (x>5 && x<=8)*pol1(2) + (x>8 && x<=19)*pol1(4) + (x>19 && x<=200)*pol2(6)',
                        'JetHT2017DE':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=20)*pol1(4) + (x>20 && x<=200)*pol2(6)',
                        'JetHT2017F':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)',
                        'JetHT2018A':'(x<=4)*pol1(0) + (x>4 && x<=10)*pol1(2) + (x>10 && x<=22)*pol1(4) + (x>22 && x<=200)*pol2(6)',
                        'JetHT2018B':'(x<=5)*pol1(0) + (x>5 && x<=25)*pol1(2) + (x>25 && x<=200)*pol2(4)',
                        'JetHT2018C':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=20)*pol1(4) + (x>20 && x<=200)*pol2(6)',
                        'JetHT2018D':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)',

                        # good ele and good muons 
                        
                        # 'SingleLepton2017B':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017C':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017D':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017E':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017F':'(x>=20 && x<=200)*pol1(0)'
                        
                        #Good Muon
                        # 'SingleLepton2018A':'(x>=20 && x<=60)*pol1(0) + (x>=60 && x<=200)*pol1(2)',
                        # 'SingleLepton2018B':'(x>=20 && x<=60)*pol1(0) + (x>=60 && x<=200)*pol1(2)',
                        # 'SingleLepton2018C':'(x>=20 && x<=60)*pol1(0) + (x>=60 && x<=200)*pol1(2)',
                        # 'SingleLepton2018D':'(x>=20 && x<=60)*pol1(0) + (x>=60 && x<=200)*pol1(2)',
                        
                        'SingleLepton2018A':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018B':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018C':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018D':'(x>=20 && x<=200)*pol1(0)'
                        
                        #Good Electron
                        # 'SingleLepton2018A':'(x>=20 && x<=70)*pol2(0) + (x>=70 && x<=200)*pol2(3)', # 65 -> 70
                        # 'SingleLepton2018B':'(x>=20 && x<=65)*pol2(0) + (x>=65 && x<=200)*pol2(3)',
                        # 'SingleLepton2018C':'(x>=20 && x<=70)*pol2(0) + (x>=70 && x<=200)*pol2(3)',
                        # 'SingleLepton2018D':'(x>=20 && x<=65)*pol2(0) + (x>=65 && x<=200)*pol2(3)'

                        # sel tracks 
                        # 'SingleLepton2017B':'(x<=5)*pol2(0) + (x>5 && x<=12)*pol2(3) + (x>12 && x<=45)*pol1(6) + (x>45 && x<=200)*pol1(8)',
                        # 'SingleLepton2017C':'(x<=5)*pol2(0) + (x>5 && x<=10)*pol2(3) + (x>10 && x<=45)*pol1(6) + (x>45 && x<=200)*pol1(8)', 
                        # 'SingleLepton2017D':'(x<=5)*pol2(0) + (x>5 && x<=10)*pol2(3) + (x>10 && x<=45)*pol1(6) + (x>45 && x<=200)*pol1(8)', 
                        # 'SingleLepton2017E':'(x<=5)*pol2(0) + (x>5 && x<=12)*pol2(3) + (x>12 && x<=200)*pol1(6)',
                        # 'SingleLepton2017F':'(x<=5)*pol2(0) + (x>5 && x<=11)*pol2(3) + (x>11 && x<=200)*pol1(6)'
                        # 'SingleLepton2018A':'(x<=4)*pol1(0) + (x>=4 && x<=11)*pol2(2) + (x>=11 && x<=200)*pol2(5)',
                        # 'SingleLepton2018B':'(x<=4)*pol1(0) + (x>=4 && x<=12)*pol2(2) + (x>=12 && x<=200)*pol2(5)', 
                        # 'SingleLepton2018C':'(x<=4)*pol1(0) + (x>=4 && x<=12)*pol2(2) + (x>=12 && x<=200)*pol2(5)', 
                        # 'SingleLepton2018D':'(x<=4)*pol1(0) + (x>=4 && x<=12)*pol2(2) + (x>=12 && x<=200)*pol2(5)' 

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
                        'JetHT2018D':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)',

                       # Group A) good electron & good muon
                        # 'SingleLepton2017B':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017C':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017D':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017E':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017F':'(x>=20 && x<=200)*pol1(0)'
                        
                        #Good Muon & Good Electron
                        'SingleLepton2018A':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018B':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018C':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018D':'(x>=20 && x<=200)*pol1(0)'
                        
                        # #Group B) sel tracks 
                        # 'SingleLepton2017B':'(x<=5)*pol2(0) + (x>5 && x<=20)*pol1(3) + (x>20 && x<=200)*pol1(5)',
                        # 'SingleLepton2017C':'(x<=5)*pol2(0) + (x>5 && x<=200)*pol1(3)',
                        # 'SingleLepton2017D':'(x<=5)*pol2(0) + (x>5 && x<=200)*pol1(3)',
                        # 'SingleLepton2017E':'(x<=5)*pol2(0) + (x>5 && x<=200)*pol1(3)',
                        # 'SingleLepton2017F':'(x<=5)*pol2(0) + (x>5 && x<=200)*pol1(3)',
                        # 'SingleLepton2018A':'(x<=4)*pol1(0) + (x>=4 && x<=10)*pol1(2) + (x>=10 && x<=22)*pol1(4) + (x>=22 && x<=200)*pol2(6)',
                        # 'SingleLepton2018B':'(x<=4)*pol1(0) + (x>=4 && x<=10)*pol1(2) + (x>=10 && x<=200)*pol2(4)',
                        # 'SingleLepton2018C':'(x<=4)*pol1(0) + (x>=4 && x<=10)*pol1(2) + (x>=10 && x<=200)*pol1(4)', 
                        # 'SingleLepton2018D':'(x<=3)*pol1(0) + (x>3 && x<=8)*pol1(2) + (x>=8 && x<=200)*pol1(4)' 

                        }
        #dsz err gt1p5
        else:
            fitfuncs = {'JetHT2017B':'(x<=7)*pol1(0) + (x>7 && x<=17)*pol1(2) + (x>17 && x<=200)*pol2(4)',
                        'JetHT2017C':'(x<=5.5)*pol1(0) + (x>5.5 && x<=10)*pol1(2) + (x>10 && x<=19)*pol1(4) + (x>19 && x<=200)*pol4(6)',
                        'JetHT2017DE':'(x<=7)*pol1(0) + (x>7 && x<=13)*pol1(2) + (x>13 && x<=21)*pol1(4) + (x>21 && x<=200)*pol3(6)',
                        'JetHT2017F':'(x<=7)*pol1(0) + (x>7 && x<=16)*pol1(2) + (x>16 && x<=200)*pol3(4)',
                        'JetHT2018A':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=200)*pol3(4)',
                        'JetHT2018B':'(x<=4)*pol1(0) + (x>4 && x<=17)*pol2(2) + (x>17 && x<=200)*pol1(5)',
                        'JetHT2018C':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol1(6)',
                        'JetHT2018D':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)',
                        
                        #Group A) good electron & good muon
                        # 'SingleLepton2017B':'(x>=20 && x<=200)*pol1(0)', #+ (x>55 && x<=100)*pol1(2) + (x>100 && x<=200)*pol1(4)',
                        # 'SingleLepton2017C':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017D':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017E':'(x>=20 && x<=200)*pol1(0)',
                        # 'SingleLepton2017F':'(x>=20 && x<=200)*pol1(0)'
                        
                        # #Good Muon
                        # 'SingleLepton2018A':'(x>=20 && x<=60)*pol2(0) + (x>=60 && x<=200)*pol1(3)',
                        # 'SingleLepton2018B':'(x>=20 && x<=60)*pol2(0) + (x>=60 && x<=200)*pol1(3)',
                        # 'SingleLepton2018C':'(x>=20 && x<=60)*pol2(0) + (x>=60 && x<=200)*pol1(3)',
                        # 'SingleLepton2018D':'(x>=20 && x<=60)*pol2(0) + (x>=60 && x<=200)*pol1(3)',
                        
                        'SingleLepton2018A':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018B':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018C':'(x>=20 && x<=200)*pol1(0)',
                        'SingleLepton2018D':'(x>=20 && x<=200)*pol1(0)',
                        
                        #Good Electron
                        # 'SingleLepton2018A':'(x>=20 && x<=65)*pol2(0) + (x>=65 && x<=200)*pol2(3)',
                        # 'SingleLepton2018B':'(x>=20 && x<=65)*pol2(0) + (x>=65 && x<=200)*pol2(3)',
                        # 'SingleLepton2018C':'(x>=20 && x<=65)*pol2(0) + (x>=65 && x<=200)*pol2(3)',
                        # 'SingleLepton2018D':'(x>=20 && x<=65)*pol2(0) + (x>=65 && x<=200)*pol2(3)'

                        
                        # #Group C) sel tracks 
                        # 'SingleLepton2017B':'(x<=5)*pol2(0) + (x>5 && x<=15)*pol2(3) + (x>15 && x<=200)*pol1(6)', 
                        # 'SingleLepton2017C':'(x<=5)*pol2(0) + (x>5 && x<=15)*pol2(3) + (x>15 && x<=200)*pol1(6)', 
                        # 'SingleLepton2017D':'(x<=5)*pol2(0) + (x>5 && x<=15)*pol2(3) + (x>15 && x<=200)*pol1(6)',
                        # 'SingleLepton2017E':'(x<=5)*pol2(0) + (x>5 && x<=15)*pol1(3) + (x>15 && x<=200)*pol1(6)', 
                        # 'SingleLepton2017F':'(x<=5)*pol2(0) + (x>5 && x<=19)*pol2(3) + (x>19 && x<=200)*pol1(6)'
                        # 'SingleLepton2018A':'(x<=4)*pol1(0) + (x>=4 && x<=10)*pol1(2) + (x>=10 && x<=22)*pol1(4) + (x>=22 && x<=200)*pol2(6)',
                        # 'SingleLepton2018B':'(x<=4)*pol1(0) + (x>=4 && x<=25)*pol1(2) + (x>=25 && x<=200)*pol2(4)',
                        # 'SingleLepton2018C':'(x<=4)*pol1(0) + (x>=4 && x<=10)*pol1(2) + (x>=10 && x<=18)*pol1(4) + (x>=18 && x<=200)*pol2(6)', 
                        # 'SingleLepton2018D':'(x<=4)*pol1(0) + (x>=4 && x<=10)*pol2(2) + (x>=10 && x<=200)*pol2(5)'

                        }
            
    else:
        #dxydszcov
        if etabin == 'lt1p5':
            fitfuncs = {'JetHT2017B':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol1(2) + (x>20)*pol0(4)',
                        'JetHT2017C':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol1(2) + (x>20)*pol0(4)',
                        'JetHT2017DE':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol1(2) + (x>20)*pol0(4)',
                        'JetHT2017F':'(x<=3.5)*pol1(0) + (x>3.5 && x<=20)*pol1(2) + (x>20 && x<=60)*pol1(4) + (x>60)*pol0(6)',
                        'JetHT2018A':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=25)*pol1(2)+ (x>25 && x<=200)*pol1(4)',
                        'JetHT2018B':'(x<=5)*pol1(0) + (x>5 && x<=20)*pol1(2) + (x>20 && x<=200)*pol2(4)',
                        'JetHT2018C':'(x<=4)*pol1(0) + (x>4 && x<=25)*pol1(2) + (x>25 && x<=200)*pol2(4)',
                        'JetHT2018D':'(x<=5)*pol1(0) + (x>5 && x<=20)*pol1(2) + (x>20 && x<=60)*pol1(4) + (x>60)*pol0(6)',
                        
                        # Lepton tracks (Muon & ELECTRON?)
                        # 'SingleLepton2017B':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        # 'SingleLepton2017C':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        # 'SingleLepton2017D':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        # 'SingleLepton2017E':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        # 'SingleLepton2017F':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        
                        'SingleLepton2018A':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        'SingleLepton2018B':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        'SingleLepton2018C':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        'SingleLepton2018D':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        
                        #Sel Tracks
                        # 'SingleLepton2017B':'(x<=3)*pol1(0) + (x>3 && x<=7)*pol1(2) + (x>7 && x<=20)*pol1(4) + (x>20 && x<=200)*pol1(6)',
                        # 'SingleLepton2017C':'(x<=3)*pol1(0) + (x>3 && x<=7)*pol1(2) + (x>7 && x<=20)*pol1(4) + (x>20 && x<=200)*pol1(6)',
                        # 'SingleLepton2017D':'(x<=3)*pol1(0) + (x>3 && x<=7)*pol1(2) + (x>7 && x<=20)*pol1(4) + (x>20 && x<=200)*pol1(6)',
                        # 'SingleLepton2017E':'(x<=3)*pol1(0) + (x>3 && x<=7)*pol1(2) + (x>7 && x<=20)*pol1(4) + (x>20 && x<=200)*pol1(6)',
                        # 'SingleLepton2017F':'(x<=4)*pol1(0) + (x>4 && x<=15)*pol2(2) + (x>15 && x<=200)*pol1(5)',
                        # 'SingleLepton2018A':'(x<=4)*pol1(0) + (x>4 && x<=10)*pol1(2) + (x>10 && x<=22)*pol1(4) + (x>22 && x<=200)*pol2(6)',
                        # 'SingleLepton2018B':'(x<=5)*pol1(0) + (x>5 && x<=25)*pol1(2) + (x>25 && x<=200)*pol2(4)',
                        # 'SingleLepton2018C':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=20)*pol1(4) + (x>20 && x<=200)*pol2(6)',
                        # 'SingleLepton2018D':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)'
                        
                        }

        else:
            fitfuncs = {'JetHT2017B':'(x<=5)*pol1(0) + (x>5 && x<=21)*pol1(2) + (x>21)*pol0(4)',
                        'JetHT2017C':'(x<=4.5)*pol1(0) + (x>4.5 && x<=21)*pol1(2) + (x>21)*pol0(4)',
                        'JetHT2017DE':'(x<=5)*pol1(0) + (x>5 && x<=21)*pol1(2) + (x>21)*pol0(4)',
                        'JetHT2017F':'(x<=5)*pol1(0) + (x>5 && x<=21)*pol1(2) + (x>21)*pol0(4)',
                        'JetHT2018A':'(x<=7)*pol1(0) + (x>7 && x<=20)*pol1(2) + (x>20 && x<=60)*pol1(4) + (x>60)*pol0(6)',
                        'JetHT2018B':'(x<=6)*pol1(0) + (x>6 && x<=20)*pol1(2) + (x>20 && x<=200)*pol2(4)',
                        'JetHT2018C':'(x<=5)*pol1(0) + (x>5 && x<=10)*pol1(2) + (x>10 && x<=40)*pol1(4) + (x>40 && x<=200)*pol1(6)',
                        'JetHT2018D':'(x<=3.5)*pol1(0) + (x>3.5 && x<=15)*pol1(2) + (x>15 && x<=20)*pol1(4) + (x>20 && x<=60)*pol1(6) + (x>60)*pol0(8)',
                        
                        #ELECTRON tracks
                        # 'SingleLepton2017B':'(x>=20 && x<=45)*pol2(0) + (x>45 && x<=200)*pol1(3)',
                        # 'SingleLepton2017C':'(x>=20 && x<=40)*pol1(0) + (x>40 && x<=200)*pol1(3)',
                        # 'SingleLepton2017D':'(x>=20 && x<=45)*pol2(0) + (x>45 && x<=200)*pol1(3)',
                        # 'SingleLepton2017E':'(x>=20 && x<=40)*pol1(0) + (x>40 && x<=200)*pol1(2)',
                        # 'SingleLepton2017F':'(x>=20 && x<=60)*pol2(0) + (x>60 && x<=200)*pol1(3)',
                        
                        # 'SingleLepton2018A':'(x>=20 && x<=45)*pol2(0) + (x>45 && x<=200)*pol1(3)',
                        # 'SingleLepton2018B':'(x>=20 && x<=40)*pol1(0) + (x>40 && x<=200)*pol1(3)',
                        # 'SingleLepton2018C':'(x>=20 && x<=45)*pol2(0) + (x>45 && x<=200)*pol1(3)',
                        # 'SingleLepton2018D':'(x>=20 && x<=40)*pol1(0) + (x>40 && x<=200)*pol1(2)',
                        
                        
                        #MUON tracks 
                        # 'SingleLepton2017B':'(x>=20 && x<=40)*pol2(0) + (x>40 && x<=75)*pol1(3) + (x>75 && x<=200)*pol1(5)',
                        # 'SingleLepton2017C':'(x>=20 && x<=40)*pol2(0) + (x>40 && x<=75)*pol1(3) + (x>75 && x<=200)*pol1(5)',
                        # 'SingleLepton2017D':'(x>=20 && x<=40)*pol2(0) + (x>40 && x<=75)*pol1(3) + (x>75 && x<=200)*pol1(5)',
                        # 'SingleLepton2017E':'(x>=20 && x<=40)*pol2(0) + (x>40 && x<=75)*pol1(3) + (x>75 && x<=200)*pol1(5)',
                        # 'SingleLepton2017F':'(x>=20 && x<=80)*pol2(0) + (x>80 && x<=200)*pol1(3)',
                        
                        
                        #Sel Tracks 
                        # 'SingleLepton2017D':'(x<=5)*pol2(0) + (x>5 && x<=10)*pol1(3) + (x>10 && x<=18)*pol1(5) + (x>18 && x<=200)*pol1(7)',
                        # 'SingleLepton2017B':'(x<=5)*pol2(0) + (x>5 && x<=10)*pol1(3) + (x>10 && x<=18)*pol1(5) + (x>18 && x<=200)*pol1(7)',
                        # 'SingleLepton2017C':'(x<=5)*pol2(0) + (x>5 && x<=10)*pol1(3) + (x>10 && x<=18)*pol1(5) + (x>18 && x<=200)*pol1(7)',
                        # 'SingleLepton2017E':'(x<=5)*pol2(0) + (x>5 && x<=10)*pol1(3) + (x>10 && x<=18)*pol1(5) + (x>18 && x<=200)*pol1(7)',
                        # 'SingleLepton2017F':'(x<=5)*pol2(0) + (x>5 && x<=14)*pol2(3) + (x>14 && x<=200)*pol1(6)',
                        'SingleLepton2018A':'(x<=4)*pol1(0) + (x>4 && x<=10)*pol1(2) + (x>10 && x<=22)*pol1(4) + (x>22 && x<=200)*pol2(6)',
                        'SingleLepton2018B':'(x<=5)*pol1(0) + (x>5 && x<=25)*pol1(2) + (x>25 && x<=200)*pol2(4)',
                        'SingleLepton2018C':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=20)*pol1(4) + (x>20 && x<=200)*pol2(6)',
                        'SingleLepton2018D':'(x<=5)*pol1(0) + (x>5 && x<=9)*pol1(2) + (x>9 && x<=17)*pol1(4) + (x>17 && x<=200)*pol2(6)'
                        
                        }
    return fitfuncs
        
if do_fits:
    for var in cov:
        for etabin in etabins:
            for idata, data in enumerate(datasets):
                num = get_profile(fn_string % (etabin, data), hn % var)
                den = get_profile(fn_string % (etabin, bkgr) if 'dxydszcov' not in var else fn_scale_string % (etabin, eras[idata], bkgr), hn % var)
    
                if etabin == 'lt1p5':
                    if is_muon or is_ele: 
                        bins = lep_bins_lt1p5
                    else :
                        bins = seltracks_bins_lt1p5
                else :
                    if is_muon : 
                        bins = mu_bins_gt1p5
                    elif is_ele :
                        bins = ele_bins_gt1p5
                    else :
                        bins = seltracks_bins_gt1p5
                
                newnum = num.Rebin(len(bins)-1, 'newnum', array('d', bins))
                newden = den.Rebin(len(bins)-1, 'newden', array('d', bins))
    
                ratio = ratio_hist(newnum, newden)

                ratio.GetXaxis().SetRangeUser(1,200)
    
                fitfuncs = fit_func_dict(var, etabin)
                fnc = ROOT.TF1('fnc', '%s' % fitfuncs[data], 1, 200)
                ratio.Fit(fnc, 'Rq')
                ratio.GetYaxis().SetRangeUser(0.5, 2.0)

                #new_fit = ROOT.TSpline3(ratio, 1, 200)
    
                tratioplot = ROOT.TRatioPlot(ratio)
    
                ratio.Draw('hist e')
                ROOT.gStyle.SetOptFit(0)
                fnc.Draw('same')
                #new_fit.Draw('same')
                tratioplot.SetGraphDrawOpt("P")
                tratioplot.Draw('same')
                ps.save('%s_%s_ratio_eta%s_fit' % (data, var, etabin))
                
                print
                print '****%s %s eta%s****' % (data, var, etabin)
                print fnc.GetExpFormula()
                print [fnc.GetParameter(x) for x in xrange(fnc.GetNpar())]
                print
