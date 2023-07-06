#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal
from tabulate import tabulate
#import pandas as pd

set_style()
#version = 'V27m'
#version = 'V1UL_Lepm'
#ps = plot_saver(plot_dir('sigeff_wrt_presel_beampipe_origin_%s_correct_release_2018' % version), size=(600,600), pdf=True, log=False)
#ps = plot_saver(plot_dir('sigeff_wrt_presel_V1UL_Lepm_2017'), size=(600,600), pdf=True, log=False)
ps = plot_saver(plot_dir('sigeff_wrt_presel_V1UL_Lepm_2018'), size=(800,600), pdf=True, log=False)

#multijet = Samples.mfv_signal_samples_2018
#dijet = Samples.mfv_stopdbardbar_samples_2018
stoplb = Samples.mfv_stoplb_samples_2018
stopld = Samples.mfv_stopld_samples_2018

qcd_samples = Samples.qcd_lep_samples_2017
ttbar_samples = Samples.met_samples_2017
leptonic_samples = Samples.leptonic_samples_2017
wjet_samples = [Samples.leptonic_samples_2017[0]]
dyjet_samples = Samples.leptonic_samples_2017[1:]
diboson_samples = Samples.diboson_samples_2017

#for sample in multijet + dijet:
    #fn = os.path.join('/uscms/home/joeyr/crabdirs/Histos_within_fiducial_fixed_beampipe_wrt_origin_correct_release%s' % version, sample.name + '.root')

#versions = ['_SingleLep', '_wDispLep']
#lepton_vtx_eff = ['_ele', '_mu', '_tau']
#nice = ['e', 'm', 'tau']
lepton_vtx_eff = ['_ele', '_mu']
nice = ['e', 'm']
colors = [ROOT.kBlue+1, ROOT.kMagenta+1, ROOT.kGreen+1]

#print_data = []

table_ngensv = {
    '00100' : [],
    '00300' : [],
    '01000' : [],
    '10000' : [],
    '30000' : []
    
}
table_nlepinsv = {
    '00100' : [],
    '00300' : [],
    '01000' : [],
    '10000' : [],
    '30000' : []
} 

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
    # h_novtx = f.Get('mfvVertexHistosNoCuts/h_lepdau_novtx%s' % lep)
    # h_vtx = f.Get('mfvVertexHistosNoCuts/h_lepdau_closestvtx%s' % lep)
    # h_invtx = f.Get('mfvVertexHistosNoCuts/h_lepdau_invtx%s' % lep)
    
    # h_novtx = f.Get('MinNtk4mfvVertexHistosPreSel/h_lepdau_novtx%s' % lep)
    # h_vtx = f.Get('MinNtk4mfvVertexHistosPreSel/h_lepdau_closestvtx%s' % lep)
    # h_invtx = f.Get('MinNtk4mfvVertexHistosPreSel/h_lepdau_invtx%s' % lep)
    
    # h_new = f.Get('mfvVertexHistosNoCuts/h_matchlep_wlep%s' % lep)
    # h_new = f.Get('MinNtk4mfvVertexHistosPreSel/h_matchlep_wlep%s' % lep)
    
    if lep == '_ele' :
        h_nomatch = f.Get('mfvAnaCutFlowHistos/h_noe_vtx_cutflow')
        h_match = f.Get('mfvAnaCutFlowHistos/h_e_vtxlep_cutflow')
    elif lep == '_mu' :
        h_nomatch = f.Get('mfvAnaCutFlowHistos/h_nom_vtx_cutflow')
        h_match = f.Get('mfvAnaCutFlowHistos/h_m_vtxlep_cutflow')

    #looking at : N SV that we miss out on / NSV that we have gen matched 
    # num = h_nomatch.GetBinContent(1) - h_nomatch.GetBinContent(4)
    # den = (h_match.GetBinContent(4) + h_nomatch.GetBinContent(4))

    #how many sv we keep after cuts 
    num = h_match.GetBinContent(4)
    den = h_match.GetBinContent(1)

    
    #print_data.append([sample.name, lep, num, den, ratio])
    
    return clopper_pearson(num, den)
   

