import FWCore.ParameterSet.Config as cms

process = cms.Process("Dumpers")

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10)
    ),
    toGet = cms.VPSet(),
    connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
    globaltag = cms.string('PHYS14_25_V1')
)

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring('file:a.root'))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.genMuons = cms.EDFilter('GenParticleSelector',
                                src = cms.InputTag('genParticles'),
                                cut = cms.string('abs(pdgId) == 13 & status == 1'),
                                )

process.a = cms.EDAnalyzer('JMTEventDump',
                           #track_labels = cms.untracked.VInputTag(cms.InputTag('tevMuons','firstHit'),
                           #                                       cms.InputTag('tevMuons','picky'),
                           #                                       cms.InputTag('globalMuons'),
                           #                                       cms.InputTag('standAloneMuons')),
                           genparticle_labels = cms.untracked.VInputTag(cms.InputTag('genMuons')),
                           muon_labels = cms.untracked.VInputTag(cms.InputTag('muons')),
                           use_cout = cms.untracked.bool(True),
                           )

process.p = cms.Path(process.genMuons * process.a)

