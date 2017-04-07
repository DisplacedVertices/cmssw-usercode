
from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

mfvAnalysisCuts.min_nvertex = 1

mfvMiniTree = cms.EDAnalyzer('MFVMiniTreer',
                             event_src = cms.InputTag('mfvEvent'),
                             vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                             weight_src = cms.InputTag('mfvWeight'),
                             save_tracks = cms.bool(True)
                             )

pMiniTree = cms.Path(mfvWeight * mfvSelectedVerticesTight * mfvAnalysisCuts * mfvMiniTree)

for mn,mx in (3,3), (3,4), (4,4):
    exec '''
vtxMNMX = mfvSelectedVerticesTight.clone(min_ntracks = MN, max_ntracks = MX)
anaMNMX = mfvAnalysisCuts.clone(vertex_src = 'vtxMNMX')
treMNMX = mfvMiniTree.clone(vertex_src = 'vtxMNMX')
pMiniTreeMNMX = cms.Path(mfvWeight * vtxMNMX * anaMNMX * treMNMX)
'''.replace('MN', str(mn)).replace('MX', str(mx))
