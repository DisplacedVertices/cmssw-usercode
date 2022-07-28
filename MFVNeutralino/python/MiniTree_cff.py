import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

mfvAnalysisCutsGE1Vtx = mfvAnalysisCuts.clone(min_nvertex = 1)
mfvAnalysisCutsPreSelEvtFilt = mfvAnalysisCuts.clone(min_nvertex = 0)

mfvMiniTree = cms.EDAnalyzer('MFVMiniTreer',
                             event_src = cms.InputTag('mfvEvent'),
                             vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                             weight_src = cms.InputTag('mfvWeight'),
                             save_tracks = cms.bool(True),
                             )

pMiniTree = cms.Path(mfvWeight * mfvSelectedVerticesTight * mfvAnalysisCutsGE1Vtx * mfvMiniTree)

mfvAnalysisCutsGE1VtxNtk3    = mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightNtk3')
mfvAnalysisCutsGE1VtxNtk4    = mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightNtk4')
mfvAnalysisCutsGE1VtxNtk3or4 = mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or4')
mfvAnalysisCutsGE1VtxNtk3or5 = mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or5')
mfvAnalysisCutsGE1VtxNtk4or5 = mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightNtk4or5')
mfvAnalysisCutsGE1VtxNtk3or4exact = mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or4', ntracks01_0=4, ntracks01_1=3)
mfvAnalysisCutsGE1VtxNtk3or5exact = mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or5', ntracks01_0=5, ntracks01_1=3)
mfvAnalysisCutsGE1VtxNtk4or5exact = mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightNtk4or5', ntracks01_0=5, ntracks01_1=4)

mfvAnalysisCutsPreSelEvtFilt    = mfvAnalysisCutsPreSelEvtFilt.clone(vertex_src = 'mfvSelectedVerticesTight') 

mfvMiniTreeNtk3    = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk3')
mfvMiniTreeNtk4    = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk4')
mfvMiniTreeNtk3or4 = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or4')
mfvMiniTreeNtk3or5 = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or5')
mfvMiniTreeNtk4or5 = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk4or5')
mfvMiniTreeNtk3or4exact = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or4')
mfvMiniTreeNtk3or5exact = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or5')
mfvMiniTreeNtk4or5exact = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk4or5')

mfvMiniTreePreSelEvtFilt = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTight')

pMiniTreeNtk3    = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk3    * mfvAnalysisCutsGE1VtxNtk3    * mfvMiniTreeNtk3)
pMiniTreeNtk4    = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk4    * mfvAnalysisCutsGE1VtxNtk4    * mfvMiniTreeNtk4)
pMiniTreeNtk3or4 = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk3or4 * mfvAnalysisCutsGE1VtxNtk3or4 * mfvMiniTreeNtk3or4)
pMiniTreeNtk3or5 = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk3or5 * mfvAnalysisCutsGE1VtxNtk3or5 * mfvMiniTreeNtk3or5)
pMiniTreeNtk4or5 = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk4or5 * mfvAnalysisCutsGE1VtxNtk4or5 * mfvMiniTreeNtk4or5)
pMiniTreeNtk3or4exact = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk3or4 * mfvAnalysisCutsGE1VtxNtk3or4exact * mfvMiniTreeNtk3or4exact)
pMiniTreeNtk3or5exact = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk3or5 * mfvAnalysisCutsGE1VtxNtk3or5exact * mfvMiniTreeNtk3or5exact)
pMiniTreeNtk4or5exact = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk4or5 * mfvAnalysisCutsGE1VtxNtk4or5exact * mfvMiniTreeNtk4or5exact)

pMiniTreePreSelEvtFilt    = cms.Path(mfvWeight * mfvSelectedVerticesTight    * mfvAnalysisCutsPreSelEvtFilt    * mfvMiniTreePreSelEvtFilt) 
