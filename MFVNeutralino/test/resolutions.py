import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

h2xqq = False

process.source.fileNames = '''/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_10_1_cUZ.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_11_1_g7H.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_12_1_HZL.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_13_1_DBl.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_14_1_ZAk.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_15_1_q8c.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_16_1_WXy.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_17_1_gz0.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_18_1_RSd.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_19_1_RAW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_1_1_WwV.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_20_1_AJ1.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_21_1_TyW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_22_1_4dW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_23_1_kAv.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_24_1_RXW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_25_1_g97.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_26_1_f0l.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_27_1_968.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_28_1_wAo.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_29_1_Ap2.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_2_1_aSP.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_30_1_Lbq.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_31_1_Kbr.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_32_1_sJO.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_33_1_5jX.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_34_1_yum.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_35_1_kXz.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_36_1_9f7.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_37_1_ZDs.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_38_1_BGe.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_39_1_x69.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_3_1_87r.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_40_1_ipP.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_41_1_qkw.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_42_1_WVb.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_43_1_Y8L.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_44_1_gup.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_45_1_dSN.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_46_1_ezj.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_47_1_A6t.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_48_1_OSp.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_49_1_Dna.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_4_1_oFW.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_50_1_NN6.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_5_1_RSz.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_6_1_JNY.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_7_1_Wuf.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_8_1_9eh.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_9_1_YYJ.root'''.split('\n')

process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20_wgen/4c67a9d5a51f11cf2da50127721f7362/ntuple_1_1_WwV.root']

if h2xqq:
    process.source.fileNames = '''/store/user/tucker/duh/ntuple_10_1_S8P.root
/store/user/tucker/duh/ntuple_11_1_7sv.root
/store/user/tucker/duh/ntuple_12_1_CBb.root
/store/user/tucker/duh/ntuple_13_1_F8t.root
/store/user/tucker/duh/ntuple_14_1_cPx.root
/store/user/tucker/duh/ntuple_15_1_JLc.root
/store/user/tucker/duh/ntuple_16_1_Pfi.root
/store/user/tucker/duh/ntuple_17_1_3D8.root
/store/user/tucker/duh/ntuple_18_1_bbt.root
/store/user/tucker/duh/ntuple_19_1_FtH.root
/store/user/tucker/duh/ntuple_1_1_e6b.root
/store/user/tucker/duh/ntuple_20_1_u23.root
/store/user/tucker/duh/ntuple_21_1_EYH.root
/store/user/tucker/duh/ntuple_22_1_zBY.root
/store/user/tucker/duh/ntuple_23_1_KBB.root
/store/user/tucker/duh/ntuple_24_1_5Mf.root
/store/user/tucker/duh/ntuple_25_1_eGB.root
/store/user/tucker/duh/ntuple_26_1_701.root
/store/user/tucker/duh/ntuple_27_1_mWU.root
/store/user/tucker/duh/ntuple_28_1_bke.root
/store/user/tucker/duh/ntuple_29_1_rGZ.root
/store/user/tucker/duh/ntuple_2_1_IhR.root
/store/user/tucker/duh/ntuple_30_1_u98.root
/store/user/tucker/duh/ntuple_31_1_6cp.root
/store/user/tucker/duh/ntuple_32_1_raJ.root
/store/user/tucker/duh/ntuple_33_1_0V9.root
/store/user/tucker/duh/ntuple_34_1_msr.root
/store/user/tucker/duh/ntuple_35_1_loz.root
/store/user/tucker/duh/ntuple_36_2_Ymf.root
/store/user/tucker/duh/ntuple_37_1_d9W.root
/store/user/tucker/duh/ntuple_38_1_lcv.root
/store/user/tucker/duh/ntuple_39_1_6m7.root
/store/user/tucker/duh/ntuple_3_1_vBh.root
/store/user/tucker/duh/ntuple_40_1_68q.root
/store/user/tucker/duh/ntuple_41_1_UVQ.root
/store/user/tucker/duh/ntuple_42_1_G9w.root
/store/user/tucker/duh/ntuple_43_1_7SF.root
/store/user/tucker/duh/ntuple_44_1_w93.root
/store/user/tucker/duh/ntuple_45_1_51p.root
/store/user/tucker/duh/ntuple_46_1_05X.root
/store/user/tucker/duh/ntuple_47_1_Xg6.root
/store/user/tucker/duh/ntuple_48_1_HRp.root
/store/user/tucker/duh/ntuple_49_1_W7t.root
/store/user/tucker/duh/ntuple_4_1_wQn.root
/store/user/tucker/duh/ntuple_50_1_zA4.root
/store/user/tucker/duh/ntuple_5_1_zDT.root
/store/user/tucker/duh/ntuple_6_1_CV7.root
/store/user/tucker/duh/ntuple_7_1_0u3.root
/store/user/tucker/duh/ntuple_8_1_kVE.root
/store/user/tucker/duh/ntuple_9_1_pea.root'''.split('\n')

