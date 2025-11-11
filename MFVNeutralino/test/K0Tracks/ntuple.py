from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
#changed this to False to get data jobs to run properly
settings.is_mc = False
settings.is_miniaod = True
#settings.event_filter = 'jets only novtx' Alec commented
settings.event_filter = 'muons only novtx'

version = settings.version + 'v1'

debug = False

####

process = ntuple_process(settings)
#max_events(process, 10000)
max_events(process, 10)
remove_output_module(process)
tfileservice(process, 'k0tree.root')
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'qcdht1500_2017' if settings.is_mc else 'JetHT2017F', dataset, 1)
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/DE019DB3-A431-7546-8BC1-30ABC37AD495.root')
#input_files(process, '/store/mc/RunIISummer20UL16MiniAODAPVv2/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/021F6565-4CCB-6F42-AF5E-6F60D8B8BF6B.root')
#input_files(process, '/store/mc/RunIISummer20UL18MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/110000/21CACF46-2819-A34A-AF51-127DB6F04E90.root')
input_files(process, '/uscms/home/joeyr/nobackup/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')
cmssw_from_argv(process)

####

from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset

#process.jmtUnpackedCandidateTracks.debug = debug
process.jmtUnpackedCandidateTracks.cut_level = 1

from JMTucker.MFVNeutralino.Vertexer_cfi import kvr_params
process.mfvK0s = cms.EDAnalyzer('MFVK0Treer',
                                jmtNtupleFiller_pset(settings.is_miniaod),
                                kvr_params = kvr_params,
                                debug = cms.untracked.bool(debug),
                                )

if use_MET_triggers: ###Alec added from this line
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
  #process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices * process.mfvK0s)
  #process.p = cms.Path(process.mfvEventFilterSequence *process.mfvGenParticles*process.BadPFMuonFilterUpdateDz * process.fullPatMetSequence * process.mfvTriggerFloats) Alec later commented because not generating trees properly
  process.mfvEvent.vertex_seed_tracks_src = ''
  process.load('JMTucker.Tools.WeightProducer_cfi')
  process.load('JMTucker.MFVNeutralino.WeightProducer_cfi') # JMTBAD
  process.mfvWeight.throw_if_no_mcstat = False
 
  process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices* process.BadPFMuonFilterUpdateDz * process.fullPatMetSequence * process.mfvTriggerFloats * process.mfvK0s)
ReferencedTagsTaskAdder(process)('p')  ###Alec to this line from btag branch

#process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices * process.mfvK0s)  Alec commented
#ReferencedTagsTaskAdder(process)('p')   Alec commented

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    #samples = pick_samples(dataset, ttbar=False, all_signal=False) Alec commented              SWITCH BETWEEN data AND MC BELOW DEPENDING ON WHAT is_mc IS SET TO!!!!
    #samples = pick_samples(dataset, Lepton_data=True, leptonic=True, diboson=True, qcd_lep=False, ttbar=True, all_signal=False)#Alec set qcd_lep=False, qcd negligible to Z and K
    #samples = pick_samples(dataset, Lepton_data=False, leptonic=True, diboson=True, qcd_lep=False, ttbar=True, all_signal=False) #MC only
    samples = pick_samples(dataset, Lepton_data=True, leptonic=False, diboson=False, qcd_lep=False, ttbar=False, all_signal=False) #data only
    #set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'), 4)
    set_splitting(samples, dataset, 'default', json_path('ana_2016.json' if year in [20161, 20162] else 'ana_2017p8.json'), 4)

    ms = MetaSubmitter('mfvK0sNtuple20161_masswide_' + version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
