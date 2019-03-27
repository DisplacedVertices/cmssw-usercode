from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.event_filter = 'jets only novtx'

version = settings.version + 'v2'

debug = False

####

process = ntuple_process(settings)
remove_output_module(process)
tfileservice(process, 'splitpv.root')
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'qcdht1500_2017' if settings.is_mc else 'JetHT2017F', dataset, 1)
cmssw_from_argv(process)

####

from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset

from JMTucker.MFVNeutralino.Vertexer_cfi import kvr_params
process.mfvSplitPVs = cms.EDAnalyzer('MFVSplitPV',
                                     jmtNtupleFiller_pset(settings.is_miniaod),
                                     kvr_params = kvr_params,
                                     debug = cms.untracked.bool(debug),
                                     )

process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices * process.mfvSplitPVs)

ReferencedTagsTaskAdder(process)('p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.data_samples_2017 + Samples.qcd_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018 + Samples.qcd_samples_2017

    set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'), 16)

    ms = MetaSubmitter('SplitPVNtuple' + version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
