# Level 1 ECAL prefiring recipe for 2016 & 2017 MC samples:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1ECALPrefiringWeightRecipe

import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatUtils.l1ECALPrefiringWeightProducer_cfi import l1ECALPrefiringWeightProducer
prefiringweight= l1ECALPrefiringWeightProducer.clone(
    TheJets = cms.InputTag("updatedJetsMiniAOD"), #this should be the slimmedJets collection with up to date JECs !
    L1Maps = cms.string("L1PrefiringMaps.root"),
    DataEra = cms.string('UL2017BtoF'),
    UseJetEMPt = cms.bool(False),
    PrefiringRateSystematicUncty = cms.double(0.2),
    SkipWarnings = False
    )

