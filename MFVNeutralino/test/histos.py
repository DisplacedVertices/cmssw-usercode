from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding
do_track = False # this can only be used for ntuple with keep_tk=True
do_uncert_suite = True # set to True to make all necessary portions of the total trigger uncert study

# 0 = ALL  1 = GoodJets  2 = WeirdJets  3 = BadJets  4 = AltWeirdJets (false positive)
calo_cat = 0
jth_trig = False
jth_study_tagged = False
jth_study_untagged = False

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_MET_triggers
#sample_files(process, 'ttbar_2017' if is_mc else 'SingleMuon2017C', dataset, 1)
#sample_files(process, 'mfv_neu_tau010000um_M0400_2017' if is_mc else 'SingleMuon2017C', dataset, 10)
sample_files(process, 'ttbar_2018', dataset, 1)
tfileservice(process, 'histos.root')
global_tag(process)
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
process.mfvFilterHistosNoCuts = process.mfvFilterHistos.clone()
process.mfvVertexHistosNoCuts = process.mfvVertexHistos.clone()
process.mfvJetTksHistosNoCuts = process.mfvJetTksHistos.clone(require_gen_sumdbv = False, study_hlt_tagged_jets = jth_study_tagged, study_hlt_nontagged_jets = jth_study_untagged, pt_lo_for_tag_probe = 100.0, study_hlt_btagging = False)
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts * process.mfvVertexHistosNoCuts * process.mfvJetTksHistosNoCuts * process.mfvFilterHistosNoCuts) # just trigger for now

process.mfvJetTksHistosNominal = process.mfvJetTksHistos.clone(require_gen_sumdbv = False, study_hlt_tagged_jets = False, study_hlt_nontagged_jets = False, pt_lo_for_tag_probe = 30.0)
process.pJetTksHistsNominal = cms.Path(common * process.mfvJetTksHistosNominal)

