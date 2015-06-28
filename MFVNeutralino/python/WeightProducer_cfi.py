import FWCore.ParameterSet.Config as cms

mfvWeight = cms.EDProducer('MFVWeightProducer',
                           mevent_src = cms.InputTag('mfvEvent'),
                           enable = cms.bool(False),
                           prints = cms.untracked.bool(False),
                           weight_pileup = cms.bool(True),
                           pileup_weights = cms.vdouble(),
                           )

