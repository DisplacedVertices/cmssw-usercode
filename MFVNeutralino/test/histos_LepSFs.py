from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_Lepton_triggers, use_btag_triggers, use_btag_vetoLepHT_triggers 
#input_files(process, '/store/group/lpclonglived/gdecastr/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/Ntuple_Table28Validation_CorrectedLepm_NoEF_2018/260206_144855/0000/ntuple_0.root')
#input_files(process, "root://cmsxrootd-site.fnal.gov//store/user/gdecastr/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/Ntuple_Table28Validation_2016APV_Lepm_NoEF_2018/260130_183335//0000/ntuple_1.root")
#sample_files(process, 'qcdht2000_2017' if is_mc else 'JetHT2017B', dataset, 1)
#input_files(process, '/store/group/lpclonglived/pkotamni/ggH_HToSSTodddd_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleOnnormdzULV30Bm_NoEF_20161/250122_131504/0000/ntuple_0.root')
#input_files(process, '/store/group/lpclonglived/pkotamni/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleOnnormdzULV30Lepm_2017/250101_200106/0000/ntuple_0.root')
#input_files(process, '/uscms/home/pkotamni/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/ntuple.root')

tfileservice(process, 'histos.root')
cmssw_from_argv(process)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

# Hack to get around weird vertexing bug in WminusHToSSTodddd_tau10mm_M40_20162

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    SkipEvent = cms.untracked.vstring("ProductNotFound"),
)

# Explicitly skip the bad event (run:lumi:event)
process.source.eventsToSkip = cms.untracked.VEventRange("1:1:189")


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


# Only build FullSel with central, PU, and flavor-split lepton SF variations.
# No cutflow / N-1 / nv scanning.

ntks = [5]

