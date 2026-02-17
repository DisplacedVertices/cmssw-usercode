from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_Lepton_triggers, use_btag_triggers, use_btag_vetoLepHT_triggers 
#input_files(process, "root://cmsxrootd-site.fnal.gov//store/user/gdecastr/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/Ntuple_Table28Validation_2016APV_Lepm_NoEF_2018/260130_183335//0000/ntuple_1.root")
#sample_files(process, 'qcdht2000_2017' if is_mc else 'JetHT2017B', dataset, 1)
#input_files(process, '/store/group/lpclonglived/pkotamni/ggH_HToSSTodddd_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleOnnormdzULV30Bm_NoEF_20161/250122_131504/0000/ntuple_0.root')
#input_files(process, '/store/group/lpclonglived/pkotamni/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleOnnormdzULV30Lepm_2017/250101_200106/0000/ntuple_0.root')
#input_files(process, '/uscms/home/pkotamni/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/ntuple.root')

tfileservice(process, 'histos.root')
cmssw_from_argv(process)

# Hack to get around weird vertexing bug in WminusHToSSTodddd_tau10mm_M40_20162
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

#process.mfvFilterHistosNoCuts = process.mfvFilterHistos.clone()

process.mfvEventHistosNoCuts = process.mfvEventHistos.clone()
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts ) # just trigger for now

process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel)

############## CUTFLOW CODE!! (START)

process.mfvSelectedVerticesCutflow0 = process.mfvSelectedVertices.clone(mevent_src='mfvEvent', exclude_beampipe=False, min_ntracks=0, min_bsbs2ddist=0, max_rescale_bs2derr=1e9)
process.mfvSelectedVerticesCutflow1 = process.mfvSelectedVerticesCutflow0.clone(exclude_beampipe=True)
process.mfvSelectedVerticesCutflow2 = process.mfvSelectedVerticesCutflow1.clone(min_ntracks=5)
process.mfvSelectedVerticesCutflow3 = process.mfvSelectedVerticesCutflow2.clone(min_bsbs2ddist=0.01)
process.mfvSelectedVerticesCutflow4 = process.mfvSelectedVerticesCutflow3.clone(max_rescale_bs2derr=0.005)

process.mfvSelectedVerticesCutflowSeq = cms.Sequence(process.mfvSelectedVerticesCutflow0 * process.mfvSelectedVerticesCutflow1 * process.mfvSelectedVerticesCutflow2 * process.mfvSelectedVerticesCutflow3 * process.mfvSelectedVerticesCutflow4)
common_cutflow = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvSelectedVerticesCutflowSeq * process.mfvWeight)

def _mk_cf(name, vtxsrc, minnv, maxnv=100000):
    ana = process.mfvAnalysisCuts.clone(apply_presel = 0, apply_vertex_cuts = True)
    ana.vertex_src = vtxsrc
    ana.min_nvertex = minnv
    ana.max_nvertex = maxnv
    setattr(process, name, ana)
    return ana

process.mfvEventHistosCutflowVertexSel = process.mfvEventHistos.clone()
process.mfvVertexHistosCutflowVertexSel = process.mfvVertexHistos.clone(vertex_src='mfvSelectedVerticesCutflow0')
process.mfvAnalysisCutsCutflowVertexSel = _mk_cf('mfvAnalysisCutsCutflowVertexSel', 'mfvSelectedVerticesCutflow0', 1)

process.mfvEventHistosCutflowBeamPipe = process.mfvEventHistos.clone()
process.mfvVertexHistosCutflowBeamPipe = process.mfvVertexHistos.clone(vertex_src='mfvSelectedVerticesCutflow1')
process.mfvAnalysisCutsCutflowBeamPipe = _mk_cf('mfvAnalysisCutsCutflowBeamPipe', 'mfvSelectedVerticesCutflow1', 1)

