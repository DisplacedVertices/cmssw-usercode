import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, file_event_from_argv, process

simple = False

process.source.fileNames = ['root://osg-se.cac.cornell.edu//xrootd/path/cms/store/user/tucker/mfv_hltrun2_M0400/patpu40/150626_223437/0000/pat_1.root']
process.TFileService.fileName = 'histos.root'
process.maxEvents.input = 100
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.Histos_cff')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

nm1s = [
    ('Ntracks', 'min_ntracks = 0, min_njetsntks = 0'),
    ('Drmin',   'max_drmin = 1e9'),
    ('Drmax',   'max_drmax = 1e9'),
    ('Mindrmax','min_drmax = 0'),
    ('Bs2derr', 'max_bs2derr = 1e9'),
    ('Njets',   'min_njetsntks = 0'),
    ('Ntracksptgt3', 'min_ntracksptgt3 = 0'),
    ('Sumnhitsbehind', 'max_sumnhitsbehind = 1000000'),
    ('ButNtracksAndGt3', 'max_drmin = 1e9, max_drmax = 1e9, min_drmax = 0, max_bs2derr = 1e9, min_njetsntks = 0'),
    ]

if simple:
    nm1s = []

    del process.pOneVtx
    del process.pFullSel
    del process.pOnlyOneVtx
    del process.pPreSel
    del process.pTrigSel
    del process.pSigReg

    process.p = cms.Path(process.mfvSelectedVerticesLoose +
                         process.mfvSelectedVerticesTight +
                         process.mfvWeight +
                         process.mfvEventHistosNoCuts +
                         process.mfvVertexHistosNoCuts +
                         process.mfvVertexHistos +
                         process.mfvAnalysisCuts +
                         process.mfvEventHistos +
                         process.mfvVertexHistosWAnaCuts)

for name, cut in nm1s:
    evt_cut = ''
    if type(cut) == tuple:
        cut, evt_cut = cut

    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name

    for only in ('', 'Only'):
        for nv in (1,2):
            if nv == 2 and only == 'Only':
                continue

            ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
            ana.vertex_src = vtx_name
            if only == 'Only':
                ana.max_nvertex = nv
            ana.min_nvertex = nv
            ana_name = 'ana%s%iVNo' % (only, nv) + name

            evt_hst = process.mfvEventHistos.clone()
            evt_hst_name = 'evtHst%s%iVNo' % (only, nv) + name

            vtx_hst = process.mfvVertexHistos.clone(vertex_aux_src = vtx_name)
            vtx_hst_name = 'vtxHst%s%iVNo' % (only, nv) + name

            setattr(process, vtx_name, vtx)
            setattr(process, ana_name, ana)
            setattr(process, evt_hst_name, evt_hst)
            setattr(process, vtx_hst_name, vtx_hst)
            setattr(process, 'p%s%iV' % (only, nv) + name, cms.Path(vtx * ana * evt_hst * vtx_hst))

def force_bs(process, bs):
    for ana in process.analyzers:
        if hasattr(ana, 'force_bs'):
            ana.force_bs = bs

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Sample import anon_samples
    samples = anon_samples('''
''', dbs_inst='phys03')

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('HistosV2',
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 50000,
                       total_units = -1,
                       aaa = True,
                       )
    cs.submit_all(samples)