for ntk in ntks:
    # Only the default >=5 track selection
    EX1 = EX2 = EX3 = ''

    exec '''
process.EX1mfvAnalysisCutsFullSel = process.mfvAnalysisCuts.clone(EX2EX3)

process.EX1mfvEventHistosFullSel = process.mfvEventHistos.clone()
process.EX1mfvVertexHistosFullSel = process.mfvVertexHistos.clone(EX2)

# Flavor-split lepton SF variations for FullSel
process.EX1mfvEventHistosFullSel_MuRecoUp   = process.EX1mfvEventHistosFullSel.clone(weight_src = 'mfvWeight:murecoup')
process.EX1mfvEventHistosFullSel_MuRecoDown = process.EX1mfvEventHistosFullSel.clone(weight_src = 'mfvWeight:murecodown')
process.EX1mfvEventHistosFullSel_MuIDUp     = process.EX1mfvEventHistosFullSel.clone(weight_src = 'mfvWeight:muidup')
process.EX1mfvEventHistosFullSel_MuIDDown   = process.EX1mfvEventHistosFullSel.clone(weight_src = 'mfvWeight:muiddown')
process.EX1mfvEventHistosFullSel_MuISOUp    = process.EX1mfvEventHistosFullSel.clone(weight_src = 'mfvWeight:muisoup')
process.EX1mfvEventHistosFullSel_MuISODown  = process.EX1mfvEventHistosFullSel.clone(weight_src = 'mfvWeight:muisodown')
process.EX1mfvEventHistosFullSel_ElIDUp     = process.EX1mfvEventHistosFullSel.clone(weight_src = 'mfvWeight:eleidup')
process.EX1mfvEventHistosFullSel_ElIDDown   = process.EX1mfvEventHistosFullSel.clone(weight_src = 'mfvWeight:eleiddown')

process.EX1mfvVertexHistosFullSel_MuRecoUp   = process.EX1mfvVertexHistosFullSel.clone(weight_src = 'mfvWeight:murecoup')
process.EX1mfvVertexHistosFullSel_MuRecoDown = process.EX1mfvVertexHistosFullSel.clone(weight_src = 'mfvWeight:murecodown')
process.EX1mfvVertexHistosFullSel_MuIDUp     = process.EX1mfvVertexHistosFullSel.clone(weight_src = 'mfvWeight:muidup')
process.EX1mfvVertexHistosFullSel_MuIDDown   = process.EX1mfvVertexHistosFullSel.clone(weight_src = 'mfvWeight:muiddown')
process.EX1mfvVertexHistosFullSel_MuISOUp    = process.EX1mfvVertexHistosFullSel.clone(weight_src = 'mfvWeight:muisoup')
process.EX1mfvVertexHistosFullSel_MuISODown  = process.EX1mfvVertexHistosFullSel.clone(weight_src = 'mfvWeight:muisodown')
process.EX1mfvVertexHistosFullSel_ElIDUp     = process.EX1mfvVertexHistosFullSel.clone(weight_src = 'mfvWeight:eleidup')
process.EX1mfvVertexHistosFullSel_ElIDDown   = process.EX1mfvVertexHistosFullSel.clone(weight_src = 'mfvWeight:eleiddown')

process.EX1pFullSel = cms.Path(
    common
  * process.EX1mfvAnalysisCutsFullSel
  * process.EX1mfvEventHistosFullSel
  * process.EX1mfvVertexHistosFullSel
  * process.EX1mfvEventHistosFullSel_MuRecoUp
  * process.EX1mfvVertexHistosFullSel_MuRecoUp
  * process.EX1mfvEventHistosFullSel_MuRecoDown
  * process.EX1mfvVertexHistosFullSel_MuRecoDown
  * process.EX1mfvEventHistosFullSel_MuIDUp
  * process.EX1mfvVertexHistosFullSel_MuIDUp
  * process.EX1mfvEventHistosFullSel_MuIDDown
  * process.EX1mfvVertexHistosFullSel_MuIDDown
  * process.EX1mfvEventHistosFullSel_MuISOUp
  * process.EX1mfvVertexHistosFullSel_MuISOUp
  * process.EX1mfvEventHistosFullSel_MuISODown
  * process.EX1mfvVertexHistosFullSel_MuISODown
  * process.EX1mfvEventHistosFullSel_ElIDUp
  * process.EX1mfvVertexHistosFullSel_ElIDUp
  * process.EX1mfvEventHistosFullSel_ElIDDown
  * process.EX1mfvVertexHistosFullSel_ElIDDown
)
'''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
     
    # 2016APV
    '''
    dataset = "Ntuple_ttHComparisonLepm_NoEF_2016APV"
    #dataset = "Ntuple_Table28Validation_CorrectedLepm_NoEF_2016APV"
    
    samples = [
         # ttH
        #getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_20161'),
        getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_20161'),
    ]
    

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
    ]
    '''
    
    # 2016
    #dataset = "Ntuple_ttHComparisonLepm_NoEF_2016"
    dataset = "Ntuple_Table28Validation_CorrectedLepm_NoEF_2016"
    samples = [getattr(Samples, "WminusHToSSTodddd_tau10mm_M40_20162")]
    '''
    samples = [
        #getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_20162'),
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
    ]
    '''
    '''
    #2017
    dataset = "Ntuple_ttHComparisonLepm_NoEF_2017"
    #dataset = "Ntuple_Table28Validation_CorrectedLepm_NoEF_2017"

    samples = [
        getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_2017'),
        getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_2017'),
        #getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_JOEY_2017'),
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
    ]
    '''
    '''
    dataset = "Ntuple_ttHComparisonLepm_NoEF_2018"
    #dataset = "Ntuple_Table28Validation_CorrectedLepm_NoEF_2018"

    samples = [
        #getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_2018'),
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
    ]
    '''

    pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('Histos_LepSFs' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         pset_template_fn = '/uscms_data/d3/gdecastr/work/DVCode/mfv_10648/src/JMTucker/MFVNeutralino/test/histos_LepSFs.py',
                         )
    cs.submit_all(samples)
