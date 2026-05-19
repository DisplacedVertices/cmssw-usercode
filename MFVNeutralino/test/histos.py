from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding
study_20pc = True

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_Lepton_triggers, use_btag_triggers, use_btag_vetoLepHT_triggers, use_Muon_triggers, use_Electron_triggers
#sample_files(process, 'qcdht2000_2017' if is_mc else 'JetHT2017B', dataset, 1)
#input_files(process, '/store/group/lpclonglived/pkotamni/ggH_HToSSTodddd_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleOnnormdzULV30Bm_NoEF_20161/250122_131504/0000/ntuple_0.root')
#input_files(process, '/store/group/lpclonglived/pkotamni/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleOnnormdzULV30Lepm_2017/250101_200106/0000/ntuple_0.root')
input_files(process, '/uscms/home/pkotamni/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/ntuple.root')

tfileservice(process, 'histos.root')
cmssw_from_argv(process)

# Hack to get around weird vertexing bug in WminusHToSSTodddd_tau10mm_M40_20162 - Uncomment when running this point
'''
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    SkipEvent = cms.untracked.vstring("ProductNotFound"),
)

# Explicitly skip the bad event (run:lumi:event)
process.source.eventsToSkip = cms.untracked.VEventRange("1:1:189")
'''

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexHistos_cfi')
process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
#process.load('JMTucker.MFVNeutralino.FilterHistos_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)

# If we want these, we should at minimum make use of the Ntk criteria (to avoid accidentally looking at presel plots w/ 5-tracks per vertex before unblinding).
# I think (but have not dug to confirm) that "presel" includes the AnalysisCuts w/o any vertex cuts while "no cuts" is purely the event filter + possibly trigger
#process.mfvEventHistosNoCuts = process.mfvEventHistos.clone()
#process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts ) # just trigger for now
#
#process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False) # (used by "process.EX1pPreSel" below)
#process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel)

nm1s = [
    ('Ntracks', 'min_ntracks = 0'),
    ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
    ('Bs2derr',    'max_rescale_bs2derr = 1e9'),
    ]

ntks = [5,3,4,7,8,9]
nvs = [0,1,2]

# blind data events with >= 4 tracks per vertex until we're ready
if not is_mc :
    ntks = [3]
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
        EX3 = ''

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

process.EX1mfvEventHistosOnlyOneVtx = process.mfvEventHistos.clone()
process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()

process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosOnlyOneVtx = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosFullSel    = process.mfvVertexHistos.clone(EX2)

process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel * process.EX1mfvVertexHistosPreSel)
process.EX1pOnlyOneVtx = cms.Path(common * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvEventHistosOnlyOneVtx * process.EX1mfvVertexHistosOnlyOneVtx)
'''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)

    if 2 in nvs:
        exec '''
process.EX1pFullSel    = cms.Path(common * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvEventHistosFullSel    * process.EX1mfvVertexHistosFullSel)
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
            if nv == 1 : 
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

    if use_Muon_triggers or use_Electron_triggers :
        sys.exit('In histos.py, use_Muon_triggers and use_Electron_triggers should not be used (they are only needed for the MiniAOD -> ntuple step). Instead, do use_Lepton_triggers.')

    if  use_btag_vetoLepHT_triggers:
        if is_mc :
            samples = pick_samples(dataset, all_bjet_signal=True, qcd=True, ttbar=True)
            pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), ttH_duplicate_check_modifier)
        else :
            samples = pick_samples(dataset, BTagCSV_data=True, DisplacedJet_data=True)
            pset_modifier = None

    elif use_Lepton_triggers :
        if is_mc :
            samples = pick_samples(dataset, all_lep_signal=True, qcd_lep=True, leptonic=True, ttbar=True, diboson=True)
            pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), ttH_duplicate_check_modifier)
        else :
            samples = pick_samples(dataset, Muon_data=True, Electron_data=True)
            pset_modifier = None

    else :
        print 'trigger scenario not set properly in minitree.py, please double check! Submitting some jobs nonetheless...'
        samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, splitSUSY=True)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), ttH_duplicate_check_modifier)

    json_filename = 'ana_run2_displacement_trigger.json' if use_btag_vetoLepHT_triggers else 'ana_run2.json'
    if study_20pc : 
        json_filename = json_filename.replace(".json", "_20pc.json")
    print "json file is:", json_filename

    set_splitting(samples, dataset, 'histos', data_json=json_path(json_filename))

    cs = CondorSubmitter('Histos' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
