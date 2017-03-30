import FWCore.ParameterSet.Config as cms

mfvTriggerFloatsFilter = cms.EDFilter('MFVTriggerFloatsFilter',
                                      hltht_cut = cms.double(-1),
                                      )
