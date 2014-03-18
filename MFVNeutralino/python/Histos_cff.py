import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.WeightProducer_cfi import *
from JMTucker.MFVNeutralino.VertexHistos_cfi import *
from JMTucker.MFVNeutralino.EventHistos_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *

mfvVertexHistosNoCuts = mfvVertexHistos.clone(vertex_aux_src = 'mfvSelectedVerticesLoose')
mfvVertexHistosTrigCut = mfvVertexHistos.clone()
mfvVertexHistosOneVtx = mfvVertexHistos.clone()
mfvVertexHistosNoCutsWAnaCuts = mfvVertexHistosNoCuts.clone()
mfvEventHistosNoCuts = mfvEventHistos.clone()
mfvEventHistosTrigCut = mfvEventHistos.clone()
mfvEventHistosOneVtx = mfvEventHistos.clone()
mfvVertexHistosWAnaCuts = mfvVertexHistos.clone()

mfvHistos = cms.Sequence(mfvWeight *
                         mfvVertexHistos *
                         mfvVertexHistosNoCuts *
                         mfvEventHistosNoCuts *
                         mfvAnalysisCutsTrigOnly *
                         mfvVertexHistosTrigCut *
                         mfvEventHistosTrigCut *
                         mfvAnalysisCutsOneVtx *
                         mfvVertexHistosOneVtx *
                         mfvEventHistosOneVtx *
                         mfvAnalysisCuts *
                         mfvEventHistos *
                         mfvVertexHistosNoCutsWAnaCuts *
                         mfvVertexHistosWAnaCuts)

def re_trigger(process):
    process.mfvAnalysisCuts     .re_trigger = True # JMTBAD make an "EventRedoer"
    process.mfvEventHistosNoCuts.re_trigger = True
    process.mfvEventHistos      .re_trigger = True