def getit_nsv(f, lifetime):
    
    #h_matchsv = f.Get('MinNtk4mfvVertexHistosPreSel/h_nsv_genmatched')
    h_nsv = f.Get('MinNtk4mfvVertexHistosPreSel/h_nsv')
    
    h_mmatchsv = f.Get('mfvVertexHistosNoCuts/h_lepdau_invtx_mu')
    h_ematchsv = f.Get('mfvVertexHistosNoCuts/h_lepdau_invtx_el')
    # h_nsv = f.Get('mfvVertexHistosNoCuts/h_nsv')
        
    gennsv = h_matchsv.GetEntries() * 2
    #matchnsv = h_matchsv.GetBinContent(2) + 2* (h_matchsv.GetBinContent(3))
    matchnsv = h_mmatchsv.GetBinContent(2) + h_ematchsv.GetBinContent(2)
    nsv = h_nsv.GetBinContent(2) + 2* (h_nsv.GetBinContent(3)) + 3*(h_nsv.GetBinContent(4)) + 4*(h_nsv.GetBinContent(5)) + 5*(h_nsv.GetBinContent(6)) + 6*(h_nsv.GetBinContent(7)) + 7*(h_nsv.GetBinContent(8))
    #print h_nsv.GetBinContent(9)
    
    h_eleinvtx = f.Get('MinNtk4mfvVertexHistosPreSel/h_matchlep_wlep_ele')
    h_muinvtx = f.Get('MinNtk4mfvVertexHistosPreSel/h_matchlep_wlep_mu')
    
    # h_eleinvtx = f.Get('mfvVertexHistosNoCuts/h_matchlep_wlep_ele')
    # h_muinvtx = f.Get('mfvVertexHistosNoCuts/h_matchlep_wlep_mu')
   
    num = h_eleinvtx.GetBinContent(2) + h_muinvtx.GetBinContent(2)
    den = matchnsv
    
    ratio = (num)/den
    #print_data.append([sample.name, num, den, ratio])
    table_ngensv['%s'%lifetime].append(den)
    table_nlepinsv['%s'%lifetime].append(num)
    # filling the tables : 
    
    return clopper_pearson(num, den)



for sample in stoplb: 
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosULV1Lepm_SingleLep', sample.name + '.root')
    lifetime = sample.name[15:20]
    #print lifetime
    if not os.path.exists(fn):
        # table_ngensv['%s'%lifetime].append(0)
        # table_nlepinsv['%s'%lifetime].append(0)
       # print sample.name + '; not finding it'
        continue
    f = ROOT.TFile(fn)
    # print sample.name
    sample.ys = {n: getit(f,n) for n in lepton_vtx_eff}
    #sample.ys = getit_nsv(f,lifetime)


#kind = 'semilept_lb'
#per = PerSignal('efficiency', y_range=(0.,1.0))
#per = PerSignal('How often genmatched lep in vtx', y_range=(0.,1.0))
per = PerSignal('How Often Vtx passes Cuts with Lep', y_range=(0.,1.0))
#per = PerSignal('How Many Missing SV Out of ALL GenMtchd SV', y_range=(0.,1.0))
#per = PerSignal('How Many SV we keep after Cuts', y_range=(0.,1.0))

for ilep, lep in enumerate(lepton_vtx_eff):
    for sample in stoplb:
        fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosULV1Lepm_SingleLep', sample.name + '.root')
        if not os.path.exists(fn) :
        #print sample.name + '; not finding it'
            continue 
        #ample.y, sample.yl, sample.yh = sample.ys
        sample.y, sample.yl, sample.yh = sample.ys[lep]
    per.add(stoplb, title='#tilde{t} #rightarrow %sb'% nice[ilep], color=colors[ilep])
    
#per.add(stoplb, title='#tilde{t} #rightarrow lb', color=ROOT.kBlue+1)
#per.add(stopld, title='#tilde{t} #rightarrow ld', color=ROOT.kMagenta+1)

per.draw(canvas=ps.c)
# mvpave(per.decay_paves[0], 0.703, 0.098, 6, 0.158)
# mvpave(per.decay_paves[1], 0.703, 0.038, 6, 0.098)
#ps.save('sigeff_compare_genmatch_sv')
#ps.save('sigeff_compare_overall_lepinvtx')
ps.save('sigeff_compare_vtx_aftercuts_lb')

# df_den = pd.DataFrame(data=table_ngensv)
# df_num = pd.DataFrame(data=table_nlepinsv)

#print df_den
#df_den.to_clipboard(sep=',', index=False)
#print (tabulate(print_data, headers = ["sample", "lepton", "numerator", "denominator", "ratio"]))
#print (tabulate(print_data, headers = ["sample", "ngenmatchedsv", "nsv(gen)", "ratio"]))