from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_btag_vetoLepHT_triggers, use_MET_triggers, use_Lepton_triggers, use_Muon_triggers, use_Electron_triggers
#sample_files(process, 'WplusHToSSTodddd_tau1mm_M55_2017' if is_mc else 'JetHT2017B', dataset, 1)
#sample_files(process, 'mfv_stopld_tau000100um_M0200_2018' if is_mc else 'JetHT2017B', dataset, 1)
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/100000/177D06A8-D7E8-E14A-8FB8-E638820EDFF3.root')
#max_events(process, 100)
input_files(process, '/store/group/lpclonglived/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleOnnormdzULV30BvetoLHTm_20161/250222_142639/0000/ntuple_1.root')
tfileservice(process, 'minitree.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

# Hack to get around weird vertexing bug in WminusHToSSTodddd_tau10mm_M40_20162
'''
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    SkipEvent = cms.untracked.vstring("ProductNotFound"),
)

# Explicitly skip the bad event (run:lumi:event)
process.source.eventsToSkip = cms.untracked.VEventRange("1:1:189")
'''

# blind btag triggered events
#if not is_mc and use_btag_triggers :
#    del process.pMiniTreeNtk3
#    del process.pMiniTreeNtk4
#    del process.pMiniTreeNtk3or4
#    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    '''
    # 2016
    #dataset = "Ntuple_ttHComparisonLepm_NoEF_2016APV" 
    dataset = "Ntuple_Table28Validation_CorrectedLepm_NoEF_2016APV"   
    samples = [
        # ttH
    #    getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_20161'),
    #    getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_20161'),
    #]
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

    # 2016
    #dataset = "Ntuple_ttHComparisonLepm_NoEF_2016" 
    dataset = "Ntuple_Table28Validation_CorrectedLepm_NoEF_2016"  
    #samples = [
    #    getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_20162'),
    #    getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_20162'),
    #]
    samples = [
                getattr(Samples, "WminusHToSSTodddd_tau10mm_M40_20162"),
    ]
    '''
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

    #2017
    #dataset = "Ntuple_Table28Validation_CorrectedLepm_NoEF_2017"
    #dataset = "Ntuple_ttHComparisonLepm_NoEF_2017"
    #samples = [
    #    getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_2017'),
    #    getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_2017'),
    #]
    '''
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

    #2018
    #dataset = "Ntuple_Table28Validation_CorrectedLepm_NoEF_2018"
    #dataset = "Ntuple_ttHComparisonLepm_NoEF_2018"
    #samples = [
    #    getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_2018'),
    #    getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_2018'),
    #]
    '''
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

    '''
    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=False, ttbar=False, all_signal=True, data=False, bjet=False) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif  use_btag_vetoLepHT_triggers:
        samples = pick_samples(dataset, qcd=True, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_MET_triggers :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, leptonic=False, splitSUSY=True, Zvv=False, met=False, span_signal=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_Lepton_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=False, leptonic=True, ttbar=False, diboson=False, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_Muon_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep = False, leptonic=False, met=False, diboson=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_Electron_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep = True, leptonic=True, met=True, diboson=True)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    else :
        samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, splitSUSY=True)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    '''
    pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8.json'))
    

    cs = CondorSubmitter('MiniTree' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
