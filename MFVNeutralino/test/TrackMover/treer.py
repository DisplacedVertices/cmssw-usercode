from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = ['file:ntuple.root']
process.TFileService.fileName = 'movedtree.root'

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

process.mfvMovedTree = cms.EDAnalyzer('MFVMovedTracksTreer',
                                      event_src = cms.InputTag('mfvEvent'),
                                      vertices_src = cms.InputTag('mfvVerticesAux'),
                                      weight_src = cms.InputTag('mfvWeight'),
                                      mover_src = cms.string('mfvMovedTracks'),
                                      max_dist2move = cms.double(0.02),
                                      )

process.p = cms.Path(process.mfvWeight * process.mfvMovedTree)
