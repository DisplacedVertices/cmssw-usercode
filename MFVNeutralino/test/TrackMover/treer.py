from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = ['file:ntuple.root']
process.TFileService.fileName = 'movedtree.root'

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

process.p = cms.Path(process.mfvWeight)

for njets in xrange(1,5):
    for nbjets in xrange(0,3):
        if njets == 1 and nbjets == 0:
            continue
        ex = '%i%i' % (njets, nbjets)
        obj = cms.EDAnalyzer('MFVMovedTracksTreer',
                             event_src = cms.InputTag('mfvEvent'),
                             weight_src = cms.InputTag('mfvWeight'),
                             mover_src = cms.string('mfvMovedTracks' + ex),
                             vertices_src = cms.InputTag('mfvVerticesAux' + ex),
                             max_dist2move = cms.double(0.02),
                             )
        setattr(process, 'mfvMovedTree' + ex, obj)
        process.p *= obj
