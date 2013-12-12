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
                               'tobtecfakesfilter',
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

def makeLeptonProducers(process, postfix='PF', params=jtupleParams):
    for name in 'semilepMuons dilepMuons semilepElectrons dilepElectrons jtupleMuonSequence jtupleElectronSequence jtupleSemileptonSequence jtupleDileptonSequence countSemileptonicMuons countDileptonicMuons countSemileptonicElectrons countDileptonicElectrons countSemileptons countDileptons'.split():
        name += postfix
        if hasattr(process, name):
            raise ValueError('refusing to clobber already existing module with label %s' % name)
    
    semilepMuons     = cms.EDFilter('PATMuonSelector',     src = cms.InputTag('selectedPatMuons'     + postfix), cut = params.semilepMuonCut)
    dilepMuons       = cms.EDFilter('PATMuonSelector',     src = cms.InputTag('selectedPatMuons'     + postfix), cut = params.dilepMuonCut)
    semilepElectrons = cms.EDFilter('PATElectronSelector', src = cms.InputTag('selectedPatElectrons' + postfix), cut = params.semilepElectronCut)
    dilepElectrons   = cms.EDFilter('PATElectronSelector', src = cms.InputTag('selectedPatElectrons' + postfix), cut = params.dilepElectronCut)

    setattr(process, 'semilepMuons'     + postfix, semilepMuons)    
    setattr(process, 'dilepMuons'       + postfix, dilepMuons)      
    setattr(process, 'semilepElectrons' + postfix, semilepElectrons)
    setattr(process, 'dilepElectrons'   + postfix, dilepElectrons)

    process.jtupleMuonSequence       = cms.Sequence(semilepMuons + dilepMuons)
    process.jtupleElectronSequence   = cms.Sequence(semilepElectrons + dilepElectrons)
    process.jtupleSemileptonSequence = cms.Sequence(semilepMuons + semilepElectrons)
    process.jtupleDileptonSequence   = cms.Sequence(dilepMuons + dilepElectrons)

    process.countSemileptonicMuons     = cms.EDFilter('PATCandViewCountFilter', src = cms.InputTag('semilepMuons'     + postfix), minNumber = cms.uint32(1), maxNumber = cms.uint32(999999))
    process.countSemileptonicElectrons = cms.EDFilter('PATCandViewCountFilter', src = cms.InputTag('semilepElectrons' + postfix), minNumber = cms.uint32(1), maxNumber = cms.uint32(999999))
    process.countDileptonicMuons       = cms.EDFilter('PATCandViewCountFilter', src = cms.InputTag('dilepMuons'       + postfix), minNumber = cms.uint32(2), maxNumber = cms.uint32(999999))
    process.countDileptonicElectrons   = cms.EDFilter('PATCandViewCountFilter', src = cms.InputTag('dilepElectrons'   + postfix), minNumber = cms.uint32(2), maxNumber = cms.uint32(999999))

    from PhysicsTools.PatAlgos.selectionLayer1.leptonCountFilter_cfi import countPatLeptons
    process.countSemileptons = countPatLeptons.clone(muonSource = cms.InputTag('semilepMuons' + postfix), electronSource = cms.InputTag('semilepElectrons' + postfix), minNumber = cms.uint32(1))
    process.countDileptons   = countPatLeptons.clone(muonSource = cms.InputTag('dilepMuons'   + postfix), electronSource = cms.InputTag('dilepElectrons'   + postfix), minNumber = cms.uint32(2))
