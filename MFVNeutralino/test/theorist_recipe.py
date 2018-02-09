from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev16_wgenv2'
sample_files(process, 'mfv_neu_tau01000um_M0800', dataset, 10)
process.TFileService.fileName = 'theorist_recipe.root'
file_event_from_argv(process)
#want_summary(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.mfvGenParticles.last_flag_check = False # JMTBAD need this until wgenv2

mfvTheoristRecipe = cms.EDAnalyzer('MFVTheoristRecipe',
                                   gen_jets_src = cms.InputTag('ak4GenJetsNoNu'),
                                   gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
                                   mci_src = cms.InputTag('mfvGenParticles'),
                                   mevent_src = cms.InputTag('mfvEvent'),
                                   vertex_src = cms.InputTag('mfvSelectedVertices'),
                                   max_dist = cms.double(0.0084),
                                   verbose = cms.untracked.bool(False),
                                   )

process.common = cms.Sequence(process.mfvSelectedVertices * process.mfvGenParticles)

if False:
    #set_events_to_process(process, [(1,5,65)])
    report_every(process, 1)
    process.load('JMTucker.Tools.ParticleListDrawer_cff')
    process.ParticleListDrawer.maxEventsToPrint = 10000
    process.common = process.ParticleListDrawer * process.common

#reconstructed cutflow
process.mfvTheoristRecipeNoCuts = mfvTheoristRecipe.clone()
process.pNoCuts = cms.Path(process.common * process.mfvTheoristRecipeNoCuts)

process.mfvAnalysisCutsOfflineJets = process.mfvAnalysisCuts.clone(apply_trigger = False, min_ht = 0, apply_vertex_cuts = False)
process.mfvTheoristRecipeOfflineJets = mfvTheoristRecipe.clone()
process.pOfflineJets = cms.Path(process.common * process.mfvAnalysisCutsOfflineJets * process.mfvTheoristRecipeOfflineJets)

process.mfvAnalysisCutsTrigSel = process.mfvAnalysisCuts.clone(min_ht = 0, apply_vertex_cuts = False)
process.mfvTheoristRecipeTrigSel = mfvTheoristRecipe.clone()
process.pTrigSel = cms.Path(process.common * process.mfvAnalysisCutsTrigSel * process.mfvTheoristRecipeTrigSel)

process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.mfvTheoristRecipePreSel = mfvTheoristRecipe.clone()
process.pPreSel = cms.Path(process.common * process.mfvAnalysisCutsPreSel * process.mfvTheoristRecipePreSel)

process.mfvAnalysisCutsTwoVtxNoCuts = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVertices')
process.mfvTheoristRecipeTwoVtxNoCuts = mfvTheoristRecipe.clone()
process.pTwoVtxNoCuts = cms.Path(process.common * process.mfvSelectedVertices * process.mfvAnalysisCutsTwoVtxNoCuts * process.mfvTheoristRecipeTwoVtxNoCuts)

process.mfvSelectedVerticesBsbs2ddist = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', min_bsbs2ddist = 0.01)
process.mfvAnalysisCutsTwoVtxBsbs2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesBsbs2ddist')
process.mfvTheoristRecipeTwoVtxBsbs2ddist = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesBsbs2ddist')
process.pTwoVtxBsbs2ddist = cms.Path(process.common * process.mfvSelectedVerticesBsbs2ddist * process.mfvAnalysisCutsTwoVtxBsbs2ddist * process.mfvTheoristRecipeTwoVtxBsbs2ddist)

process.mfvSelectedVerticesGeo2ddist = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', min_bsbs2ddist = 0.01, max_geo2ddist = 2.0)
process.mfvAnalysisCutsTwoVtxGeo2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.mfvTheoristRecipeTwoVtxGeo2ddist = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.pTwoVtxGeo2ddist = cms.Path(process.common * process.mfvSelectedVerticesGeo2ddist * process.mfvAnalysisCutsTwoVtxGeo2ddist * process.mfvTheoristRecipeTwoVtxGeo2ddist)

process.mfvAnalysisCutsDvv400um = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist', min_svdist2d = 0.04)
process.mfvTheoristRecipeTwoVtxDvv400um = mfvTheoristRecipe.clone()
process.pTwoVtxDvv400um = cms.Path(process.common * process.mfvAnalysisCutsDvv400um * process.mfvTheoristRecipeTwoVtxDvv400um)

