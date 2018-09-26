import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

dataset = 'ntuplev20m'
sample_files(process, 'qcdht2000_2017', dataset, 1)
process.TFileService.fileName = 'histos.root'
process.maxEvents.input = -1
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexHistos_cfi')
process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)

process.mfvEventHistosNoCuts = process.mfvEventHistos.clone()
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts) # just trigger for now

process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel)

nm1s = [
    ('Njets',      ('', 'apply_presel = 0, min_ht = 1200, min_njets = 0')),
    ('Ht',         ('', 'apply_presel = 0, min_njets = 4, min_ht = 0')),
    ('Ntracks',    'min_ntracks = 0'),
    ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
    ('Geo2ddist',  'max_geo2ddist = 1e9'),
    ('Bs2derr',    'max_bs2derr = 1e9'),
    ]

ntks = [5,3,4,7]
nvs = [0,1,2]

for ntk in ntks:
    if ntk == 5:
        EX1 = EX2 = ''
    elif ntk == 7:
        EX1 = 'Ntk3or4'
    else:
        EX1 = 'Ntk%i' % ntk
    if EX1:
        EX2 = "vertex_src = 'mfvSelectedVerticesTight%s', " % EX1

    exec '''
process.EX1mfvAnalysisCutsOnlyOneVtx = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, max_nvertex = 1)
process.EX1mfvAnalysisCutsFullSel    = process.mfvAnalysisCuts.clone(EX2)
process.EX1mfvAnalysisCutsSigReg     = process.mfvAnalysisCuts.clone(EX2min_svdist2d = 0.04)

process.EX1mfvEventHistosOnlyOneVtx = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()
process.EX1mfvEventHistosSigReg     = process.mfvEventHistos.clone()

process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosOnlyOneVtx = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosFullSel    = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosSigReg     = process.mfvVertexHistos.clone(EX2)

process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreSel)
process.EX1pOnlyOneVtx = cms.Path(common * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvEventHistosOnlyOneVtx * process.EX1mfvVertexHistosOnlyOneVtx)
'''.replace('EX1', EX1).replace('EX2', EX2)

    if 2 in nvs:
        exec '''
process.EX1pFullSel    = cms.Path(common * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvEventHistosFullSel    * process.EX1mfvVertexHistosFullSel)
process.EX1pSigReg     = cms.Path(common * process.EX1mfvAnalysisCutsSigReg     * process.EX1mfvEventHistosSigReg     * process.EX1mfvVertexHistosSigReg)
'''.replace('EX1', EX1).replace('EX2', EX2)

    for name, cut in nm1s:
        evt_cut = ''
        if type(cut) == tuple:
            cut, evt_cut = cut

        vtx = eval('process.mfvSelectedVerticesTight%s.clone(%s)' % (EX1, cut))
        vtx_name = '%svtxNo' % EX1 + name

        for nv in nvs:
            if nv == 0 and (cut != '' or EX1 != ''):
                continue

            ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
            ana.vertex_src = vtx_name
            if nv == 1:
                ana.max_nvertex = nv
            ana.min_nvertex = nv
            ana_name = '%sana%iVNo' % (EX1, nv) + name

            evt_hst = process.mfvEventHistos.clone()
            evt_hst_name = '%sevtHst%iVNo' % (EX1, nv) + name

            vtx_hst = process.mfvVertexHistos.clone(vertex_src = vtx_name)
            vtx_hst_name = '%svtxHst%iVNo' % (EX1, nv) + name

            setattr(process, vtx_name, vtx)
            setattr(process, ana_name, ana)
            setattr(process, evt_hst_name, evt_hst)
            setattr(process, vtx_hst_name, vtx_hst)
            setattr(process, '%sp%iV' % (EX1, nv) + name, cms.Path(process.mfvWeight * vtx * ana * evt_hst * vtx_hst))

if not is_mc:
    for p in process.paths.keys():
        if not (p == 'pSkimSel' or p == 'pEventPreSel' or p == 'Ntk3pOnlyOneVtx' or p.startswith('p0V') or p.startswith('Ntk3p1V')):  # everything but skim/presel and 3-track 1-vertex paths blind
       #if not (p == 'pSkimSel' or p == 'pEventPreSel' or p.startswith('Ntk3') or p.startswith('Ntk4') or p.startswith('p0V')):       # unblinds all 3,4-track sets, keeps 5-track stuff blind
            delattr(process, p)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples 

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017 + Samples.data_samples_2017
        #samples = Samples.ttbar_samples_2017 + Samples.leptonic_samples_2017 + Samples.mfv_signal_samples_2017

    #samples = [s for s in samples if s.has_dataset(dataset)]

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017_1pc.json'))

    cs = CondorSubmitter('HistosV20mp1',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(is_mc_modifier, half_mc_modifier(), per_sample_pileup_weights_modifier()),
                         )
    cs.submit_all(samples)
