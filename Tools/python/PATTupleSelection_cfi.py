import FWCore.ParameterSet.Config as cms

# Cuts for muons and electrons, including relative isolation with
# delta beta corrections. First set (no "signal" or "semilep"/"dilep")
# is for loose cuts (e.g. for vetos), and "semilep"/"dilep" are the
# reference cuts for those channels from TWikiTopRefEventSel. // JMTBAD were those cuts
# Can/should re-do cuts in ntupler starting from loose selection,
# including impact parameter cuts that aren't included here. We store
# these strings in a process-level PSet so they can be easily gotten
# later from provenance (should also be able to get them from the
# modules' PSets).

muonIso = '(chargedHadronIso + neutralHadronIso + photonIso - 0.5*puChargedHadronIso)/pt'
electronIso = '(chargedHadronIso + max(0.,neutralHadronIso) + photonIso - 0.5*puChargedHadronIso)/et'

# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentification#Non_triggering_MVA
electronMVA = ' '.join('''
(
 (pt > 7 && pt < 10 &&
  ((                                  abs(superCluster.eta) < 0.8   && electronID("mvaNonTrigV0") > 0.47 ) ||
   (abs(superCluster.eta) >= 0.8   && abs(superCluster.eta) < 1.479 && electronID("mvaNonTrigV0") > 0.004) ||
   (abs(superCluster.eta) >= 1.479 && abs(superCluster.eta) < 2.5   && electronID("mvaNonTrigV0") > 0.295))
 ) ||
 (pt >= 10 &&
  ((                                  abs(superCluster.eta) < 0.8   && electronID("mvaNonTrigV0") > -0.34) ||
   (abs(superCluster.eta) >= 0.8   && abs(superCluster.eta) < 1.479 && electronID("mvaNonTrigV0") > -0.65) ||
   (abs(superCluster.eta) >= 1.479 && abs(superCluster.eta) < 2.5   && electronID("mvaNonTrigV0") >  0.6 ))
 )
)
'''.replace('\n','').split()) # ignore the weirdo behind the curtain

jtupleParams = cms.PSet(
    jetCut = cms.string('pt > 20. && abs(eta) < 2.5 && ' \
                        'numberOfDaughters > 1 && ' \
                        'neutralHadronEnergyFraction < 0.99 && ' \
                        'neutralEmEnergyFraction < 0.99 && ' \
                        '(abs(eta) >= 2.4 || (chargedEmEnergyFraction < 0.99 && chargedHadronEnergyFraction > 0. && chargedMultiplicity > 0))'
                        ),

    muonCut = cms.string('isPFMuon && (isGlobalMuon || isTrackerMuon) && ' \
                         'pt > 7. && abs(eta) < 2.4 && ' \
                         '%s < 0.2' % muonIso
                         ),

    semilepMuonCut = cms.string('isPFMuon && isGlobalMuon && ' \
                                'pt > 7. && abs(eta) < 2.4 && ' \
                                'globalTrack.normalizedChi2 < 10. && ' \
                                'track.hitPattern.trackerLayersWithMeasurement > 5 && ' \
                                'globalTrack.hitPattern.numberOfValidMuonHits > 0 && ' \
                                'innerTrack.hitPattern.numberOfValidPixelHits > 0 && ' \
                                'numberOfMatchedStations > 1 && ' \
                                '%s < 0.12' % muonIso
                                ),

    dilepMuonCut = cms.string('isPFMuon && (isGlobalMuon || isTrackerMuon) && ' \
                              'pt > 7. && abs(eta) < 2.4 && ' \
                              '%s < 0.2' % muonIso
                              ),

    electronCut = cms.string('pt > 7. && abs(eta) < 2.5 && ' \
                             '%s && ' \
                             '%s < 0.2' % (electronMVA, electronIso)
                             ),
    
    semilepElectronCut = cms.string('pt > 7. && abs(eta) < 2.5 && ' \
                                    '%s && ' \
                                    '(abs(superCluster.eta) < 1.4442 || abs(superCluster.eta) > 1.5660) && ' \
                                    '%s < 0.1' % (electronMVA, electronIso)
                                    ),
    
    dilepElectronCut = cms.string('pt > 7. && abs(eta) < 2.5 && ' \
                                  '%s && ' \
                                  '%s < 0.15' % (electronMVA, electronIso)
                                  ),
    
    eventFilters = cms.vstring('hltPhysicsDeclared',
                               'FilterOutScraping',
                               'goodOfflinePrimaryVertices',
                               'HBHENoiseFilter',
                               'CSCTightHaloFilter',
                               'hcalLaserEventFilter',
                               'EcalDeadCellTriggerPrimitiveFilter',
                               'trackingFailureFilter',
                               'eeBadScFilter',
                               'ecalLaserCorrFilter',
                               '~tobtecfakesfilter',
                               '~logErrorTooManyClusters',
                               '~logErrorTooManySeeds',
                               '~logErrorTooManySeedsDefault',
                               '~logErrorTooManySeedsMainIterations',
                               '~logErrorTooManyTripletsPairs',
                               '~logErrorTooManyTripletsPairsMainIterations',
                               '~manystripclus53X',
                               '~toomanystripclus53X',
                               ),
    )
