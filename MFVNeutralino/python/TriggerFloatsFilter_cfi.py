import FWCore.ParameterSet.Config as cms

mfvTriggerFloatsFilter = cms.EDFilter('MFVTriggerFloatsFilter',
                                      require_hlt = cms.int32(-1),
                                      require_l1 = cms.int32(-1),
                                      min_njets = cms.int32(0),
                                      hltht_cut = cms.double(-1),
                                      ht_cut = cms.double(-1),
                                      myhtt_m_l1htt_cut = cms.double(-1),
                                      myhttwbug_m_l1htt_cut = cms.double(-1),
                                      )
