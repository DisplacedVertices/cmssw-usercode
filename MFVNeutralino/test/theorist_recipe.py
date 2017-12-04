from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev16_wgenv2'
sample_files(process, 'mfv_neu_tau01000um_M0800', 'ntuplev16_wgenv2', 1)
process.TFileService.fileName = 'theorist_recipe.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.mfvGenParticles.last_flag_check = False # JMTBAD need this until wgenv2

mfvTheoristRecipe = cms.EDAnalyzer('MFVTheoristRecipe',
                                   gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
                                   mci_src = cms.InputTag('mfvGenParticles'),
                                   mevent_src = cms.InputTag('mfvEvent'),
                                   vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                   which_mom = cms.int32(0),
                                   max_dr = cms.double(-1),
                                   max_dist = cms.double(0.0084),
                                   min_dbv = cms.double(0.2),
                                   max_dbv = cms.double(0.3),
                                   )

common = process.mfvSelectedVerticesTight * process.mfvGenParticles

#reconstructed cutflow
process.mfvTheoristRecipeNoCuts = mfvTheoristRecipe.clone()
process.pNoCuts = cms.Path(common * process.mfvTheoristRecipeNoCuts)

process.mfvAnalysisCutsTrigSel = process.mfvAnalysisCuts.clone(min_njets = 0, min_ht = 0, apply_vertex_cuts = False)
process.mfvTheoristRecipeTrigSel = mfvTheoristRecipe.clone()
process.pTrigSel = cms.Path(common * process.mfvAnalysisCutsTrigSel * process.mfvTheoristRecipeTrigSel)

process.mfvAnalysisCutsOfflineJets = process.mfvAnalysisCuts.clone(min_ht = 0, apply_vertex_cuts = False)
process.mfvTheoristRecipeOfflineJets = mfvTheoristRecipe.clone()
process.pOfflineJets = cms.Path(common * process.mfvAnalysisCutsOfflineJets * process.mfvTheoristRecipeOfflineJets)

process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.mfvTheoristRecipePreSel = mfvTheoristRecipe.clone()
process.pPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvTheoristRecipePreSel)

process.mfvAnalysisCutsTwoVtxNoCuts = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVertices')
process.mfvTheoristRecipeTwoVtxNoCuts = mfvTheoristRecipe.clone()
process.pTwoVtxNoCuts = cms.Path(common * process.mfvSelectedVertices * process.mfvAnalysisCutsTwoVtxNoCuts * process.mfvTheoristRecipeTwoVtxNoCuts)

process.mfvSelectedVerticesGeo2ddist = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', max_geo2ddist = 2.0)
process.mfvAnalysisCutsTwoVtxGeo2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.mfvTheoristRecipeTwoVtxGeo2ddist = mfvTheoristRecipe.clone()
process.pTwoVtxGeo2ddist = cms.Path(common * process.mfvSelectedVerticesGeo2ddist * process.mfvAnalysisCutsTwoVtxGeo2ddist * process.mfvTheoristRecipeTwoVtxGeo2ddist)

process.mfvSelectedVerticesBsbs2ddist = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', max_geo2ddist = 2.0, min_bsbs2ddist = 0.01)
process.mfvAnalysisCutsTwoVtxBsbs2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesBsbs2ddist')
process.mfvTheoristRecipeTwoVtxBsbs2ddist = mfvTheoristRecipe.clone()
process.pTwoVtxBsbs2ddist = cms.Path(common * process.mfvSelectedVerticesBsbs2ddist * process.mfvAnalysisCutsTwoVtxBsbs2ddist * process.mfvTheoristRecipeTwoVtxBsbs2ddist)

process.mfvSelectedVerticesNtracks = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', max_geo2ddist = 2.0, min_bsbs2ddist = 0.01, min_ntracks = 5)
process.mfvAnalysisCutsTwoVtxNtracks = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.mfvTheoristRecipeTwoVtxNtracks = mfvTheoristRecipe.clone()
process.pTwoVtxNtracks = cms.Path(common * process.mfvSelectedVerticesNtracks * process.mfvAnalysisCutsTwoVtxNtracks * process.mfvTheoristRecipeTwoVtxNtracks)

