import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev20m_ntkseeds'
sample_files(process, 'qcdht2000_2017', dataset, 1)
process.TFileService.fileName = 'vertexer_pair_effs.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.VertexerPairEffs_cfi')

process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.p = cms.Path(process.mfvWeight * process.mfvAnalysisCutsPreSel * process.mfvVertexerPairEffsSeq)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples 

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017
        #samples += Samples.data_samples_2017

    set_splitting(samples, dataset, 'histos', data_json='jsons/ana_2017.json')

    cs = CondorSubmitter('VertexerPairEffsV20m',
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)