process.mfvSelectedVerticesNtracks = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', min_bsbs2ddist = 0.01, max_geo2ddist = 2.0, min_ntracks = 5)
process.mfvAnalysisCutsTwoVtxNtracks = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracks', min_svdist2d = 0.04)
process.mfvTheoristRecipeTwoVtxNtracks = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.pTwoVtxNtracks = cms.Path(process.common * process.mfvSelectedVerticesNtracks * process.mfvAnalysisCutsTwoVtxNtracks * process.mfvTheoristRecipeTwoVtxNtracks)

process.mfvAnalysisCutsTwoVtxBs2derr = process.mfvAnalysisCuts.clone(min_svdist2d = 0.04)
process.mfvTheoristRecipeTwoVtxBs2derr = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesTight')
process.pTwoVtxBs2derr = cms.Path(process.common * process.mfvSelectedVerticesTight * process.mfvAnalysisCutsTwoVtxBs2derr * process.mfvTheoristRecipeTwoVtxBs2derr)

process.mfvAnalysisCutsDvv400um = process.mfvAnalysisCuts.clone(min_svdist2d = 0.04)
process.mfvTheoristRecipeTwoVtxDvv400um = mfvTheoristRecipe.clone()
process.pTwoVtxDvv400um = cms.Path(process.common * process.mfvAnalysisCutsDvv400um * process.mfvTheoristRecipeTwoVtxDvv400um)

process.mfvTheoristRecipeBsbs2ddist = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesBsbs2ddist')
process.pBsbs2ddist = cms.Path(process.common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesBsbs2ddist * process.mfvTheoristRecipeBsbs2ddist)

process.mfvTheoristRecipeGeo2ddist = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.pGeo2ddist = cms.Path(process.common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesGeo2ddist * process.mfvTheoristRecipeGeo2ddist)

process.mfvTheoristRecipeNtracks = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.pNtracks = cms.Path(process.common * process.mfvAnalysisCutsPreSel * process.mfvSelectedVerticesNtracks * process.mfvTheoristRecipeNtracks)

process.mfvTheoristRecipeBs2derr = mfvTheoristRecipe.clone(vertex_src = 'mfvSelectedVerticesTight')
process.pBs2derr = cms.Path(process.common * process.mfvAnalysisCutsPreSel * process.mfvTheoristRecipeBs2derr)

#generated cutflow
process.mfvGenNoCuts = mfvTheoristRecipe.clone()
process.pGenNoCuts = cms.Path(process.common * process.mfvGenParticleFilter * process.mfvGenNoCuts)

process.mfvGenParticleFilterFourJets = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20)
process.mfvGenFourJets = mfvTheoristRecipe.clone()
process.pGenFourJets = cms.Path(process.common * process.mfvGenParticleFilterFourJets * process.mfvGenFourJets)

process.mfvGenParticleFilterHT40 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000)
process.mfvGenHT40 = mfvTheoristRecipe.clone()
process.pGenHT40 = cms.Path(process.common * process.mfvGenParticleFilterHT40 * process.mfvGenHT40)

process.mfvGenParticleFilterBsbs2ddist = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01)
process.mfvGenBsbs2ddist = mfvTheoristRecipe.clone()
process.pGenBsbs2ddist = cms.Path(process.common * process.mfvGenParticleFilterBsbs2ddist * process.mfvGenBsbs2ddist)

process.mfvGenParticleFilterGeo2ddist = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0)
process.mfvGenGeo2ddist = mfvTheoristRecipe.clone()
process.pGenGeo2ddist = cms.Path(process.common * process.mfvGenParticleFilterGeo2ddist * process.mfvGenGeo2ddist)

process.mfvGenParticleFilterSumpt350 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04)
process.mfvGenSumpt350 = mfvTheoristRecipe.clone()
process.pGenSumpt350 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350 * process.mfvGenSumpt350)

