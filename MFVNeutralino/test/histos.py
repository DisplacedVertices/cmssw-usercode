from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding
do_track = False # this can onlky be used for ntuple with keep_tk=True

<<<<<<< HEAD
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_MET_triggers, use_Muon_triggers, use_Electron_triggers
max_events(process, 1000)
=======
#currently : keep histos slim -> do only Loose Vertices & NoCuts, Minntk = 3, 4, 5 
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_MET_triggers, use_Lepton_triggers

>>>>>>> UL_Lepton
tfileservice(process, 'histos.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexHistos_cfi')
process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
process.load('JMTucker.MFVNeutralino.TrackHistos_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.CutFlowHistos_cfi')

#process.load('JMTucker.MFVNeutralino.CutFlowHistos_cfi')
import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)
common_a = cms.Sequence(process.mfvWeight)

process.mfvEventHistosNoCuts = process.mfvEventHistos.clone()
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts) # just trigger for now

process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel)

process.mfvVertexHistosNoCuts = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts) # just trigger for now
process.pSkimSelVtx = cms.Path(common * process.mfvVertexHistosNoCuts)
if do_track:
  process.mfvTrackHistosNoCuts = process.mfvTrackHistos.clone()
  process.pTrackNoCut = cms.Path(common * process.mfvTrackHistos)

# process.mfvEventHistosExtraLoose = process.mfvEventHistos.clone()
# process.mfvAnalysisCutsExtraLoose = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesExtraLoose', min_nvertex = 1)
# process.mfvVertexHistosExtraLoose = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')
# process.pEventExtraLoose = cms.Path(common * process.mfvAnalysisCutsExtraLoose * process.mfvEventHistosExtraLoose)
# process.pExtraLoose = cms.Path(common * process.mfvAnalysisCutsExtraLoose * process.mfvVertexHistosExtraLoose)

# process.mfvEventHistosLoose = process.mfvEventHistos.clone()
# process.mfvAnalysisCutsLoose = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesLoose')
# process.mfvVertexHistosLoose = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesLoose')
# process.pEventLoose = cms.Path(common * process.mfvAnalysisCutsLoose * process.mfvEventHistosLoose)
# process.pLoose = cms.Path(common * process.mfvAnalysisCutsLoose * process.mfvVertexHistosLoose)
# if do_track:
#   process.mfvTrackHistosExtraLoose = process.mfvTrackHistos.clone()
#   process.pTrackExtraLoose = cms.Path(common * process.mfvAnalysisCutsExtraLoose * process.mfvTrackHistosExtraLoose)

#process.mfvEventHistosExtraLooseOnlyOneVtx = process.mfvEventHistos.clone()
#process.mfvAnalysisCutsExtraLooseOnlyOneVtx = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesExtraLoose', min_nvertex = 1, max_nvertex = 1)
#process.mfvVertexHistosExtraLooseOnlyOneVtx = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')

#process.mfvAnaCutFlowHistos = process.mfvCutFlowHistos.clone()

#process.pEventExtraLooseOnlyOneVtx = cms.Path(common * process.mfvAnalysisCutsExtraLooseOnlyOneVtx * process.mfvEventHistosExtraLooseOnlyOneVtx)
#process.pExtraLooseOnlyOneVtx = cms.Path(common * process.mfvAnalysisCutsExtraLooseOnlyOneVtx * process.mfvVertexHistosExtraLooseOnlyOneVtx)

#process.pCutFlow = cms.Path(common_a * process.mfvAnaCutFlowHistos)

#process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
#process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
#process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel)

nm1s = [
    ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
    ('Bs2derr',    'max_rescale_bs2derr = 1e9'),
    ]

ntks = [] #5,3,4,7,8,9]
nvs = [] #0,1,2]

# new setup for lepton : min3, min4, min5 with 'Loose' Vertices 
for ntk in ntks : 
    if ntk == 5: 
        EX1 = '' 
    else : 
        EX1 = 'MinNtk%i' % ntk 
    EX2 = "vertex_src = 'mfvSelectedVerticesLoose%s', " % EX1
    EX3 = ''
## Done 


# for ntk in ntks:
#     if ntk == 5:
#         EX1 = EX2 = EX3 = ''
#     # elif ntk == 7:
#     #     EX1 = 'Ntk3or4'
#     # elif ntk == 8:
#     #     EX1 = 'Ntk3or5'
#     # elif ntk == 9:
#     #     EX1 = 'Ntk4or5'
#     # else:
#     #     EX1 = 'Ntk%i' % ntk

