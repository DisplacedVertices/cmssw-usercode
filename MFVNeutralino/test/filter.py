import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV13', 'mfv_neutralino_tau1000um_M0400', 5000)
del process.TFileService

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.mfvSelectedVerticesBase = process.mfvSelectedVerticesTight.clone()
process.mfvSelectedVerticesBase.min_ntracks = 5
process.mfvSelectedVerticesBase.min_maxtrackpt = 0
process.mfvSelectedVerticesBase.min_njetsntks = 1

process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCuts.vertex_src = 'mfvSelectedVerticesBase'
process.mfvAnalysisCuts.min_sumht = 500
process.mfvAnalysisCuts.min_ntracks01 = 0
process.mfvAnalysisCuts.min_maxtrackpt01 = 0

process.p = cms.Path(process.mfvSelectedVerticesBase * process.mfvAnalysisCuts)

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('ntuple_filtered.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep MFVEvent_mfvEvent__*',
                                   'keep MFVVertexAuxs_mfvSelectedVerticesBase__*',
                                   )
                               )
process.outp = cms.EndPath(process.out)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.ttbar_samples + Samples.qcd_samples #+ Samples.leptonic_background_samples
    samples += [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('MFVFilteredNtupleV13',
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       get_edm_output = True,
                       data_retrieval = 'fnal_eos',
                       manual_datasets = SampleFiles['MFVNtupleV13'],
                       )
    cs.submit_all(samples)
