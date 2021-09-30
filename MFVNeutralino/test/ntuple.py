#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = False
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
    settings.event_filter = 'met only'
    #settings.event_filter = 'met trigger or low met'
    #settings.event_filter = False
else :
    settings.event_filter = 'jets only'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'mfv_splitSUSY_tau000001000um_M2000_1800_2017', dataset, -1)
#sample_files(process, 'mfv_neu_tau001000um_M1600_year', dataset, 1)
#sample_files(process, 'qcdht0700_year', dataset, 1)
#sample_files(process, 'dyjetstollM50_year', dataset, 1)

input_files(process,[
  "/store/data/Run2017C/SingleMuon/MINIAOD/09Aug2019_UL2017-v1/50000/58DFB2FB-4A16-0D4C-9A7B-7F834A0C9E03.root",
  "/store/data/Run2017C/SingleMuon/MINIAOD/09Aug2019_UL2017-v1/50000/545A3138-42CD-F245-AAB2-DA3E54EBF2AC.root",
                   ])
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
max_events(process,-1)
cmssw_from_argv(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=False) # no data currently; no sliced ttbar since inclusive is used
    elif use_MET_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
        #samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, leptonic=False, splitSUSY=True, Zvv=False, span_signal=False)
        #samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, leptonic=False, splitSUSY=False, Zvv=False, span_signal=False)
    else :
        samples = pick_samples(dataset, qcd=True, ttbar=True, data=False, leptonic=True, splitSUSY=True, Zvv=True)

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
