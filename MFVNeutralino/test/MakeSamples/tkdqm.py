import FWCore.ParameterSet.Config as cms

process = cms.Process("MULTITRACKVALIDATOR")

# message logger
process.MessageLogger = cms.Service("MessageLogger",
     default = cms.untracked.PSet( limit = cms.untracked.int32(10) )
)

# source
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( ['file:reco.root' ] );


secFiles.extend( ['file:gensimhlt.root'] );

process.source = source
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )

### conditions
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'START53_V7C::All'

### standard includes
process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration.Geometry.GeometryPilot2_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

### validation-specific includes
#process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")
process.load("SimTracker.TrackAssociation.quickTrackAssociatorByHits_cfi")
process.load("SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cfi")
process.load("Validation.RecoTrack.cuts_cff")
process.load("Validation.RecoTrack.MultiTrackValidator_cff")
process.load("DQMServices.Components.EDMtoMEConverter_cff")
process.load("Validation.Configuration.postValidation_cff")
process.quickTrackAssociatorByHits.SimToRecoDenominator = cms.string('reco')

########### configuration MultiTrackValidator ########
process.multiTrackValidator.outputFile = 'multitrackvalidator.root'
process.multiTrackValidator.associators = ['quickTrackAssociatorByHits']
process.multiTrackValidator.skipHistoFit=cms.untracked.bool(False)
#process.cutsRecoTracks.quality = cms.vstring('','highPurity')
#process.cutsRecoTracks.quality = cms.vstring('')
process.multiTrackValidator.label = ['cutsRecoTracks']
process.multiTrackValidator.useLogPt=cms.untracked.bool(True)
process.multiTrackValidator.minpT = cms.double(0.1)
process.multiTrackValidator.maxpT = cms.double(3000.0)
process.multiTrackValidator.nintpT = cms.int32(40)
process.multiTrackValidator.UseAssociators = cms.bool(True)

process.load("Validation.RecoTrack.cuts_cff")
process.cutsRecoTracks.ptMin    = cms.double(1.0)
process.cutsRecoTracks.minHit   = cms.int32(8)
process.cutsRecoTracks.minRapidity  = cms.double(-2.5)
process.cutsRecoTracks.maxRapidity  = cms.double(2.5)
process.cutsRecoTracks.quality = cms.vstring('highPurity')
process.cutsRecoTracks.min3DHit   = cms.int32(1)
process.cutsRecoTracks.lip   = cms.double(30.0)
process.cutsRecoTracks.tip   = cms.double(30.0)

process.validation = cms.Sequence(
    #process.cutsRecoTracks *
    process.multiTrackValidator
)

# paths
process.p = cms.Path(
      process.cutsRecoTracks
    * process.validation
)
process.schedule = cms.Schedule(
      process.p
)
