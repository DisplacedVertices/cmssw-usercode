import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.WeightProducer_cfi import *
from JMTucker.MFVNeutralino.VertexHistos_cfi import *
from JMTucker.MFVNeutralino.EventHistos_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *

mfvVertexHistosNoCuts = mfvVertexHistos.clone(vertex_aux_src = 'mfvVerticesAux')
mfvVertexHistosNoCutsWAnaCuts = mfvVertexHistosNoCuts.clone()
mfvEventHistosNoCuts = mfvEventHistos.clone()
mfvVertexHistosWAnaCuts = mfvVertexHistos.clone()

mfvHistos = cms.Sequence(mfvWeight *
                         mfvVertexHistos *
                         mfvVertexHistosNoCuts *
                         mfvEventHistosNoCuts *
                         mfvAnalysisCuts *
                         mfvEventHistos *
                         mfvVertexHistosNoCutsWAnaCuts *
                         mfvVertexHistosWAnaCuts)