process.TFileService.fileName = 'resolutions.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')

mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                mode = cms.string('mfv3j'),
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                which_mom = cms.int32(0),
                                max_dr = cms.double(-1),
                                max_dist = cms.double(0.012),
                                gen_src = cms.InputTag('genParticles'),
                                gen_jet_src = cms.InputTag('ak5GenJets'),
                                )
if h2xqq:
    process.mfvGenParticleFilter.mode = 'h2xqq'
    mfvResolutions.mode = 'h2xqq'
process.p = cms.Path(process.mfvSelectedVerticesTight)


#reconstructed cutflow
process.mfvResolutionsNoCuts = mfvResolutions.clone()
process.pNoCuts = cms.Path(process.mfvResolutionsNoCuts)

process.mfvAnalysisCutsTrigSel = process.mfvAnalysisCuts.clone(apply_cleaning_filters = False, min_4th_calojet_pt = 0, min_njets = 0, min_sumht = 0, apply_vertex_cuts = False)
process.mfvResolutionsTrigSel = mfvResolutions.clone()
process.pTrigSel = cms.Path(process.mfvAnalysisCutsTrigSel * process.mfvResolutionsTrigSel)

process.mfvAnalysisCutsCleaningFilters = process.mfvAnalysisCuts.clone(min_4th_calojet_pt = 0, min_njets = 0, min_sumht = 0, apply_vertex_cuts = False)
process.mfvResolutionsCleaningFilters = mfvResolutions.clone()
process.pCleaningFilters = cms.Path(process.mfvAnalysisCutsCleaningFilters * process.mfvResolutionsCleaningFilters)

process.mfvAnalysisCutsOfflineJets = process.mfvAnalysisCuts.clone(min_sumht = 0, apply_vertex_cuts = False)
process.mfvResolutionsOfflineJets = mfvResolutions.clone()
process.pOfflineJets = cms.Path(process.mfvAnalysisCutsOfflineJets * process.mfvResolutionsOfflineJets)

process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.mfvResolutionsPreSel = mfvResolutions.clone()
process.pPreSel = cms.Path(process.mfvAnalysisCutsPreSel * process.mfvResolutionsPreSel)

process.mfvAnalysisCutsTwoVtxNoCuts = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVertices')
process.mfvResolutionsTwoVtxNoCuts = mfvResolutions.clone()
process.pTwoVtxNoCuts = cms.Path(process.mfvSelectedVertices * process.mfvAnalysisCutsTwoVtxNoCuts * process.mfvResolutionsTwoVtxNoCuts)

process.mfvSelectedVerticesGeo2ddist = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0)
process.mfvAnalysisCutsTwoVtxGeo2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.mfvResolutionsTwoVtxGeo2ddist = mfvResolutions.clone()
process.pTwoVtxGeo2ddist = cms.Path(process.mfvSelectedVerticesGeo2ddist * process.mfvAnalysisCutsTwoVtxGeo2ddist * process.mfvResolutionsTwoVtxGeo2ddist)

process.mfvSelectedVerticesMindrmax = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_drmax = 1.2)
process.mfvAnalysisCutsTwoVtxMindrmax = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesMindrmax')
process.mfvResolutionsTwoVtxMindrmax = mfvResolutions.clone()
process.pTwoVtxMindrmax = cms.Path(process.mfvSelectedVerticesMindrmax * process.mfvAnalysisCutsTwoVtxMindrmax * process.mfvResolutionsTwoVtxMindrmax)

