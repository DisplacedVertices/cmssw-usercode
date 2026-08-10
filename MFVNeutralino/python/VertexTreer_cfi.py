import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

mfvVertexTreer = cms.EDAnalyzer('MFVVertexTreer',
                                 mevent_src = cms.InputTag('mfvEvent'),
                                 weight_src = cms.InputTag('mfvWeight'),
                                 vertex_src = cms.InputTag('mfvSelectedVerticesVeryLoose'),
                                 )

mfvSelectedVerticesVeryLoose = mfvSelectedVerticesLoose.clone(min_bsbs2ddist = 0, max_rescale_bs2derr = 1e9)

pVertexTreer = cms.Path(mfvSelectedVerticesVeryLoose * mfvWeight * mfvVertexTreer)
