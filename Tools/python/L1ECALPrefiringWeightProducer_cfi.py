import FWCore.ParameterSet.Config as cms

prefiringweight = cms.EDProducer("L1ECALPrefiringWeightProducer",
                                 ThePhotons = cms.InputTag("slimmedPhotons"),
                                 TheJets = cms.InputTag("slimmedJets"),
                                 L1Maps = cms.string("L1PrefiringMaps_new.root"),
                                 DataEra = cms.string("2017BtoF"),
                                 UseJetEMPt = cms.bool(True),
                                 PrefiringRateSystematicUncty = cms.double(0.2)
                                 )
