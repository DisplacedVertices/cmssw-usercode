import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

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
process.TFileService.fileName = 'resolutions.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')

mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                which_mom = cms.int32(0),
                                max_dr = cms.double(-1),
                                max_dist = cms.double(0.012),
                                gen_src = cms.InputTag('genParticles'),
                                gen_jet_src = cms.InputTag('ak5GenJets'),
                                )
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

process.mfvSelectedVerticesGeo2ddist = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5)
process.mfvAnalysisCutsTwoVtxGeo2ddist = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesGeo2ddist')
process.mfvResolutionsTwoVtxGeo2ddist = mfvResolutions.clone()
process.pTwoVtxGeo2ddist = cms.Path(process.mfvSelectedVerticesGeo2ddist * process.mfvAnalysisCutsTwoVtxGeo2ddist * process.mfvResolutionsTwoVtxGeo2ddist)

process.mfvSelectedVerticesMindrmax = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, min_drmax = 1.2)
process.mfvAnalysisCutsTwoVtxMindrmax = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesMindrmax')
process.mfvResolutionsTwoVtxMindrmax = mfvResolutions.clone()
process.pTwoVtxMindrmax = cms.Path(process.mfvSelectedVerticesMindrmax * process.mfvAnalysisCutsTwoVtxMindrmax * process.mfvResolutionsTwoVtxMindrmax)

process.mfvSelectedVerticesMaxdrmax = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, min_drmax = 1.2, max_drmax = 4)
process.mfvAnalysisCutsTwoVtxMaxdrmax = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesMaxdrmax')
process.mfvResolutionsTwoVtxMaxdrmax = mfvResolutions.clone()
process.pTwoVtxMaxdrmax = cms.Path(process.mfvSelectedVerticesMaxdrmax * process.mfvAnalysisCutsTwoVtxMaxdrmax * process.mfvResolutionsTwoVtxMaxdrmax)

process.mfvSelectedVerticesDrmin = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4)
process.mfvAnalysisCutsTwoVtxDrmin = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesDrmin')
process.mfvResolutionsTwoVtxDrmin = mfvResolutions.clone()
process.pTwoVtxDrmin = cms.Path(process.mfvSelectedVerticesDrmin * process.mfvAnalysisCutsTwoVtxDrmin * process.mfvResolutionsTwoVtxDrmin)

process.mfvSelectedVerticesNtracks = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_ntracks = 5)
process.mfvAnalysisCutsTwoVtxNtracks = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracks')
process.mfvResolutionsTwoVtxNtracks = mfvResolutions.clone()
process.pTwoVtxNtracks = cms.Path(process.mfvSelectedVerticesNtracks * process.mfvAnalysisCutsTwoVtxNtracks * process.mfvResolutionsTwoVtxNtracks)

process.mfvSelectedVerticesNtracksptgt3 = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_ntracks = 5, min_ntracksptgt3 = 3)
process.mfvAnalysisCutsTwoVtxNtracksptgt3 = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtracksptgt3')
process.mfvResolutionsTwoVtxNtracksptgt3 = mfvResolutions.clone()
process.pTwoVtxNtracksptgt3 = cms.Path(process.mfvSelectedVerticesNtracksptgt3 * process.mfvAnalysisCutsTwoVtxNtracksptgt3 * process.mfvResolutionsTwoVtxNtracksptgt3)

process.mfvSelectedVerticesNjetsntks = process.mfvSelectedVertices.clone(max_geo2ddist = 2.5, min_drmax = 1.2, max_drmax = 4, max_drmin = 0.4, min_ntracks = 5, min_ntracksptgt3 = 3, min_njetsntks = 1)
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

process.mfvGenParticleFilterNtracks = process.mfvGenParticleFilter.clone(min_npartons = 4, min_parton_pt = 60, min_parton_sumht = 500, max_rho0 = 2.5, max_rho1 = 2.5, max_drmax = 4, min_ntracks = 3)
process.mfvGenNtracks = mfvResolutions.clone()
process.pGenNtracks = cms.Path(process.mfvGenParticleFilterNtracks * process.mfvGenNtracks)


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
