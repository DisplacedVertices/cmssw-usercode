import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.CMSSWTools import silence_messages

process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau1000um_M0400/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_1_1_hdB.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root','/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root')
process.TFileService.fileName = 'prepare_vis.root'
process.maxEvents.input = 25
silence_messages(process, 'TwoTrackMinimumDistance')

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
process.out = cms.OutputModule('PoolOutputModule', fileName = cms.untracked.string('/uscms/home/tucker/scratch/mfv_vis.root')) #, outputCommands = AODSIMEventContent.outputCommands)
#process.out.outputCommands += ['keep *_*_*_BasicAnalyzer']
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
process.load('JMTucker.MFVNeutralino.Vertexer_cff')

#process.mfvVertices.verbose = True

process.pp = cms.Path(process.mfvGenParticles *
                      process.printList *
#                      process.mfvTrackMatching *
                      process.mfvVertexSequence
                      )
