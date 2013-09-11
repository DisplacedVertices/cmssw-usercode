import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, add_analyzer, geometry_etc

process.MessageLogger.cerr.FwkReport.reportEvery = 1
geometry_etc(process, 'START53_V27::All')
process.source.fileNames = ['file:reco.root']
process.source.secondaryFileNames = cms.untracked.vstring('file:gensimhlt.root')
process.load('SimTracker.TrackAssociation.TrackAssociatorByHits_cfi')
process.TFileService.fileName = 'TrackAssociator.root'

process.TrackAssociator = cms.EDAnalyzer('MFVTrackAssociator',
                                         tracks_src = cms.InputTag('generalTracks'),
                                         sim_tracks_src = cms.InputTag('g4SimHits'),
                                         sim_vertices_src = cms.InputTag('g4SimHits'),
                                         tracking_particles_src = cms.InputTag('mergedtruth','MergedTrackTruth'),
                                         gen_particles_src = cms.InputTag('genParticles'),
                                         rec_vertices_src = cms.InputTag('mfvInclusiveVertexFinder'),
                                         do_checks = cms.bool(True),
                                         )

process.load('JMTucker.MFVNeutralino.GenParticles_cff')

process.load('JMTucker.Tools.ParticleListDrawer_cff')
process.ParticleListDrawer2 = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'All'))
process.ParticleListDrawer3 = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'Visible'))

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(True)

process.load('JMTucker.MFVNeutralino.VertexReco_cff')

process.p2 = cms.Path(process.mfvGenParticles * process.ParticleListDrawer2 * process.ParticleListDrawer3 * process.ParticleListDrawer)
process.p = cms.Path(process.mfvVertexReco *  process.TrackAssociator)
