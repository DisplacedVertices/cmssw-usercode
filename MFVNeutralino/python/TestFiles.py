import sys, FWCore.ParameterSet.Config as cms

tau1000M0400 = ['/store/user/jchu/mfv_neutralino_tau1000um_M0400/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_1_1_hdB.root']
tau1000M0400_sec = cms.untracked.vstring(
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1185_1_JKO.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1198_1_miF.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1202_1_6Rq.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1330_1_emA.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_842_1_2Hs.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_180_1_X9e.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_425_2_ZeH.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_426_3_7Ql.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_645_2_WPD.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1368_1_0Cu.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1372_1_Rce.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1840_1_OPG.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1847_1_ceP.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1981_1_9Va.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1983_1_QCo.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_574_1_GvQ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_579_1_Y9Z.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_614_1_Qgx.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_707_1_GYJ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_717_1_IO1.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1946_1_YCr.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_107_2_9uk.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_847_2_MbS.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1930_1_i4a.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1933_1_C1w.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_42_2_0A8.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_46_2_Ceq.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_53_1_yFF.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_772_1_NOh.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_773_1_jbZ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_774_1_cKg.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_782_1_RDa.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1838_1_sTl.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1842_1_YG6.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_780_4_4jN.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1751_3_Mid.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_2000_1_THr.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_179_2_WvC.root'
    )

tau1000M0400_nt = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v8/99d7a676d206adfebd5d154091ebe5a6/ntuple_1_1_FiW.root']
tau1000M0400_nt_sec = cms.untracked.vstring(
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_847_2_MbS.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_842_1_2Hs.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_782_1_RDa.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_780_4_4jN.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_774_1_cKg.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_773_1_jbZ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_772_1_NOh.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_717_1_IO1.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_707_1_GYJ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_645_2_WPD.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_614_1_Qgx.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_579_1_Y9Z.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_574_1_GvQ.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_53_1_yFF.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_46_2_Ceq.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_42_2_0A8.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_426_3_7Ql.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_425_2_ZeH.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_2000_1_THr.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1983_1_QCo.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1981_1_9Va.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1946_1_YCr.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1933_1_C1w.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1930_1_i4a.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1847_1_ceP.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1842_1_YG6.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1840_1_OPG.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1838_1_sTl.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_180_1_X9e.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_179_2_WvC.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1751_3_Mid.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1372_1_Rce.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1368_1_0Cu.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1330_1_emA.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1202_1_6Rq.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1198_1_miF.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1185_1_JKO.root',
    '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_107_2_9uk.root',
    )
    
##########

tau9900M0400_nt = ['/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfvntuple_v8/99d7a676d206adfebd5d154091ebe5a6/ntuple_1_1_wm7.root']
tau9900M0400_nt_sec = cms.untracked.vstring(
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_680_1_n16.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_679_2_G1R.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_678_1_7Cc.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_608_1_TQw.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_606_2_mE6.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_605_1_dIp.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_544_4_lLD.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_543_2_xpc.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_542_2_mhX.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_541_2_Tia.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_540_2_IRN.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_483_3_Ng2.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_482_2_pEi.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_481_2_YIx.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_480_2_3GJ.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_443_2_Utv.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_442_3_4YW.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_441_1_YCs.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_440_1_Vau.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_378_1_BCE.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_377_2_1y1.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_376_1_55z.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_375_1_xRB.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_374_1_7vn.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_343_1_rvT.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_342_1_H3w.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_341_1_ej2.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_339_2_vKg.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_318_2_ucT.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_317_2_Vm8.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_316_1_Enr.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_315_2_AHh.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_313_1_JGt.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_289_1_vob.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_285_1_3dZ.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_284_1_cwR.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_258_2_A5T.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_257_4_83M.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_255_1_nvB.root',
    '/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_254_2_JTs.root',
    )

##########

qcdht1000 = ['/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_v7/fe6d9f80f9c0fe06cc80b089617fa99d/pat_1_1_NOT.root']
qcdht1000_sec = cms.untracked.vstring(
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/0038E6D2-860D-E211-9211-00266CFACC38.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/D4C0816B-870D-E211-B094-00266CF258D8.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/A2CEDDF1-870D-E211-A98D-00266CF258D8.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/9E8E388F-970D-E211-8D78-848F69FD298E.root',
    )

