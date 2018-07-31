import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.Tools.Year import year

mfvWeight = cms.EDProducer('MFVWeightProducer',
                           throw_if_no_mcstat = cms.bool(True),
                           mevent_src = cms.InputTag('mfvEvent'),
                           enable = cms.bool(True),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(True),
                           half_mc_weight = cms.double(1),
                           weight_gen = cms.bool(False),
                           weight_gen_sign_only = cms.bool(False),
                           weight_pileup = cms.bool(True),
                           pileup_weights = cms.vdouble(*pileup_weights[year]),
                           weight_npv = cms.bool(False),
                           npv_weights = cms.vdouble(),
                           )

def half_mc_by_lumi(process, first=True):
    assert hasattr(process, 'mfvWeight')
    process.load('JMTucker.Tools.HalfMCByLumi_cfi')
    process.HalfMCByLumi.first = first
    for p in process.paths.itervalues():
        p.replace(process.mfvWeight, process.HalfMCByLumi * process.mfvWeight)
    process.mfvWeight.half_mc_weight = 2
