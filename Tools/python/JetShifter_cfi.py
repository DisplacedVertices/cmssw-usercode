import FWCore.ParameterSet.Config as cms

jmtJetShifter = cms.EDProducer('JMTJetShifter',
                               jets_src = cms.InputTag('selectedPatJets'),
                               enable = cms.bool(True),
                               mult = cms.double(1),
                               jes = cms.bool(True),
                               up = cms.bool(True),
                               )
