import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import patJetCorrFactors
from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import updatedPatJets

jetCorrectionFactors = patJetCorrFactors.clone(
    src = 'patJets',
    levels = cms.vstring('L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'),
    )

jetCorrectionFactorsMiniAOD = jetCorrectionFactors.clone(
    src = 'slimmedJets',
    primaryVertices = 'offlineSlimmedPrimaryVertices',
    )

updatedJets = updatedPatJets.clone(
    jetSource = 'patJets',
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag('jetCorrectionFactors'))
    )

updatedJetsMiniAOD = updatedJets.clone(
    jetSource = 'slimmedJets',
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag('jetCorrectionFactorsMiniAOD'))
    )

updatedJetsSeq        = cms.Sequence(jetCorrectionFactors        * updatedJets)
updatedJetsSeqMiniAOD = cms.Sequence(jetCorrectionFactorsMiniAOD * updatedJetsMiniAOD)
