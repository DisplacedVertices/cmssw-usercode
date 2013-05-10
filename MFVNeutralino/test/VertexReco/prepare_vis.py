import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

from JMTucker.MFVNeutralino.SimFiles import load as load_files
load_files(process, 'tau9900um_M0400', 0)
process.source.fileNames = ['file:reco.root']
process.source.secondaryFileNames = ['/store/user/tucker/mfv_gensimhlt_neutralino_tau1000um_M0400/mfv_gensimhlt_neutralino_tau1000um_M0400/c9c4c27381f6625ed3d8394ffaf0b9cd/gensimhlt_16_1_FFD.root']
process.TFileService.fileName = 'prepare_vis.root'
process.maxEvents.input = 20

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

process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                   src = cms.InputTag('genParticles'),
                                   printVertex = cms.untracked.bool(True),
                                   )

process.load('JMTucker.MFVNeutralino.MatchedTracks_cff')
process.load('JMTucker.MFVNeutralino.VertexReco_cff')

process.pp = cms.Path(process.mfvGenParticles *
                      process.printList *
                      process.mfvTrackMatching *
                      process.mfvVertexReco
                      )
