import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

sample_files(process, 'qcdht2000', 'ntuplev15', 1)
process.TFileService.fileName = 'vertexer_pair_effs.root'
process.maxEvents.input = -1

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.VertexerPairEffs_cfi')

process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)

process.p = cms.Path(process.mfvWeight * process.mfvAnalysisCutsPreSel * process.mfvVertexerPairEffs)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    from JMTucker.Tools import Samples 
    if year == 2015:
        samples = Samples.data_samples_2015 + \
            Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + \
            Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    from JMTucker.Tools.MetaSubmitter import set_splitting
    dataset = 'ntuplev15'
    set_splitting(samples, dataset, 'histos', data_json='ana_2015p6_10pc.json')

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('VertexerPairEffsV15',
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)
