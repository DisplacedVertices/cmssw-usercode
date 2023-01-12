from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding
do_track = False # this can onlky be used for ntuple with keep_tk=True

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_MET_triggers
#sample_files(process, 'mfv_neu_tau000300um_M0300_2017' if is_mc else 'JetHT2017B', dataset, 1)
sample_files(process, 'ttbar_2017', dataset, 1) 
max_events(process, 100) 
tfileservice(process, 'histos.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexHistos_cfi')
process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
process.load('JMTucker.MFVNeutralino.TrackHistos_cfi')
process.load('JMTucker.MFVNeutralino.FilterHistos_cfi')
process.load('JMTucker.MFVNeutralino.JetTksHistos_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)

process.mfvEventHistosNoCuts = process.mfvEventHistos.clone()
process.mfvJetTksHistosNoCuts = process.mfvJetTksHistos.clone()
process.mfvFilterHistosNoCuts = process.mfvFilterHistos.clone()
process.mfvVertexHistosNoCuts = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts * process.mfvJetTksHistosNoCuts * process.mfvFilterHistosNoCuts) # just trigger for now
process.pSkimSelVtx = cms.Path(common * process.mfvVertexHistosNoCuts)
if do_track:
  process.mfvTrackHistosNoCuts = process.mfvTrackHistos.clone()
  process.pTrackNoCut = cms.Path(common * process.mfvTrackHistos)

process.mfvEventHistosExtraLoose = process.mfvEventHistos.clone()
process.mfvAnalysisCutsExtraLoose = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesExtraLoose', min_nvertex = 1)
process.mfvVertexHistosExtraLoose = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')
process.pEventExtraLoose = cms.Path(common * process.mfvAnalysisCutsExtraLoose * process.mfvEventHistosExtraLoose)
process.pExtraLoose = cms.Path(common * process.mfvAnalysisCutsExtraLoose * process.mfvVertexHistosExtraLoose)
if do_track:
  process.mfvTrackHistosExtraLoose = process.mfvTrackHistos.clone()
  process.pTrackExtraLoose = cms.Path(common * process.mfvAnalysisCutsExtraLoose * process.mfvTrackHistosExtraLoose)

process.mfvEventHistosExtraLooseOnlyOneVtx = process.mfvEventHistos.clone()
process.mfvAnalysisCutsExtraLooseOnlyOneVtx = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesExtraLoose', min_nvertex = 1, max_nvertex = 1)
process.mfvVertexHistosExtraLooseOnlyOneVtx = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')
process.pEventExtraLooseOnlyOneVtx = cms.Path(common * process.mfvAnalysisCutsExtraLooseOnlyOneVtx * process.mfvEventHistosExtraLooseOnlyOneVtx)
process.pExtraLooseOnlyOneVtx = cms.Path(common * process.mfvAnalysisCutsExtraLooseOnlyOneVtx * process.mfvVertexHistosExtraLooseOnlyOneVtx)

process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel)

nm1s = [
    ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
    ('Bs2derr',    'max_rescale_bs2derr = 1e9'),
    ]

ntks = [5,3,4,7,8,9]
nvs = [0,1,2]

for ntk in ntks:
    if ntk == 5:
        EX1 = EX2 = EX3 = ''
    elif ntk == 7:
        EX1 = 'Ntk3or4'
    elif ntk == 8:
        EX1 = 'Ntk3or5'
    elif ntk == 9:
        EX1 = 'Ntk4or5'
    else:
        EX1 = 'Ntk%i' % ntk

    if EX1:
        EX2 = "vertex_src = 'mfvSelectedVerticesTight%s', " % EX1
    if ntk == 7:
        EX3 = 'min_ntracks01 = 7, max_ntracks01 = 7, '
    if ntk == 8:
        EX3 = 'ntracks01_0 = 5, ntracks01_1 = 3, '
    if ntk == 9:
        EX3 = 'ntracks01_0 = 5, ntracks01_1 = 4, '

    exec '''
process.EX1mfvAnalysisCutsOnlyOneVtx = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, max_nvertex = 1)
process.EX1mfvAnalysisCutsFullSel    = process.mfvAnalysisCuts.clone(EX2EX3)
process.EX1mfvAnalysisCutsSigReg     = process.mfvAnalysisCuts.clone(EX2EX3min_svdist2d = 0.04)

process.EX1mfvEventHistosOnlyOneVtx = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()
process.EX1mfvEventHistosSigReg     = process.mfvEventHistos.clone()

process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosOnlyOneVtx = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosFullSel    = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosSigReg     = process.mfvVertexHistos.clone(EX2)

process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreSel)
process.EX1pOnlyOneVtx = cms.Path(common * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvEventHistosOnlyOneVtx * process.EX1mfvVertexHistosOnlyOneVtx)
'''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)

    if 2 in nvs:
        exec '''
process.EX1pFullSel    = cms.Path(common * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvEventHistosFullSel    * process.EX1mfvVertexHistosFullSel)
process.EX1pSigReg     = cms.Path(common * process.EX1mfvAnalysisCutsSigReg     * process.EX1mfvEventHistosSigReg     * process.EX1mfvVertexHistosSigReg)
'''.replace('EX1', EX1)

