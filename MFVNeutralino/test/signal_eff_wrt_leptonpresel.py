#!/usr/bin/env python

#current set up : get the efficiency w.r.t. preselection (just trigger and event preselection) 
# for : >= 1 SV, >= 1 SV + 1 displ lept >= 100um, >= 1 SV w/ lepton in the SV (Pt >= 20 GeV), >= 2SV
#to compare with results from BDT 

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal
from tabulate import tabulate
#import pandas as pd

set_style()

ps = plot_saver(plot_dir('sigeff_V5UL_Lepm_2018'), size=(800,600), pdf=True, log=False)

stoplb = Samples.mfv_stoplb_samples_2018
stopld = Samples.mfv_stopld_samples_2018

#versions = ['_SingleLep', '_wDispLep']
lepton_vtx_eff = ['_ele', '_mu']
nice = ['e', 'm']
colors = [ROOT.kBlue+1, ROOT.kMagenta+1, ROOT.kGreen+1]

print_data = []

def mvpave(pave, x1, y1, x2, y2):
    pave.SetX1(x1)
    pave.SetX2(x2)
    pave.SetY1(y1)
    pave.SetY2(y2)


## This was to compare single lepton triggers with displaced lepton triggers 
# for i, v in enumerate(versions) : 
#     print "trigger set : ", v
#     #for sample in stopld : 
#     for sample in qcd_samples + ttbar_samples + leptonic_samples + wjet_samples + dyjet_samples + diboson_samples : 
#         print "sample name : ", sample.name 
#         fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosULV1Lepm%s' % v, sample.name + '.root')
#         if not os.path.exists(fn):
#          print 'no', sample.name
#          continue
#         f = ROOT.TFile(fn)
#         t = f.Get('SimpleTriggerResults/t')
#         hr = draw_hist_register(t, True)
#         cut_den = 'MinNtk4pPreSel'
#         #cut_den = 'pSkimSel'
#         h_den = hr.draw('weight', cut_den, binning='1,0,1', goff=True)
#         cut_num = 'MinNtk4pTestSel'
#         #cut_num = 'MinNtk4pFullSel'
#         h_num = hr.draw('weight', cut_num, binning='1,0,1', goff=True)

#         den, _ = get_integral(h_den)
#         print "number of events pass presel : ", den
#         num, _ = get_integral(h_num)
#         print "number of events pass fullsel : ", num
#         sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # ignore integral != entries, just get central value right
#         print '%26s: efficiency = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)
#         #print sample.name, ' ', sample.y
# 

def getit(f,lep):
    h_invtx = f.Get('mfvVertexHistosExtraLooseMinOneVtx/h_lepdau_invtx%s' % lep)
    
    #if take sv0 or 1 that has been gen matched; lepton0 or 1 that has been gen matched; calculate how often the lep is in the sv 
    num = h_invtx.GetBinContent(2)
    den = h_invtx.GetBinContent(1) + h_invtx.GetBinContent(2) 
    
    #ratio = num/den
    #print_data.append([sample.name, lep, num, den, ratio])
    return clopper_pearson(num, den)
   

def getit_nsv(f):
    h_matchsv = f.Get('mfvVertexHistosExtraLooseMinOneVtx/h_nsv_genmatched')
    h_gensv = f.Get('mfvVertexHistosExtraLooseMinOneVtx/h_gensv_winbp')
    
    #at least 1 SV w/ min4tks, bs2derr, bs2ddist cuts 
    #h_nsv = f.Get('mfvVertexHistos_MinOneSelVtx/h_nsv')
    
    #at least 1 SV w/ above + at least 1 displaced lepton 
    #h_nsv = f.Get('mfvVertexHistos_MinOneSelVtx_wDispLep/h_nsv')

    #at least 1 SV w/ vertex cuts & have an assoc lepton in SV 
    #h_nsv = f.Get('mfvVertexHistos_MinOneSelVtx_wAssocLep/h_nsv')
    
    #at least 2 SV w/ vertex cuts 
    #h_nsv = f.Get('mfvVertexHistos_MinTwoSelVtx/h_nsv')
        
    num = h_matchsv.GetBinContent(2) + 2* (h_matchsv.GetBinContent(3))
    den = h_gensv.GetBinContent(2) 
    
    #ratio = (num)/den
    #print_data.append([sample.name, num, den, ratio])
    
    return clopper_pearson(num, den)



for sample in stoplb + stopld: #do both when considering nsv;
#for sample in stopld: #do one sample when considering lep; 

    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosULV7Lepm_SingleLep', sample.name + '.root')
    #fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosULV5Lepm_SingleLep/background_leptonpresel_2018.root')
    lifetime = sample.name[15:20]

    #print lifetime
    if not os.path.exists(fn):
        print ' not finding it'
        continue
    f = ROOT.TFile(fn)
    # print sample.name
    #sample.ys = {n: getit(f,n) for n in lepton_vtx_eff}
    sample.ys = getit_nsv(f)


#kind = 'semilept_lb'
per = PerSignal('SV Reconstruction Eff', y_range=(0.,1.0))
#per = PerSignal('How Often Lepton in Vertex', y_range=(0.,1.0))

#for ilep, lep in enumerate(lepton_vtx_eff):
for sample in stoplb + stopld:
    #for sample in stopld : 
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosULV7Lepm_SingleLep', sample.name + '.root')
    #fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosULV5Lepm_SingleLep/background_leptonpresel_2018.root')
    if not os.path.exists(fn) :
        print sample.name + '; not finding it'
        continue 
    sample.y, sample.yl, sample.yh = sample.ys
    #sample.y, sample.yl, sample.yh = sample.ys[lep]
    print(sample.y)
#per.add(stopld, title='#tilde{t} #rightarrow %sd'% nice[ilep], color=colors[ilep])

per.add(stoplb, title='#tilde{t} #rightarrow lb', color=ROOT.kBlue+1)
per.add(stopld, title='#tilde{t} #rightarrow ld', color=ROOT.kMagenta+1)

per.draw(canvas=ps.c)

# mvpave(per.decay_paves[0], 0.703, 0.098, 6, 0.158)
# mvpave(per.decay_paves[1], 0.703, 0.038, 6, 0.098)
ps.save('sigeff_eff_svreco_geninbp')
#ps.save('sigeff_compare_overall_lepinvtx')


# df_den = pd.DataFrame(data=table_ngensv)
# df_num = pd.DataFrame(data=table_nlepinsv)

#print df_den
#df_den.to_clipboard(sep=',', index=False)
#print (tabulate(print_data, headers = ["sample", "lepton", "numerator", "denominator", "ratio"]))
#print (tabulate(print_data, headers = ["sample", "nsv", "nsv sel", "ratio"]))