process.mfvEventHistosCutflowNtk5 = process.mfvEventHistos.clone()
process.mfvVertexHistosCutflowNtk5 = process.mfvVertexHistos.clone(vertex_src='mfvSelectedVerticesCutflow2')
process.mfvAnalysisCutsCutflowNtk5 = _mk_cf('mfvAnalysisCutsCutflowNtk5', 'mfvSelectedVerticesCutflow2', 1)

process.mfvEventHistosCutflow2dist = process.mfvEventHistos.clone()
process.mfvVertexHistosCutflow2dist = process.mfvVertexHistos.clone(vertex_src='mfvSelectedVerticesCutflow3')
process.mfvAnalysisCutsCutflow2dist = _mk_cf('mfvAnalysisCutsCutflow2dist', 'mfvSelectedVerticesCutflow3', 1)

process.mfvEventHistosCutflowBs2derr = process.mfvEventHistos.clone()
process.mfvVertexHistosCutflowBs2derr = process.mfvVertexHistos.clone(vertex_src='mfvSelectedVerticesCutflow4')
process.mfvAnalysisCutsCutflowBs2derr = _mk_cf('mfvAnalysisCutsCutflowBs2derr', 'mfvSelectedVerticesCutflow4', 1)

process.mfvEventHistosCutflow2V = process.mfvEventHistos.clone()
process.mfvVertexHistosCutflow2V = process.mfvVertexHistos.clone(vertex_src='mfvSelectedVerticesCutflow4')
process.mfvAnalysisCutsCutflow2V = _mk_cf('mfvAnalysisCutsCutflow2V', 'mfvSelectedVerticesCutflow4', 2)

process.pCutflowVertexSel = cms.Path(common_cutflow * process.mfvAnalysisCutsPreSel * process.mfvAnalysisCutsCutflowVertexSel * process.mfvEventHistosCutflowVertexSel * process.mfvVertexHistosCutflowVertexSel)
process.pCutflowBeamPipe  = cms.Path(common_cutflow * process.mfvAnalysisCutsPreSel * process.mfvAnalysisCutsCutflowBeamPipe  * process.mfvEventHistosCutflowBeamPipe  * process.mfvVertexHistosCutflowBeamPipe)
process.pCutflowNtk5      = cms.Path(common_cutflow * process.mfvAnalysisCutsPreSel * process.mfvAnalysisCutsCutflowNtk5      * process.mfvEventHistosCutflowNtk5      * process.mfvVertexHistosCutflowNtk5)
process.pCutflow2dist     = cms.Path(common_cutflow * process.mfvAnalysisCutsPreSel * process.mfvAnalysisCutsCutflow2dist     * process.mfvEventHistosCutflow2dist     * process.mfvVertexHistosCutflow2dist)
process.pCutflowBs2derr   = cms.Path(common_cutflow * process.mfvAnalysisCutsPreSel * process.mfvAnalysisCutsCutflowBs2derr   * process.mfvEventHistosCutflowBs2derr   * process.mfvVertexHistosCutflowBs2derr)
process.pCutflow2V        = cms.Path(common_cutflow * process.mfvAnalysisCutsPreSel * process.mfvAnalysisCutsCutflow2V        * process.mfvEventHistosCutflow2V        * process.mfvVertexHistosCutflow2V)

############## CUTFLOW CODE!! (END)

