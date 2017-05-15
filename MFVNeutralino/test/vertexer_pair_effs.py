import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

sample_files(process, 'qcdht2000', 'ntuplev14p2', 1)
process.TFileService.fileName = 'vertexer_pair_effs.root'
process.maxEvents.input = -1

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.VertexerPairEffs_cfi')

process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)

process.p = cms.Path(process.mfvAnalysisCutsPreSel * process.mfvVertexerPairEffs)

ntks = [5,3,4,7]

for ntk in ntks:
    if ntk == 5:
        EX1 = EX2 = ''
    elif ntk == 7:
        EX1 = 'Ntk3or4'
    else:
        EX1 = 'Ntk%i' % ntk
    if EX1:
        EX2 = "vertex_src = 'mfvSelectedVerticesTight%s', " % EX1

    exec '''
process.EX1mfvAnalysisCutsOnlyOneVtx = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, max_nvertex = 1)
process.EX1mfvAnalysisCutsFullSel    = process.mfvAnalysisCuts.clone(EX2)

process.EX1mfvVertexerPairEffsOnlyOneVtx = process.mfvVertexerPairEffs.clone()
process.EX1mfvVertexerPairEffsFullSel    = process.mfvVertexerPairEffs.clone()

process.EX1pOnlyOneVtx = cms.Path(process.mfvSelectedVerticesSeq * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvVertexerPairEffsOnlyOneVtx)
process.EX1pFullSel    = cms.Path(process.mfvSelectedVerticesSeq * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvVertexerPairEffsFullSel)
'''.replace('EX1', EX1).replace('EX2', EX2)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    from JMTucker.Tools import Samples 
    if year == 2015:
        samples = Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    from JMTucker.Tools.MetaSubmitter import set_splitting
    dataset = 'ntuplev14p2'
    set_splitting(samples, dataset, 'histos', data_json='ana_2015p6_10pc.json')

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('VertexerPairEffsV14p2',
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)
