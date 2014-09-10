import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

mfvCommon = cms.Sequence(mfvSelectedVerticesSeq * mfvWeight)

from JMTucker.MFVNeutralino.VertexHistos_cfi import *
from JMTucker.MFVNeutralino.EventHistos_cfi import *
from JMTucker.MFVNeutralino.ABCDHistos_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *

mfvEventHistosNoCuts = mfvEventHistos.clone()
mfvVertexHistosNoCuts = mfvVertexHistos.clone(vertex_aux_src = 'mfvSelectedVerticesLoose')
pTrigSel = cms.Path(mfvCommon * mfvEventHistosNoCuts * mfvVertexHistos * mfvVertexHistosNoCuts)

mfvAnalysisCutsPreSel = mfvAnalysisCuts.clone(apply_vertex_cuts = False)
mfvEventHistosPreSel = mfvEventHistos.clone()
mfvVertexHistosPreSel = mfvVertexHistos.clone()
pPreSel = cms.Path(mfvCommon * mfvAnalysisCutsPreSel * mfvEventHistosPreSel * mfvVertexHistosPreSel)

mfvAnalysisCutsOneVtx = mfvAnalysisCuts.clone(min_nvertex = 1)
mfvEventHistosOneVtx = mfvEventHistos.clone()
mfvVertexHistosOneVtx = mfvVertexHistos.clone()
pOneVtx = cms.Path(mfvCommon * mfvAnalysisCutsOneVtx * mfvEventHistosOneVtx * mfvVertexHistosOneVtx)

mfvAnalysisCutsOnlyOneVtx = mfvAnalysisCuts.clone(min_nvertex = 1, max_nvertex = 1)
mfvEventHistosOnlyOneVtx = mfvEventHistos.clone()
mfvVertexHistosOnlyOneVtx = mfvVertexHistos.clone()
pOnlyOneVtx = cms.Path(mfvCommon * mfvAnalysisCutsOnlyOneVtx * mfvEventHistosOnlyOneVtx * mfvVertexHistosOnlyOneVtx)

mfvSelectedVerticesNtk5 = mfvSelectedVerticesTight.clone(max_ntracks = 5)
mfvAnalysisCuts2VSideA = mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesNtk5', max_svdist2d = 0.04)
mfvEventHistos2VSideA = mfvEventHistos.clone()
mfvVertexHistos2VSideA = mfvVertexHistos.clone(vertex_aux_src = 'mfvSelectedVerticesNtk5')
p2VSideA = cms.Path(mfvCommon * mfvSelectedVerticesNtk5 * mfvAnalysisCuts2VSideA * mfvEventHistos2VSideA * mfvVertexHistos2VSideA)

mfvAnalysisCuts2VSideB = mfvAnalysisCuts.clone(max_svdist2d = 0.04)
mfvEventHistos2VSideB = mfvEventHistos.clone()
mfvVertexHistos2VSideB = mfvVertexHistos.clone()
p2VSideB = cms.Path(mfvCommon * mfvAnalysisCuts2VSideB * mfvEventHistos2VSideB * mfvVertexHistos2VSideB)

mfvVertexHistosNoCutsWAnaCuts = mfvVertexHistosNoCuts.clone()
mfvVertexHistosWAnaCuts = mfvVertexHistos.clone()
pFullSel = cms.Path(mfvCommon * mfvAnalysisCuts * mfvEventHistos * mfvVertexHistosNoCutsWAnaCuts * mfvVertexHistosWAnaCuts * mfvAbcdHistosSeq)
