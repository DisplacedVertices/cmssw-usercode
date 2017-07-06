import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.MFVNeutralino.Year import year

dataset = 'ntuplev15'
sample_files(process, 'mfv_neu_tau01000um_M0800', dataset, 1)
#sample_files(process, 'qcdht0700', dataset, 1)
process.TFileService.fileName = 'jethistos.root'
process.maxEvents.input = -1
file_event_from_argv(process)
geometry_etc(process, which_global_tag(True, year, H=False))

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.JetEnergyHistos_cfi')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)

process.mfvAnalysisCutsFullSel = process.mfvAnalysisCuts.clone(min_ht = 0)

process.p = cms.Path(common * process.mfvAnalysisCutsFullSel * process.mfvJetEnergyHistos)

def force_bs(process, bs):
    for ana in process.analyzers:
        if hasattr(ana, 'force_bs'):
            ana.force_bs = bs

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    from JMTucker.Tools import Samples 
    if year == 2015:
        samples = Samples.data_samples_2015 + \
            Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015 + \
            Samples.mfv_signal_samples_2015
    elif year == 2016:
        samples = Samples.data_samples + \
            Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
            Samples.mfv_signal_samples + Samples.mfv_ddbar_samples + Samples.mfv_hip_samples + Samples.qcd_hip_samples

    from JMTucker.Tools.MetaSubmitter import set_splitting
    dataset = 'ntuplev15'
    set_splitting(samples, dataset, 'histos', data_json='ana_2015p6.json')

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('JetEnergyHistosV15',
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(Samples.mfv_signal_samples + Samples.mfv_ddbar_samples)