process.mfvSelectedVerticesMaxdrmax = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_drmax = 1.2, max_drmax = 4)
process.mfvAnalysisCutsTwoVtxMaxdrmax = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesMaxdrmax')
process.mfvResolutionsTwoVtxMaxdrmax = mfvResolutions.clone()
process.pTwoVtxMaxdrmax = cms.Path(process.mfvSelectedVerticesMaxdrmax * process.mfvAnalysisCutsTwoVtxMaxdrmax * process.mfvResolutionsTwoVtxMaxdrmax)

process.mfvSelectedVerticesDrmin = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4)
process.mfvAnalysisCutsTwoVtxDrmin = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesDrmin')
process.mfvResolutionsTwoVtxDrmin = mfvResolutions.clone()
process.pTwoVtxDrmin = cms.Path(process.mfvSelectedVerticesDrmin * process.mfvAnalysisCutsTwoVtxDrmin * process.mfvResolutionsTwoVtxDrmin)

process.mfvSelectedVerticesNtracks = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_ntracks = 5)
process.mfvAnalysisCutsTwoVtxNtracks = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.mfvResolutionsTwoVtxNtracks = mfvResolutions.clone()
process.pTwoVtxNtracks = cms.Path(process.mfvSelectedVerticesNtracks * process.mfvAnalysisCutsTwoVtxNtracks * process.mfvResolutionsTwoVtxNtracks)

process.mfvSelectedVerticesNtracksptgt3 = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_ntracks = 5, min_ntracksptgt3 = 3)
process.mfvAnalysisCutsTwoVtxNtracksptgt3 = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracksptgt3')
process.mfvResolutionsTwoVtxNtracksptgt3 = mfvResolutions.clone()
process.pTwoVtxNtracksptgt3 = cms.Path(process.mfvSelectedVerticesNtracksptgt3 * process.mfvAnalysisCutsTwoVtxNtracksptgt3 * process.mfvResolutionsTwoVtxNtracksptgt3)

process.mfvSelectedVerticesNjetsntks = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, max_sumnhitsbehind = 0, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_ntracks = 5, min_ntracksptgt3 = 3, min_njetsntks = 1)
process.mfvAnalysisCutsTwoVtxNjetsntks = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNjetsntks')
process.mfvResolutionsTwoVtxNjetsntks = mfvResolutions.clone()
process.pTwoVtxNjetsntks = cms.Path(process.mfvSelectedVerticesNjetsntks * process.mfvAnalysisCutsTwoVtxNjetsntks * process.mfvResolutionsTwoVtxNjetsntks)

process.mfvResolutionsFullSel = mfvResolutions.clone()
process.TwoVtxFullSel = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.mfvResolutionsFullSel)


#generated cutflow
process.mfvGenNoCuts = mfvResolutions.clone()
process.pGenNoCuts = cms.Path(process.mfvGenParticleFilter * process.mfvGenNoCuts)

process.mfvGenParticleFilterFourJets = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60)
process.mfvGenFourJets = mfvResolutions.clone()
process.pGenFourJets = cms.Path(process.mfvGenParticleFilterFourJets * process.mfvGenFourJets)

process.mfvGenParticleFilterSumHT = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500)
process.mfvGenSumHT = mfvResolutions.clone()
process.pGenSumHT = cms.Path(process.mfvGenParticleFilterSumHT * process.mfvGenSumHT)

process.mfvGenParticleFilterGeo2ddist = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5)
process.mfvGenGeo2ddist = mfvResolutions.clone()
process.pGenGeo2ddist = cms.Path(process.mfvGenParticleFilterGeo2ddist * process.mfvGenGeo2ddist)

process.mfvGenParticleFilterDrmax = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4)
process.mfvGenDrmax = mfvResolutions.clone()
process.pGenDrmax = cms.Path(process.mfvGenParticleFilterDrmax * process.mfvGenDrmax)

process.mfvGenParticleFilterNtracks1 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_ntracks = 1)
process.mfvGenNtracks1 = mfvResolutions.clone()
process.pGenNtracks1 = cms.Path(process.mfvGenParticleFilterNtracks1 * process.mfvGenNtracks1)

process.mfvGenParticleFilterNtracks2 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_ntracks = 2)
process.mfvGenNtracks2 = mfvResolutions.clone()
process.pGenNtracks2 = cms.Path(process.mfvGenParticleFilterNtracks2 * process.mfvGenNtracks2)

