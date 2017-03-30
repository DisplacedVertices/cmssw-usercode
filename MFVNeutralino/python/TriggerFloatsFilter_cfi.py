import FWCore.ParameterSet.Config as cms

mfvTriggerFloatsFilter = cms.EDFilter('MFVTriggerFloatsFilter',
                                      hltht_cut = cms.double(-1),
                                      ht_cut = cms.double(-1),
                                      myhtt_m_l1htt_cut = cms.double(-1),
                                      myhttwbug_m_l1htt_cut = cms.double(-1),
                                      )
