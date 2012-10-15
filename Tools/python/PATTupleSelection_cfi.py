import FWCore.ParameterSet.Config as cms

# Cuts for muons and electrons, including relative isolation with
# delta beta corrections. First set (no "signal" or "semilep"/"dilep")
# is for loose cuts (e.g. for vetos), and "semilep"/"dilep" are the
# reference cuts for those channels from TWikiTopRefEventSel.
# Can/should re-do cuts in ntupler starting from loose selection,
# including impact parameter cuts that aren't included here. We store
# these strings in a process-level PSet so they can be easily gotten
# later from provenance (should also be able to get them from the
# modules' PSets).

muonIso = '(chargedHadronIso + neutralHadronIso + photonIso - 0.5*puChargedHadronIso)/pt'
electronIso = '(chargedHadronIso + max(0.,neutralHadronIso) + photonIso - 0.5*puChargedHadronIso)/et'

jtupleParams = cms.PSet(
    jetCut = cms.string('pt > 20. && abs(eta) < 2.5 && ' \
                        'numberOfDaughters > 1 && ' \
                        'neutralHadronEnergyFraction < 0.99 && ' \
                        'neutralEmEnergyFraction < 0.99 && ' \
                        '(abs(eta) >= 2.4 || (chargedEmEnergyFraction < 0.99 && chargedHadronEnergyFraction > 0. && chargedMultiplicity > 0))'
                        ),

    muonCut = cms.string('isPFMuon && (isGlobalMuon || isTrackerMuon) && ' \
                         'pt > 10. && abs(eta) < 2.5 && ' \
                         '%s < 0.2' % muonIso
                         ),

    semilepMuonCut = cms.string('isPFMuon && isGlobalMuon && ' \
                                'pt > 26. && abs(eta) < 2.1 && ' \
                                'globalTrack.normalizedChi2 < 10. && ' \
                                'track.hitPattern.trackerLayersWithMeasurement > 5 && ' \
                                'globalTrack.hitPattern.numberOfValidMuonHits > 0 && ' \
                                'innerTrack.hitPattern.numberOfValidPixelHits > 0 && ' \
                                'numberOfMatchedStations > 1 && ' \
                                '%s < 0.12' % muonIso
                                ),

    dilepMuonCut = cms.string('isPFMuon && (isGlobalMuon || isTrackerMuon) && ' \
                              'pt > 20. && abs(eta) < 2.4 && ' \
                              '%s < 0.2' % muonIso
                              ),
    
    electronCut = cms.string('pt > 20. && abs(eta) < 2.5 && ' \
                             'electronID("mvaTrigV0") > 0. && ' \
                             '%s < 0.2' % electronIso
                             ),
    
    semilepElectronCut = cms.string('pt > 30. && abs(eta) < 2.5 && ' \
                                    'abs(superCluster.eta) < 1.4442 && abs(superCluster.eta) > 1.5660 && ' \
                                    'passConversionVeto && ' \
                                    '%s < 0.1' % electronIso
                                    ),
    
    dilepElectronCut = cms.string('pt > 20. && abs(eta) < 2.5 && ' \
                                  'passConversionVeto && ' \
                                  '%s < 0.15' % electronIso
                                  ),
    
    eventFilters = cms.vstring('hltPhysicsDeclared',
                               'FilterOutScraping',
                               'goodOfflinePrimaryVertices',
                               'HBHENoiseFilter',
                               'CSCTightHaloFilter',
                               'hcalLaserEventFilter',
                               'EcalDeadCellTriggerPrimitiveFilter',
                               'trackingFailureFilter',
                               'eeBadScFilter'),
    )
