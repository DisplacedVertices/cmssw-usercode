import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.CMSSWTools import which_global_tag
from JMTucker.Tools.Year import year

dataset = 'ntuplev16'
sample_files(process, 'mfv_neu_tau01000um_M0800', dataset, 1)
process.TFileService.fileName = 'jet_energy.root'
process.maxEvents.input = -1
file_event_from_argv(process)
geometry_etc(process, which_global_tag(True, year, H=False, repro=False))

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.JetEnergyHistos_cfi')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

process.mfvAnalysisCuts.apply_presel = 0
process.mfvAnalysisCuts.min_njets = 4
process.mfvAnalysisCuts.min_ht = 0

process.mfvJetEnergyHistos = cms.EDAnalyzer('MFVJetEnergyHistos',
                                            mevent_src = cms.InputTag('mfvEvent'),
                                            weight_src = cms.InputTag('mfvWeight'),
                                            jes = cms.bool(False),
                                            )

process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvWeight * process.mfvAnalysisCuts * process.mfvJetEnergyHistos)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples 
    samples = Samples.mfv_signal_samples + Samples.mfv_stopdbardbar_samples

    from JMTucker.Tools.MetaSubmitter import set_splitting
    set_splitting(samples, dataset, 'histos')

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('JetEnergyHistosV16',
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)
