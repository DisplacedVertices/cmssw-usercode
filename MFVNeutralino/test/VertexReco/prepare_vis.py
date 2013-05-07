import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

from JMTucker.MFVNeutralino.SimFiles import load as load_files
load_files(process, 'tau9900um_M0400', 0)
process.TFileService.fileName = 'prepare_vis.root'
process.maxEvents.input = 10

process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('SimTracker.TrackAssociation.TrackAssociatorByHits_cfi')

from Configuration.EventContent.EventContent_cff import AODSIMEventContent
process.out = cms.OutputModule('PoolOutputModule', fileName = cms.untracked.string('/uscms/home/tucker/scratch/mfv_vis.root'), outputCommands = AODSIMEventContent.outputCommands)
process.out.outputCommands += ['keep *_*_*_BasicAnalyzer']
process.outp = cms.EndPath(process.out)

process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                         gen_src = cms.InputTag('genParticles'),
                                         print_info = cms.bool(True),
                                         )

process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                   maxEventsToPrint = cms.untracked.int32(100),
                                   src = cms.InputTag('genParticles'),
                                   printOnlyHardInteraction = cms.untracked.bool(False),
                                   useMessageLogger = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(True),
                                   )

process.load('JMTucker.MFVNeutralino.MatchedTracks_cff')
process.load('JMTucker.MFVNeutralino.VertexReco_cff')

process.pp = cms.Path(process.mfvGenParticles *
                      process.printList *
                      process.mfvTrackMatching *
                      process.mfvVertexReco
                      )
