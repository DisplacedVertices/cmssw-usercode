import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/tucker/TTJets_HadronicMGDecays_8TeV-madgraph/mfvntuple_v18/c761ddfa7f093d8f86a338439e06a1d4/ntuple_1_1_nWG.root']
process.TFileService.fileName = 'beamspot_tree.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCutsOnlyOneVtx = process.mfvAnalysisCuts.clone(min_nvertex = 1, max_nvertex = 1)

process.BeamSpotTree = cms.EDAnalyzer('BeamSpotTreeProducer',
                                      event_src = cms.InputTag('mfvEvent'),
                                      )
process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCutsOnlyOneVtx * process.BeamSpotTree)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv(Samples.data_samples)

    for s in Samples.data_samples:
        s.json = '../../MFVNeutralino/test/ana_all.json'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('BeamSpotTree',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       run_half_mc = True,
                       )
    cs.submit_all(samples)
