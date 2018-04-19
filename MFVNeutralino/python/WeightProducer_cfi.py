import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.Tools.Year import year

mfvWeight = cms.EDProducer('MFVWeightProducer',
                           throw_if_no_mcstat = cms.bool(True),
                           mevent_src = cms.InputTag('mfvEvent'),
                           enable = cms.bool(True),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(True),
                           weight_gen = cms.bool(False),
                           weight_gen_sign_only = cms.bool(False),
                           weight_pileup = cms.bool(True),
                           pileup_weights = cms.vdouble(*pileup_weights[year]),
                           weight_npv = cms.bool(False),
                           npv_weights = cms.vdouble(),
                           )
