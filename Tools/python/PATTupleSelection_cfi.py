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
                                    'electronID("mvaTrigV0") > 0. && ' \
                                    '(abs(superCluster.eta) < 1.4442 || abs(superCluster.eta) > 1.5660) && ' \
                                    'passConversionVeto && ' \
                                    '%s < 0.1' % electronIso
                                    ),
    
    dilepElectronCut = cms.string('pt > 20. && abs(eta) < 2.5 && ' \
                                  'electronID("mvaTrigV0") > 0. && ' \
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

def makeLeptonProducers(process, postfix='PF', params=jtupleParams):
    for name in 'semilepMuons dilepMuons semilepElectrons dilepElectrons jtupleMuonSequence jtupleElectronSequence jtupleSemileptonSequence jtupleDileptonSequence countSemileptonicMuons countDileptonicMuons countSemileptonicElectrons countDileptonicElectrons countSemileptons countDileptons'.split()
        name += postfix
        if hasattr(process, name):
            raise ValueError('refusing to clobber already existing module with label %s' % name)
    
    semilepMuons     = cms.EDFilter('PATMuonSelector',     src = cms.InputTag('selectedPatMuons' + postfix),     cut = jtupleParams.semilepMuonCut))
    dilepMuons       = cms.EDFilter('PATMuonSelector',     src = cms.InputTag('selectedPatMuons' + postfix),     cut = jtupleParams.dilepMuonCut))
    semilepElectrons = cms.EDFilter('PATElectronSelector', src = cms.InputTag('selectedPatElectrons' + postfix), cut = jtupleParams.semilepElectronCut))
    dilepElectrons   = cms.EDFilter('PATElectronSelector', src = cms.InputTag('selectedPatElectrons' + postfix), cut = jtupleParams.dilepElectronCut))

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
    process.countDileptons   = countPatLeptons.clone(muonSource = cms.InputTag('dilepMuons'   + postfix), electronSource = cms.InputTag('dilepElectrons'   + postfix), minNumber = cms.uint32(1))
