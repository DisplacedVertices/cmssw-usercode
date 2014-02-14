import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV15', 'mfv_neutralino_tau1000um_M0400', 1000)
process.TFileService.fileName = 'resolutions.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')

mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                which_mom = cms.int32(0),
                                max_dr = cms.double(-1),
                                max_dist = cms.double(1e99),
                                )

process.p = cms.Path(process.mfvSelectedVerticesSeq)

process.mfvResolutionsByDistAllTrks = mfvResolutions.clone()
process.p *= process.mfvResolutionsByDistAllTrks

process.mfvResolutionsByDistCutTrks = mfvResolutions.clone(max_dist = 0.008)
process.p *= process.mfvResolutionsByDistCutTrks

process.mfvResolutionsByDistAllJets = mfvResolutions.clone(which_mom = 1)
process.p *= process.mfvResolutionsByDistAllJets

process.mfvResolutionsByDistCutJets = mfvResolutions.clone(which_mom = 1, max_dist = 0.008)
process.p *= process.mfvResolutionsByDistCutJets

process.mfvResolutionsByDistAllTrksJets = mfvResolutions.clone(which_mom = 2)
process.p *= process.mfvResolutionsByDistAllTrksJets

process.mfvResolutionsByDistCutTrksJets = mfvResolutions.clone(which_mom = 2, max_dist = 0.008)
process.p *= process.mfvResolutionsByDistCutTrksJets

process.mfvResolutionsByDRAllTrks = mfvResolutions.clone(max_dr = 1e99, max_dist = -1)
process.p *= process.mfvResolutionsByDRAllTrks

process.mfvResolutionsByDRCutTrks = mfvResolutions.clone(max_dr = 0.3, max_dist = -1)
process.p *= process.mfvResolutionsByDRCutTrks

process.mfvResolutionsByDRAllJets = mfvResolutions.clone(max_dr = 1e99, max_dist = -1, which_mom = 1)
process.p *= process.mfvResolutionsByDRAllJets

process.mfvResolutionsByDRCutJets = mfvResolutions.clone(max_dr = 0.3, max_dist = -1, which_mom = 1)
process.p *= process.mfvResolutionsByDRCutJets

process.mfvResolutionsByDRAllTrksJets = mfvResolutions.clone(max_dr = 1e99, max_dist = -1, which_mom = 2)
process.p *= process.mfvResolutionsByDRAllTrksJets

process.mfvResolutionsByDRCutTrksJets = mfvResolutions.clone(max_dr = 0.3, max_dist = -1, which_mom = 2)
process.p *= process.mfvResolutionsByDRCutTrksJets


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('MFVResolutionsV15',
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       manual_datasets = SampleFiles['MFVNtupleV15'],
                       )

    cs.submit_all(Samples.mfv_signal_samples)
