import FWCore.ParameterSet.Config as cms

mfvSkimmedTracks = cms.EDProducer('MFVSkimmedTracks',
                                  apply_sigmadxybs = cms.bool(False),
                                  )