process.mfvGenParticleFilterNtracks3 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_ntracks = 3)
process.mfvGenNtracks3 = mfvResolutions.clone()
process.pGenNtracks3 = cms.Path(process.mfvGenParticleFilterNtracks3 * process.mfvGenNtracks3)

process.mfvGenParticleFilterNtracks4 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_ntracks = 4)
process.mfvGenNtracks4 = mfvResolutions.clone()
process.pGenNtracks4 = cms.Path(process.mfvGenParticleFilterNtracks4 * process.mfvGenNtracks4)

process.mfvGenParticleFilterNtracks5 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_ntracks = 5)
process.mfvGenNtracks5 = mfvResolutions.clone()
process.pGenNtracks5 = cms.Path(process.mfvGenParticleFilterNtracks5 * process.mfvGenNtracks5)

process.mfvGenParticleFilterNquarks1 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_nquarks = 1)
process.mfvGenNquarks1 = mfvResolutions.clone()
process.pGenNquarks1 = cms.Path(process.mfvGenParticleFilterNquarks1 * process.mfvGenNquarks1)

process.mfvGenParticleFilterNquarks2 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_nquarks = 2)
process.mfvGenNquarks2 = mfvResolutions.clone()
process.pGenNquarks2 = cms.Path(process.mfvGenParticleFilterNquarks2 * process.mfvGenNquarks2)

process.mfvGenParticleFilterNquarks3 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_nquarks = 3)
process.mfvGenNquarks3 = mfvResolutions.clone()
process.pGenNquarks3 = cms.Path(process.mfvGenParticleFilterNquarks3 * process.mfvGenNquarks3)

process.mfvGenParticleFilterNquarks4 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_nquarks = 4)
process.mfvGenNquarks4 = mfvResolutions.clone()
process.pGenNquarks4 = cms.Path(process.mfvGenParticleFilterNquarks4 * process.mfvGenNquarks4)

process.mfvGenParticleFilterNquarks5 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_nquarks = 5)
process.mfvGenNquarks5 = mfvResolutions.clone()
process.pGenNquarks5 = cms.Path(process.mfvGenParticleFilterNquarks5 * process.mfvGenNquarks5)

process.mfvGenParticleFilterSumpt60 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 60)
process.mfvGenSumpt60 = mfvResolutions.clone()
process.pGenSumpt60 = cms.Path(process.mfvGenParticleFilterSumpt60 * process.mfvGenSumpt60)

process.mfvGenParticleFilterSumpt70 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 70)
process.mfvGenSumpt70 = mfvResolutions.clone()
process.pGenSumpt70 = cms.Path(process.mfvGenParticleFilterSumpt70 * process.mfvGenSumpt70)

process.mfvGenParticleFilterSumpt80 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 80)
process.mfvGenSumpt80 = mfvResolutions.clone()
process.pGenSumpt80 = cms.Path(process.mfvGenParticleFilterSumpt80 * process.mfvGenSumpt80)

process.mfvGenParticleFilterSumpt90 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 90)
process.mfvGenSumpt90 = mfvResolutions.clone()
process.pGenSumpt90 = cms.Path(process.mfvGenParticleFilterSumpt90 * process.mfvGenSumpt90)

process.mfvGenParticleFilterSumpt100 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 100)
process.mfvGenSumpt100 = mfvResolutions.clone()
process.pGenSumpt100 = cms.Path(process.mfvGenParticleFilterSumpt100 * process.mfvGenSumpt100)

process.mfvGenParticleFilterSumpt110 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 110)
process.mfvGenSumpt110 = mfvResolutions.clone()
process.pGenSumpt110 = cms.Path(process.mfvGenParticleFilterSumpt110 * process.mfvGenSumpt110)

process.mfvGenParticleFilterSumpt120 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 120)
process.mfvGenSumpt120 = mfvResolutions.clone()
process.pGenSumpt120 = cms.Path(process.mfvGenParticleFilterSumpt120 * process.mfvGenSumpt120)

process.mfvGenParticleFilterSumpt130 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 130)
process.mfvGenSumpt130 = mfvResolutions.clone()
process.pGenSumpt130 = cms.Path(process.mfvGenParticleFilterSumpt130 * process.mfvGenSumpt130)

