import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
geometry_etc(process, 'FT_P_V42_AN4::All')

process.source.fileNames = ['/store/data/Run2012D/MultiJet1Parked/AOD/part1_10Dec2012-v1/10000/002C29AE-3344-E211-85F6-001E673973D2.root']
process.TFileService.fileName = 'beamspot_tree.root'

process.bs = cms.EDAnalyzer('BeamSpotTreer',
                            beamspot_src = cms.InputTag('offlineBeamSpot'),
                            primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                            )
process.p = cms.Path(process.bs)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv(Samples.data_samples)

    for s in Samples.data_samples:
        s.json = '207477.json'
        s.lumis_per = 1
        s.total_lumis = -1

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('BeamSpotTree',
                       job_control_from_sample = True,
                       )
    cs.submit_all([Samples.MultiJetPk2012D1])
