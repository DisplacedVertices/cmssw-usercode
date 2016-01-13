import FWCore.ParameterSet.Config as cms

mfvWeight = cms.EDProducer('MFVWeightProducer',
                           mevent_src = cms.InputTag('mfvEvent'),
                           enable = cms.bool(False),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(True),
                           weight_gen = cms.bool(True),
                           weight_pileup = cms.bool(False),
                           pileup_weights = cms.vdouble(),
                           )
