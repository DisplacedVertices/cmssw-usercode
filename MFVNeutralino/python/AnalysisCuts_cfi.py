import FWCore.ParameterSet.Config as cms
from JMTucker.MFVNeutralino.NtupleCommon import use_btag_triggers, use_MET_triggers

if use_btag_triggers:
  apply_presel = cms.int32(4)
elif use_MET_triggers:
  apply_presel = cms.int32(5)
else:
  apply_presel = cms.int32(1)

mfvAnalysisCuts = cms.EDFilter('MFVAnalysisCuts',
                               mevent_src = cms.InputTag('mfvEvent'),
                               apply_presel = apply_presel,  # 1 = jets, 2 = el/mu, 3 = jets OR bjet/displaced dijet triggers, 4 = bjet/displaced dijet triggers veto HT trigger, 5 = MET trigger
                               require_met_filters = cms.bool(True),
                               require_bquarks = cms.bool(False),
                               # to make any of the next 3 trigger cuts work, or min/max_njets/ht, you have to set apply_presel = 0 above
                               l1_bit = cms.int32(-1),
                               trigger_bit = cms.int32(-1),
                               apply_trigger = cms.int32(0),
                               apply_cleaning_filters = cms.bool(False),
                               min_npv = cms.int32(0),
                               max_npv = cms.int32(100000),
                               min_npu = cms.double(-1e9),
                               max_npu = cms.double(1e9),
                               max_pv_ntracks = cms.int32(100000),
                               min_njets = cms.int32(0),
                               max_njets = cms.int32(100000),
                               min_nbtags = cms.vint32(0,0,0),
                               max_nbtags = cms.vint32(100000,100000,100000),
                               min_ht = cms.double(0),
                               max_ht = cms.double(1e9),
                               min_nleptons = cms.int32(0),
                               min_nselleptons = cms.int32(0),
                               apply_vertex_cuts = cms.bool(True),
                               vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                               min_nvertex = cms.int32(2),
                               max_nvertex = cms.int32(100000),
                               ntracks01_0 = cms.int32(0),
                               ntracks01_1 = cms.int32(0),
                               min_ntracks01 = cms.int32(0),
                               max_ntracks01 = cms.int32(100000),
                               min_maxtrackpt01 = cms.double(0),
                               max_maxtrackpt01 = cms.double(1e9),
                               min_njetsntks01 = cms.int32(0),
                               min_tkonlymass01 = cms.double(0),
                               min_jetsntkmass01 = cms.double(0),
                               min_tksjetsntkmass01 = cms.double(0),
                               min_absdeltaphi01 = cms.double(0),
                               min_bs2ddist01 = cms.double(0),
                               min_bs2dsig01 = cms.double(0),
                               min_pv2ddist01 = cms.double(0),
                               min_pv3ddist01 = cms.double(0),
                               min_pv2dsig01 = cms.double(0),
                               min_pv3dsig01 = cms.double(0),
                               min_svdist2d = cms.double(0),
                               max_svdist2d = cms.double(1e9),
                               min_svdist3d = cms.double(0),
                               max_ntrackssharedwpv01 = cms.int32(100000),
                               max_ntrackssharedwpvs01 = cms.int32(100000),
                               max_fractrackssharedwpv01 = cms.double(1e9),
                               max_fractrackssharedwpvs01 = cms.double(1e9),
                               )
