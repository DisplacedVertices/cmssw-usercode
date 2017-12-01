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

'''
process.mfvAnalysisCutsTrigSel = process.mfvAnalysisCuts.clone(apply_cleaning_filters = False, min_njets = 0, min_ht = 0, apply_vertex_cuts = False)
process.mfvTheoristRecipeTrigSel = mfvTheoristRecipe.clone()
process.pTrigSel = cms.Path(common * process.mfvAnalysisCutsTrigSel * process.mfvTheoristRecipeTrigSel)

process.mfvAnalysisCutsCleaningFilters = process.mfvAnalysisCuts.clone(apply_cleaning_filters = True, min_njets = 0, min_ht = 0, apply_vertex_cuts = False)
process.mfvTheoristRecipeCleaningFilters = mfvTheoristRecipe.clone()
process.pCleaningFilters = cms.Path(common * process.mfvAnalysisCutsCleaningFilters * process.mfvTheoristRecipeCleaningFilters)

process.mfvAnalysisCutsOfflineJets = process.mfvAnalysisCuts.clone(min_ht = 0, apply_vertex_cuts = False)
process.mfvTheoristRecipeOfflineJets = mfvTheoristRecipe.clone()
process.pOfflineJets = cms.Path(common * process.mfvAnalysisCutsOfflineJets * process.mfvTheoristRecipeOfflineJets)

process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.mfvTheoristRecipePreSel = mfvTheoristRecipe.clone()
process.pPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvTheoristRecipePreSel)

process.mfvAnalysisCutsTwoVtxNoCuts = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVertices')
process.mfvTheoristRecipeTwoVtxNoCuts = mfvTheoristRecipe.clone()
process.pTwoVtxNoCuts = cms.Path(common * process.mfvSelectedVertices * process.mfvAnalysisCutsTwoVtxNoCuts * process.mfvTheoristRecipeTwoVtxNoCuts)

process.mfvSelectedVerticesGeo2ddist = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0)
process.mfvAnalysisCutsTwoVtxGeo2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.mfvTheoristRecipeTwoVtxGeo2ddist = mfvTheoristRecipe.clone()
process.pTwoVtxGeo2ddist = cms.Path(common * process.mfvSelectedVerticesGeo2ddist * process.mfvAnalysisCutsTwoVtxGeo2ddist * process.mfvTheoristRecipeTwoVtxGeo2ddist)

process.mfvSelectedVerticesNtracks = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_ntracks = 5)
process.mfvAnalysisCutsTwoVtxNtracks = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.mfvTheoristRecipeTwoVtxNtracks = mfvTheoristRecipe.clone()
process.pTwoVtxNtracks = cms.Path(common * process.mfvSelectedVerticesNtracks * process.mfvAnalysisCutsTwoVtxNtracks * process.mfvTheoristRecipeTwoVtxNtracks)

process.mfvSelectedVerticesBs2derr = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_ntracks = 5, max_bs2derr = 0.0025)
process.mfvAnalysisCutsTwoVtxBs2derr = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesBs2derr')
process.mfvTheoristRecipeTwoVtxBs2derr = mfvTheoristRecipe.clone()
process.pTwoVtxBs2derr = cms.Path(common * process.mfvSelectedVerticesBs2derr * process.mfvAnalysisCutsTwoVtxBs2derr * process.mfvTheoristRecipeTwoVtxBs2derr)

process.mfvSelectedVerticesMindrmax = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_ntracks = 5, max_bs2derr = 0.0025, min_drmax = 1.2)
process.mfvAnalysisCutsTwoVtxMindrmax = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesMindrmax')
process.mfvTheoristRecipeTwoVtxMindrmax = mfvTheoristRecipe.clone()
process.pTwoVtxMindrmax = cms.Path(common * process.mfvSelectedVerticesMindrmax * process.mfvAnalysisCutsTwoVtxMindrmax * process.mfvTheoristRecipeTwoVtxMindrmax)

process.mfvSelectedVerticesMaxdrmax = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_ntracks = 5, max_bs2derr = 0.0025, min_drmax = 1.2, max_drmax = 4)
process.mfvAnalysisCutsTwoVtxMaxdrmax = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesMaxdrmax')
process.mfvTheoristRecipeTwoVtxMaxdrmax = mfvTheoristRecipe.clone()
process.pTwoVtxMaxdrmax = cms.Path(common * process.mfvSelectedVerticesMaxdrmax * process.mfvAnalysisCutsTwoVtxMaxdrmax * process.mfvTheoristRecipeTwoVtxMaxdrmax)

process.mfvSelectedVerticesDrmin = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_ntracks = 5, max_bs2derr = 0.0025, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4)
process.mfvAnalysisCutsTwoVtxDrmin = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesDrmin')
process.mfvTheoristRecipeTwoVtxDrmin = mfvTheoristRecipe.clone()
process.pTwoVtxDrmin = cms.Path(common * process.mfvSelectedVerticesDrmin * process.mfvAnalysisCutsTwoVtxDrmin * process.mfvTheoristRecipeTwoVtxDrmin)

process.mfvSelectedVerticesNjetsntks = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_ntracks = 5, max_bs2derr = 0.0025, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_njetsntks = 1)
process.mfvAnalysisCutsTwoVtxNjetsntks = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNjetsntks')
process.mfvTheoristRecipeTwoVtxNjetsntks = mfvTheoristRecipe.clone()
process.pTwoVtxNjetsntks = cms.Path(common * process.mfvSelectedVerticesNjetsntks * process.mfvAnalysisCutsTwoVtxNjetsntks * process.mfvTheoristRecipeTwoVtxNjetsntks)

process.mfvSelectedVerticesNtracksptgt3 = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_ntracks = 5, max_bs2derr = 0.0025, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_njetsntks = 1, min_ntracksptgt3 = 3)
process.mfvAnalysisCutsTwoVtxNtracksptgt3 = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracksptgt3')
process.mfvTheoristRecipeTwoVtxNtracksptgt3 = mfvTheoristRecipe.clone()
process.pTwoVtxNtracksptgt3 = cms.Path(common * process.mfvSelectedVerticesNtracksptgt3 * process.mfvAnalysisCutsTwoVtxNtracksptgt3 * process.mfvTheoristRecipeTwoVtxNtracksptgt3)

process.mfvAnalysisCutsDvv600um = process.mfvAnalysisCuts.clone(min_svdist2d = 0.06)
process.mfvTheoristRecipeTwoVtxDvv600um = mfvTheoristRecipe.clone()
process.pTwoVtxDvv600um = cms.Path(common * process.mfvSelectedVerticesTight * process.mfvAnalysisCutsDvv600um * process.mfvTheoristRecipeTwoVtxDvv600um)

process.mfvTheoristRecipeVertices = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVertices')
process.pVertices = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVertices * process.mfvTheoristRecipeVertices)

process.mfvTheoristRecipeGeo2ddist = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.pGeo2ddist = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesGeo2ddist * process.mfvTheoristRecipeGeo2ddist)

process.mfvTheoristRecipeNtracks = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.pNtracks = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesNtracks * process.mfvTheoristRecipeNtracks)

process.mfvTheoristRecipeBs2derr = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesBs2derr')
process.pBs2derr = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesBs2derr * process.mfvTheoristRecipeBs2derr)

process.mfvTheoristRecipeMindrmax = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesMindrmax')
process.pMindrmax = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesMindrmax * process.mfvTheoristRecipeMindrmax)

process.mfvTheoristRecipeMaxdrmax = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesMaxdrmax')
process.pMaxdrmax = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesMaxdrmax * process.mfvTheoristRecipeMaxdrmax)

process.mfvTheoristRecipeDrmin = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesDrmin')
process.pDrmin = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesDrmin * process.mfvTheoristRecipeDrmin)

process.mfvTheoristRecipeNjetsntks = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesNjetsntks')
process.pNjetsntks = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesNjetsntks * process.mfvTheoristRecipeNjetsntks)

process.mfvTheoristRecipeNtracksptgt3 = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesNtracksptgt3')
process.pNtracksptgt3 = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesNtracksptgt3 * process.mfvTheoristRecipeNtracksptgt3)

process.mfvSelectedVerticesNoNtracksBs2derrNtracksptgt3 = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_njetsntks = 1)
process.mfvTheoristRecipeNoNtracksBs2derrNtracksptgt3 = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesNoNtracksBs2derrNtracksptgt3')
process.pNoNtracksBs2derrNtracksptgt3 = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesNoNtracksBs2derrNtracksptgt3 * process.mfvTheoristRecipeNoNtracksBs2derrNtracksptgt3)
'''

