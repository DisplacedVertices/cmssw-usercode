import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/dquach/mfv_neu_tau01000um_M0800/ntuplev6p1_76x_signal/160329_200918/0000/ntuple_1.root']
process.TFileService.fileName = 'resolutions.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                which_mom = cms.int32(0),
                                max_dr = cms.double(-1),
                                max_dist = cms.double(0.005),
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



#if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
#    import JMTucker.Tools.Samples as Samples
#    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
#    from JMTucker.Tools.SampleFiles import SampleFiles
#
#    cs = CRABSubmitter('MFVResolutionsV18',
#                       job_control_from_sample = True,
#                       use_ana_dataset = True,
#                       )
#    cs.submit_all([Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400])

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
