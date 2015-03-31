import FWCore.ParameterSet.Config as cms

def add(process):

    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT25040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT25040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT25060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT25060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT25080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT25080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT250100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT250100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT25040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT25040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT25060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT25060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT25080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT25080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT250100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT250100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT25040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT25040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT25060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT25060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT25080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT25080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT250100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT250100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT25040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT25040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT25060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT25060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT25080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT25080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT250100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT250100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 250 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT30040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT30040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT30060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT30060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT30080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT30080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT300100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT300100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT30040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT30040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT30060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT30060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT30080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT30080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT300100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT300100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT30040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT30040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT30060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT30060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT30080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT30080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT300100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT300100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT30040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT30040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT30060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT30060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT30080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT30080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT300100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT300100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 300 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT35040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT35040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT35060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT35060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT35080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT35080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT350100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT350100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT35040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT35040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT35060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT35060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT35080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT35080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT350100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT350100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT35040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT35040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT35060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT35060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT35080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT35080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT350100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT350100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT35040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT35040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT35060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT35060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT35080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT35080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT350100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT350100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 350 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT40040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT40040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT40060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT40060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT40080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT40080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT400100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT400100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT40040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT40040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT40060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT40060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT40080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT40080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT400100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT400100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT40040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT40040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT40060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT40060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT40080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT40080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT400100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT400100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT40040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT40040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT40060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT40060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT40080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT40080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT400100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT400100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 400 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT45040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT45040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT45060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT45060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT45080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT45080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT450100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT450100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT45040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT45040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT45060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT45060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT45080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT45080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT450100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT450100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT45040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT45040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT45060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT45060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT45080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT45080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT450100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT450100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT45040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT45040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT45060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT45060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT45080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT45080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT450100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT450100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 450 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT50040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT50040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT50060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT50060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT50080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT50080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT500100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT500100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT50040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT50040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT50060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT50060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT50080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT50080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT500100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT500100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT50040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT50040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT50060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT50060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT50080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT50080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT500100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT500100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT50040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT50040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT50060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT50060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT50080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT50080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT500100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT500100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 500 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT55040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT55040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT55060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT55060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT55080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT55080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT550100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT550100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT55040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT55040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT55060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT55060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT55080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT55080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT550100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT550100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT55040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT55040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT55060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT55060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT55080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT55080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT550100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT550100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT55040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT55040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT55060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT55060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT55080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT55080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT550100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT550100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 550 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT60040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT60040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT60060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT60060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT60080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT60080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT600100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT600100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT60040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT60040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT60060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT60060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT60080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT60080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT600100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT600100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT60040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT60040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT60060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT60060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT60080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT60080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT600100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT600100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT60040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT60040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT60060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT60060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT60080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT60080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT600100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT600100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 600 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT65040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT65040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT65060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT65060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT65080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT65080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT650100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT650100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT65040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT65040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT65060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT65060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT65080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT65080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT650100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT650100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT65040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT65040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT65060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT65060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT65080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT65080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT650100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT650100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT65040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT65040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT65060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT65060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT65080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT65080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT650100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT650100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 650 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT70040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT70040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT70060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT70060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT70080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT70080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT700100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT700100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT70040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT70040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT70060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT70060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT70080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT70080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT700100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT700100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT70040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT70040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT70060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT70060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT70080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT70080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT700100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT700100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT70040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT70040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT70060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT70060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT70080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT70080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT700100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT700100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 700 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT75040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT75040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT75060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT75060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT75080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT75080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT750100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT750100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT75040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT75040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT75060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT75060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT75080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT75080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT750100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT750100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT75040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT75040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT75060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT75060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT75080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT75080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT750100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT750100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT75040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT75040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT75060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT75060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT75080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT75080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT750100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT750100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 750 )
    )


    process.hltPFHT4Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT80040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT4Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT80040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet40Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT4Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT80060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT4Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT80060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet60Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT4Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT80080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT4Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT80080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet80Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT4Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT800100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT4Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 4 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF4JetHT800100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT4Jet100Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT6Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT80040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT6Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT80040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet40Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT6Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT80060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT6Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT80060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet60Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT6Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT80080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT6Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT80080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet80Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT6Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT800100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT6Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 6 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF6JetHT800100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT6Jet100Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT8Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT80040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT8Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT80040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet40Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT8Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT80060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT8Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT80060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet60Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT8Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT80080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT8Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT80080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet80Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT8Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT800100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT8Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 8 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF8JetHT800100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT8Jet100Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT10Jet40Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT80040Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT10Jet40Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 40 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT80040Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet40Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT10Jet60Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT80060Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT10Jet60Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 60 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT80060Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet60Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT10Jet80Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT80080Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT10Jet80Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 80 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT80080Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet80Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT10Jet100Pt30Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 3.0 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT800100Pt30Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt30Eta' ),
        minHt = cms.vdouble( 800 )
    )


    process.hltPFHT10Jet100Pt26Eta = cms.EDProducer( "HLTHtMhtProducer",
        usePt = cms.bool( True ),
        minPtJetHt = cms.double( 100 ),
        maxEtaJetMht = cms.double( 999.0 ),
        minNJetMht = cms.int32( 0 ),
        jetsLabel = cms.InputTag( "hltAK4PFJetsCorrected" ),
        maxEtaJetHt = cms.double( 2.6 ),
        minPtJetMht = cms.double( 0.0 ),
        minNJetHt = cms.int32( 10 ),
        pfCandidatesLabel = cms.InputTag( "hltParticleFlow" ),
        excludePFMuons = cms.bool( False )
    )


    process.hltPF10JetHT800100Pt26Eta = cms.EDFilter( "HLTHtMhtFilter",
        saveTags = cms.bool( True ),
        mhtLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        meffSlope = cms.vdouble( 1.0 ),
        minMeff = cms.vdouble( 0.0 ),
        minMht = cms.vdouble( 0.0 ),
        htLabels = cms.VInputTag( 'hltPFHT10Jet100Pt26Eta' ),
        minHt = cms.vdouble( 800 )
    )

    process.HLT_PFHT250_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT25040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT25040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT25060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT25060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT25080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT25080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT250100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT250100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT25040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT25040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT25060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT25060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT25080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT25080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT250100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT250100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT25040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT25040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT25060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT25060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT25080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT25080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT250100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT250100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT25040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT25040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT25060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT25060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT25080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT25080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT250_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT250100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT250_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT250100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT30040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT30040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT30060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT30060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT30080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT30080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT300100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT300100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT30040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT30040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT30060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT30060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT30080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT30080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT300100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT300100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT30040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT30040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT30060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT30060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT30080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT30080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT300100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT300100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT30040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT30040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT30060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT30060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT30080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT30080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT300_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT300100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT300_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT300100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT35040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT35040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT35060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT35060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT35080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT35080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT350100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT350100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT35040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT35040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT35060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT35060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT35080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT35080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT350100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT350100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT35040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT35040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT35060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT35060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT35080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT35080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT350100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT350100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT35040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT35040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT35060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT35060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT35080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT35080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT350_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT350100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT350_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT350100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT40040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT40040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT40060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT40060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT40080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT40080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT400100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT400100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT40040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT40040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT40060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT40060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT40080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT40080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT400100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT400100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT40040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT40040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT40060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT40060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT40080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT40080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT400100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT400100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT40040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT40040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT40060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT40060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT40080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT40080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT400_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT400100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT400_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT400100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT45040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT45040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT45060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT45060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT45080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT45080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT450100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT450100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT45040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT45040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT45060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT45060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT45080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT45080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT450100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT450100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT45040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT45040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT45060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT45060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT45080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT45080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT450100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT450100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT45040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT45040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT45060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT45060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT45080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT45080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT450_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT450100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT450_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT450100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT50040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT50040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT50060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT50060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT50080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT50080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT500100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT500100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT50040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT50040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT50060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT50060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT50080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT50080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT500100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT500100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT50040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT50040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT50060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT50060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT50080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT50080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT500100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT500100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT50040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT50040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT50060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT50060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT50080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT50080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT500_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT500100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT500_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT500100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT55040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT55040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT55060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT55060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT55080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT55080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT550100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT550100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT55040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT55040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT55060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT55060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT55080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT55080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT550100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT550100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT55040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT55040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT55060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT55060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT55080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT55080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT550100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT550100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT55040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT55040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT55060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT55060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT55080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT55080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT550_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT550100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT550_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT550100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT60040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT60040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT60060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT60060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT60080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT60080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT600100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT600100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT60040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT60040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT60060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT60060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT60080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT60080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT600100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT600100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT60040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT60040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT60060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT60060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT60080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT60080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT600100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT600100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT60040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT60040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT60060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT60060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT60080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT60080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT600_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT600100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT600_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT600100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT65040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT65040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT65060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT65060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT65080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT65080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT650100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT650100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT65040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT65040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT65060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT65060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT65080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT65080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT650100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT650100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT65040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT65040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT65060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT65060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT65080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT65080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT650100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT650100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT65040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT65040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT65060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT65060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT65080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT65080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT650_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT650100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT650_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT650100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT70040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT70040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT70060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT70060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT70080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT70080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT700100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT700100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT70040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT70040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT70060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT70060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT70080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT70080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT700100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT700100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT70040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT70040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT70060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT70060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT70080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT70080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT700100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT700100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT70040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT70040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT70060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT70060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT70080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT70080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT700_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT700100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT700_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT700100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT75040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT75040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT75060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT75060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT75080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT75080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT750100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT750100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT75040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT75040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT75060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT75060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT75080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT75080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT750100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT750100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT75040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT75040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT75060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT75060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT75080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT75080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT750100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT750100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT75040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT75040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT75060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT75060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT75080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT75080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT750_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT750100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT750_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT750100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_4Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt30Eta + process.hltPF4JetHT80040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_4Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet40Pt26Eta + process.hltPF4JetHT80040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_4Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt30Eta + process.hltPF4JetHT80060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_4Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet60Pt26Eta + process.hltPF4JetHT80060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_4Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt30Eta + process.hltPF4JetHT80080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_4Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet80Pt26Eta + process.hltPF4JetHT80080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_4Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt30Eta + process.hltPF4JetHT800100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_4Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT4Jet100Pt26Eta + process.hltPF4JetHT800100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_6Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt30Eta + process.hltPF6JetHT80040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_6Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet40Pt26Eta + process.hltPF6JetHT80040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_6Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt30Eta + process.hltPF6JetHT80060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_6Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet60Pt26Eta + process.hltPF6JetHT80060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_6Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt30Eta + process.hltPF6JetHT80080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_6Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet80Pt26Eta + process.hltPF6JetHT80080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_6Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt30Eta + process.hltPF6JetHT800100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_6Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT6Jet100Pt26Eta + process.hltPF6JetHT800100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_8Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt30Eta + process.hltPF8JetHT80040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_8Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet40Pt26Eta + process.hltPF8JetHT80040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_8Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt30Eta + process.hltPF8JetHT80060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_8Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet60Pt26Eta + process.hltPF8JetHT80060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_8Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt30Eta + process.hltPF8JetHT80080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_8Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet80Pt26Eta + process.hltPF8JetHT80080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_8Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt30Eta + process.hltPF8JetHT800100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_8Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT8Jet100Pt26Eta + process.hltPF8JetHT800100Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_10Jet_40Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt30Eta + process.hltPF10JetHT80040Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_10Jet_40Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet40Pt26Eta + process.hltPF10JetHT80040Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_10Jet_60Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt30Eta + process.hltPF10JetHT80060Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_10Jet_60Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet60Pt26Eta + process.hltPF10JetHT80060Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_10Jet_80Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt30Eta + process.hltPF10JetHT80080Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_10Jet_80Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet80Pt26Eta + process.hltPF10JetHT80080Pt26Eta + process.HLTEndSequence )
    process.HLT_PFHT800_10Jet_100Pt30Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt30Eta + process.hltPF10JetHT800100Pt30Eta + process.HLTEndSequence )
    process.HLT_PFHT800_10Jet_100Pt26Eta_v1 = cms.Path( process.HLTBeginSequence + process.hltL1sL1HTT150ORHTT175 + process.HLTAK4PFJetsSequence + process.hltPFHT10Jet100Pt26Eta + process.hltPF10JetHT800100Pt26Eta + process.HLTEndSequence )

    junk = ( process.HLT_PFHT250_4Jet_40Pt30Eta_v1, process.HLT_PFHT250_4Jet_40Pt26Eta_v1, process.HLT_PFHT250_4Jet_60Pt30Eta_v1, process.HLT_PFHT250_4Jet_60Pt26Eta_v1, process.HLT_PFHT250_4Jet_80Pt30Eta_v1, process.HLT_PFHT250_4Jet_80Pt26Eta_v1, process.HLT_PFHT250_4Jet_100Pt30Eta_v1, process.HLT_PFHT250_4Jet_100Pt26Eta_v1, process.HLT_PFHT250_6Jet_40Pt30Eta_v1, process.HLT_PFHT250_6Jet_40Pt26Eta_v1, process.HLT_PFHT250_6Jet_60Pt30Eta_v1, process.HLT_PFHT250_6Jet_60Pt26Eta_v1, process.HLT_PFHT250_6Jet_80Pt30Eta_v1, process.HLT_PFHT250_6Jet_80Pt26Eta_v1, process.HLT_PFHT250_6Jet_100Pt30Eta_v1, process.HLT_PFHT250_6Jet_100Pt26Eta_v1, process.HLT_PFHT250_8Jet_40Pt30Eta_v1, process.HLT_PFHT250_8Jet_40Pt26Eta_v1, process.HLT_PFHT250_8Jet_60Pt30Eta_v1, process.HLT_PFHT250_8Jet_60Pt26Eta_v1, process.HLT_PFHT250_8Jet_80Pt30Eta_v1, process.HLT_PFHT250_8Jet_80Pt26Eta_v1, process.HLT_PFHT250_8Jet_100Pt30Eta_v1, process.HLT_PFHT250_8Jet_100Pt26Eta_v1, process.HLT_PFHT250_10Jet_40Pt30Eta_v1, process.HLT_PFHT250_10Jet_40Pt26Eta_v1, process.HLT_PFHT250_10Jet_60Pt30Eta_v1, process.HLT_PFHT250_10Jet_60Pt26Eta_v1, process.HLT_PFHT250_10Jet_80Pt30Eta_v1, process.HLT_PFHT250_10Jet_80Pt26Eta_v1, process.HLT_PFHT250_10Jet_100Pt30Eta_v1, process.HLT_PFHT250_10Jet_100Pt26Eta_v1, process.HLT_PFHT300_4Jet_40Pt30Eta_v1, process.HLT_PFHT300_4Jet_40Pt26Eta_v1, process.HLT_PFHT300_4Jet_60Pt30Eta_v1, process.HLT_PFHT300_4Jet_60Pt26Eta_v1, process.HLT_PFHT300_4Jet_80Pt30Eta_v1, process.HLT_PFHT300_4Jet_80Pt26Eta_v1, process.HLT_PFHT300_4Jet_100Pt30Eta_v1, process.HLT_PFHT300_4Jet_100Pt26Eta_v1, process.HLT_PFHT300_6Jet_40Pt30Eta_v1, process.HLT_PFHT300_6Jet_40Pt26Eta_v1, process.HLT_PFHT300_6Jet_60Pt30Eta_v1, process.HLT_PFHT300_6Jet_60Pt26Eta_v1, process.HLT_PFHT300_6Jet_80Pt30Eta_v1, process.HLT_PFHT300_6Jet_80Pt26Eta_v1, process.HLT_PFHT300_6Jet_100Pt30Eta_v1, process.HLT_PFHT300_6Jet_100Pt26Eta_v1, process.HLT_PFHT300_8Jet_40Pt30Eta_v1, process.HLT_PFHT300_8Jet_40Pt26Eta_v1, process.HLT_PFHT300_8Jet_60Pt30Eta_v1, process.HLT_PFHT300_8Jet_60Pt26Eta_v1, process.HLT_PFHT300_8Jet_80Pt30Eta_v1, process.HLT_PFHT300_8Jet_80Pt26Eta_v1, process.HLT_PFHT300_8Jet_100Pt30Eta_v1, process.HLT_PFHT300_8Jet_100Pt26Eta_v1, process.HLT_PFHT300_10Jet_40Pt30Eta_v1, process.HLT_PFHT300_10Jet_40Pt26Eta_v1, process.HLT_PFHT300_10Jet_60Pt30Eta_v1, process.HLT_PFHT300_10Jet_60Pt26Eta_v1, process.HLT_PFHT300_10Jet_80Pt30Eta_v1, process.HLT_PFHT300_10Jet_80Pt26Eta_v1, process.HLT_PFHT300_10Jet_100Pt30Eta_v1, process.HLT_PFHT300_10Jet_100Pt26Eta_v1, process.HLT_PFHT350_4Jet_40Pt30Eta_v1, process.HLT_PFHT350_4Jet_40Pt26Eta_v1, process.HLT_PFHT350_4Jet_60Pt30Eta_v1, process.HLT_PFHT350_4Jet_60Pt26Eta_v1, process.HLT_PFHT350_4Jet_80Pt30Eta_v1, process.HLT_PFHT350_4Jet_80Pt26Eta_v1, process.HLT_PFHT350_4Jet_100Pt30Eta_v1, process.HLT_PFHT350_4Jet_100Pt26Eta_v1, process.HLT_PFHT350_6Jet_40Pt30Eta_v1, process.HLT_PFHT350_6Jet_40Pt26Eta_v1, process.HLT_PFHT350_6Jet_60Pt30Eta_v1, process.HLT_PFHT350_6Jet_60Pt26Eta_v1, process.HLT_PFHT350_6Jet_80Pt30Eta_v1, process.HLT_PFHT350_6Jet_80Pt26Eta_v1, process.HLT_PFHT350_6Jet_100Pt30Eta_v1, process.HLT_PFHT350_6Jet_100Pt26Eta_v1, process.HLT_PFHT350_8Jet_40Pt30Eta_v1, process.HLT_PFHT350_8Jet_40Pt26Eta_v1, process.HLT_PFHT350_8Jet_60Pt30Eta_v1, process.HLT_PFHT350_8Jet_60Pt26Eta_v1, process.HLT_PFHT350_8Jet_80Pt30Eta_v1, process.HLT_PFHT350_8Jet_80Pt26Eta_v1, process.HLT_PFHT350_8Jet_100Pt30Eta_v1, process.HLT_PFHT350_8Jet_100Pt26Eta_v1, process.HLT_PFHT350_10Jet_40Pt30Eta_v1, process.HLT_PFHT350_10Jet_40Pt26Eta_v1, process.HLT_PFHT350_10Jet_60Pt30Eta_v1, process.HLT_PFHT350_10Jet_60Pt26Eta_v1, process.HLT_PFHT350_10Jet_80Pt30Eta_v1, process.HLT_PFHT350_10Jet_80Pt26Eta_v1, process.HLT_PFHT350_10Jet_100Pt30Eta_v1, process.HLT_PFHT350_10Jet_100Pt26Eta_v1, process.HLT_PFHT400_4Jet_40Pt30Eta_v1, process.HLT_PFHT400_4Jet_40Pt26Eta_v1, process.HLT_PFHT400_4Jet_60Pt30Eta_v1, process.HLT_PFHT400_4Jet_60Pt26Eta_v1, process.HLT_PFHT400_4Jet_80Pt30Eta_v1, process.HLT_PFHT400_4Jet_80Pt26Eta_v1, process.HLT_PFHT400_4Jet_100Pt30Eta_v1, process.HLT_PFHT400_4Jet_100Pt26Eta_v1, process.HLT_PFHT400_6Jet_40Pt30Eta_v1, process.HLT_PFHT400_6Jet_40Pt26Eta_v1, process.HLT_PFHT400_6Jet_60Pt30Eta_v1, process.HLT_PFHT400_6Jet_60Pt26Eta_v1, process.HLT_PFHT400_6Jet_80Pt30Eta_v1, process.HLT_PFHT400_6Jet_80Pt26Eta_v1, process.HLT_PFHT400_6Jet_100Pt30Eta_v1, process.HLT_PFHT400_6Jet_100Pt26Eta_v1, process.HLT_PFHT400_8Jet_40Pt30Eta_v1, process.HLT_PFHT400_8Jet_40Pt26Eta_v1, process.HLT_PFHT400_8Jet_60Pt30Eta_v1, process.HLT_PFHT400_8Jet_60Pt26Eta_v1, process.HLT_PFHT400_8Jet_80Pt30Eta_v1, process.HLT_PFHT400_8Jet_80Pt26Eta_v1, process.HLT_PFHT400_8Jet_100Pt30Eta_v1, process.HLT_PFHT400_8Jet_100Pt26Eta_v1, process.HLT_PFHT400_10Jet_40Pt30Eta_v1, process.HLT_PFHT400_10Jet_40Pt26Eta_v1, process.HLT_PFHT400_10Jet_60Pt30Eta_v1, process.HLT_PFHT400_10Jet_60Pt26Eta_v1, process.HLT_PFHT400_10Jet_80Pt30Eta_v1, process.HLT_PFHT400_10Jet_80Pt26Eta_v1, process.HLT_PFHT400_10Jet_100Pt30Eta_v1, process.HLT_PFHT400_10Jet_100Pt26Eta_v1, process.HLT_PFHT450_4Jet_40Pt30Eta_v1, process.HLT_PFHT450_4Jet_40Pt26Eta_v1, process.HLT_PFHT450_4Jet_60Pt30Eta_v1, process.HLT_PFHT450_4Jet_60Pt26Eta_v1, process.HLT_PFHT450_4Jet_80Pt30Eta_v1, process.HLT_PFHT450_4Jet_80Pt26Eta_v1, process.HLT_PFHT450_4Jet_100Pt30Eta_v1, process.HLT_PFHT450_4Jet_100Pt26Eta_v1, process.HLT_PFHT450_6Jet_40Pt30Eta_v1, process.HLT_PFHT450_6Jet_40Pt26Eta_v1, process.HLT_PFHT450_6Jet_60Pt30Eta_v1, process.HLT_PFHT450_6Jet_60Pt26Eta_v1, process.HLT_PFHT450_6Jet_80Pt30Eta_v1, process.HLT_PFHT450_6Jet_80Pt26Eta_v1, process.HLT_PFHT450_6Jet_100Pt30Eta_v1, process.HLT_PFHT450_6Jet_100Pt26Eta_v1, process.HLT_PFHT450_8Jet_40Pt30Eta_v1, process.HLT_PFHT450_8Jet_40Pt26Eta_v1, process.HLT_PFHT450_8Jet_60Pt30Eta_v1, process.HLT_PFHT450_8Jet_60Pt26Eta_v1, process.HLT_PFHT450_8Jet_80Pt30Eta_v1, process.HLT_PFHT450_8Jet_80Pt26Eta_v1, process.HLT_PFHT450_8Jet_100Pt30Eta_v1, process.HLT_PFHT450_8Jet_100Pt26Eta_v1, process.HLT_PFHT450_10Jet_40Pt30Eta_v1, process.HLT_PFHT450_10Jet_40Pt26Eta_v1, process.HLT_PFHT450_10Jet_60Pt30Eta_v1, process.HLT_PFHT450_10Jet_60Pt26Eta_v1, process.HLT_PFHT450_10Jet_80Pt30Eta_v1, process.HLT_PFHT450_10Jet_80Pt26Eta_v1, process.HLT_PFHT450_10Jet_100Pt30Eta_v1, process.HLT_PFHT450_10Jet_100Pt26Eta_v1, process.HLT_PFHT500_4Jet_40Pt30Eta_v1, process.HLT_PFHT500_4Jet_40Pt26Eta_v1, process.HLT_PFHT500_4Jet_60Pt30Eta_v1, process.HLT_PFHT500_4Jet_60Pt26Eta_v1, process.HLT_PFHT500_4Jet_80Pt30Eta_v1, process.HLT_PFHT500_4Jet_80Pt26Eta_v1, process.HLT_PFHT500_4Jet_100Pt30Eta_v1, process.HLT_PFHT500_4Jet_100Pt26Eta_v1, process.HLT_PFHT500_6Jet_40Pt30Eta_v1, process.HLT_PFHT500_6Jet_40Pt26Eta_v1, process.HLT_PFHT500_6Jet_60Pt30Eta_v1, process.HLT_PFHT500_6Jet_60Pt26Eta_v1, process.HLT_PFHT500_6Jet_80Pt30Eta_v1, process.HLT_PFHT500_6Jet_80Pt26Eta_v1, process.HLT_PFHT500_6Jet_100Pt30Eta_v1, process.HLT_PFHT500_6Jet_100Pt26Eta_v1, process.HLT_PFHT500_8Jet_40Pt30Eta_v1, process.HLT_PFHT500_8Jet_40Pt26Eta_v1, process.HLT_PFHT500_8Jet_60Pt30Eta_v1, process.HLT_PFHT500_8Jet_60Pt26Eta_v1, process.HLT_PFHT500_8Jet_80Pt30Eta_v1, process.HLT_PFHT500_8Jet_80Pt26Eta_v1, process.HLT_PFHT500_8Jet_100Pt30Eta_v1, process.HLT_PFHT500_8Jet_100Pt26Eta_v1, process.HLT_PFHT500_10Jet_40Pt30Eta_v1, process.HLT_PFHT500_10Jet_40Pt26Eta_v1, process.HLT_PFHT500_10Jet_60Pt30Eta_v1, process.HLT_PFHT500_10Jet_60Pt26Eta_v1, process.HLT_PFHT500_10Jet_80Pt30Eta_v1, process.HLT_PFHT500_10Jet_80Pt26Eta_v1, process.HLT_PFHT500_10Jet_100Pt30Eta_v1, process.HLT_PFHT500_10Jet_100Pt26Eta_v1, process.HLT_PFHT550_4Jet_40Pt30Eta_v1, process.HLT_PFHT550_4Jet_40Pt26Eta_v1, process.HLT_PFHT550_4Jet_60Pt30Eta_v1, process.HLT_PFHT550_4Jet_60Pt26Eta_v1, process.HLT_PFHT550_4Jet_80Pt30Eta_v1, process.HLT_PFHT550_4Jet_80Pt26Eta_v1, process.HLT_PFHT550_4Jet_100Pt30Eta_v1, process.HLT_PFHT550_4Jet_100Pt26Eta_v1, process.HLT_PFHT550_6Jet_40Pt30Eta_v1, process.HLT_PFHT550_6Jet_40Pt26Eta_v1, process.HLT_PFHT550_6Jet_60Pt30Eta_v1, process.HLT_PFHT550_6Jet_60Pt26Eta_v1, process.HLT_PFHT550_6Jet_80Pt30Eta_v1, process.HLT_PFHT550_6Jet_80Pt26Eta_v1, process.HLT_PFHT550_6Jet_100Pt30Eta_v1, process.HLT_PFHT550_6Jet_100Pt26Eta_v1, process.HLT_PFHT550_8Jet_40Pt30Eta_v1, process.HLT_PFHT550_8Jet_40Pt26Eta_v1, process.HLT_PFHT550_8Jet_60Pt30Eta_v1, process.HLT_PFHT550_8Jet_60Pt26Eta_v1, process.HLT_PFHT550_8Jet_80Pt30Eta_v1, process.HLT_PFHT550_8Jet_80Pt26Eta_v1, process.HLT_PFHT550_8Jet_100Pt30Eta_v1, process.HLT_PFHT550_8Jet_100Pt26Eta_v1, process.HLT_PFHT550_10Jet_40Pt30Eta_v1, process.HLT_PFHT550_10Jet_40Pt26Eta_v1, process.HLT_PFHT550_10Jet_60Pt30Eta_v1, process.HLT_PFHT550_10Jet_60Pt26Eta_v1, process.HLT_PFHT550_10Jet_80Pt30Eta_v1, process.HLT_PFHT550_10Jet_80Pt26Eta_v1, process.HLT_PFHT550_10Jet_100Pt30Eta_v1, process.HLT_PFHT550_10Jet_100Pt26Eta_v1, process.HLT_PFHT600_4Jet_40Pt30Eta_v1, process.HLT_PFHT600_4Jet_40Pt26Eta_v1, process.HLT_PFHT600_4Jet_60Pt30Eta_v1, process.HLT_PFHT600_4Jet_60Pt26Eta_v1, process.HLT_PFHT600_4Jet_80Pt30Eta_v1, process.HLT_PFHT600_4Jet_80Pt26Eta_v1, process.HLT_PFHT600_4Jet_100Pt30Eta_v1, process.HLT_PFHT600_4Jet_100Pt26Eta_v1, process.HLT_PFHT600_6Jet_40Pt30Eta_v1, process.HLT_PFHT600_6Jet_40Pt26Eta_v1, process.HLT_PFHT600_6Jet_60Pt30Eta_v1, process.HLT_PFHT600_6Jet_60Pt26Eta_v1, process.HLT_PFHT600_6Jet_80Pt30Eta_v1, process.HLT_PFHT600_6Jet_80Pt26Eta_v1, process.HLT_PFHT600_6Jet_100Pt30Eta_v1, process.HLT_PFHT600_6Jet_100Pt26Eta_v1, process.HLT_PFHT600_8Jet_40Pt30Eta_v1, process.HLT_PFHT600_8Jet_40Pt26Eta_v1, process.HLT_PFHT600_8Jet_60Pt30Eta_v1, process.HLT_PFHT600_8Jet_60Pt26Eta_v1, process.HLT_PFHT600_8Jet_80Pt30Eta_v1, process.HLT_PFHT600_8Jet_80Pt26Eta_v1, process.HLT_PFHT600_8Jet_100Pt30Eta_v1, process.HLT_PFHT600_8Jet_100Pt26Eta_v1, process.HLT_PFHT600_10Jet_40Pt30Eta_v1, process.HLT_PFHT600_10Jet_40Pt26Eta_v1, process.HLT_PFHT600_10Jet_60Pt30Eta_v1, process.HLT_PFHT600_10Jet_60Pt26Eta_v1, process.HLT_PFHT600_10Jet_80Pt30Eta_v1, process.HLT_PFHT600_10Jet_80Pt26Eta_v1, process.HLT_PFHT600_10Jet_100Pt30Eta_v1, process.HLT_PFHT600_10Jet_100Pt26Eta_v1, process.HLT_PFHT650_4Jet_40Pt30Eta_v1, process.HLT_PFHT650_4Jet_40Pt26Eta_v1, process.HLT_PFHT650_4Jet_60Pt30Eta_v1, process.HLT_PFHT650_4Jet_60Pt26Eta_v1, process.HLT_PFHT650_4Jet_80Pt30Eta_v1, process.HLT_PFHT650_4Jet_80Pt26Eta_v1, process.HLT_PFHT650_4Jet_100Pt30Eta_v1, process.HLT_PFHT650_4Jet_100Pt26Eta_v1, process.HLT_PFHT650_6Jet_40Pt30Eta_v1, process.HLT_PFHT650_6Jet_40Pt26Eta_v1, process.HLT_PFHT650_6Jet_60Pt30Eta_v1, process.HLT_PFHT650_6Jet_60Pt26Eta_v1, process.HLT_PFHT650_6Jet_80Pt30Eta_v1, process.HLT_PFHT650_6Jet_80Pt26Eta_v1, process.HLT_PFHT650_6Jet_100Pt30Eta_v1, process.HLT_PFHT650_6Jet_100Pt26Eta_v1, process.HLT_PFHT650_8Jet_40Pt30Eta_v1, process.HLT_PFHT650_8Jet_40Pt26Eta_v1, process.HLT_PFHT650_8Jet_60Pt30Eta_v1, process.HLT_PFHT650_8Jet_60Pt26Eta_v1, process.HLT_PFHT650_8Jet_80Pt30Eta_v1, process.HLT_PFHT650_8Jet_80Pt26Eta_v1, process.HLT_PFHT650_8Jet_100Pt30Eta_v1, process.HLT_PFHT650_8Jet_100Pt26Eta_v1, process.HLT_PFHT650_10Jet_40Pt30Eta_v1, process.HLT_PFHT650_10Jet_40Pt26Eta_v1, process.HLT_PFHT650_10Jet_60Pt30Eta_v1, process.HLT_PFHT650_10Jet_60Pt26Eta_v1, process.HLT_PFHT650_10Jet_80Pt30Eta_v1, process.HLT_PFHT650_10Jet_80Pt26Eta_v1, process.HLT_PFHT650_10Jet_100Pt30Eta_v1, process.HLT_PFHT650_10Jet_100Pt26Eta_v1, process.HLT_PFHT700_4Jet_40Pt30Eta_v1, process.HLT_PFHT700_4Jet_40Pt26Eta_v1, process.HLT_PFHT700_4Jet_60Pt30Eta_v1, process.HLT_PFHT700_4Jet_60Pt26Eta_v1, process.HLT_PFHT700_4Jet_80Pt30Eta_v1, process.HLT_PFHT700_4Jet_80Pt26Eta_v1, process.HLT_PFHT700_4Jet_100Pt30Eta_v1, process.HLT_PFHT700_4Jet_100Pt26Eta_v1, process.HLT_PFHT700_6Jet_40Pt30Eta_v1, process.HLT_PFHT700_6Jet_40Pt26Eta_v1, process.HLT_PFHT700_6Jet_60Pt30Eta_v1, process.HLT_PFHT700_6Jet_60Pt26Eta_v1, process.HLT_PFHT700_6Jet_80Pt30Eta_v1, process.HLT_PFHT700_6Jet_80Pt26Eta_v1, process.HLT_PFHT700_6Jet_100Pt30Eta_v1, process.HLT_PFHT700_6Jet_100Pt26Eta_v1, process.HLT_PFHT700_8Jet_40Pt30Eta_v1, process.HLT_PFHT700_8Jet_40Pt26Eta_v1, process.HLT_PFHT700_8Jet_60Pt30Eta_v1, process.HLT_PFHT700_8Jet_60Pt26Eta_v1, process.HLT_PFHT700_8Jet_80Pt30Eta_v1, process.HLT_PFHT700_8Jet_80Pt26Eta_v1, process.HLT_PFHT700_8Jet_100Pt30Eta_v1, process.HLT_PFHT700_8Jet_100Pt26Eta_v1, process.HLT_PFHT700_10Jet_40Pt30Eta_v1, process.HLT_PFHT700_10Jet_40Pt26Eta_v1, process.HLT_PFHT700_10Jet_60Pt30Eta_v1, process.HLT_PFHT700_10Jet_60Pt26Eta_v1, process.HLT_PFHT700_10Jet_80Pt30Eta_v1, process.HLT_PFHT700_10Jet_80Pt26Eta_v1, process.HLT_PFHT700_10Jet_100Pt30Eta_v1, process.HLT_PFHT700_10Jet_100Pt26Eta_v1, process.HLT_PFHT750_4Jet_40Pt30Eta_v1, process.HLT_PFHT750_4Jet_40Pt26Eta_v1, process.HLT_PFHT750_4Jet_60Pt30Eta_v1, process.HLT_PFHT750_4Jet_60Pt26Eta_v1, process.HLT_PFHT750_4Jet_80Pt30Eta_v1, process.HLT_PFHT750_4Jet_80Pt26Eta_v1, process.HLT_PFHT750_4Jet_100Pt30Eta_v1, process.HLT_PFHT750_4Jet_100Pt26Eta_v1, process.HLT_PFHT750_6Jet_40Pt30Eta_v1, process.HLT_PFHT750_6Jet_40Pt26Eta_v1, process.HLT_PFHT750_6Jet_60Pt30Eta_v1, process.HLT_PFHT750_6Jet_60Pt26Eta_v1, process.HLT_PFHT750_6Jet_80Pt30Eta_v1, process.HLT_PFHT750_6Jet_80Pt26Eta_v1, process.HLT_PFHT750_6Jet_100Pt30Eta_v1, process.HLT_PFHT750_6Jet_100Pt26Eta_v1, process.HLT_PFHT750_8Jet_40Pt30Eta_v1, process.HLT_PFHT750_8Jet_40Pt26Eta_v1, process.HLT_PFHT750_8Jet_60Pt30Eta_v1, process.HLT_PFHT750_8Jet_60Pt26Eta_v1, process.HLT_PFHT750_8Jet_80Pt30Eta_v1, process.HLT_PFHT750_8Jet_80Pt26Eta_v1, process.HLT_PFHT750_8Jet_100Pt30Eta_v1, process.HLT_PFHT750_8Jet_100Pt26Eta_v1, process.HLT_PFHT750_10Jet_40Pt30Eta_v1, process.HLT_PFHT750_10Jet_40Pt26Eta_v1, process.HLT_PFHT750_10Jet_60Pt30Eta_v1, process.HLT_PFHT750_10Jet_60Pt26Eta_v1, process.HLT_PFHT750_10Jet_80Pt30Eta_v1, process.HLT_PFHT750_10Jet_80Pt26Eta_v1, process.HLT_PFHT750_10Jet_100Pt30Eta_v1, process.HLT_PFHT750_10Jet_100Pt26Eta_v1, process.HLT_PFHT800_4Jet_40Pt30Eta_v1, process.HLT_PFHT800_4Jet_40Pt26Eta_v1, process.HLT_PFHT800_4Jet_60Pt30Eta_v1, process.HLT_PFHT800_4Jet_60Pt26Eta_v1, process.HLT_PFHT800_4Jet_80Pt30Eta_v1, process.HLT_PFHT800_4Jet_80Pt26Eta_v1, process.HLT_PFHT800_4Jet_100Pt30Eta_v1, process.HLT_PFHT800_4Jet_100Pt26Eta_v1, process.HLT_PFHT800_6Jet_40Pt30Eta_v1, process.HLT_PFHT800_6Jet_40Pt26Eta_v1, process.HLT_PFHT800_6Jet_60Pt30Eta_v1, process.HLT_PFHT800_6Jet_60Pt26Eta_v1, process.HLT_PFHT800_6Jet_80Pt30Eta_v1, process.HLT_PFHT800_6Jet_80Pt26Eta_v1, process.HLT_PFHT800_6Jet_100Pt30Eta_v1, process.HLT_PFHT800_6Jet_100Pt26Eta_v1, process.HLT_PFHT800_8Jet_40Pt30Eta_v1, process.HLT_PFHT800_8Jet_40Pt26Eta_v1, process.HLT_PFHT800_8Jet_60Pt30Eta_v1, process.HLT_PFHT800_8Jet_60Pt26Eta_v1, process.HLT_PFHT800_8Jet_80Pt30Eta_v1, process.HLT_PFHT800_8Jet_80Pt26Eta_v1, process.HLT_PFHT800_8Jet_100Pt30Eta_v1, process.HLT_PFHT800_8Jet_100Pt26Eta_v1, process.HLT_PFHT800_10Jet_40Pt30Eta_v1, process.HLT_PFHT800_10Jet_40Pt26Eta_v1, process.HLT_PFHT800_10Jet_60Pt30Eta_v1, process.HLT_PFHT800_10Jet_60Pt26Eta_v1, process.HLT_PFHT800_10Jet_80Pt30Eta_v1, process.HLT_PFHT800_10Jet_80Pt26Eta_v1, process.HLT_PFHT800_10Jet_100Pt30Eta_v1, process.HLT_PFHT800_10Jet_100Pt26Eta_v1, )
    return junk
# num paths: 384
