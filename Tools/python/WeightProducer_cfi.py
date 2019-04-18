import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PileupWeights import get_pileup_weights

jmtWeight = cms.EDProducer('JMTWeightProducer',
                           enable = cms.bool(True),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(True),
                           gen_info_src = cms.InputTag('generator'),
                           pileup_info_src = cms.InputTag('addPileupInfo'),
                           primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                           weight_gen = cms.bool(False),
                           weight_gen_sign_only = cms.bool(True),
                           weight_pileup = cms.bool(True),
                           pileup_weights = cms.vdouble(*get_pileup_weights('default')),
                           weight_npv = cms.bool(False),
                           npv_weights = cms.vdouble(),
                           weight_misc = cms.bool(False),
                           misc_srcs = cms.VInputTag(),
                           )

jmtWeightMiniAOD = jmtWeight.clone(
    pileup_info_src = 'slimmedAddPileupInfo',
    primary_vertex_src = 'offlineSlimmedPrimaryVertices'
    )
