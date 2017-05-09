import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

sample_files(process, 'mfv_neu_tau01000um_M0800', 'ntuplev14', -1)
process.TFileService.fileName = 'resolutions.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                which_mom = cms.int32(0),
                                max_dr = cms.double(-1),
                                max_dist = cms.double(0.0084),
                                max_dist_2d = cms.double(1e9),
                                max_dist_2d_square = cms.double(1e9)
                                )

process.p = cms.Path(process.mfvSelectedVerticesSeq)

process.mfvResolutionsByDistCutTrks = mfvResolutions.clone()
process.p *= process.mfvResolutionsByDistCutTrks

process.mfvResolutionsByDistCutJets = mfvResolutions.clone(which_mom = 1)
process.p *= process.mfvResolutionsByDistCutJets

process.mfvResolutionsByDistCutTrksJets = mfvResolutions.clone(which_mom = 2)
process.p *= process.mfvResolutionsByDistCutTrksJets

process.p *= process.mfvAnalysisCuts

process.mfvResolutionsFullSelByDistCutTrks = mfvResolutions.clone()
process.p *= process.mfvResolutionsFullSelByDistCutTrks

process.mfvResolutionsFullSelByDistCutJets = mfvResolutions.clone(which_mom = 1)
process.p *= process.mfvResolutionsFullSelByDistCutJets

process.mfvResolutionsFullSelByDistCutTrksJets = mfvResolutions.clone(which_mom = 2)
process.p *= process.mfvResolutionsFullSelByDistCutTrksJets


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.registry.from_argv([Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800])

    for sample in samples:
        if sample.is_mc:
            sample.events_per = 250000
        else:
            sample.json = 'ana_10pc.json'
            sample.lumis_per = 200

    cs = CRABSubmitter('MFVResolutionsV6p1_76x_nstlays3',
                       dataset = 'ntuplev6p1_76x_nstlays3',
                       job_control_from_sample = True,
                       aaa = True, # stored at FNAL, easy to run on T2_USes
                       use_ana_dataset = True,
                       )

    cs.submit_all(samples)
