import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, geometry_etc
from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel

#process.source.fileNames = ['file:out.root']
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(

#new menu w/ 6jet triggers
#400
#400
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_10_1_DIC.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_1_1_b2N.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_2_1_23h.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_3_1_kNb.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_4_1_mA6.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_5_1_GgE.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_6_1_Q3U.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_7_1_Pku.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_8_1_04m.root',
#'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_9_1_DYY.root',

#500
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_10_1_Nf4.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_1_1_KnQ.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_2_1_I7b.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_3_1_LP8.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_4_1_kmK.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_5_1_PjX.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_6_1_cqs.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_7_1_GKk.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_8_1_JHS.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_9_1_0jj.root',

#'600
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_10_1_ET2.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_1_1_q3M.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_2_1_Ie7.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_3_1_O6f.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_4_1_0jG.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_5_1_OaD.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_6_1_eQ2.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_7_1_7sh.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_8_1_wrK.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_9_1_yds.root',

#'700
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_10_1_1V7.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_1_1_kgG.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_2_1_1ig.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_3_1_dHW.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_4_1_Nv5.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_5_1_aPg.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_6_1_IgF.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_7_1_los.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_8_1_tvI.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_9_1_0ip.root',


#'800
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_10_1_wXD.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_1_1_mt3.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_2_1_qFq.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_3_1_C7z.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_4_1_GgZ.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_5_1_tSf.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_6_1_fkl.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_7_1_l0z.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_8_1_8qs.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_9_1_0iV.root',

#'900
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_10_1_Yky.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_1_1_Hvm.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_2_1_3U9.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_3_1_ti4.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_4_1_ONL.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_5_1_btA.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_6_1_VC2.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_7_1_ZUh.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_8_1_wJP.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_9_1_qTh.root',

#'1000
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_10_1_0uM.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_1_1_LYn.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_2_1_FNH.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_3_1_Gli.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_4_1_e2y.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_5_1_0uS.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_6_1_dqg.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_7_1_Tat.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_8_1_UJZ.root',
'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod_ht6jet/0bea2cc30dbc97fc6074512158d9b553/out_9_1_7KL.root',



#old (standard) menu
#400
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_10_1_BIL.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_2_oEB.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_2_qc2.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_3_1_mLB.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_4_1_pLq.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_5_1_lqh.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_6_1_sXa.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_tfK.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_WXy.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_9_1_Bpn.root',

#500
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_10_1_whz.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_1_wua.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_1_Vwa.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_3_1_fCl.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_4_1_E6p.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_5_1_hz7.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_6_1_Lfx.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_uul.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_bgo.root',
#'/store/user/mzientek/Neutralino_M500_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m500_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_9_1_ZDj.root',

#600
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_10_1_JE7.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_1_X8B.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_1_y9n.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_3_1_NNF.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_4_1_IQi.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_5_1_kFx.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_6_1_2lZ.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_pU6.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_jZF.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_wVV.root',
#'/store/user/mzientek/Neutralino_M600_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m600_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_9_1_fwc.root',

#700
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_10_1_ob1.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_1_18B.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_1_PM9.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_1_mvR.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_3_1_n90.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_4_1_ksw.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_5_1_fL0.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_6_1_nfg.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_dmi.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_gdE.root',
#'/store/user/mzientek/Neutralino_M700_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m700_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_9_1_2xW.root',

#800
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_10_1_ZE0.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_1_1wo.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_1_2Dx.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_1_XvK.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_3_1_rsM.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_4_1_UtO.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_5_1_YTJ.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_6_1_S8f.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_BHy.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_xR4.root',
#'/store/user/mzientek/Neutralino_M800_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m800_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_9_1_JK6.root',

#900
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_10_1_tyj.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_1_tu2.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_1_MrR.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_3_1_1d8.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_4_1_ee8.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_5_1_Re1.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_6_1_xmj.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_8cy.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_n3o.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_VIT.root',
#'/store/user/mzientek/Neutralino_M900_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m900_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_9_1_Lz4.root',

#1000
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_10_1_9iQ.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_1_IgY.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_1_z8L.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_1_gRQ.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_3_1_THL.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_4_1_6cC.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_5_1_CcV.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_6_1_hHX.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_3ao.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_tIl.root',
#'/store/user/mzientek/Neutralino_M1TeV_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m1000_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_9_1_56i.root',


#400 8 TeV
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_10_1_BIL.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_1_2_oEB.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_2_2_qc2.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_3_1_mLB.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_4_1_pLq.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_5_1_lqh.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_6_1_sXa.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_7_1_tfK.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_8_1_WXy.root',
#'/store/user/mzientek/Neutralino_M400_8TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_8TeV_miniaod/0bea2cc30dbc97fc6074512158d9b553/out_9_1_Bpn.root',


))


process.TFileService.fileName = 'histos.root'
process.maxEvents.input = 100

process.load('JMTucker.MFVNeutralino.Histos_cff')

process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process, weight_src='mfvWeight')