#     ## changed this to be min ntk 3
#     else:
#       if ntk == 3:
#         EX1 = 'MinNtk3'
#       else: 
#         EX1 = 'MinNtk%i' % ntk

#     if EX1:
#         EX2 = "vertex_src = 'mfvSelectedVerticesLoose%s', " % EX1
#         print EX2
#     if ntk == 7:
#         EX3 = 'min_ntracks01 = 7, max_ntracks01 = 7, '
#     if ntk == 8:
#         EX3 = 'ntracks01_0 = 5, ntracks01_1 = 3, '
#     if ntk == 9:
#         EX3 = 'ntracks01_0 = 5, ntracks01_1 = 4, '

#     exec '''
# process.EX1mfvAnalysisCutsOnlyOneVtx = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, max_nvertex = 1)
# process.EX1mfvAnalysisCutsFullSel    = process.mfvAnalysisCuts.clone(EX2EX3)
# process.EX1mfvAnalysisCutsSigReg     = process.mfvAnalysisCuts.clone(EX2EX3min_svdist2d = 0.04)

# process.EX1mfvEventHistosOnlyOneVtx = process.mfvEventHistos.clone()
# process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()
# process.EX1mfvEventHistosSigReg     = process.mfvEventHistos.clone()

# process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2)
# process.EX1mfvVertexHistosOnlyOneVtx = process.mfvVertexHistos.clone(EX2)
# process.EX1mfvVertexHistosFullSel    = process.mfvVertexHistos.clone(EX2)
# process.EX1mfvVertexHistosSigReg     = process.mfvVertexHistos.clone(EX2)

# process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreRSel)
# process.EX1pOnlyOneVtx = cms.Path(common * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvEventHistosOnlyOneVtx * process.EX1mfvVertexHistosOnlyOneVtx)
# '''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)

#     if 2 in nvs:
#         exec '''
# process.EX1pFullSel    = cms.Path(common * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvEventHistosFullSel    * process.EX1mfvVertexHistosFullSel)
# process.EX1pSigReg     = cms.Path(common * process.EX1mfvAnalysisCutsSigReg     * process.EX1mfvEventHistosSigReg     * process.EX1mfvVertexHistosSigReg)
# '''.replace('EX1', EX1)

    exec '''
process.EX1mfvAnalysisCutsOnlyOneVtx = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, max_nvertex = 1)
process.EX1mfvAnalysisCutsFullSel    = process.mfvAnalysisCuts.clone(EX2EX3)
process.EX1mfvAnalysisCutsTestSel    = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, require_displaced_lepton = True)

process.EX1mfvEventHistosOnlyOneVtx = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()
process.EX1mfvEventHistosTestSel    = process.mfvEventHistos.clone()

process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesLoose')
process.EX1mfvVertexHistosOnlyOneVtx = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosTestSel    = process.mfvVertexHistos.clone(EX2)

process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreSel)
process.EX1pTestSel    = cms.Path(common * process.EX1mfvAnalysisCutsTestSel    * process.EX1mfvEventHistosTestSel    * process.EX1mfvVertexHistosTestSel)
'''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)

    if 2 in nvs:
        exec '''
process.EX1pFullSel    = cms.Path(common * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvEventHistosFullSel    * process.EX1mfvVertexHistosFullSel)
'''.replace('EX1', EX1)

    for name, cut in nm1s:
        evt_cut = ''
        if type(cut) == tuple:
            cut, evt_cut = cut

        vtx = eval('process.mfvSelectedVerticesLoose%s.clone(%s)' % (EX1, cut))
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
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=True, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), half_mc_modifier())
    elif use_MET_triggers:
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
<<<<<<< HEAD
        pset_modifier = chain_modifiers(is_mc_modifier)
    elif use_Muon_triggers :
        samples = pick_samples(dataset, qcd=True, all_signal=False, qcd_lep = True, leptonic=True, met=True, diboson=True, Lepton_data=False )
        pset_modifier = chain_modifiers(is_mc_modifier, half_mc_modifier())
    elif use_Electron_triggers :
        samples = pick_samples(dataset, qcd=True, all_signal=False, qcd_lep = True, leptonic=True, met=True, diboson=True, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, half_mc_modifier())
=======
    elif use_Lepton_triggers : 
        samples = pick_samples(dataset, qcd=False, all_signal=False, qcd_lep = True, leptonic=False, met=False, diboson=False, Lepton_data=False )
        pset_modifier = chain_modifiers(is_mc_modifier)
>>>>>>> UL_Lepton
    else :
        samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_SingleLept_2017_10pc.json'))

    cs = CondorSubmitter('Histos' + version + '_SingleLep',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
