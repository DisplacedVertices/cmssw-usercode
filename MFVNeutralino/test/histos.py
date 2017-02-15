import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

import JMTucker.Tools.SampleFiles as sf
sf.set_process(process, 'qcdht2000', 'ntuplev10', 10)

process.TFileService.fileName = 'histos.root'
process.maxEvents.input = -1
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.Histos_cff')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

nm1s = [
    ('Njets',      ('', 'min_njets = 0')),
    ('Ht',         ('', 'min_ht = 0')),
    ('Ntracks',    'min_ntracks = 0'),
    ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
    ('Geo2ddist',  'max_geo2ddist = 1e9'),
    ('Bs2derr',    'max_bs2derr = 1e9'),
    ]

#nm1s = []

for name, cut in nm1s:
    evt_cut = ''
    if type(cut) == tuple:
        cut, evt_cut = cut

    vtx = eval('process.mfvSelectedVerticesTight.clone(%s)' % cut)
    vtx_name = 'vtxNo' + name

    for nv in (1,2):
        ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
        ana.vertex_src = vtx_name
        if nv == 1:
            ana.max_nvertex = nv
        ana.min_nvertex = nv
        ana_name = 'ana%iVNo' % nv + name

        evt_hst = process.mfvEventHistos.clone()
        evt_hst_name = 'evtHst%iVNo' % nv + name

        vtx_hst = process.mfvVertexHistos.clone(vertex_src = vtx_name)
        if nv == 1:
            vtx_hst.do_only_1v = True
        vtx_hst_name = 'vtxHst%iVNo' % nv + name

        setattr(process, vtx_name, vtx)
        setattr(process, ana_name, ana)
        setattr(process, evt_hst_name, evt_hst)
        setattr(process, vtx_hst_name, vtx_hst)
        setattr(process, 'p%iV' % nv + name, cms.Path(vtx * ana * evt_hst * vtx_hst))

def force_bs(process, bs):
    for ana in process.analyzers:
        if hasattr(ana, 'force_bs'):
            ana.force_bs = bs

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.data_samples + \
        Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        [Samples.xx4j_tau00001mm_M0300, Samples.xx4j_tau00010mm_M0300, Samples.xx4j_tau00001mm_M0700, Samples.xx4j_tau00010mm_M0700]

    for sample in samples:
        sample.files_per = 50
        if not sample.is_mc:
            sample.json = 'ana_2015p6.json'

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('HistosV10_15_afterreorg', dataset='ntuplev10')
    cs.submit_all(samples)
