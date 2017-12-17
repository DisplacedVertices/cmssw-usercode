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
                                   vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                   max_dist = cms.double(0.0084),
                                   verbose = cms.untracked.bool(False),
                                   )

process.common = cms.Sequence(process.mfvSelectedVerticesTight * process.mfvGenParticles)

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

process.mfvSelectedVerticesNtracks = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', min_ntracks = 5)
process.mfvAnalysisCutsTwoVtxNtracks = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.mfvTheoristRecipeTwoVtxNtracks = mfvTheoristRecipe.clone()
process.pTwoVtxNtracks = cms.Path(process.common * process.mfvSelectedVerticesNtracks * process.mfvAnalysisCutsTwoVtxNtracks * process.mfvTheoristRecipeTwoVtxNtracks)

process.mfvSelectedVerticesGeo2ddist = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', min_ntracks = 5, max_geo2ddist = 2.0)
process.mfvAnalysisCutsTwoVtxGeo2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.mfvTheoristRecipeTwoVtxGeo2ddist = mfvTheoristRecipe.clone()
process.pTwoVtxGeo2ddist = cms.Path(process.common * process.mfvSelectedVerticesGeo2ddist * process.mfvAnalysisCutsTwoVtxGeo2ddist * process.mfvTheoristRecipeTwoVtxGeo2ddist)

process.mfvSelectedVerticesBsbs2ddist = process.mfvSelectedVertices.clone(mevent_src = 'mfvEvent', min_ntracks = 5, max_geo2ddist = 2.0, min_bsbs2ddist = 0.01)
process.mfvAnalysisCutsTwoVtxBsbs2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesBsbs2ddist')
process.mfvTheoristRecipeTwoVtxBsbs2ddist = mfvTheoristRecipe.clone()
process.pTwoVtxBsbs2ddist = cms.Path(process.common * process.mfvSelectedVerticesBsbs2ddist * process.mfvAnalysisCutsTwoVtxBsbs2ddist * process.mfvTheoristRecipeTwoVtxBsbs2ddist)

process.mfvAnalysisCutsDvv400um = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesBsbs2ddist', min_svdist2d = 0.04)
process.mfvTheoristRecipeTwoVtxDvv400um = mfvTheoristRecipe.clone()
process.pTwoVtxDvv400um = cms.Path(process.common * process.mfvSelectedVerticesTight * process.mfvAnalysisCutsDvv400um * process.mfvTheoristRecipeTwoVtxDvv400um)

process.mfvAnalysisCutsTwoVtxBs2derr = process.mfvAnalysisCuts.clone(min_svdist2d = 0.04)
process.mfvTheoristRecipeTwoVtxBs2derr = mfvTheoristRecipe.clone()
process.pTwoVtxBs2derr = cms.Path(process.common * process.mfvAnalysisCutsTwoVtxBs2derr * process.mfvTheoristRecipeTwoVtxBs2derr)

#generated cutflow
process.mfvGenNoCuts = mfvTheoristRecipe.clone()
process.pGenNoCuts = cms.Path(process.common * process.mfvGenParticleFilter * process.mfvGenNoCuts)

process.mfvGenParticleFilterFourJets = process.mfvGenParticleFilter.clone(min_npartons = 4)
process.mfvGenFourJets = mfvTheoristRecipe.clone()
process.pGenFourJets = cms.Path(process.common * process.mfvGenParticleFilterFourJets * process.mfvGenFourJets)

process.mfvGenParticleFilterHT40 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000)
process.mfvGenHT40 = mfvTheoristRecipe.clone()
process.pGenHT40 = cms.Path(process.common * process.mfvGenParticleFilterHT40 * process.mfvGenHT40)

process.mfvGenParticleFilterNtracks1 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1)
process.mfvGenNtracks1 = mfvTheoristRecipe.clone()
process.pGenNtracks1 = cms.Path(process.common * process.mfvGenParticleFilterNtracks1 * process.mfvGenNtracks1)

process.mfvGenParticleFilterGeo2ddist = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0)
process.mfvGenGeo2ddist = mfvTheoristRecipe.clone()
process.pGenGeo2ddist = cms.Path(process.common * process.mfvGenParticleFilterGeo2ddist * process.mfvGenGeo2ddist)

process.mfvGenParticleFilterBsbs2ddist = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01)
process.mfvGenBsbs2ddist = mfvTheoristRecipe.clone()
process.pGenBsbs2ddist = cms.Path(process.common * process.mfvGenParticleFilterBsbs2ddist * process.mfvGenBsbs2ddist)

process.mfvGenParticleFilterDvv400um = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04)
process.mfvGenDvv400um = mfvTheoristRecipe.clone()
process.pGenDvv400um = cms.Path(process.common * process.mfvGenParticleFilterDvv400um * process.mfvGenDvv400um)

process.mfvGenParticleFilterSumpt50 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 50)
process.mfvGenSumpt50 = mfvTheoristRecipe.clone()
process.pGenSumpt50 = cms.Path(process.common * process.mfvGenParticleFilterSumpt50 * process.mfvGenSumpt50)

process.mfvGenParticleFilterSumpt100 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 100)
process.mfvGenSumpt100 = mfvTheoristRecipe.clone()
process.pGenSumpt100 = cms.Path(process.common * process.mfvGenParticleFilterSumpt100 * process.mfvGenSumpt100)

process.mfvGenParticleFilterSumpt150 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 150)
process.mfvGenSumpt150 = mfvTheoristRecipe.clone()
process.pGenSumpt150 = cms.Path(process.common * process.mfvGenParticleFilterSumpt150 * process.mfvGenSumpt150)

process.mfvGenParticleFilterSumpt200 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 200)
process.mfvGenSumpt200 = mfvTheoristRecipe.clone()
process.pGenSumpt200 = cms.Path(process.common * process.mfvGenParticleFilterSumpt200 * process.mfvGenSumpt200)

process.mfvGenParticleFilterSumpt250 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 250)
process.mfvGenSumpt250 = mfvTheoristRecipe.clone()
process.pGenSumpt250 = cms.Path(process.common * process.mfvGenParticleFilterSumpt250 * process.mfvGenSumpt250)

process.mfvGenParticleFilterSumpt300 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 300)
process.mfvGenSumpt300 = mfvTheoristRecipe.clone()
process.pGenSumpt300 = cms.Path(process.common * process.mfvGenParticleFilterSumpt300 * process.mfvGenSumpt300)

process.mfvGenParticleFilterSumpt350 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 350)
process.mfvGenSumpt350 = mfvTheoristRecipe.clone()
process.pGenSumpt350 = cms.Path(process.common * process.mfvGenParticleFilterSumpt350 * process.mfvGenSumpt350)

process.mfvGenParticleFilterSumpt400 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 400)
process.mfvGenSumpt400 = mfvTheoristRecipe.clone()
process.pGenSumpt400 = cms.Path(process.common * process.mfvGenParticleFilterSumpt400 * process.mfvGenSumpt400)

process.mfvGenParticleFilterSumpt450 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 450)
process.mfvGenSumpt450 = mfvTheoristRecipe.clone()
process.pGenSumpt450 = cms.Path(process.common * process.mfvGenParticleFilterSumpt450 * process.mfvGenSumpt450)

process.mfvGenParticleFilterSumpt500 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_dvv = 0.04, min_sumpt = 500)
process.mfvGenSumpt500 = mfvTheoristRecipe.clone()
process.pGenSumpt500 = cms.Path(process.common * process.mfvGenParticleFilterSumpt500 * process.mfvGenSumpt500)


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
