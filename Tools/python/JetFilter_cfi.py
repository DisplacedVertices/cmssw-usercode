import FWCore.ParameterSet.Config as cms

jmtJetFilter = cms.EDFilter('JMTJetFilter',
                            jets_src = cms.InputTag('selectedPatJets'),
                            min_njets = cms.int32(4),
                            min_pt_for_ht = cms.double(40),
                            max_pt_for_ht = cms.double(1e9),
                            min_ht = cms.double(1000),
                            debug = cms.untracked.bool(False),
                            )