#generated cutflow
process.mfvGenNoCuts = mfvTheoristRecipe.clone()
process.pGenNoCuts = cms.Path(common * process.mfvGenParticleFilter * process.mfvGenNoCuts)

process.mfvGenParticleFilterFourJets = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60)
process.mfvGenFourJets = mfvTheoristRecipe.clone()
process.pGenFourJets = cms.Path(common * process.mfvGenParticleFilterFourJets * process.mfvGenFourJets)

process.mfvGenParticleFilterSumHT = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_ht = 500)
process.mfvGenSumHT = mfvTheoristRecipe.clone()
process.pGenSumHT = cms.Path(common * process.mfvGenParticleFilterSumHT * process.mfvGenSumHT)

process.mfvGenParticleFilterGeo2ddist = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_ht = 500, max_rho0 = 2.5, max_rho1 = 2.5)
process.mfvGenGeo2ddist = mfvTheoristRecipe.clone()
process.pGenGeo2ddist = cms.Path(common * process.mfvGenParticleFilterGeo2ddist * process.mfvGenGeo2ddist)

process.mfvGenParticleFilterNtracks2 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_ht = 500, max_rho0 = 2.5, max_rho1 = 2.5, min_ntracks = 2)
process.mfvGenNtracks2 = mfvTheoristRecipe.clone()
process.pGenNtracks2 = cms.Path(common * process.mfvGenParticleFilterNtracks2 * process.mfvGenNtracks2)