if do_uncert_suite:
    # AnalysisCuts ONLY considers the low-HT dispalced dijet trigger
    process.mfvAnalysisCutsLowHTPreSel = process.mfvAnalysisCuts.clone(trigbit_tostudy = 18, apply_vertex_cuts = False, require_trigbit = False)
    process.mfvFilterHistosLowHTPreSel = process.mfvFilterHistos.clone()
    process.mfvJetTksHistosLowHtNominal   = process.mfvJetTksHistos.clone(calojet_category = calo_cat, require_triggers = False, trigger_bit = 18, do_tk_filt_refactor = False)
    process.mfvJetTksHistosLowHtRefactor  = process.mfvJetTksHistos.clone(calojet_category = calo_cat, require_triggers = False, trigger_bit = 18, do_tk_filt_refactor = True)
    process.mfvJetTksHistosLowHtRefactor2 = process.mfvJetTksHistos.clone(calojet_category = calo_cat, require_triggers = False, trigger_bit = 18, do_tk_filt_refactor = True, study_offline_dxy_res = True)
    process.pEventLowHTPreSel = cms.Path(common * process.mfvAnalysisCutsLowHTPreSel * process.mfvJetTksHistosLowHtNominal * process.mfvFilterHistosLowHTPreSel * process.mfvJetTksHistosLowHtRefactor * process.mfvJetTksHistosLowHtRefactor2)
    
    # AnalysisCuts ONLY considers the High-HT displaced dijet trigger
    process.mfvAnalysisCutsHighHTPreSel = process.mfvAnalysisCuts.clone(trigbit_tostudy = 19, apply_vertex_cuts = False, require_trigbit = False)
    process.mfvFilterHistosHighHTPreSel = process.mfvFilterHistos.clone()
    process.pEventHighHTPreSel = cms.Path(common * process.mfvAnalysisCutsHighHTPreSel * process.mfvFilterHistosHighHTPreSel)

    # AnalysisCuts remains agnostic to the displaced dijet selection, trigger bits required
    process.mfvAnalysisCutsDijetAgnosticTrigOn = process.mfvAnalysisCuts.clone(dijet_agnostic = True)
    process.mfvEventHistosDijetAgnosticTrigOn  = process.mfvEventHistos.clone()
    process.pDijetAgnosticTrigOn = cms.Path(common * process.mfvAnalysisCutsDijetAgnosticTrigOn * process.mfvEventHistosDijetAgnosticTrigOn)

    # AnalysisCuts remains agnostic to the displaced dijet selection, trigger bits required, btag SF variations applied
    process.mfvAnalysisCutsDijetAgnosticTrigOnSFVarUp = process.mfvAnalysisCuts.clone(dijet_agnostic = True, study_btag_sf = True, study_btag_sfvar =  1)
    process.mfvAnalysisCutsDijetAgnosticTrigOnSFVarDn = process.mfvAnalysisCuts.clone(dijet_agnostic = True, study_btag_sf = True, study_btag_sfvar = -1)
    process.mfvEventHistosDijetAgnosticTrigOnSFVarUp  = process.mfvEventHistos.clone()
    process.mfvEventHistosDijetAgnosticTrigOnSFVarDn  = process.mfvEventHistos.clone()
    process.pDijetAgnosticTrigOnSFVarUp = cms.Path(common * process.mfvAnalysisCutsDijetAgnosticTrigOnSFVarUp * process.mfvEventHistosDijetAgnosticTrigOnSFVarUp)
    process.pDijetAgnosticTrigOnSFVarDn = cms.Path(common * process.mfvAnalysisCutsDijetAgnosticTrigOnSFVarDn * process.mfvEventHistosDijetAgnosticTrigOnSFVarDn)
    
    # AnalysisCuts remains agnostic to the displaced dijet selection, trigger bits TURNED OFF
    process.mfvAnalysisCutsDijetAgnosticTrigOff = process.mfvAnalysisCuts.clone(dijet_agnostic = True, require_trigbit = False)
    process.mfvEventHistosDijetAgnosticTrigOff  = process.mfvEventHistos.clone()
    process.mfvJetTksHistosHLTBtagStudyVar      = process.mfvJetTksHistos.clone(require_triggers = False, study_hlt_btagging = True)
    process.mfvJetTksHistosHLTBtagStudyNom      = process.mfvJetTksHistos.clone(require_triggers = False, study_hlt_btagging = False)
    process.pDijetAgnosticTrigOff = cms.Path(common * process.mfvAnalysisCutsDijetAgnosticTrigOff * process.mfvEventHistosDijetAgnosticTrigOff * process.mfvJetTksHistosHLTBtagStudyVar * process.mfvJetTksHistosHLTBtagStudyNom)

if do_track:
  process.mfvTrackHistosNoCuts = process.mfvTrackHistos.clone()
  process.pTrackNoCut = cms.Path(common * process.mfvTrackHistos * process.mfvFilterHistosNoCuts)


process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
process.mfvVertexHistosPreSel = process.mfvVertexHistos.clone()
process.mfvFilterHistosPreSel = process.mfvFilterHistos.clone()
process.mfvJetTksHistosPreSel = process.mfvJetTksHistos.clone(require_gen_sumdbv = False)
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False, require_trigbit = False)
process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel * process.mfvVertexHistosPreSel * process.mfvJetTksHistosPreSel * process.mfvFilterHistosPreSel)

nm1s = []
#    ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
#    ('Bs2derr',    'max_rescale_bs2derr = 1e9'),
#    ]

ntks = [5,]#,3,4,7,8,9]
#nvs = [0,1,2]
nvs = [2,]
#ntks = []
#nvs = []

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
process.EX1mfvAnalysisCutsOnlyOneVtx      = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, max_nvertex = 1)
process.EX1mfvAnalysisCutsVtxSelOnly      = process.mfvAnalysisCuts.clone(EX2EX3apply_presel = 0)
process.EX1mfvAnalysisCutsFullSel         = process.mfvAnalysisCuts.clone(EX2EX3)
process.EX1mfvAnalysisCutsFullSelUpJER    = process.mfvAnalysisCuts.clone(EX2EX3study_jer = True, jes_jer_var_up = True)
process.EX1mfvAnalysisCutsFullSelDnJER    = process.mfvAnalysisCuts.clone(EX2EX3study_jer = True, jes_jer_var_up = False)
process.EX1mfvAnalysisCutsFullSelUpJES    = process.mfvAnalysisCuts.clone(EX2EX3study_jes = True, jes_jer_var_up = True)
process.EX1mfvAnalysisCutsFullSelDnJES    = process.mfvAnalysisCuts.clone(EX2EX3study_jes = True, jes_jer_var_up = False)
process.EX1mfvAnalysisCutsFullSelDijetAgnostic = process.mfvAnalysisCuts.clone(EX2EX3dijet_agnostic = True)
process.EX1mfvAnalysisCutsFullSelBjetAgnostic  = process.mfvAnalysisCuts.clone(EX2EX3bjet_agnostic = True)
process.EX1mfvAnalysisCutsSigReg          = process.mfvAnalysisCuts.clone(EX2EX3min_svdist2d = 0.04)

