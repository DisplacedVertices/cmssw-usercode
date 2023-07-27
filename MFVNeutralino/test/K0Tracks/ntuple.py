from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
if use_btag_triggers :
    settings.event_filter = 'bjets OR displaced dijet' # for new trigger studies
elif use_MET_triggers :
  settings.event_filter = 'met only novtx'
else:
  settings.event_filter = 'jets only novtx'

version = settings.version + 'v2'

debug = False

####

process = ntuple_process(settings)
remove_output_module(process)
tfileservice(process, 'k0tree.root')
max_events(process, 2000)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'qcdht1500_2017' if settings.is_mc else 'JetHT2017F', dataset, 1)
input_files(process,[
  '/uscms/home/joeyr/nobackup/test_files/BTagCSV_2017_UL_test_miniaod.root',
  #'/store/mc/RunIISummer20UL17MiniAODv2/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/30000/9A36F224-68B3-454D-A8CC-B53352322D09.root',
  #'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/2540000/00AF8175-C641-344B-8777-F62041FD6308.root',
  #'/store/data/Run2017C/MET/MINIAOD/UL2017_MiniAODv2-v1/270000/23338FE8-AD9B-8A40-A838-42E4F0AD17E7.root',
  #'/store/mc/RunIISummer20UL18MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/240000/272B27A9-BBBC-1546-BF4B-2D2C189A5748.root',
]
)
cmssw_from_argv(process)

####

from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset

#process.jmtUnpackedCandidateTracks.debug = debug
process.jmtUnpackedCandidateTracks.cut_level = 1

from JMTucker.MFVNeutralino.Vertexer_cfi import kvr_params
process.mfvK0s = cms.EDAnalyzer('MFVK0Treer',
                                #jmtNtupleFiller_pset(settings.is_miniaod, using_rescaled_tracks=False, corrected_met=use_MET_triggers),
                                jmtNtupleFiller_pset(settings.is_miniaod),
                                kvr_params = kvr_params,
                                debug = cms.untracked.bool(debug),
                                )

if use_MET_triggers:
  process.load('JMTucker.Tools.METBadPFMuonDzFilter_cfi')
  process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
  process.mfvTriggerFloats.met_src = cms.InputTag('slimmedMETs', '', 'Ntuple')
  if not settings.is_mc:
    process.mfvTriggerFloats.met_filters_src = cms.InputTag('TriggerResults', '', 'RECO')
  process.mfvTriggerFloats.isMC = settings.is_mc
  process.mfvTriggerFloats.year = settings.year

  # MET correction and filters
  # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription#PF_MET
  from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
  process.load("Configuration.StandardSequences.GeometryRecoDB_cff") 
  runMetCorAndUncFromMiniAOD(process,
                             isData = not settings.is_mc,
                             )
  process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices * process.BadPFMuonFilterUpdateDz * process.fullPatMetSequence * process.mfvTriggerFloats * process.mfvK0s)
else:
  process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices * process.mfvK0s)
ReferencedTagsTaskAdder(process)('p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=True, BTagCSV_data=True)
        #samples = Samples.mfv_signal_samples_2017 + Samples.mfv_stopdbardbar_samples_2017 + Samples.mfv_stopbbarbbar_samples_2017
    elif use_MET_triggers:
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=True, leptonic=True, splitSUSY=False, Zvv=True, met=True, span_signal=False, diboson=True, singletop=True, all_signal=False)
    else:
        samples = pick_samples(dataset, ttbar=False, all_signal=False)
    set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'))
    #set_splitting(samples, dataset, 'default', json_path('ana_2016.json'))

    ms = MetaSubmitter('K0Ntuple' + version + '_Summer20UL_MiniAODv2', dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
