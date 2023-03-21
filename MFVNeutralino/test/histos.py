from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding
do_track = True # this can only be used for ntuple with keep_tk=True

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_MET_triggers
sample_files(process, 'mfv_neu_tau010000um_M0300_2017' if is_mc else 'JetHT2017B', dataset, 10)
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
#process.mfvVertexHistosNoCuts = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')
#process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts) # just trigger for now
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts * process.mfvJetTksHistosNoCuts) # just trigger for now
#process.pSkimSelVtx = cms.Path(common * process.mfvVertexHistosNoCuts)
if do_track:
  process.mfvTrackHistosNoCuts = process.mfvTrackHistos.clone()
  process.mfvFilterHistosNoCuts = process.mfvFilterHistos.clone()
  process.pTrackNoCut = cms.Path(common * process.mfvTrackHistos * process.mfvFilterHistosNoCuts)

process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
process.mfvFilterHistosPreSel = process.mfvFilterHistos.clone()
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel * process.mfvFilterHistosPreSel)

process.mfvFilterHistosPreSelDiBjet = process.mfvFilterHistos.clone()
process.mfvAnalysisCutsPreSelDiBjet = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False, trigbit_tostudy = 8,    calo_seed_threshold = 4, calo_prompt_threshold = 4)
process.pEventPreSelDiBjet = cms.Path(common * process.mfvAnalysisCutsPreSelDiBjet * process.mfvFilterHistosPreSelDiBjet)

process.mfvFilterHistosPreSelTriBjet = process.mfvFilterHistos.clone()
process.mfvAnalysisCutsPreSelTriBjet = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False, trigbit_tostudy = 9,    calo_seed_threshold = 4, calo_prompt_threshold = 4)
process.pEventPreSelTriBjet = cms.Path(common * process.mfvAnalysisCutsPreSelTriBjet * process.mfvFilterHistosPreSelTriBjet)

process.mfvFilterHistosPreSelLowHT = process.mfvFilterHistos.clone()
process.mfvAnalysisCutsPreSelLowHT = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False, trigbit_tostudy = 18,    calo_seed_threshold = 4, calo_prompt_threshold = 4)
process.pEventPreSelLowHT = cms.Path(common * process.mfvAnalysisCutsPreSelLowHT * process.mfvFilterHistosPreSelLowHT)

process.mfvFilterHistosPreSelHighHT = process.mfvFilterHistos.clone()
process.mfvAnalysisCutsPreSelHighHT = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False, trigbit_tostudy = 19,    calo_seed_threshold = 4, calo_prompt_threshold = 4)
process.pEventPreSelHighHT = cms.Path(common * process.mfvAnalysisCutsPreSelHighHT * process.mfvFilterHistosPreSelHighHT)

nm1s = []
#    ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
#    ('Bs2derr',    'max_rescale_bs2derr = 1e9'),
#    ]

ntks = [5,]#,3,4,7,8,9]
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
    
#    for nseed in [0, 1, 2, 3, 4, 5, 6]:
#        if (ntk != 5):
#            continue
#        
#        ana = process.mfvAnalysisCuts.clone()
#        ana.require_trigbit = True
#        ana.calo_seed_threshold = nseed
#        ana.calo_prompt_threshold = 9999
#        ana_name = 'anaCaloSeed%iNum' % (nseed)
#
#        vtx = process.mfvSelectedVerticesTight.clone()
#        vtx_hst = process.mfvVertexHistos.clone()
#        vtx_hst_name = 'vtxHstCaloSeed%iNum' % (nseed)
#
#        setattr(process, 'test', vtx)
#        setattr(process, ana_name, ana)
#        setattr(process, vtx_hst_name, vtx_hst)
#        setattr(process, 'caloSeed%iNum' % (nseed), cms.Path(process.mfvWeight * vtx * ana * vtx_hst))
#
#    for nseed in [0, 1, 2, 3, 4, 5, 6]:
#        if (ntk != 5):
#            continue
#        
#        ana = process.mfvAnalysisCuts.clone()
#        ana.calo_seed_threshold = nseed
#        ana.calo_prompt_threshold = 9999
#        ana.require_trigbit = False
#        ana_name = 'anaCaloSeed%iDen' % (nseed)
#
#        vtx = process.mfvSelectedVerticesTight.clone()
#        vtx_hst = process.mfvVertexHistos.clone()
#        vtx_hst_name = 'vtxHstCaloSeed%iDen' % (nseed)
#
#        setattr(process, 'test', vtx)
#        setattr(process, ana_name, ana)
#        setattr(process, vtx_hst_name, vtx_hst)
#        setattr(process, 'caloSeed%iDen' % (nseed), cms.Path(process.mfvWeight * vtx * ana * vtx_hst))

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017
        #samples = Samples.HToSSTodddd_samples_2017 + Samples.mfv_signal_samples_2017
        #samples = Samples.mfv_stopdbardbar_samples_2017
        samples = Samples.mfv_signal_samples_lowmass_2017# + Samples.HToSSTodddd_samples_2017
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_MET_triggers:
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
        #samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, leptonic=False, splitSUSY=True, Zvv=False, met=False, span_signal=False)
        pset_modifier = chain_modifiers(is_mc_modifier)
    else :
        samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('Histos' + version + '_ughJetTkHists',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