process.mfvGenParticleFilterSumpt140 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 140)
process.mfvGenSumpt140 = mfvResolutions.clone()
process.pGenSumpt140 = cms.Path(process.mfvGenParticleFilterSumpt140 * process.mfvGenSumpt140)

process.mfvGenParticleFilterSumpt150 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 150)
process.mfvGenSumpt150 = mfvResolutions.clone()
process.pGenSumpt150 = cms.Path(process.mfvGenParticleFilterSumpt150 * process.mfvGenSumpt150)

process.mfvGenParticleFilterSumpt160 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 160)
process.mfvGenSumpt160 = mfvResolutions.clone()
process.pGenSumpt160 = cms.Path(process.mfvGenParticleFilterSumpt160 * process.mfvGenSumpt160)

process.mfvGenParticleFilterSumpt170 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 170)
process.mfvGenSumpt170 = mfvResolutions.clone()
process.pGenSumpt170 = cms.Path(process.mfvGenParticleFilterSumpt170 * process.mfvGenSumpt170)

process.mfvGenParticleFilterSumpt180 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 180)
process.mfvGenSumpt180 = mfvResolutions.clone()
process.pGenSumpt180 = cms.Path(process.mfvGenParticleFilterSumpt180 * process.mfvGenSumpt180)

process.mfvGenParticleFilterSumpt190 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 190)
process.mfvGenSumpt190 = mfvResolutions.clone()
process.pGenSumpt190 = cms.Path(process.mfvGenParticleFilterSumpt190 * process.mfvGenSumpt190)

process.mfvGenParticleFilterSumpt200 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 200)
process.mfvGenSumpt200 = mfvResolutions.clone()
process.pGenSumpt200 = cms.Path(process.mfvGenParticleFilterSumpt200 * process.mfvGenSumpt200)

process.mfvGenParticleFilterSumpt210 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 210)
process.mfvGenSumpt210 = mfvResolutions.clone()
process.pGenSumpt210 = cms.Path(process.mfvGenParticleFilterSumpt210 * process.mfvGenSumpt210)

process.mfvGenParticleFilterSumpt220 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 220)
process.mfvGenSumpt220 = mfvResolutions.clone()
process.pGenSumpt220 = cms.Path(process.mfvGenParticleFilterSumpt220 * process.mfvGenSumpt220)

process.mfvGenParticleFilterSumpt230 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 230)
process.mfvGenSumpt230 = mfvResolutions.clone()
process.pGenSumpt230 = cms.Path(process.mfvGenParticleFilterSumpt230 * process.mfvGenSumpt230)

process.mfvGenParticleFilterSumpt240 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 240)
process.mfvGenSumpt240 = mfvResolutions.clone()
process.pGenSumpt240 = cms.Path(process.mfvGenParticleFilterSumpt240 * process.mfvGenSumpt240)

process.mfvGenParticleFilterSumpt250 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 250)
process.mfvGenSumpt250 = mfvResolutions.clone()
process.pGenSumpt250 = cms.Path(process.mfvGenParticleFilterSumpt250 * process.mfvGenSumpt250)

process.mfvGenParticleFilterSumpt300 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 300)
process.mfvGenSumpt300 = mfvResolutions.clone()
process.pGenSumpt300 = cms.Path(process.mfvGenParticleFilterSumpt300 * process.mfvGenSumpt300)

process.mfvGenParticleFilterSumpt350 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 350)
process.mfvGenSumpt350 = mfvResolutions.clone()
process.pGenSumpt350 = cms.Path(process.mfvGenParticleFilterSumpt350 * process.mfvGenSumpt350)

process.mfvGenParticleFilterSumpt400 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 400)
process.mfvGenSumpt400 = mfvResolutions.clone()
process.pGenSumpt400 = cms.Path(process.mfvGenParticleFilterSumpt400 * process.mfvGenSumpt400)

process.mfvGenParticleFilterSumpt450 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 450)
process.mfvGenSumpt450 = mfvResolutions.clone()
process.pGenSumpt450 = cms.Path(process.mfvGenParticleFilterSumpt450 * process.mfvGenSumpt450)

