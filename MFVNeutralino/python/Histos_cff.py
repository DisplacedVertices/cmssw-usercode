import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

mfvCommon = cms.Sequence(mfvSelectedVerticesSeq * mfvWeight)

from JMTucker.MFVNeutralino.VertexHistos_cfi import *
from JMTucker.MFVNeutralino.EventHistos_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *

mfvEventHistosNoCuts = mfvEventHistos.clone()
pSkimSel = cms.Path(mfvCommon * mfvEventHistosNoCuts) # just trigger for now

for ntk in ([3]):
    if ntk == 5:
        EX = EX2 = ''
    elif ntk == 7:
        EX = 'Ntk3or4'
    else:
        EX = 'Ntk%i' % ntk
    if EX:
        EX2 = "vertex_src = 'mfvSelectedVerticesTight%s', " % EX

    exec '''
%(EX)smfvAnalysisCutsPreSel     = mfvAnalysisCuts.clone(%(EX2)sapply_vertex_cuts = False)
%(EX)smfvAnalysisCutsOnlyOneVtx = mfvAnalysisCuts.clone(%(EX2)smin_nvertex = 1, max_nvertex = 1)

%(EX)smfvEventHistosPreSel     = mfvEventHistos.clone()
%(EX)smfvEventHistosOnlyOneVtx = mfvEventHistos.clone()

%(EX)smfvVertexHistosPreSel     = mfvVertexHistos.clone(%(EX2)s)
%(EX)smfvVertexHistosOnlyOneVtx = mfvVertexHistos.clone(%(EX2)sdo_only_1v = True)

%(EX)spPreSel     = cms.Path(mfvCommon * %(EX)smfvAnalysisCutsPreSel     * %(EX)smfvEventHistosPreSel     * %(EX)smfvVertexHistosPreSel)
%(EX)spOnlyOneVtx = cms.Path(mfvCommon * %(EX)smfvAnalysisCutsOnlyOneVtx * %(EX)smfvEventHistosOnlyOneVtx * %(EX)smfvVertexHistosOnlyOneVtx)
''' % locals()

#    exec '''
#%(EX)smfvAnalysisCutsPreSel     = mfvAnalysisCuts.clone(%(EX2)sapply_vertex_cuts = False)
#%(EX)smfvAnalysisCutsOnlyOneVtx = mfvAnalysisCuts.clone(%(EX2)smin_nvertex = 1, max_nvertex = 1)
#%(EX)smfvAnalysisCutsFullSel    = mfvAnalysisCuts.clone(%(EX2)s)
#%(EX)smfvAnalysisCutsSigReg     = mfvAnalysisCuts.clone(%(EX2)smin_svdist2d = 0.04)
#
#%(EX)smfvEventHistosPreSel     = mfvEventHistos.clone()
#%(EX)smfvEventHistosOnlyOneVtx = mfvEventHistos.clone()
#%(EX)smfvEventHistosFullSel    = mfvEventHistos.clone()
#%(EX)smfvEventHistosSigReg     = mfvEventHistos.clone()
#
#%(EX)smfvVertexHistosPreSel     = mfvVertexHistos.clone(%(EX2)s)
#%(EX)smfvVertexHistosOnlyOneVtx = mfvVertexHistos.clone(%(EX2)sdo_only_1v = True)
#%(EX)smfvVertexHistosFullSel    = mfvVertexHistos.clone(%(EX2)s)
#%(EX)smfvVertexHistosSigReg     = mfvVertexHistos.clone(%(EX2)s)
#
#%(EX)spPreSel     = cms.Path(mfvCommon * %(EX)smfvAnalysisCutsPreSel     * %(EX)smfvEventHistosPreSel     * %(EX)smfvVertexHistosPreSel)
#%(EX)spOnlyOneVtx = cms.Path(mfvCommon * %(EX)smfvAnalysisCutsOnlyOneVtx * %(EX)smfvEventHistosOnlyOneVtx * %(EX)smfvVertexHistosOnlyOneVtx)
#%(EX)spFullSel    = cms.Path(mfvCommon * %(EX)smfvAnalysisCutsFullSel    * %(EX)smfvEventHistosFullSel    * %(EX)smfvVertexHistosFullSel)
#%(EX)spSigReg     = cms.Path(mfvCommon * %(EX)smfvAnalysisCutsSigReg     * %(EX)smfvEventHistosSigReg     * %(EX)smfvVertexHistosSigReg)
#''' % locals()
