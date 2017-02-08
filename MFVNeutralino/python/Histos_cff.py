import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

mfvCommon = cms.Sequence(mfvSelectedVerticesSeq * mfvWeight)

from JMTucker.MFVNeutralino.VertexHistos_cfi import *
from JMTucker.MFVNeutralino.EventHistos_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *

from JMTucker.Tools.SimpleTriggerEfficiency_cfi import *

mfvEventHistosNoCuts = mfvEventHistos.clone()
pSkimSel = cms.Path(mfvCommon * mfvEventHistosNoCuts) # just trigger for now

mfvAnalysisCutsPreSel = mfvAnalysisCuts.clone(apply_vertex_cuts = False)
mfvEventHistosPreSel = mfvEventHistos.clone()
mfvVertexHistosPreSel = mfvVertexHistos.clone()
pPreSel = cms.Path(mfvCommon * mfvAnalysisCutsPreSel * mfvEventHistosPreSel * mfvVertexHistosPreSel)

mfvAnalysisCutsOnlyOneVtx = mfvAnalysisCuts.clone(min_nvertex = 1, max_nvertex = 1)
mfvEventHistosOnlyOneVtx = mfvEventHistos.clone()
mfvVertexHistosOnlyOneVtx = mfvVertexHistos.clone(do_only_1v = True)
pOnlyOneVtx = cms.Path(mfvCommon * mfvAnalysisCutsOnlyOneVtx * mfvEventHistosOnlyOneVtx * mfvVertexHistosOnlyOneVtx)

mfvVertexHistosWAnaCuts = mfvVertexHistos.clone()
pFullSel = cms.Path(mfvCommon * mfvAnalysisCuts * mfvEventHistos * mfvVertexHistosWAnaCuts)

mfvAnalysisCutsSigReg = mfvAnalysisCuts.clone(min_svdist2d = 0.04)
mfvEventHistosSigReg = mfvEventHistos.clone()
mfvVertexHistosSigReg = mfvVertexHistos.clone()
pSigReg = cms.Path(mfvCommon * mfvAnalysisCutsSigReg * mfvEventHistosSigReg * mfvVertexHistosSigReg)
