from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev25m'
sample_files(process, 'mfv_neu_tau001000um_M0800_2017', dataset, 1)
tfileservice(process, 'jet_energy.root')
global_tag(process)
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

process.mfvAnalysisCuts.apply_presel = 0
process.mfvAnalysisCuts.min_njets = 4
process.mfvAnalysisCuts.min_ht = 0
#process.mfvAnalysisCuts.apply_vertex_cuts = False

process.mfvJetEnergyHistosJES = cms.EDAnalyzer('MFVJetEnergyHistos',
                                               mevent_src = cms.InputTag('mfvEvent'),
                                               weight_src = cms.InputTag('mfvWeight'),
                                               jes = cms.bool(True),
                                               )

process.mfvJetEnergyHistosJER = process.mfvJetEnergyHistosJES.clone(jes = False)

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.mfvWeight * process.mfvJetEnergyHistosJES * process.mfvJetEnergyHistosJER)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    samples = pick_samples(dataset, all_signal='only')
    set_splitting(samples, dataset, 'histos')

    cs = CondorSubmitter('JetEnergyHistosV16',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = per_sample_pileup_weights_modifier(),
                         )
    cs.submit_all(samples)
