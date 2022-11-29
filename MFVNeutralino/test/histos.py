from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers
sample_files(process, 'ggHToSSTodddd_tau1mm_M40_2017' if is_mc else 'JetHT2017B', 'ntuplev31am', 5)
#sample_files(process, 'ggHToSSTodddd_tau1mm_M55_2017' if is_mc else 'JetHT2017B', 'ntuplev31am', 15)
#sample_files(process, 'mfv_neu_tau001000um_M0400_2017' if is_mc else 'JetHT2017B', 'ntuplev30am', 10)
#sample_files(process, 'ttbar_2017' if is_mc else 'JetHT2017B', 'ntuplev31am', 5)
tfileservice(process, 'histos.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexHistos_cfi')
process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
process.load('JMTucker.MFVNeutralino.FilterHistos_cfi')
process.load('JMTucker.MFVNeutralino.JetTksHistos_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)

process.mfvFilterHistosNoCuts = process.mfvFilterHistos.clone()
process.mfvJetTksHistosNoCuts = process.mfvJetTksHistos.clone()
process.mfvEventHistosNoCuts  = process.mfvEventHistos.clone()

process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts) # just trigger for now
#process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts * process.mfvFilterHistosNoCuts) # just trigger for now
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts * process.mfvFilterHistosNoCuts * process.mfvJetTksHistosNoCuts) # just trigger for now

process.mfvEventHistosPreSel  = process.mfvEventHistos.clone()
process.mfvFilterHistosPreSel = process.mfvFilterHistos.clone()
process.mfvJetTksHistosPreSel = process.mfvJetTksHistos.clone()
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel * process.mfvFilterHistosPreSel * process.mfvJetTksHistosNoCuts)

nm1s = [
    ('Bs2derr',    'max_rescale_bs2derr = 1e9'),
    ]

nm1s = []

ntks = [5,]#3,4]#,7,8,9]
nvs = [1,2]
#nvs = [0,1,2]

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
process.EX1mfvAnalysisCutsFullSel    = process.mfvAnalysisCuts.clone(EX2min_nvertex = 2, max_nvertex = 20)
process.EX1mfvAnalysisCutsSigReg     = process.mfvAnalysisCuts.clone(EX2EX3min_svdist2d = 0.04)

process.EX1mfvEventHistosOnlyOneVtx = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()
process.EX1mfvEventHistosSigReg     = process.mfvEventHistos.clone()

process.EX1mfvFilterHistosOnlyOneVtx = process.mfvFilterHistos.clone()
process.EX1mfvFilterHistosFullSel    = process.mfvFilterHistos.clone()
process.EX1mfvFilterHistosSigReg     = process.mfvFilterHistos.clone()

process.EX1mfvJetTksHistosOnlyOneVtx = process.mfvJetTksHistos.clone()
process.EX1mfvJetTksHistosFullSel    = process.mfvJetTksHistos.clone()
process.EX1mfvJetTksHistosSigReg     = process.mfvJetTksHistos.clone()

process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosOnlyOneVtx = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosFullSel    = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosSigReg     = process.mfvVertexHistos.clone(EX2)

process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreSel)
process.EX1pOnlyOneVtx = cms.Path(common * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvEventHistosOnlyOneVtx * process.EX1mfvFilterHistosOnlyOneVtx * process.EX1mfvJetTksHistosOnlyOneVtx * process.EX1mfvVertexHistosOnlyOneVtx)
'''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)

    if 2 in nvs:
    #if False:
        exec '''
process.EX1pFullSel    = cms.Path(common * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvEventHistosFullSel    * process.EX1mfvFilterHistosFullSel    * process.EX1mfvJetTksHistosFullSel * process.EX1mfvVertexHistosFullSel)
process.EX1pSigReg     = cms.Path(common * process.EX1mfvAnalysisCutsSigReg     * process.EX1mfvEventHistosSigReg     * process.EX1mfvFilterHistosSigReg     * process.EX1mfvJetTksHistosSigReg  * process.EX1mfvVertexHistosSigReg)
'''.replace('EX1', EX1)

    for bs2derrcut in [25., 30., 35., 40., 45., 50., 55., 60., 65., 70., 75.]:
        name = 'Bs2derr%s' % str(int(bs2derrcut))
        hicut = str(bs2derrcut/1e4)
        vtx = eval('process.mfvSelectedVerticesTight%s.clone(max_rescale_bs2derr = %s)' % (EX1, hicut))
        vtx_name = '%svtx' % EX1 + name
       
        evt_cut = ''

        for nv in nvs:
            if nv == 0 and (hicut != '' or EX1 != ''):
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
            ana_name = '%sana%iV' % (EX1, nv) + name

            evt_hst = process.mfvEventHistos.clone()
            evt_hst_name = '%sevtHst%iV' % (EX1, nv) + name

            vtx_hst = process.mfvVertexHistos.clone(vertex_src = vtx_name)
            vtx_hst_name = '%svtxHst%iV' % (EX1, nv) + name

            setattr(process, vtx_name, vtx)
            setattr(process, ana_name, ana)
            setattr(process, evt_hst_name, evt_hst)
            setattr(process, vtx_hst_name, vtx_hst)
            setattr(process, '%sp%iV' % (EX1, nv) + name, cms.Path(process.mfvWeight * vtx * ana * evt_hst * vtx_hst))

#    for name, cut in nm1s:
#        evt_cut = ''
#        if type(cut) == tuple:
#            cut, evt_cut = cut
#
#        vtx = eval('process.mfvSelectedVerticesTight%s.clone(%s)' % (EX1, cut))
#        vtx_name = '%svtxNo' % EX1 + name
#
#        for nv in nvs:
#            if nv == 0 and (cut != '' or EX1 != ''):
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
#            ana_name = '%sana%iVNo' % (EX1, nv) + name
#
#            evt_hst = process.mfvEventHistos.clone()
#            evt_hst_name = '%sevtHst%iVNo' % (EX1, nv) + name
#
#            vtx_hst = process.mfvVertexHistos.clone(vertex_src = vtx_name)
#            vtx_hst_name = '%svtxHst%iVNo' % (EX1, nv) + name
#
#            setattr(process, vtx_name, vtx)
#            setattr(process, ana_name, ana)
#            setattr(process, evt_hst_name, evt_hst)
#            setattr(process, vtx_hst_name, vtx_hst)
#            setattr(process, '%sp%iV' % (EX1, nv) + name, cms.Path(process.mfvWeight * vtx * ana * evt_hst * vtx_hst))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples =  Samples.HToSSTodddd_samples_2017# + Samples.mfv_signal_samples_2017
        #samples =  Samples.bjet_samples_2017
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    else :
        #samples = pick_samples(dataset)
        samples = Samples.bjet_samples_2017
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('HistosV31_nobs2derrFix',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
