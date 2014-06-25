import FWCore.ParameterSet.Config as cms

dummyBeamSpot = cms.EDProducer('dummyBeamSpotProducer',                           
                                X0 = cms.double(1),
                                Y0 = cms.double(1),
                                Z0 = cms.double(1),
                                covariance = cms.vdouble((1,1,1)),
                                SigmaZ = cms.double(1),
                                dxdz = cms.double(1),
                                dydz = cms.double(1),
                                BeamWidthX = cms.double(1),
                                BeamWidthY = cms.double(1),
                                EmittanceX = cms.double(1),
                                EmittanceY = cms.double(1),
                                BetaStar = cms.double(1),
                             )
