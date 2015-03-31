prod_template = '''
    process.%(prodname)s = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( %(jetpt)i ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( %(jetetaf).1f ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( %(njet)i ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )
'''

filt_template = '''
    process.%(filtname)s = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( '%(prodname)s' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( '%(prodname)s' ),
        minHt = cms.vdouble( %(ht)i )
    )
'''

path_template = '    process.%(pathname)s = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.%(prodname)s + process.%(filtname)s + process.HLTEndSequence )'

paths = []

print 'import FWCore.ParameterSet.Config as cms'
print '\ndef add(process):'

for ht in xrange(250, 801, 50):
    for njet in xrange(4,11,2):
        for jetpt in xrange(40, 101, 20):
            for jeteta in (30,26):
                jetetaf = jeteta/10.
                d = locals()
                prodname = 'hltPFHT%(njet)iJet%(jetpt)iPt%(jeteta)iEta' % d
                filtname = 'hltPF%(njet)iJetHT%(ht)i%(jetpt)iPt%(jeteta)iEta' % d
                pathname = 'HLT_PFHT%(ht)i_%(njet)iJet_%(jetpt)iPt%(jeteta)iEta_v1' % d

                print prod_template % d
                print filt_template % d
                paths.append((pathname, path_template % d))

for pathname, path_template in paths:
    print path_template

print '\n    junk = (',
for pathname, path_template in paths:
    print 'process.%s,' % pathname,
print ')'
print '    return junk'

print '# num paths: %i' % len(paths)
