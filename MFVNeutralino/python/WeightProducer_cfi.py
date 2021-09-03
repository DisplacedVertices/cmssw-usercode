import FWCore.ParameterSet.Config as cms
from DVCode.Tools.PileupWeights import get_pileup_weights

mfvWeight = cms.EDProducer('MFVWeightProducer',
                           throw_if_no_mcstat = cms.bool(True),
                           mevent_src = cms.InputTag('mfvEvent'),
                           enable = cms.bool(True),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(True),
                           partial_mc_stats_weight = cms.double(1),
                           weight_gen = cms.bool(False),
                           weight_gen_sign_only = cms.bool(True),
                           weight_pileup = cms.bool(True),
                           pileup_weights = cms.vdouble(*get_pileup_weights('default')),
                           weight_npv = cms.bool(False),
                           npv_weights = cms.vdouble(),
                           misc_weight_indices = cms.vint32(),
                           )

def half_mc_by_lumi(process, first=True):
    assert hasattr(process, 'mfvWeight')
    process.load('DVCode.Tools.HalfMCByLumi_cfi')
    process.HalfMCByLumi.first = first
    for p in process.paths.itervalues():
        p.replace(process.mfvWeight, process.HalfMCByLumi * process.mfvWeight)
    process.mfvWeight.partial_mc_stats_weight = 0.5 # generally not different by more than 0.1%

def quarter_mc_by_lumi(process, first=True, second=False, third=False, fourth=False):
    assert hasattr(process, 'mfvWeight')
    process.load('DVCode.Tools.QuarterMCByLumi_cfi')
    process.QuarterMCByLumi.first = first
    process.QuarterMCByLumi.second = second
    process.QuarterMCByLumi.third = third
    process.QuarterMCByLumi.fourth = fourth
    nquarters = [first,second,third,fourth].count(True)
    for p in process.paths.itervalues():
        p.replace(process.mfvWeight, process.QuarterMCByLumi * process.mfvWeight)
    process.mfvWeight.partial_mc_stats_weight = 0.25 * nquarters 