qcdht1000_nt = ['/store/user/tucker/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/mfvntuple_v8/944db31db2a0af057913c3b3bd5ae1df/ntuple_1_1_3QM.root']
qcdht1000_nt_sec = cms.untracked.vstring(
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/E095A6E2-910D-E211-873A-00266CF9B970.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/D4C0816B-870D-E211-B094-00266CF258D8.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/A2CEDDF1-870D-E211-A98D-00266CF258D8.root',
    '/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/0038E6D2-860D-E211-9211-00266CFACC38.root',
    )

##########

ttbarhadronic = ['/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_v7/fe6d9f80f9c0fe06cc80b089617fa99d/pat_1_1_HLq.root']
ttbarhadronic_sec = cms.untracked.vstring(
    '/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/BCE41FBC-BE17-E211-9679-00259073E3FC.root',
    '/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/562EF878-5017-E211-976D-E0CB4E5536A7.root'
    )

##########

multijet = ['file:/uscms_data/d1/tucker/multijetb.root']
multijet_sec = cms.untracked.vstring('/store/data/Run2012B/MultiJet1Parked/AOD/05Nov2012-v2/10002/84082899-BB49-E211-9227-001E67398052.root')

multijet_nt = ['/store/user/tucker/MultiJet1Parked/mfvntuple_v8/00b5523718eb71b4bef18c6d45967745/ntuple_100_1_M3M.root']
multijet_nt_sec = cms.untracked.vstring(
    '/store/data/Run2012B/MultiJet1Parked/AOD/05Nov2012-v2/10013/C0CB1188-0C4E-E211-919C-00304866C47A.root',
    '/store/data/Run2012B/MultiJet1Parked/AOD/05Nov2012-v2/10013/6C729CA5-0C4E-E211-9EEE-002590200908.root',
    '/store/data/Run2012B/MultiJet1Parked/AOD/05Nov2012-v2/10013/3A2771A8-0C4E-E211-BA5D-001E67396E64.root',
    '/store/data/Run2012B/MultiJet1Parked/AOD/05Nov2012-v2/10003/CE536601-124E-E211-B325-001E67397CC9.root',
    )

##########

def set_test_files(process):
    if 'testfileshelp' in sys.argv:
        print 'set_test_files sample keywords available: testdata (multijet), testqcd, testttbar. default is tau1000M0400.'
        print 'words set_test_files recognizes in argv:'
        print '  temp    : use ntuple.root in current directory.'
        print '  usesec  : use secondary files.'
        print '  frompat : use PAT tuples as input instead, and implies usesec. default is to run on MFV ntuples.'
        sys.exit(1)

    if 'temp' in sys.argv:
        process.source.fileNames = ['file:ntuple.root']
        process.source.secondaryFileNames = cms.untracked.vstring('/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/0C57EA77-AEE3-E211-8DCA-00259073E4D4.root')
        return

    nt = 'frompat' not in sys.argv
    sec = not nt or 'usesec' in sys.argv

    if 'testqcd' in sys.argv:
        if nt:
            process.source.fileNames = qcdht1000_nt
            if sec:
                process.source.secondaryFileNames = qcdht1000_nt_sec
        else:
            process.source.fileNames = qcdht1000
            if sec:
                process.source.secondaryFileNames = qcdht1000_sec
    elif 'testttbar' in sys.argv:
        if nt:
            process.source.fileNames = ttbarhadronic_nt
            if sec:
                process.source.secondaryFileNames = ttbarhadronic_nt_sec
        else:
            process.source.fileNames = ttbarhadronic
            if sec:
                process.source.secondaryFileNames = ttbarhadronic_sec
    elif 'testdata' in sys.argv:
        if nt:
            process.source.fileNames = multijet_nt
            if sec:
                process.source.secondaryFileNames = multijet_nt_sec
        else:
            process.source.fileNames = multijet
            if sec:
                process.source.secondaryFileNames = multijet_sec
    elif 'test9900' in sys.argv:
        if nt:
            process.source.fileNames = tau9900M0400_nt
            if sec:
                process.source.secondaryFileNames = tau9900M0400_nt_sec
        else:
            assert 0
    else:
        if nt:
            process.source.fileNames = tau1000M0400_nt
            if sec:
                process.source.secondaryFileNames = tau1000M0400_nt_sec
        else:
            process.source.fileNames = tau1000M0400
            if sec:
                process.source.secondaryFileNames = tau1000M0400_sec

    print 'set_test_files:'
    print 'process.source.fileNames:'
    print process.source.fileNames
    if hasattr(process.source, 'secondaryFileNames'):
        print 'process.source.secondaryFileNames:'
        print process.source.secondaryFileNames
