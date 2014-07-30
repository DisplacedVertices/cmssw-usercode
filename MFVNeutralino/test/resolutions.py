import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

#SampleFiles.setup(process, 'MFVNtupleV18', 'mfv_neutralino_tau1000um_M0400', 1000)
process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvmergentuple_v18/2f015b87b0f183c443d811e67eceec2e/merge_1_1_S9a.root','/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvmergentuple_v18/2f015b87b0f183c443d811e67eceec2e/merge_2_1_Qi0.root']
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



if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('MFVResolutionsV18',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all([Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400])
