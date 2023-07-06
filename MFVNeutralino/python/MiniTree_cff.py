import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

mfvAnalysisCutsGE1Vtx = mfvAnalysisCuts.clone(min_nvertex = 1)
mfvAnalysisCutsGE1Vtx_1dl = mfvAnalysisCuts.clone(min_nvertex = 1, require_displaced_lepton=True, vertex_src = 'mfvSelectedVerticesLoose')
mfvAnalysisCutsGE1Vtx_loose = mfvAnalysisCuts.clone(min_nvertex = 1, vertex_src = 'mfvSelectedVerticesLoose')


mfvMiniTree = cms.EDAnalyzer('MFVMiniTreer',
                             event_src = cms.InputTag('mfvEvent'),
                             vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                             weight_src = cms.InputTag('mfvWeight'),
                             save_tracks = cms.bool(True),
                             )

#pMiniTree = cms.Path(mfvWeight * mfvSelectedVerticesTight * mfvAnalysisCutsGE1Vtx * mfvMiniTree)
mfvMiniTree_loose = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLoose')
mfvMiniTree_lep = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLoose')


mfvAnalysisCutsGE1VtxMinNtk3_loose   =  mfvAnalysisCutsGE1Vtx_loose.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3')
mfvAnalysisCutsGE1VtxMinNtk4_loose   =  mfvAnalysisCutsGE1Vtx_loose.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')
mfvAnalysisCutsGE1VtxMinNtk3_lep   =  mfvAnalysisCutsGE1Vtx_1dl.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3')
mfvAnalysisCutsGE1VtxMinNtk4_lep   =  mfvAnalysisCutsGE1Vtx_1dl.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')


mfvMiniTreeMinNtk3_loose = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3')
mfvMiniTreeMinNtk4_loose = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')
mfvMiniTreeMinNtk3_lep = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3')
mfvMiniTreeMinNtk4_lep = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')


pMiniTree_loose = cms.Path(mfvWeight * mfvSelectedVerticesLoose *mfvAnalysisCutsGE1Vtx_loose  * mfvMiniTree_loose)
pMiniTreeMinNtk3_loose = cms.Path(mfvWeight * mfvSelectedVerticesLooseMinNtk3 *mfvAnalysisCutsGE1VtxMinNtk3_loose  * mfvMiniTreeMinNtk3_loose)
pMiniTreeMinNtk4_loose = cms.Path(mfvWeight * mfvSelectedVerticesLooseMinNtk4 *mfvAnalysisCutsGE1VtxMinNtk4_loose  * mfvMiniTreeMinNtk4_loose)
pMiniTree_lep = cms.Path(mfvWeight * mfvSelectedVerticesLoose *mfvAnalysisCutsGE1Vtx_1dl  * mfvMiniTree_lep)
pMiniTreeMinNtk3_lep = cms.Path(mfvWeight * mfvSelectedVerticesLooseMinNtk3 *mfvAnalysisCutsGE1VtxMinNtk3_lep  * mfvMiniTreeMinNtk3_lep)
pMiniTreeMinNtk4_lep = cms.Path(mfvWeight * mfvSelectedVerticesLooseMinNtk4 *mfvAnalysisCutsGE1VtxMinNtk4_lep  * mfvMiniTreeMinNtk4_lep)