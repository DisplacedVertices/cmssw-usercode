#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False 
settings.keep_all = False #it was False to filler events by default
settings.keep_gen = False
if use_btag_triggers :
    settings.event_filter = 'bjets OR displaced dijet veto HT' # for new trigger studies
else :
    settings.event_filter = 'jets only'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'mfv_neu_tau001000um_M1600_2017', dataset, 1)
#max_events(process, 100)
#input_files(process, '/uscms/home/joeyr/nobackup/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8_MINIAODSIM_PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_testfile.root') 
#input_files(process, '~/nobackup/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8_testfile2.root')
#input_files(process, '/eos/uscms/store/user/shogan/stop_bbarbbar_miniaod/mfv_stopbbarbbar_tau001000um_M1600_2017')
#input_files(process, '/eos/uscms/store/mc/RunIIFall17MiniAODv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/4C30AF82-EAFE-E811-A934-0025904CF102.root')
#input_files(process,' root://cmsxrootd-site.fnal.gov//store/mc/RunIIFall17MiniAODv2/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/10000/28BE28C9-175D-E811-B983-002590E39F2E.root')
#input_files(process,'root://cmsxrootd.fnal.gov//store/mc/RunIIFall17MiniAODv2/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/80000/4A94755A-F10B-E911-9B14-246E96D14C70.root')
#input_files(process,'root://cmseos.fnal.gov//store/mc/RunIIFall17MiniAODv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/B087C639-C503-E911-BF3F-B083FECFEF7C.root')

#input_files(process, ['/store/mc/RunIIFall17MiniAODv2/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/24BDABCC-BC86-E811-BB9E-0CC47AD98CFA.root','/store/mc/RunIIFall17MiniAODv2/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/40000/14F7EEED-A79E-E811-A065-0CC47AD98B8E.root','/store/mc/RunIIFall17MiniAODv2/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/80000/6E377E22-090C-E911-9BD4-A4BF011588E0.root'])
#set_events(process,[(1,63544,32153108),(1,64757,32766607),(1,66843,33822521),(1,104823,53040256),(1,104577,52915600),(1,2551,2782096),(1,2771,3022676),(1,58,57620),(1,58,57627),(1,58,57619),(1,58,57796),(1,58,57811),(1,58,57620),(1,58,57627)])
#input_files(process,['/store/mc/RunIIFall17MiniAODv2/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/8414233C-E34E-E811-AA14-0025904CDDFA.root','/store/mc/RunIIFall17MiniAODv2/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/9CDA00C0-4651-E811-BA93-D4AE52E7F9ED.root','/store/mc/RunIIFall17MiniAODv2/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/BEB07ABE-8551-E811-A3BE-0CC47A4D763C.root','/store/mc/RunIIFall17MiniAODv2/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/64293046-0751-E811-A809-0CC47A4C8E7E.root'])
#set_events(process,[(1,485881,302703834),(1,485881,302703813),(1,530355,330410896),(1,375638,234021984),(1,386780,240963628),(1,386781,240964514),(1,435811,271509768),(1,461831,287720114)])

input_files(process, 'root://cmsxrootd.fnal.gov//store/mc/RunIIFall17MiniAODv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/743B6FB5-4302-E911-A003-0CC47AD98F6E.root')
set_events(process,[(1,33,32091)])
cmssw_from_argv(process)
silence_messages(process, ['TwoTrackMinimumDistanceHelixLine'])
silence_messages(process, ['TwoTrackMinimumDistance']) 

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = pick_samples(dataset, qcd=True, ttbar=True, span_signal=False, all_signal=False, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
        #samples = [getattr(Samples, 'ttbarht1200_2017')]
        samples = [getattr(Samples, 'mfv_neu_tau001000um_M1600_2017')]
        #samples = [getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1600_2017')] 
    else :
        #samples = pick_samples(dataset,qcd=True,ttbar=True, data=False, span_signal=False, all_signal=False)
        #samples = [getattr(Samples, 'ttbarht1200_2017')]
        samples = [getattr(Samples, 'mfv_neu_tau001000um_M1600_2017')]
        #samples = [getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1600_2017')] 
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod),signals_no_event_filter_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
