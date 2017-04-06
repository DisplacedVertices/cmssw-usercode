import FWCore.ParameterSet.Config as cms

mfvJetFilter = cms.EDFilter('MFVJetFilter',
                            jets_src = cms.InputTag('selectedPatJets'),
                            min_njets = cms.int32(4),
                            min_ht = cms.double(1000),
                            debug = cms.untracked.bool(False),
                            )
