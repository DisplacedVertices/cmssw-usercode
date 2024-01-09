import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

mfvAnalysisCutsGE1Vtx = mfvAnalysisCuts.clone(min_nvertex = 1)
mfvAnalysisCutsPreSelEvtFilt = mfvAnalysisCuts.clone(min_nvertex = 0, apply_trigger = cms.bool(False), min_njets = cms.int32(-1), min_ht = cms.double(-1), apply_vertex_cuts = cms.bool(False)) # Note! Enabling this for the purpose of storing all events to the MiniTree also requires a change in MiniTreer.cc to actually keep 0-vtx events in the MiniTree

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
mfvAnalysisCutsPreSelEvtFilt = mfvAnalysisCutsPreSelEvtFilt.clone(vertex_src = 'mfvSelectedVerticesTight') 

mfvMiniTreeNtk3    = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk3')
mfvMiniTreeNtk4    = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk4')
mfvMiniTreeNtk3or4 = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightNtk3or4')
mfvMiniTreePreSelEvtFilt = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTight')

pMiniTreeNtk3    = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk3    * mfvAnalysisCutsGE1VtxNtk3    * mfvMiniTreeNtk3)
pMiniTreeNtk4    = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk4    * mfvAnalysisCutsGE1VtxNtk4    * mfvMiniTreeNtk4)
pMiniTreeNtk3or4 = cms.Path(mfvWeight * mfvSelectedVerticesTightNtk3or4 * mfvAnalysisCutsGE1VtxNtk3or4 * mfvMiniTreeNtk3or4)
pMiniTreePreSelEvtFilt    = cms.Path(mfvWeight * mfvSelectedVerticesTight    * mfvAnalysisCutsPreSelEvtFilt    * mfvMiniTreePreSelEvtFilt) 
