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

def re_trigger(process):
    process.mfvAnalysisCuts     .re_trigger = True # JMTBAD make an "EventRedoer"
    process.mfvEventHistosNoCuts.re_trigger = True
    process.mfvEventHistos      .re_trigger = True

def no_use_ref(process):
    for name in 'mfvVertexHistos mfvVertexHistosNoCuts mfvVertexHistosNoCutsWAnaCuts mfvVertexHistosWAnaCuts'.split():
        getattr(process, name).use_ref = False
