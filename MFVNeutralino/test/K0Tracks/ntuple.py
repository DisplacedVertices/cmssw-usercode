from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.event_filter = 'muons only novtx' #'jets only novtx'

version = settings.version + 'v1'

debug = False

####

process = ntuple_process(settings)
max_events(process, 50)
remove_output_module(process)
tfileservice(process, 'k0tree.root')
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'qcdht1500_2017' if settings.is_mc else 'JetHT2017F', dataset, 1)
input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/A8C3978F-4BE4-A844-BEE8-8DEE129A02B7.root')
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

#process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices * process.mfvK0s)
#ReferencedTagsTaskAdder(process)('p')

process.mfvEvent.vertex_seed_tracks_src = ''
process.load('JMTucker.Tools.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi') # JMTBAD
process.mfvWeight.throw_if_no_mcstat = False

process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices* process.BadPFMuonFilterUpdateDz * process.fullPatMetSequence * process.mfvTriggerFloats * process.mfvK0s)

ReferencedTagsTaskAdder(process)('p')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    samples = pick_samples(dataset, ttbar=False, all_signal=False)
    set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'), 4)

    ms = MetaSubmitter('K0Ntuple' + version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
