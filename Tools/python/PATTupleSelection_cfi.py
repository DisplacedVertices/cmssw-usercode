import FWCore.ParameterSet.Config as cms

# https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Tight_Muon
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Working_points_for_92X_and_later
# impact parameter cuts not included on leptons, and conversion veto not included on electrons
# JMTBAD electron H/E cut uses fixed rho number, should do it right in event producer

jet_cuts = (
    'abs(eta) < 2.7',
    'numberOfDaughters > 1',
    'neutralHadronEnergyFraction < 0.90',
    'neutralEmEnergyFraction < 0.90',
    'muonEnergyFraction < 0.8',
    '(abs(eta) >= 2.4 || (chargedEmEnergyFraction < 0.80 && chargedHadronEnergyFraction > 0. && chargedMultiplicity > 0))',
    )

muon_cuts = (
    'isPFMuon',
    'isGlobalMuon',
    'isGlobalMuon && globalTrack.normalizedChi2 < 10.',
    '(isGlobalMuon || isTrackerMuon) && innerTrack.hitPattern.trackerLayersWithMeasurement > 5',
    'isGlobalMuon && globalTrack.hitPattern.numberOfValidMuonHits > 0',
    '(isGlobalMuon || isTrackerMuon) && innerTrack.hitPattern.numberOfValidPixelHits > 0',
    'numberOfMatchedStations > 1',
    )

electron_rho95 = 43. # this is the 95% point for double_fixedGridRhoFastjetCentral__RECO.obj from one file of QCD HT2000, a wjets file wants 37 but that rho distribution has a peak at 0 (?)

electron_EB_cuts = (
    'full5x5_sigmaIetaIeta < 0.0128',
    'abs(deltaEtaSuperClusterTrackAtVtx - superCluster.eta + superCluster.seed.eta) < 0.00523',
    'abs(deltaPhiSuperClusterTrackAtVtx) < 0.159',
    'hadronicOverEm < 0.05 + 1.12/superCluster.energy + 0.0368*%f/superCluster.energy' % electron_rho95,
    'abs(1/ecalEnergy - eSuperClusterOverP/ecalEnergy) < 0.193',
    'gsfTrack.hitPattern.numberOfAllHits("MISSING_INNER_HITS") <= 2',
    )

electron_EE_cuts = (
    'full5x5_sigmaIetaIeta < 0.0445',
    'abs(deltaEtaSuperClusterTrackAtVtx - superCluster.eta + superCluster.seed.eta) < 0.00984',
    'abs(deltaPhiSuperClusterTrackAtVtx) < 0.157',
    'hadronicOverEm < 0.05 + 0.5/superCluster.energy + 0.201*%f/superCluster.energy' % electron_rho95,
    'abs(1/ecalEnergy - eSuperClusterOverP/ecalEnergy) < 0.0962',
    'gsfTrack.hitPattern.numberOfAllHits("MISSING_INNER_HITS") <= 3'
    )

jtupleParams = cms.PSet(
    jetCuts = cms.vstring(*jet_cuts),
    jetCut = cms.string(' && '.join(jet_cuts)),
    muonCuts = cms.vstring(*muon_cuts),
    muonCut = cms.string(' && '.join(muon_cuts)),

    electronEBCuts = cms.vstring(*electron_EB_cuts),
    electronEECuts = cms.vstring(*electron_EE_cuts),
    electronCut = cms.string('(isEB && %s) || (isEE && %s)' % (' && '.join(electron_EB_cuts), ' && '.join(electron_EE_cuts))),
    )
