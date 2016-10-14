import FWCore.ParameterSet.Config as cms

# Cuts for muons and electrons, including relative isolation with
# delta beta corrections. First set (no "signal" or "semilep"/"dilep")
# is for loose cuts (e.g. for vetos), and "semilep"/"dilep" are the
# reference cuts for those channels from TWikiTopRefEventSel. // JMTBAD were those cuts anyway...
# Can/should re-do cuts in ntupler starting from loose selection,
# including impact parameter cuts that aren't included here. We store
# these strings in a process-level PSet so they can be easily gotten
# later from provenance (should also be able to get them from the
# modules' PSets).

iso = '(chargedHadronIso + max(0.,neutralHadronIso) + photonIso - 0.5*puChargedHadronIso)'
muonIso = iso + '/pt'
electronIso = iso + '/et'

electronId = \
    '(isEB && ' \
    'gsfTrack.hitPattern.numberOfHits("MISSING_INNER_HITS") <= 2 && ' \
    'abs(deltaEtaSuperClusterTrackAtVtx) < 0.00926 && ' \
    'abs(deltaPhiSuperClusterTrackAtVtx) < 0.0336 && ' \
    'full5x5_sigmaIetaIeta < 0.0101 && ' \
    'hadronicOverEm < 0.0597 && ' \
    'abs(1/ecalEnergy - eSuperClusterOverP/ecalEnergy) < 0.012 && ' \
    'passConversionVeto) || ' \
    '(isEE && ' \
    'gsfTrack.hitPattern.numberOfHits("MISSING_INNER_HITS") <= 1 && ' \
    'abs(deltaEtaSuperClusterTrackAtVtx) < 0.00724 && ' \
    'abs(deltaPhiSuperClusterTrackAtVtx) < 0.0918 && ' \
    'full5x5_sigmaIetaIeta < 0.0279 && ' \
    'hadronicOverEm < 0.0615 && ' \
    'abs(1/ecalEnergy - eSuperClusterOverP/ecalEnergy) < 0.00999 && ' \
    'passConversionVeto)'

jtupleParams = cms.PSet(
    jetCut = cms.string('pt > 20. && abs(eta) < 2.5 && ' \
                        'numberOfDaughters > 1 && ' \
                        'neutralHadronEnergyFraction < 0.90 && ' \
                        'neutralEmEnergyFraction < 0.90 && ' \
                        'muonEnergyFraction < 0.8 && ' \
                        '(abs(eta) >= 2.4 || (chargedEmEnergyFraction < 0.90 && chargedHadronEnergyFraction > 0. && chargedMultiplicity > 0))'
                        ),

    muonCut      = cms.string('isPFMuon && (isGlobalMuon || isTrackerMuon) && abs(eta) < 2.4'),
    dilepMuonCut = cms.string('isPFMuon && (isGlobalMuon || isTrackerMuon) && abs(eta) < 2.4'),
    semilepMuonCut = cms.string('isPFMuon && isGlobalMuon && ' \
                                'pt > 7. && abs(eta) < 2.4 && ' \
                                'globalTrack.normalizedChi2 < 10. && ' \
                                'track.hitPattern.trackerLayersWithMeasurement > 5 && ' \
                                'globalTrack.hitPattern.numberOfValidMuonHits > 0 && ' \
                                'innerTrack.hitPattern.numberOfValidPixelHits > 0 && ' \
                                'numberOfMatchedStations > 1'
                                ),
    
    electronCut = cms.string(electronId),
    dilepElectronCut = cms.string('1'),
    semilepElectronCut = cms.string('1'),
)