process.mfvGenParticleFilterDvv400um = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04)
process.mfvGenDvv400um = mfvTheoristRecipe.clone()
process.pGenDvv400um = cms.Path(process.common * process.mfvGenParticleFilterDvv400um * process.mfvGenDvv400um)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p00 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.00)
process.mfvGenSumpt350BquarkptFraction0p00 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p00 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p00 * process.mfvGenSumpt350BquarkptFraction0p00)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p05 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.05)
process.mfvGenSumpt350BquarkptFraction0p05 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p05 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p05 * process.mfvGenSumpt350BquarkptFraction0p05)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p10 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.10)
process.mfvGenSumpt350BquarkptFraction0p10 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p10 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p10 * process.mfvGenSumpt350BquarkptFraction0p10)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p15 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.15)
process.mfvGenSumpt350BquarkptFraction0p15 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p15 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p15 * process.mfvGenSumpt350BquarkptFraction0p15)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p20 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.20)
process.mfvGenSumpt350BquarkptFraction0p20 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p20 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p20 * process.mfvGenSumpt350BquarkptFraction0p20)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p25 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.25)
process.mfvGenSumpt350BquarkptFraction0p25 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p25 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p25 * process.mfvGenSumpt350BquarkptFraction0p25)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p30 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.30)
process.mfvGenSumpt350BquarkptFraction0p30 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p30 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p30 * process.mfvGenSumpt350BquarkptFraction0p30)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p35 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.35)
process.mfvGenSumpt350BquarkptFraction0p35 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p35 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p35 * process.mfvGenSumpt350BquarkptFraction0p35)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p40 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.40)
process.mfvGenSumpt350BquarkptFraction0p40 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p40 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p40 * process.mfvGenSumpt350BquarkptFraction0p40)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p45 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.45)
process.mfvGenSumpt350BquarkptFraction0p45 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p45 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p45 * process.mfvGenSumpt350BquarkptFraction0p45)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p50 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.50)
process.mfvGenSumpt350BquarkptFraction0p50 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p50 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p50 * process.mfvGenSumpt350BquarkptFraction0p50)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p55 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.55)
process.mfvGenSumpt350BquarkptFraction0p55 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p55 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p55 * process.mfvGenSumpt350BquarkptFraction0p55)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p60 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.60)
process.mfvGenSumpt350BquarkptFraction0p60 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p60 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p60 * process.mfvGenSumpt350BquarkptFraction0p60)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p65 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.65)
process.mfvGenSumpt350BquarkptFraction0p65 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p65 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p65 * process.mfvGenSumpt350BquarkptFraction0p65)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p70 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.70)
process.mfvGenSumpt350BquarkptFraction0p70 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p70 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p70 * process.mfvGenSumpt350BquarkptFraction0p70)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p75 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.75)
process.mfvGenSumpt350BquarkptFraction0p75 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p75 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p75 * process.mfvGenSumpt350BquarkptFraction0p75)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p80 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.80)
process.mfvGenSumpt350BquarkptFraction0p80 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p80 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p80 * process.mfvGenSumpt350BquarkptFraction0p80)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p85 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.85)
process.mfvGenSumpt350BquarkptFraction0p85 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p85 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p85 * process.mfvGenSumpt350BquarkptFraction0p85)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p90 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.90)
process.mfvGenSumpt350BquarkptFraction0p90 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p90 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p90 * process.mfvGenSumpt350BquarkptFraction0p90)

process.mfvGenParticleFilterSumpt350BquarkptFraction0p95 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 0.95)
process.mfvGenSumpt350BquarkptFraction0p95 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction0p95 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction0p95 * process.mfvGenSumpt350BquarkptFraction0p95)

process.mfvGenParticleFilterSumpt350BquarkptFraction1p00 = process.mfvGenParticleFilter.clone(min_njets = 4, min_jet_pt = 20, min_jet_ht40 = 1000, min_rho0 = 0.01, min_rho1 = 0.01, max_rho0 = 2.0, max_rho1 = 2.0, min_sumpt = 350, min_dvv = 0.04, bquarkpt_fraction = 1.00)
process.mfvGenSumpt350BquarkptFraction1p00 = mfvTheoristRecipe.clone()
process.pGenSumpt350BquarkptFraction1p00 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350BquarkptFraction1p00 * process.mfvGenSumpt350BquarkptFraction1p00)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    from JMTucker.Tools import Samples
    if year == 2015:
        samples = Samples.mfv_signal_samples_2015
    elif year == 2016:
        samples = Samples.mfv_signal_samples + Samples.mfv_ddbar_samples + Samples.mfv_bbbar_samples + Samples.mfv_neuuds_samples + Samples.mfv_neuudmu_samples

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('TheoristRecipeV1', ex = year, dataset = dataset)
    cs.submit_all(samples)