#    for ptcut in [30., 40., 50., 60., 65., 70., 75., 80., 85., 90., 100., 110.]:
#        EX4 = 'PtCut%i' % int(ptcut)
#        EX5 = 'btag_pt_cut = ' + str(ptcut)
#        exec ''' 
#process.EX1mfvFilterHistosSigRegEX4   = process.mfvFilterHistos.clone(EX5)
#process.EX1pSigRegEX4     = cms.Path(common * process.EX1mfvAnalysisCutsSigReg      * process.EX1mfvFilterHistosSigRegEX4)
#'''.replace('EX1', EX1).replace('EX4', EX4).replace('EX5', EX5)
#
#    for bs2derrcut in [25., 30., 35., 40., 45., 50., 55., 60., 65., 70., 75.]:
#        name = 'Bs2derr%s' % str(int(bs2derrcut))
#        #lowcut, hicut = str(bs2derrcut/1e4), str((bs2derrcut+5.0)/(1e4))
#        #vtx = eval('process.mfvSelectedVerticesTight%s.clone(min_rescale_bs2derr = %s, max_rescale_bs2derr = %s)' % (EX1, lowcut, hicut))
#        hicut = str(bs2derrcut/1e4)
#        vtx = eval('process.mfvSelectedVerticesTight%s.clone(max_rescale_bs2derr = %s)' % (EX1, hicut))
#        vtx_name = '%svtx' % EX1 + name
#       
#        evt_cut = ''
#
#        for nv in nvs:
#            if nv == 0 and (bs2derrcut != '' or EX1 != ''):
#                continue
#
#            ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
#            ana.vertex_src = vtx_name
#            if nv == 1:
#                ana.max_nvertex = nv
#            ana.min_nvertex = nv
#            if nv == 2 and ntk == 7:
#                ana.min_ntracks01 = ana.max_ntracks01 = 7
#            if nv == 2 and ntk == 8:
#                ana.ntracks01_0 = 5
#                ana.ntracks01_1 = 3
#            if nv == 2 and ntk == 9:
#                ana.ntracks01_0 = 5
#                ana.ntracks01_1 = 4
#            ana_name = '%sana%iV' % (EX1, nv) + name
#
#            evt_hst = process.mfvEventHistos.clone()
#            evt_hst_name = '%sevtHst%iV' % (EX1, nv) + name
#
#            vtx_hst = process.mfvVertexHistos.clone(vertex_src = vtx_name)
#            vtx_hst_name = '%svtxHst%iV' % (EX1, nv) + name
#
#            setattr(process, vtx_name, vtx)
#            setattr(process, ana_name, ana)
#            setattr(process, evt_hst_name, evt_hst)
#            setattr(process, vtx_hst_name, vtx_hst)
#            setattr(process, '%sp%iV' % (EX1, nv) + name, cms.Path(process.mfvWeight * vtx * ana * evt_hst * vtx_hst))


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
            if nv == 2 and ntk == 7:
                ana.min_ntracks01 = ana.max_ntracks01 = 7
            if nv == 2 and ntk == 8:
                ana.ntracks01_0 = 5
                ana.ntracks01_1 = 3
            if nv == 2 and ntk == 9:
                ana.ntracks01_0 = 5
                ana.ntracks01_1 = 4
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


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = Samples.mfv_signal_samples_2017
        #samples = Samples.mfv_stopdbardbar_samples_2017
        #samples = Samples.ttbar_samples_2017 
        #samples = Samples.mfv_stopbbarbbar_samples_2018
        #samples = Samples.qcd_samples_2017 + Samples.ttbar_samples_2017
        #samples = Samples.HToSSTobbbb_samples_2017
        samples = [getattr(Samples, 'ggHToSSTobbbb_tau10mm_M55_2017')]  
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), half_mc_modifier())
    elif use_MET_triggers:
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
        #samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, leptonic=False, splitSUSY=True, Zvv=False, met=False, span_signal=False)
        pset_modifier = chain_modifiers(is_mc_modifier)
    else :
        samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('HistosNoBs2derrNtk3' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