nm1s = [
    ('Ntracks', 'min_ntracks = 0'),
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

process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel * process.EX1mfvVertexHistosPreSel)
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
    
    '''
    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=False, ttbar=False, all_signal=True, data=False, bjet=False) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif  use_btag_vetoLepHT_triggers:
        samples = pick_samples(dataset, qcd=True, data = False, all_signal = True, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif  use_Lepton_triggers:
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=True, leptonic=True, ttbar=True, diboson=True, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    else :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, ttbar=True, diboson=True, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    '''
 
    # 2016APV
    
    dataset = "Ntuple_ttHComparisonLepm_NoEF_2016APV"
    samples = [
        getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_20161'),
        getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_20161'),
    ]
    '''
    samples = [
        # WminusH
        getattr(Samples, "WminusHToSSTodddd_tau100um_M15_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M15_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M15_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M15_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M15_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M15_20161"),

        getattr(Samples, "WminusHToSSTodddd_tau100um_M40_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M40_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M40_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M40_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M40_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M40_20161"),

        getattr(Samples, "WminusHToSSTodddd_tau100um_M55_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M55_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M55_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M55_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M55_20161"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M55_20161"),

        # WplusH
        getattr(Samples, "WplusHToSSTodddd_tau100um_M15_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M15_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M15_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M15_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M15_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M15_20161"),

        getattr(Samples, "WplusHToSSTodddd_tau100um_M40_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M40_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M40_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M40_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M40_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M40_20161"),

        getattr(Samples, "WplusHToSSTodddd_tau100um_M55_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M55_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M55_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M55_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M55_20161"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M55_20161"),

        # ZH
        getattr(Samples, "ZHToSSTodddd_tau100um_M15_20161"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M15_20161"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M15_20161"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M15_20161"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M15_20161"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M15_20161"),

        getattr(Samples, "ZHToSSTodddd_tau100um_M40_20161"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M40_20161"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M40_20161"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M40_20161"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M40_20161"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M40_20161"),

        getattr(Samples, "ZHToSSTodddd_tau100um_M55_20161"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M55_20161"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M55_20161"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M55_20161"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M55_20161"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M55_20161"),

        # mfv_neu (CTau = 100um)
        getattr(Samples, "mfv_neu_tau000100um_M0200_20161"),
        getattr(Samples, "mfv_neu_tau000100um_M0300_20161"),
        getattr(Samples, "mfv_neu_tau000100um_M0400_20161"),
        getattr(Samples, "mfv_neu_tau000100um_M0600_20161"),
        getattr(Samples, "mfv_neu_tau000100um_M0800_20161"),
        getattr(Samples, "mfv_neu_tau000100um_M1200_20161"),
        getattr(Samples, "mfv_neu_tau000100um_M1600_20161"),
        getattr(Samples, "mfv_neu_tau000100um_M3000_20161"),

        # mfv_neu (CTau = 300um)
        getattr(Samples, "mfv_neu_tau000300um_M0200_20161"),
        getattr(Samples, "mfv_neu_tau000300um_M0300_20161"),
        getattr(Samples, "mfv_neu_tau000300um_M0400_20161"),
        getattr(Samples, "mfv_neu_tau000300um_M0600_20161"),
        getattr(Samples, "mfv_neu_tau000300um_M0800_20161"),
        getattr(Samples, "mfv_neu_tau000300um_M1200_20161"),
        getattr(Samples, "mfv_neu_tau000300um_M1600_20161"),
        getattr(Samples, "mfv_neu_tau000300um_M3000_20161"),

        # mfv_neu (CTau = 1mm)
        getattr(Samples, "mfv_neu_tau001000um_M0200_20161"),
        getattr(Samples, "mfv_neu_tau001000um_M0300_20161"),
        getattr(Samples, "mfv_neu_tau001000um_M0400_20161"),
        getattr(Samples, "mfv_neu_tau001000um_M0600_20161"),
        getattr(Samples, "mfv_neu_tau001000um_M0800_20161"),
        getattr(Samples, "mfv_neu_tau001000um_M1200_20161"),
        getattr(Samples, "mfv_neu_tau001000um_M1600_20161"),
        getattr(Samples, "mfv_neu_tau001000um_M3000_20161"),

        # mfv_neu (CTau = 10mm)
        getattr(Samples, "mfv_neu_tau010000um_M0200_20161"),
        getattr(Samples, "mfv_neu_tau010000um_M0300_20161"),
        getattr(Samples, "mfv_neu_tau010000um_M0400_20161"),
        getattr(Samples, "mfv_neu_tau010000um_M0600_20161"),
        getattr(Samples, "mfv_neu_tau010000um_M0800_20161"),
        getattr(Samples, "mfv_neu_tau010000um_M1600_20161"),

        # mfv_neu (CTau = 30mm)
        getattr(Samples, "mfv_neu_tau030000um_M0200_20161"),
        getattr(Samples, "mfv_neu_tau030000um_M0300_20161"),
        getattr(Samples, "mfv_neu_tau030000um_M0400_20161"),
        getattr(Samples, "mfv_neu_tau030000um_M0600_20161"),
        getattr(Samples, "mfv_neu_tau030000um_M0800_20161"),
        getattr(Samples, "mfv_neu_tau030000um_M1200_20161"),
        getattr(Samples, "mfv_neu_tau030000um_M1600_20161"),
    ]
    '''

    '''
    # 2016
    dataset = "Ntuple_ttHComparisonLepm_NoEF_2016"
    samples = [
        getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_20162'),
        getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_20162'),
    ]
    
    samples = [
        # WminusH
        getattr(Samples, "WminusHToSSTodddd_tau100um_M15_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M15_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M15_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M15_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M15_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M15_20162"),

        getattr(Samples, "WminusHToSSTodddd_tau100um_M40_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M40_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M40_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M40_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M40_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M40_20162"),

        getattr(Samples, "WminusHToSSTodddd_tau100um_M55_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M55_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M55_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M55_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M55_20162"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M55_20162"),

        # WplusH
        getattr(Samples, "WplusHToSSTodddd_tau100um_M15_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M15_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M15_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M15_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M15_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M15_20162"),

        getattr(Samples, "WplusHToSSTodddd_tau100um_M40_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M40_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M40_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M40_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M40_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M40_20162"),

        getattr(Samples, "WplusHToSSTodddd_tau100um_M55_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M55_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M55_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M55_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M55_20162"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M55_20162"),

        # ZH
        getattr(Samples, "ZHToSSTodddd_tau100um_M15_20162"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M15_20162"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M15_20162"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M15_20162"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M15_20162"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M15_20162"),

        getattr(Samples, "ZHToSSTodddd_tau100um_M40_20162"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M40_20162"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M40_20162"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M40_20162"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M40_20162"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M40_20162"),

        getattr(Samples, "ZHToSSTodddd_tau100um_M55_20162"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M55_20162"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M55_20162"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M55_20162"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M55_20162"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M55_20162"),

        # mfv_neu (CTau = 100um)
        getattr(Samples, "mfv_neu_tau000100um_M0200_20162"),
        getattr(Samples, "mfv_neu_tau000100um_M0300_20162"),
        getattr(Samples, "mfv_neu_tau000100um_M0400_20162"),
        getattr(Samples, "mfv_neu_tau000100um_M0600_20162"),
        getattr(Samples, "mfv_neu_tau000100um_M0800_20162"),
        getattr(Samples, "mfv_neu_tau000100um_M1200_20162"),
        getattr(Samples, "mfv_neu_tau000100um_M1600_20162"),

        # mfv_neu (CTau = 300um)
        getattr(Samples, "mfv_neu_tau000300um_M0200_20162"),
        getattr(Samples, "mfv_neu_tau000300um_M0300_20162"),
        getattr(Samples, "mfv_neu_tau000300um_M0400_20162"),
        getattr(Samples, "mfv_neu_tau000300um_M0600_20162"),
        getattr(Samples, "mfv_neu_tau000300um_M0800_20162"),
        getattr(Samples, "mfv_neu_tau000300um_M1200_20162"),
        getattr(Samples, "mfv_neu_tau000300um_M1600_20162"),
        getattr(Samples, "mfv_neu_tau000300um_M3000_20162"),

        # mfv_neu (CTau = 1mm)
        getattr(Samples, "mfv_neu_tau001000um_M0200_20162"),
        getattr(Samples, "mfv_neu_tau001000um_M0300_20162"),
        getattr(Samples, "mfv_neu_tau001000um_M0400_20162"),
        getattr(Samples, "mfv_neu_tau001000um_M0600_20162"),
        getattr(Samples, "mfv_neu_tau001000um_M0800_20162"),
        getattr(Samples, "mfv_neu_tau001000um_M1200_20162"),
        getattr(Samples, "mfv_neu_tau001000um_M1600_20162"),

        # mfv_neu (CTau = 10mm)
        getattr(Samples, "mfv_neu_tau010000um_M0200_20162"),
        getattr(Samples, "mfv_neu_tau010000um_M0300_20162"),
        getattr(Samples, "mfv_neu_tau010000um_M0400_20162"),
        getattr(Samples, "mfv_neu_tau010000um_M0600_20162"),
        getattr(Samples, "mfv_neu_tau010000um_M0800_20162"),
        getattr(Samples, "mfv_neu_tau010000um_M1200_20162"),
        getattr(Samples, "mfv_neu_tau010000um_M1600_20162"),

        # mfv_neu (CTau = 30mm)
        getattr(Samples, "mfv_neu_tau030000um_M0200_20162"),
        getattr(Samples, "mfv_neu_tau030000um_M0300_20162"),
        getattr(Samples, "mfv_neu_tau030000um_M0400_20162"),
        getattr(Samples, "mfv_neu_tau030000um_M0600_20162"),
        getattr(Samples, "mfv_neu_tau030000um_M0800_20162"),
        getattr(Samples, "mfv_neu_tau030000um_M1600_20162"),
    ]
    '''
    '''
    #2017
    dataset = "Ntuple_ttHComparisonBvetoLHTm_NoEF_2017"
    samples = [
        getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_2017'),
        getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_2017'),
        getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_JOEY_2017'),
    ]
    
    samples = [
        # WminusH
        getattr(Samples, "WminusHToSSTodddd_tau100um_M15_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M15_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M15_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M15_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M15_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M15_2017"),

        getattr(Samples, "WminusHToSSTodddd_tau100um_M40_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M40_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M40_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M40_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M40_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M40_2017"),

        getattr(Samples, "WminusHToSSTodddd_tau100um_M55_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M55_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M55_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M55_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M55_2017"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M55_2017"),

        # WplusH
        getattr(Samples, "WplusHToSSTodddd_tau100um_M15_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M15_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M15_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M15_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M15_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M15_2017"),

        getattr(Samples, "WplusHToSSTodddd_tau100um_M40_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M40_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M40_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M40_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M40_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M40_2017"),

        getattr(Samples, "WplusHToSSTodddd_tau100um_M55_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M55_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M55_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M55_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M55_2017"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M55_2017"),

        # ZH
        
        getattr(Samples, "ZHToSSTodddd_tau100um_M15_2017"),
        getattr(Samples, "ZHToSSTodddd_tau100um_M40_2017"),
        getattr(Samples, "ZHToSSTodddd_tau100um_M55_2017"),

        getattr(Samples, "ZHToSSTodddd_tau300um_M15_2017"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M15_2017"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M15_2017"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M15_2017"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M15_2017"),

        getattr(Samples, "ZHToSSTodddd_tau300um_M40_2017"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M40_2017"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M40_2017"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M40_2017"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M40_2017"),

        getattr(Samples, "ZHToSSTodddd_tau300um_M55_2017"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M55_2017"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M55_2017"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M55_2017"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M55_2017"),

        # mfv_neu (CTau = 100um)
        getattr(Samples, "mfv_neu_tau000100um_M0200_2017"),
        getattr(Samples, "mfv_neu_tau000100um_M0300_2017"),
        getattr(Samples, "mfv_neu_tau000100um_M0400_2017"),
        getattr(Samples, "mfv_neu_tau000100um_M0600_2017"),
        getattr(Samples, "mfv_neu_tau000100um_M0800_2017"),
        getattr(Samples, "mfv_neu_tau000100um_M1200_2017"),
        getattr(Samples, "mfv_neu_tau000100um_M1600_2017"),
        getattr(Samples, "mfv_neu_tau000100um_M3000_2017"),

        # mfv_neu (CTau = 300um)
        getattr(Samples, "mfv_neu_tau000300um_M0200_2017"),
        getattr(Samples, "mfv_neu_tau000300um_M0300_2017"),
        getattr(Samples, "mfv_neu_tau000300um_M0400_2017"),
        getattr(Samples, "mfv_neu_tau000300um_M0600_2017"),
        getattr(Samples, "mfv_neu_tau000300um_M0800_2017"),
        getattr(Samples, "mfv_neu_tau000300um_M1200_2017"),
        getattr(Samples, "mfv_neu_tau000300um_M1600_2017"),
        getattr(Samples, "mfv_neu_tau000300um_M3000_2017"),

        # mfv_neu (CTau = 1mm)
        getattr(Samples, "mfv_neu_tau001000um_M0200_2017"),
        getattr(Samples, "mfv_neu_tau001000um_M0300_2017"),
        getattr(Samples, "mfv_neu_tau001000um_M0400_2017"),
        getattr(Samples, "mfv_neu_tau001000um_M0600_2017"),
        getattr(Samples, "mfv_neu_tau001000um_M0800_2017"),
        getattr(Samples, "mfv_neu_tau001000um_M1600_2017"),

        # mfv_neu (CTau = 10mm)
        getattr(Samples, "mfv_neu_tau010000um_M0200_2017"),
        getattr(Samples, "mfv_neu_tau010000um_M0300_2017"),
        getattr(Samples, "mfv_neu_tau010000um_M0400_2017"),
        getattr(Samples, "mfv_neu_tau010000um_M0600_2017"),
        getattr(Samples, "mfv_neu_tau010000um_M0800_2017"),
        getattr(Samples, "mfv_neu_tau010000um_M1200_2017"),
        getattr(Samples, "mfv_neu_tau010000um_M1600_2017"),

        # mfv_neu (CTau = 30mm)
        getattr(Samples, "mfv_neu_tau030000um_M0200_2017"),
        getattr(Samples, "mfv_neu_tau030000um_M0300_2017"),
        getattr(Samples, "mfv_neu_tau030000um_M0400_2017"),
        getattr(Samples, "mfv_neu_tau030000um_M0600_2017"),
        getattr(Samples, "mfv_neu_tau030000um_M0800_2017"),
        getattr(Samples, "mfv_neu_tau030000um_M1200_2017"),
        getattr(Samples, "mfv_neu_tau030000um_M1600_2017"),
    ]
    '''
    '''
    dataset = "Ntuple_ttHComparisonBvetoLHTm_NoEF_2018"
    samples = [
        getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_2018'),
        getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_2018'),
    ]
    
    samples = [
        # WminusH
        getattr(Samples, "WminusHToSSTodddd_tau100um_M15_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau100um_M40_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau100um_M55_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M15_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M40_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau300um_M55_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M15_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M40_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau1mm_M55_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M15_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M40_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau3mm_M55_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M15_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M40_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau10mm_M55_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M15_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M40_2018"),
        getattr(Samples, "WminusHToSSTodddd_tau30mm_M55_2018"),

        # WplusH
        getattr(Samples, "WplusHToSSTodddd_tau100um_M15_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau100um_M40_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau100um_M55_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M15_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M40_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau300um_M55_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M15_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M40_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau1mm_M55_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M15_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M40_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau3mm_M55_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M15_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M40_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau10mm_M55_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M15_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M40_2018"),
        getattr(Samples, "WplusHToSSTodddd_tau30mm_M55_2018"),

        # ZH
        getattr(Samples, "ZHToSSTodddd_tau100um_M15_2018"),
        getattr(Samples, "ZHToSSTodddd_tau100um_M40_2018"),
        getattr(Samples, "ZHToSSTodddd_tau100um_M55_2018"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M15_2018"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M40_2018"),
        getattr(Samples, "ZHToSSTodddd_tau300um_M55_2018"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M15_2018"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M40_2018"),
        getattr(Samples, "ZHToSSTodddd_tau1mm_M55_2018"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M15_2018"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M40_2018"),
        getattr(Samples, "ZHToSSTodddd_tau3mm_M55_2018"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M15_2018"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M40_2018"),
        getattr(Samples, "ZHToSSTodddd_tau10mm_M55_2018"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M15_2018"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M40_2018"),
        getattr(Samples, "ZHToSSTodddd_tau30mm_M55_2018"),

        # mfv_neu (CTau = 100um)
        getattr(Samples, "mfv_neu_tau000100um_M0200_2018"),
        getattr(Samples, "mfv_neu_tau000100um_M0300_2018"),
        getattr(Samples, "mfv_neu_tau000100um_M0400_2018"),
        getattr(Samples, "mfv_neu_tau000100um_M0600_2018"),
        getattr(Samples, "mfv_neu_tau000100um_M0800_2018"),
        getattr(Samples, "mfv_neu_tau000100um_M1600_2018"),
        getattr(Samples, "mfv_neu_tau000100um_M3000_2018"),

        # mfv_neu (CTau = 300um)
        getattr(Samples, "mfv_neu_tau000300um_M0200_2018"),
        getattr(Samples, "mfv_neu_tau000300um_M0300_2018"),
        getattr(Samples, "mfv_neu_tau000300um_M0400_2018"),
        getattr(Samples, "mfv_neu_tau000300um_M0600_2018"),
        getattr(Samples, "mfv_neu_tau000300um_M0800_2018"),
        getattr(Samples, "mfv_neu_tau000300um_M1200_2018"),
        getattr(Samples, "mfv_neu_tau000300um_M1600_2018"),
        getattr(Samples, "mfv_neu_tau000300um_M3000_2018"),

        # mfv_neu (CTau = 1mm)
        getattr(Samples, "mfv_neu_tau001000um_M0200_2018"),
        getattr(Samples, "mfv_neu_tau001000um_M0300_2018"),
        getattr(Samples, "mfv_neu_tau001000um_M0400_2018"),
        getattr(Samples, "mfv_neu_tau001000um_M0600_2018"),
        getattr(Samples, "mfv_neu_tau001000um_M0800_2018"),
        getattr(Samples, "mfv_neu_tau001000um_M1200_2018"),
        getattr(Samples, "mfv_neu_tau001000um_M1600_2018"),

        # mfv_neu (CTau = 10mm)
        getattr(Samples, "mfv_neu_tau010000um_M0200_2018"),
        getattr(Samples, "mfv_neu_tau010000um_M0300_2018"),
        getattr(Samples, "mfv_neu_tau010000um_M0400_2018"),
        getattr(Samples, "mfv_neu_tau010000um_M0600_2018"),
        getattr(Samples, "mfv_neu_tau010000um_M0800_2018"),
        getattr(Samples, "mfv_neu_tau010000um_M1200_2018"),
        getattr(Samples, "mfv_neu_tau010000um_M1600_2018"),

        # mfv_neu (CTau = 30mm)
        getattr(Samples, "mfv_neu_tau030000um_M0200_2018"),
        getattr(Samples, "mfv_neu_tau030000um_M0300_2018"),
        getattr(Samples, "mfv_neu_tau030000um_M0400_2018"),
        getattr(Samples, "mfv_neu_tau030000um_M0600_2018"),
        getattr(Samples, "mfv_neu_tau030000um_M1200_2018"),
        getattr(Samples, "mfv_neu_tau030000um_M1600_2018"),
    ]
    '''

    # for tth!
    '''
    dataset = "ntuple_tthstudy_lepm_noef"

    samples = [
        getattr(Samples, 'ttHToLLPs_tau000001000um_M0055_2017'),
        getattr(Samples, 'ttHToLLPs_tau000010000um_M0055_2017'),
        getattr(Samples, 'ttHToLLPs_tau000100000um_M0055_2017'),
        getattr(Samples, 'ttHToLLPs_tau001000000um_M0055_2017'),
    ]
    '''

    pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('Histos' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         pset_template_fn = '/uscms_data/d3/gdecastr/work/DVCode/mfv_10648/src/JMTucker/MFVNeutralino/test/histos.py',
                         )
    cs.submit_all(samples)