process.mfvGenParticleFilterMindrmax = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_ht = 500, max_rho0 = 2.5, max_rho1 = 2.5, min_ntracks = 2, min_drmax = 1.2)
process.mfvGenMindrmax = mfvTheoristRecipe.clone()
process.pGenMindrmax = cms.Path(common * process.mfvGenParticleFilterMindrmax * process.mfvGenMindrmax)

process.mfvGenParticleFilterMaxdrmax = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_ht = 500, max_rho0 = 2.5, max_rho1 = 2.5, min_ntracks = 2, min_drmax = 1.2, max_drmax = 4)
process.mfvGenMaxdrmax = mfvTheoristRecipe.clone()
process.pGenMaxdrmax = cms.Path(common * process.mfvGenParticleFilterMaxdrmax * process.mfvGenMaxdrmax)

process.mfvGenParticleFilterNquarks1 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_ht = 500, max_rho0 = 2.5, max_rho1 = 2.5, min_ntracks = 2, min_drmax = 1.2, max_drmax = 4, min_nquarks = 1)
process.mfvGenNquarks1 = mfvTheoristRecipe.clone()
process.pGenNquarks1 = cms.Path(common * process.mfvGenParticleFilterNquarks1 * process.mfvGenNquarks1)

process.mfvGenParticleFilterSumpt200 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_ht = 500, max_rho0 = 2.5, max_rho1 = 2.5, min_ntracks = 2, min_drmax = 1.2, max_drmax = 4, min_nquarks = 1, min_sumpt = 200)
process.mfvGenSumpt200 = mfvTheoristRecipe.clone()
process.pGenSumpt200 = cms.Path(common * process.mfvGenParticleFilterSumpt200 * process.mfvGenSumpt200)

process.mfvGenParticleFilterDvv600um = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_ht = 500, max_rho0 = 2.5, max_rho1 = 2.5, min_ntracks = 2, min_drmax = 1.2, max_drmax = 4, min_nquarks = 1, min_sumpt = 200, min_dvv = 0.06)
process.mfvGenDvv600um = mfvTheoristRecipe.clone()
process.pGenDvv600um = cms.Path(common * process.mfvGenParticleFilterDvv600um * process.mfvGenDvv600um)


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