process.RandomNumberGeneratorService.SimpleTriggerEfficiency = cms.PSet(initialSeed = cms.untracked.uint32(1219))

nm1s = [
    ('Ntracks', 'min_ntracks = 0, min_njetsntks = 0'),
    ('Drmin',   'max_drmin = 1e9'),
    ('Drmax',   'max_drmax = 1e9'),
    ('Mindrmax','min_drmax = 0'),
    ('Bs2derr', 'max_bs2derr = 1e9'),
    ('Njets',   'min_njetsntks = 0'),
    ('Ntracksptgt3', 'min_ntracksptgt3 = 0'),
    ('Sumnhitsbehind', 'max_sumnhitsbehind = 1000000'),
    ('ButNtracksAndGt3', 'max_drmin = 1e9, max_drmax = 1e9, min_drmax = 0, max_bs2derr = 1e9, min_njetsntks = 0'),
    ]

for name, cut in nm1s:
    evt_cut = ''
    if type(cut) == tuple:
        cut, evt_cut = cut

    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name

    for only in ('', 'Only'):
        for nv in (1,2):
            if nv == 2 and only == 'Only':
                continue

            ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
            ana.vertex_src = vtx_name
            if only == 'Only':
                ana.max_nvertex = nv
            ana.min_nvertex = nv
            ana_name = 'ana%s%iVNo' % (only, nv) + name

            evt_hst = process.mfvEventHistos.clone()
            evt_hst_name = 'evtHst%s%iVNo' % (only, nv) + name

            vtx_hst = process.mfvVertexHistos.clone(vertex_aux_src = vtx_name)
            vtx_hst_name = 'vtxHst%s%iVNo' % (only, nv) + name

	    eff = process.SimpleTriggerEfficiency.clone()
	   
            setattr(process, vtx_name, vtx)
            setattr(process, ana_name, ana)
            setattr(process, evt_hst_name, evt_hst)
            setattr(process, vtx_hst_name, vtx_hst)
            setattr(process, 'p%s%iV' % (only, nv) + name, cms.Path(vtx * ana * evt_hst * vtx_hst ))

process.triggerFilter1 = hltHighLevel.clone()
process.triggerFilter2 = hltHighLevel.clone()
process.triggerFilter3 = hltHighLevel.clone()
process.triggerFilter4 = hltHighLevel.clone()
process.triggerFilter5 = hltHighLevel.clone()
process.triggerFilter6 = hltHighLevel.clone()
process.triggerFilter1.HLTPaths = ['HLT_PFHT750_4Jet_v*']
process.triggerFilter2.HLTPaths = ['HLT_PFHT550_6Jet_v*']
process.triggerFilter3.HLTPaths = ['HLT_PFHT600_6Jet_v*']
process.triggerFilter4.HLTPaths = ['HLT_PFHT650_6Jet_v*']
process.triggerFilter5.HLTPaths = ['HLT_PFHT700_6Jet_v*']
process.triggerFilter6.HLTPaths = ['HLT_PFHT750_6Jet_v*']
#process.triggerFilter2.HLTPaths = ['HLT_HT500_DisplacedDijet40_Inclusive_v*']
#process.triggerFilter3.HLTPaths = ['HLT_HT550_DisplacedDijet40_Inclusive_v*']
#process.triggerFilter4.HLTPaths = ['HLT_HT650_DisplacedDijet80_Inclusive_v*']
process.triggerFilter1.andOr = True # = OR
process.triggerFilter2.andOr = True # = OR
process.triggerFilter3.andOr = True # = OR
process.triggerFilter4.andOr = True # = OR
process.triggerFilter5.andOr = True # = OR
process.triggerFilter6.andOr = True # = OR

#process.pFullSel *= process.SimpleTriggerEfficiency

process.pFullSelWTrig1 = process.pFullSel.copy()
process.pFullSelWTrig1 *= process.triggerFilter1
process.pFullSelWTrig2 = process.pFullSel.copy()
process.pFullSelWTrig2 *= process.triggerFilter2
process.pFullSelWTrig3 = process.pFullSel.copy()
process.pFullSelWTrig3 *= process.triggerFilter3
process.pFullSelWTrig4 = process.pFullSel.copy()
process.pFullSelWTrig4 *= process.triggerFilter4
process.pFullSelWTrig5 = process.pFullSel.copy()
process.pFullSelWTrig5 *= process.triggerFilter5
process.pFullSelWTrig6 = process.pFullSel.copy()
process.pFullSelWTrig6 *= process.triggerFilter6

process.mfvWeight.enable = False
process.options.wantSummary = True

def force_bs(process, bs):
    for ana in process.analyzers:
        if hasattr(ana, 'force_bs'):
            ana.force_bs = bs

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
                                 Samples.mfv_neutralino_tau1000um_M0400,
                                 Samples.mfv_neutralino_tau0300um_M0400,
                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples)

    for s in Samples.data_samples:
        s.json = 'ana_all.json'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('HistosV20',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       #USER_additional_input_files = 'aaaa.root',
                       )
    cs.submit_all(samples)