process.mfvGenParticleFilterSumpt500 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_sumpt = 500)
process.mfvGenSumpt500 = mfvResolutions.clone()
process.pGenSumpt500 = cms.Path(process.mfvGenParticleFilterSumpt500 * process.mfvGenSumpt500)

process.mfvGenParticleFilterNtracks2Sumpt200 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_ntracks = 2, min_sumpt = 200)
process.mfvGenNtracks2Sumpt200 = mfvResolutions.clone()
process.pGenNtracks2Sumpt200 = cms.Path(process.mfvGenParticleFilterNtracks2Sumpt200 * process.mfvGenNtracks2Sumpt200)

process.mfvGenParticleFilterNquarks2Sumpt200 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_nquarks = 2, min_sumpt = 200)
process.mfvGenNquarks2Sumpt200 = mfvResolutions.clone()
process.pGenNquarks2Sumpt200 = cms.Path(process.mfvGenParticleFilterNquarks2Sumpt200 * process.mfvGenNquarks2Sumpt200)

process.mfvGenParticleFilterNtracks2Nquarks1Sumpt200 = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_ntracks = 2, min_nquarks = 1, min_sumpt = 200)
process.mfvGenNtracks2Nquarks1Sumpt200 = mfvResolutions.clone()
process.pGenNtracks2Nquarks1Sumpt200 = cms.Path(process.mfvGenParticleFilterNtracks2Nquarks1Sumpt200 * process.mfvGenNtracks2Nquarks1Sumpt200)

if h2xqq:
    process.zzzfilt = cms.EDFilter('MFVEXO12038SampleFilter',
                                   gen_particles_src = cms.InputTag('genParticles'),
                                   mode = cms.string('h2x'),
                                   h2x_num = cms.int32(1),
                                   min_dbv = cms.double(0),
                                   max_dbv = cms.double(1e9),
                                   min_dvv = cms.double(0),
                                   max_dvv = cms.double(1e9),
                                   )
    for n,p in process.paths.items():
        p.insert(0, process.zzzfilt)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    Samples.mfv_neutralino_tau0100um_M0200.ana_dataset_override = '/mfv_neutralino_tau0100um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M0300.ana_dataset_override = '/mfv_neutralino_tau0100um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M0400.ana_dataset_override = '/mfv_neutralino_tau0100um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M0600.ana_dataset_override = '/mfv_neutralino_tau0100um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M0800.ana_dataset_override = '/mfv_neutralino_tau0100um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0100um_M1000.ana_dataset_override = '/mfv_neutralino_tau0100um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0200.ana_dataset_override = '/mfv_neutralino_tau0300um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0300.ana_dataset_override = '/mfv_neutralino_tau0300um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0400.ana_dataset_override = '/mfv_neutralino_tau0300um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0600.ana_dataset_override = '/mfv_neutralino_tau0300um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M0800.ana_dataset_override = '/mfv_neutralino_tau0300um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau0300um_M1000.ana_dataset_override = '/mfv_neutralino_tau0300um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0200.ana_dataset_override = '/mfv_neutralino_tau1000um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0300.ana_dataset_override = '/mfv_neutralino_tau1000um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0400.ana_dataset_override = '/mfv_neutralino_tau1000um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0600.ana_dataset_override = '/mfv_neutralino_tau1000um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M0800.ana_dataset_override = '/mfv_neutralino_tau1000um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau1000um_M1000.ana_dataset_override = '/mfv_neutralino_tau1000um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0200.ana_dataset_override = '/mfv_neutralino_tau9900um_M0200/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0300.ana_dataset_override = '/mfv_neutralino_tau9900um_M0300/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0400.ana_dataset_override = '/mfv_neutralino_tau9900um_M0400/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0600.ana_dataset_override = '/mfv_neutralino_tau9900um_M0600/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M0800.ana_dataset_override = '/mfv_neutralino_tau9900um_M0800/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'
    Samples.mfv_neutralino_tau9900um_M1000.ana_dataset_override = '/mfv_neutralino_tau9900um_M1000/tucker-mfvntuple_v20_wgen-4c67a9d5a51f11cf2da50127721f7362/USER'

    for sample in Samples.mfv_signal_samples:
      sample.ana_scheduler = 'remoteGlidein'

    cs = CRABSubmitter('MFVResolutionsV20',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all([Samples.mfv_neutralino_tau1000um_M0400])
