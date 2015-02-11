import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_1_1_WwV.root']
process.TFileService.fileName = 'resolutions.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')

mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                which_mom = cms.int32(0),
                                max_dr = cms.double(-1),
                                max_dist = cms.double(0.005),
                                gen_src = cms.InputTag('genParticles'),
                                gen_jet_src = cms.InputTag('ak5GenJets'),
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


process.pGen = cms.Path(process.mfvSelectedVertices)

process.mfvResolutionsGen = mfvResolutions.clone(vertex_src = 'mfvSelectedVertices')
process.pGen *= process.mfvResolutionsGen

process.mfvGenParticleFilter.min_npartons = 4
process.mfvGenParticleFilter.min_parton_pt = 60
process.mfvGenParticleFilter.min_parton_sumht = 500
process.mfvGenParticleFilter.max_rho0 = 2.5
process.mfvGenParticleFilter.max_rho1 = 2.5
process.mfvGenParticleFilter.min_drmax = 1.2
process.mfvGenParticleFilter.max_drmax = 4

process.pGen *= process.mfvGenParticleFilter

process.mfvResolutionsGenSel = mfvResolutions.clone(vertex_src = 'mfvSelectedVertices')
process.pGen *= process.mfvResolutionsGenSel

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    Samples.mfv_neutralino_tau1000um_M0400.ana_dataset_override = '/mfv_neutralino_tau1000um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0400.ana_scheduler = 'remoteGlidein'

    cs = CRABSubmitter('MFVResolutionsV20',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all([Samples.mfv_neutralino_tau1000um_M0400])
