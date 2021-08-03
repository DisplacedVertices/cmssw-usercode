#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
settings.keep_tk = True
if use_btag_triggers :
    settings.event_filter = 'bjets OR displaced dijet veto HT' # for new trigger studies
elif use_MET_triggers :
    #settings.event_filter = 'met only'
    settings.event_filter = 'met trigger or low met'
    #settings.event_filter = False
else :
    settings.event_filter = 'jets only'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'mfv_splitSUSY_tau000001000um_M2000_1800_2017', dataset, 1)
#sample_files(process, 'mfv_neu_tau001000um_M1600_year', dataset, 1)
sample_files(process, 'ttbar_year', dataset, 1)
#sample_files(process, 'dyjetstollM50_year', dataset, 1)

#input_files(process,[
#                     'root://cmseos.fnal.gov//store/user/ali/splitSUSY/splitSUSY_M2000_1800_ctau100p0_TuneCP2_13TeV_pythia8_RunIIFall17_MINIAODSIM_v2_summaryProd/output_8.root',
#                     'root://cmseos.fnal.gov//store/user/ali/splitSUSY/splitSUSY_M2000_1800_ctau100p0_TuneCP2_13TeV_pythia8_RunIIFall17_MINIAODSIM_v2_summaryProd/output_9.root',
#                    #'/store/mc/RunIIFall17MiniAODv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/2E6A7CCF-6606-E911-B184-AC1F6B0DE490.root',
#                    #'/store/mc/RunIIFall17MiniAODv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/8AFAF178-4206-E911-A85F-008CFA1112CC.root',
#                    #'/store/mc/RunIIFall17MiniAODv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/EE806BFB-9AFE-E811-995A-0025905C3E38.root',
#                    '/store/mc/RunIIFall17MiniAODv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP2_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/EE806BFB-9AFE-E811-995A-0025905C3E38.root',
#                   ])
#set_events(process, [
#      (1,1,5504),
#       (1,1,9424),
#      #(1,1,5071),
#      #(1,1,5075),
#      #(1,1,5100),
#      #(1,1,5121),
#      #(1,1,5131),
#      #(1,1,5134),
#      #(1,1,5210),
#      #(1,1,5216),
#      (1,1,5199),
#      (1,1,5201),
#      (1,1,5203),
#      (1,1,5205),
#      (1,1,5209),
#      (1,1,5212),
#      (1,1,5213),
#      (1,1,5214),
#      (1,1,5220),
#      (1,1,5221),
#      (1,1,),
#      (1,1,),
#      (1,1,),
#      (1,1,),
#      ])
max_events(process,1000)
cmssw_from_argv(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=not settings.run_n_tk_seeds, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
    elif use_MET_triggers :
        #samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, leptonic=False, bjet=False, splitSUSY=True, Zvv=True, met=True, span_signal=False)
        #samples = pick_samples(dataset, qcd=False, ttbar=False, all_signal=False, data=False, leptonic=False, bjet=False, splitSUSY=True, Zvv=False, span_signal=False)
        samples = pick_samples(dataset, qcd=False, ttbar=True, all_signal=False, data=False, leptonic=False, bjet=False, splitSUSY=False, Zvv=False, span_signal=False)
    else :
        samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, leptonic=True, bjet=True, splitSUSY=True, Zvv=True)
        #samples = pick_samples(dataset, all_signal=not settings.run_n_tk_seeds)

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
