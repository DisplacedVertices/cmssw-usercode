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

process.mfvTheoristRecipeTwoVtxBs2derr = mfvTheoristRecipe.clone()
process.pTwoVtxBs2derr = cms.Path(process.common * process.mfvAnalysisCuts * process.mfvTheoristRecipeTwoVtxBs2derr)

process.mfvAnalysisCutsDvv400um = process.mfvAnalysisCuts.clone(min_svdist2d = 0.04)
process.mfvTheoristRecipeTwoVtxDvv400um = mfvTheoristRecipe.clone()
process.pTwoVtxDvv400um = cms.Path(process.common * process.mfvAnalysisCutsDvv400um * process.mfvTheoristRecipeTwoVtxDvv400um)

#generated cutflow
process.mfvGenNoCuts = mfvTheoristRecipe.clone()
process.pGenNoCuts = cms.Path(process.common * process.mfvGenParticleFilter * process.mfvGenNoCuts)

process.mfvGenParticleFilterThreeJets = process.mfvGenParticleFilter.clone(min_npartons = 3, min_parton_pt = 20)
process.mfvGenThreeJets = mfvTheoristRecipe.clone()
process.pGenThreeJets = cms.Path(process.common * process.mfvGenParticleFilterThreeJets * process.mfvGenThreeJets)

process.mfvGenParticleFilterHT900 = process.mfvGenParticleFilter.clone(min_npartons = 3, min_parton_pt = 20, min_parton_ht40 = 900)
process.mfvGenHT900 = mfvTheoristRecipe.clone()
process.pGenHT900 = cms.Path(process.common * process.mfvGenParticleFilterHT900 * process.mfvGenHT900)

process.mfvGenParticleFilterHT40 = process.mfvGenParticleFilter.clone(min_npartons = 3, min_parton_pt = 20, min_parton_ht40 = 1000)
process.mfvGenHT40 = mfvTheoristRecipe.clone()
process.pGenHT40 = cms.Path(process.common * process.mfvGenParticleFilterHT40 * process.mfvGenHT40)

process.mfvGenParticleFilterNtracks1 = process.mfvGenParticleFilter.clone(min_npartons = 3, min_parton_pt = 20, min_parton_ht40 = 1000, min_ntracks = 1)
process.mfvGenNtracks1 = mfvTheoristRecipe.clone()
process.pGenNtracks1 = cms.Path(process.common * process.mfvGenParticleFilterNtracks1 * process.mfvGenNtracks1)

process.mfvGenParticleFilterGeo2ddist = process.mfvGenParticleFilter.clone(min_npartons = 3, min_parton_pt = 20, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0)
process.mfvGenGeo2ddist = mfvTheoristRecipe.clone()
process.pGenGeo2ddist = cms.Path(process.common * process.mfvGenParticleFilterGeo2ddist * process.mfvGenGeo2ddist)

process.mfvGenParticleFilterBsbs2ddist = process.mfvGenParticleFilter.clone(min_npartons = 3, min_parton_pt = 20, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01)
process.mfvGenBsbs2ddist = mfvTheoristRecipe.clone()
process.pGenBsbs2ddist = cms.Path(process.common * process.mfvGenParticleFilterBsbs2ddist * process.mfvGenBsbs2ddist)

process.mfvGenParticleFilterSumpt300 = process.mfvGenParticleFilter.clone(min_npartons = 3, min_parton_pt = 20, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_sumpt = 300)
process.mfvGenSumpt300 = mfvTheoristRecipe.clone()
process.pGenSumpt300 = cms.Path(process.common * process.mfvGenParticleFilterSumpt300 * process.mfvGenSumpt300)

process.mfvGenParticleFilterDvv400um = process.mfvGenParticleFilter.clone(min_npartons = 3, min_parton_pt = 20, min_parton_ht40 = 1000, min_ntracks = 1, max_rho0 = 2.0, max_rho1 = 2.0, min_rho0 = 0.01, min_rho1 = 0.01, min_sumpt = 300, min_dvv = 0.04)
process.mfvGenDvv400um = mfvTheoristRecipe.clone()
process.pGenDvv400um = cms.Path(process.common * process.mfvGenParticleFilterDvv400um * process.mfvGenDvv400um)


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