process.mfvSelectedVerticesBs2derr = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', max_geo2ddist = 2.0, min_bsbs2ddist = 0.01, min_ntracks = 5, max_bs2derr = 0.0025)
process.mfvAnalysisCutsTwoVtxBs2derr = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesBs2derr')
process.mfvTheoristRecipeTwoVtxBs2derr = mfvTheoristRecipe.clone()
process.pTwoVtxBs2derr = cms.Path(common * process.mfvSelectedVerticesBs2derr * process.mfvAnalysisCutsTwoVtxBs2derr * process.mfvTheoristRecipeTwoVtxBs2derr)

process.mfvAnalysisCutsDvv400um = process.mfvAnalysisCuts.clone(min_svdist2d = 0.04)
process.mfvTheoristRecipeTwoVtxDvv400um = mfvTheoristRecipe.clone()
process.pTwoVtxDvv400um = cms.Path(common * process.mfvSelectedVerticesTight * process.mfvAnalysisCutsDvv400um * process.mfvTheoristRecipeTwoVtxDvv400um)

'''
process.mfvTheoristRecipeVertices = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVertices')
process.pVertices = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVertices * process.mfvTheoristRecipeVertices)

process.mfvTheoristRecipeGeo2ddist = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.pGeo2ddist = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesGeo2ddist * process.mfvTheoristRecipeGeo2ddist)

process.mfvTheoristRecipeBsbs2ddist = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesBsbs2ddist')
process.pBsbs2ddist = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesBsbs2ddist * process.mfvTheoristRecipeBsbs2ddist)

process.mfvTheoristRecipeNtracks = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.pNtracks = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesNtracks * process.mfvTheoristRecipeNtracks)

process.mfvTheoristRecipeBs2derr = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesBs2derr')
process.pBs2derr = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesBs2derr * process.mfvTheoristRecipeBs2derr)
'''

#generated cutflow
process.mfvGenNoCuts = mfvTheoristRecipe.clone()
process.pGenNoCuts = cms.Path(common * process.mfvGenParticleFilter * process.mfvGenNoCuts)

process.mfvGenParticleFilterFourJets = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 20)
process.mfvGenFourJets = mfvTheoristRecipe.clone()
process.pGenFourJets = cms.Path(common * process.mfvGenParticleFilterFourJets * process.mfvGenFourJets)

process.mfvGenParticleFilterSumHT = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 20, min_parton_ht = 1000)
process.mfvGenSumHT = mfvTheoristRecipe.clone()
process.pGenSumHT = cms.Path(common * process.mfvGenParticleFilterSumHT * process.mfvGenSumHT)

process.mfvGenParticleFilterGeo2ddist = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 20, min_parton_ht = 1000, max_rho0 = 2.0, max_rho1 = 2.0)
process.mfvGenGeo2ddist = mfvTheoristRecipe.clone()
process.pGenGeo2ddist = cms.Path(common * process.mfvGenParticleFilterGeo2ddist * process.mfvGenGeo2ddist)

process.mfvGenParticleFilterBsbs2ddist = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 20, min_parton_ht = 1000, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01)
process.mfvGenBsbs2ddist = mfvTheoristRecipe.clone()
process.pGenBsbs2ddist = cms.Path(common * process.mfvGenParticleFilterBsbs2ddist * process.mfvGenBsbs2ddist)

process.mfvGenParticleFilterSumpt200 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 20, min_parton_ht = 1000, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_sumpt = 200)
process.mfvGenSumpt200 = mfvTheoristRecipe.clone()
process.pGenSumpt200 = cms.Path(common * process.mfvGenParticleFilterSumpt200 * process.mfvGenSumpt200)

process.mfvGenParticleFilterDvv400um = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 20, min_parton_ht = 1000, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_sumpt = 200, min_dvv = 0.04)
process.mfvGenDvv400um = mfvTheoristRecipe.clone()
process.pGenDvv400um = cms.Path(common * process.mfvGenParticleFilterDvv400um * process.mfvGenDvv400um)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    from JMTucker.Tools import Samples
    if year == 2015:
        samples = Samples.mfv_signal_samples_2015
    elif year == 2016:
        samples = Samples.mfv_signal_samples + Samples.mfv_ddbar_samples + Samples.mfv_hip_samples

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('TheoristRecipeV1', ex = year, dataset = dataset)
    cs.submit_all(samples)