process.EX1mfvEventHistosOnlyOneVtx      = process.mfvEventHistos.clone()
process.EX1mfvEventHistosVtxSelOnly      = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSel         = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSelUpJER    = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSelDnJER    = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSelUpJES    = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSelDnJES    = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSelDijetAgnostic        = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSelBjetAgnostic         = process.mfvEventHistos.clone()
process.EX1mfvEventHistosSigReg          = process.mfvEventHistos.clone()

process.EX1mfvVertexHistosPreSel          = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosOnlyOneVtx      = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosVtxSelOnly      = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosFullSel         = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosSigReg          = process.mfvVertexHistos.clone(EX2)

process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreSel)
process.EX1pOnlyOneVtx = cms.Path(common * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvEventHistosOnlyOneVtx * process.EX1mfvVertexHistosOnlyOneVtx)
'''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)

    if 2 in nvs:
        exec '''
process.EX1pVtxSelOnly  = cms.Path(common * process.EX1mfvAnalysisCutsVtxSelOnly  * process.EX1mfvEventHistosVtxSelOnly  * process.EX1mfvVertexHistosVtxSelOnly)
process.EX1pFullSel     = cms.Path(common * process.EX1mfvAnalysisCutsFullSel     * process.EX1mfvEventHistosFullSel     * process.EX1mfvVertexHistosFullSel)
process.EX1pFullSelUpJER = cms.Path(common * process.EX1mfvAnalysisCutsFullSelUpJER   *   process.EX1mfvEventHistosFullSelUpJER)
process.EX1pFullSelDnJER = cms.Path(common * process.EX1mfvAnalysisCutsFullSelDnJER   *   process.EX1mfvEventHistosFullSelDnJER)
process.EX1pFullSelUpJES = cms.Path(common * process.EX1mfvAnalysisCutsFullSelUpJES   *   process.EX1mfvEventHistosFullSelUpJES)
process.EX1pFullSelDnJES = cms.Path(common * process.EX1mfvAnalysisCutsFullSelDnJES   *   process.EX1mfvEventHistosFullSelDnJES)
process.EX1pFullSelDijetAgnostic = cms.Path(common * process.EX1mfvAnalysisCutsFullSelDijetAgnostic    * process.EX1mfvEventHistosFullSelDijetAgnostic)
process.EX1pFullSelBjetAgnostic  = cms.Path(common * process.EX1mfvAnalysisCutsFullSelBjetAgnostic     * process.EX1mfvEventHistosFullSelBjetAgnostic)
process.EX1pSigReg      = cms.Path(common * process.EX1mfvAnalysisCutsSigReg      * process.EX1mfvEventHistosSigReg      * process.EX1mfvVertexHistosSigReg)
'''.replace('EX1', EX1)

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
        #samples = Samples.ttbar_alt_samples_2017
        #samples = Samples.ttbar_samples_2018 + Samples.SingleMuon_data_samples_2018
        samples = Samples.mfv_signal_samples_temp_2017 + Samples.mfv_stopdbardbar_samples_temp_2017 + Samples.mfv_stopbbarbbar_samples_temp_2017 + Samples.HToSSTodddd_samples_2017
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_MET_triggers:
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
        #samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, leptonic=False, splitSUSY=True, Zvv=False, met=False, span_signal=False)
        pset_modifier = chain_modifiers(is_mc_modifier)
    else :
        samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('Histos' + version + '_BestUncerts_2017_Dec01',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
