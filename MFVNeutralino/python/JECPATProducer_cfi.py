import FWCore.ParameterSet.Config as cms

mfvJECPATProducer = cms.EDProducer('mfvJECPATProducer',
                                   jet_src = cms.InputTag('selectedPatJetsPF'),
                                   enable = cms.bool(True),
                                   jes = cms.bool(True), # True for JES and False for JER
                                   up = cms.bool(True),
                                   )
