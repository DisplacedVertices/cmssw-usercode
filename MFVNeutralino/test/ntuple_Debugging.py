
#!/usr/bin/env python

import os
import sys

import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.general import named_product
from JMTucker.MFVNeutralino.NtupleCommon import *
from JMTucker.Tools.Year import year

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
settings.keep_tk = False


if use_btag_triggers :
    settings.event_filter = 'bjets OR displaced dijet' # for new trigger studies
elif use_btag_vetoLepHT_triggers :
    settings.event_filter = 'bjets OR displaced dijet veto leptons and HT' # for new trigger studies
elif use_MET_triggers :
    settings.event_filter = 'met only'
elif use_Lepton_triggers :
    settings.event_filter = 'leptons only'
elif use_Muon_triggers :
    settings.event_filter = 'muons only' 
elif use_Electron_triggers :
    settings.event_filter = 'electrons only' 
else :
    settings.event_filter = 'jets only'

settings.event_filter = False

settings.randpars_filter = False
# if want to test local : 
#settings.randpars_filter = 'randpar HToSSTodddd M15_ct10-'

process = ntuple_process(settings)

# Minimal MessageLogger config for vertexer debug
process.load('FWCore.MessageService.MessageLogger_cfi')

# Allow INFO messages (needed for vertexer debug prints)
process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')

# Print framework report rarely
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(0)
)

# Ensure MFVVertexer category is allowed with no limit
if not hasattr(process.MessageLogger, 'categories'):
    process.MessageLogger.categories = cms.untracked.vstring()
if 'MFVVertexer' not in list(process.MessageLogger.categories):
    process.MessageLogger.categories.append('MFVVertexer')

process.MessageLogger.cerr.MFVVertexer = cms.untracked.PSet(
    limit = cms.untracked.int32(-1)
)

# Turn on vertexer debug knobs (actual printing depends on Vertexer.cc using them)
# You can override these on the command line via: debug=2
_debug_level_cli = None
for a in sys.argv:
    if a.startswith('debug='):
        _debug_level_cli = int(a.split('=', 1)[1])
        break
if _debug_level_cli is None and os.environ.get('DEBUG'):
    _debug_level_cli = int(os.environ.get('DEBUG'))

if hasattr(process, 'mfvVertices'):
    process.mfvVertices.debug_level = cms.untracked.int32(_debug_level_cli if _debug_level_cli is not None else 1)
    # defaults; if you pass event=RUN:LUMI:EVT below, we overwrite these to match
    process.mfvVertices.debug_run   = cms.untracked.uint32(0)
    process.mfvVertices.debug_lumi  = cms.untracked.uint32(0)
    process.mfvVertices.debug_event = cms.untracked.uint64(0)

    # Fast mode: only count seed tracks and skip actual vertexing (requires the Vertexer to support this param)
    _count_only_cli = None
    for a in sys.argv:
        if a.startswith('countonly='):
            _count_only_cli = int(a.split('=', 1)[1])
            break
    if _count_only_cli is None and os.environ.get('COUNTONLY') is not None:
        _count_only_cli = int(os.environ.get('COUNTONLY'))

    process.mfvVertices.count_seed_tracks_only = cms.untracked.bool(bool(_count_only_cli) if _count_only_cli is not None else True)
# ----------------------------------------------------------------------
# Debug helpers
#
# Usage examples:
#   cmsRun ntuple.py event=1:3:2706
#   EVENT=1:3:2706 cmsRun ntuple.py
#
# If you don't know the lumi yet, you can discover it with:
#   edmFileUtil -e <file.root> | grep ' 2706$'
# (or just search for the event number).
# ----------------------------------------------------------------------

def _parse_triplet(s):
    # Accept 1:LS:EVT or 1,LS,EVT or 1 LS EVT
    for ch in [',', ':']:
        s = s.replace(ch, ' ')
    parts = [p for p in s.split() if p]
    if len(parts) != 3:
        raise ValueError("event spec must be RUN:LUMI:EVENT (e.g. 1:3:2706)")
    return tuple(int(x) for x in parts)

_debug_event = None
for a in sys.argv:
    if a.startswith('event='):
        _debug_event = a.split('=', 1)[1]
        break
if _debug_event is None:
    _debug_event = os.environ.get('EVENT')

_debug_skip = None
for a in sys.argv:
    if a.startswith('skip='):
        _debug_skip = int(a.split('=', 1)[1])
        break
if _debug_skip is None and os.environ.get('SKIP'):
    _debug_skip = int(os.environ.get('SKIP'))

_debug_max = None
for a in sys.argv:
    if a.startswith('max='):
        _debug_max = int(a.split('=', 1)[1])
        break
if _debug_max is None and os.environ.get('MAX'):
    _debug_max = int(os.environ.get('MAX'))

if _debug_skip is not None:
    # Note: this is entry-based skipping, NOT run/lumi/event selection.
    process.source.skipEvents = cms.untracked.uint32(_debug_skip)

if _debug_event is not None:
    run, lumi, evt = _parse_triplet(_debug_event)
    print('Forcing single event:', (run, lumi, evt))
    set_events(process, [(run, lumi, evt)])
    max_events(process, 1)

    # Also tell the vertexer exactly which (run,lumi,event) to be verbose on
    if hasattr(process, 'mfvVertices'):
        process.mfvVertices.debug_run   = cms.untracked.uint32(run)
        process.mfvVertices.debug_lumi  = cms.untracked.uint32(lumi)
        process.mfvVertices.debug_event = cms.untracked.uint64(evt)
        # make sure debug is on when targeting a single event
        if _debug_level_cli is None:
            process.mfvVertices.debug_level = cms.untracked.int32(2)
elif _debug_max is not None:
    max_events(process, _debug_max)

#max_events(process, 10)
dataset = 'miniaod' if settings.is_miniaod else 'main'
input_files(process, 'E0D069E6-E0B1-4340-A79F-A898233728F3.root') # condor_mfv_neu_tau030000um_M3000_20161.log FAIL
#input_files(process, 'root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL16MiniAODAPVv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/2520000/B95D82C5-D1F0-D346-B7B8-2658AB4F117F.root') #condor_mfv_neu_tau010000um_M3000_20161 FAIL
#input_files(process, 'root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL16MiniAODAPVv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/2520000/0C150E6C-72D2-D34B-ACC0-A0B4BFFC35FB.root') #condor_mfv_neu_tau010000um_M1600_20161 SUC
#input_files(process, 'root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL16MiniAODAPVv2/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/2430000/194DAC07-F004-0243-B6B5-4DE78CA75956.root') #condor_mfv_neu_tau001000um_M3000_20161 SUC



# Tip: for local debugging, consider copying the file locally and using a file:// path
# to remove XRootD from the equation, e.g.
#   xrdcp root://cmsxrootd.fnal.gov//store/.../E0D0...root .
#   input_files(process, 'file:E0D069E6-E0B1-4340-A79F-A898233728F3.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2550000/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/0BD790C6-883F-0147-A66E-8EC9DC53750F.root')
#input_files(process, '/store/mc/RunIISummer20UL16MiniAODAPVv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/30000/F80DB8BA-EB71-E04B-A334-5B701A3FDF3E.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/DC0DDB54-E968-A948-B805-FCCDA9CDB11A.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/A8C3978F-4BE4-A844-BEE8-8DEE129A02B7.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120000/8ABE7321-B876-E248-951A-02BA0140B498.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2810000/056FAB59-F395-374B-BB32-E4A70D6C65BA.root')
#max_events(process, 200)
#input_files(process, '~/nobackup/crabdirs/TTJets_UL2017_MINIAOD.root')
#input_files(process, '~/nobackup/crabdirs/WplsuH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_UL2017_MINIAOD.root')
#input_files(process, '~/nobackup/crabdirs/TTJets_UL2017_MINIAOD.root')
#set_events(process, [(1, 12002, 31167330)])
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/100000/177D06A8-D7E8-E14A-8FB8-E638820EDFF3.root')
#input_files(process, '/store/data/Run2017B/MET/MINIAOD/UL2017_MiniAODv2-v1/100000/9B53ACB7-C063-1D44-A564-42435C24DE7B.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/240000/5B73F7F4-DF5B-7E4D-8F50-71A5E8024689.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/240000/5B73F7F4-DF5B-7E4D-8F50-71A5E8024689.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAOD/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/260000/00F00BE5-0C38-D047-88F7-D8EC2FCDDDFA.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTHTo2C_TTTo2L2Nu_M-125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/2540000/036644E2-9F05-8D41-8CD4-885679962D80.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/100000/3B05C6F7-7877-BD43-8F5F-E29283865170.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_SingleLeptFromT_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2430000/00351BB6-B311-8F40-B684-A1C7A375AF71.root')
#input_files(process, '/uscms/home/joeyr/nobackup/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')

# Test file!
#max_events(process, 10)
#input_files(process,
#    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16MiniAODAPVv2/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/60000/EA3D8723-2B40-1A4B-B164-9ADFF4555DDD.root"
#)
#cmssw_from_argv(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    # Override Samples:
    if year == 20161:
        samples = [
            getattr(Samples, 'mfv_neu_tau030000um_M3000_20161'),
        ]
        '''
        # ttH Private
        samples = [
            getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_20161'),
            getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_20161'),
        ]
        
        # Jet-triggered samples
        samples = [
            # --- ggH, MS = 15 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M15_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M15_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M15_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M15_20161'),

            # --- ggH, MS = 40 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M40_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M40_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M40_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M40_20161'),

            # --- ggH, MS = 55 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M55_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M55_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M55_20161'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M55_20161'),

            # --- MFV stop -> bbar bbar, M = 200 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0200_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0200_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0200_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0200_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0200_20161'),

            # --- MFV stop -> bbar bbar, M = 300 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0300_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0300_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0300_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0300_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0300_20161'),

            # --- MFV stop -> bbar bbar, M = 400 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0400_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0400_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0400_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0400_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0400_20161'),

            # --- MFV stop -> bbar bbar, M = 600 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0600_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0600_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0600_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0600_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0600_20161'),

            # --- MFV stop -> bbar bbar, M = 800 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0800_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0800_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0800_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0800_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0800_20161'),

            # --- MFV stop -> bbar bbar, M = 1200 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M1200_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M1200_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M1200_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M1200_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M1200_20161'),

            # --- MFV stop -> bbar bbar, M = 1600 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M1600_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M1600_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M1600_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M1600_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M1600_20161'),

            # --- MFV stop -> bbar bbar, M = 3000 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M3000_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M3000_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M3000_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M3000_20161'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M3000_20161'),

            # --- MFV stop -> dbar dbar, M = 200 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0200_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0200_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0200_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0200_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0200_20161'),

            # --- MFV stop -> dbar dbar, M = 300 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0300_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0300_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0300_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0300_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0300_20161'),

            # --- MFV stop -> dbar dbar, M = 400 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0400_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0400_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0400_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0400_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0400_20161'),

            # --- MFV stop -> dbar dbar, M = 600 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0600_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0600_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0600_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0600_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0600_20161'),

            # --- MFV stop -> dbar dbar, M = 800 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0800_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0800_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0800_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0800_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0800_20161'),

            # --- MFV stop -> dbar dbar, M = 1200 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M1200_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M1200_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1200_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M1200_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M1200_20161'),

            # --- MFV stop -> dbar dbar, M = 1600 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M1600_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M1600_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1600_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M1600_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M1600_20161'),

            # --- MFV stop -> dbar dbar, M = 3000 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M3000_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M3000_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M3000_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M3000_20161'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M3000_20161'),

            # --- MFV neutralino (gluino->neu neu->2T2B2S), M = 200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0200_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0200_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0200_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0200_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0200_20161'),

            # --- MFV neutralino, M = 300 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0300_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0300_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0300_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0300_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0300_20161'),

            # --- MFV neutralino, M = 400 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0400_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0400_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0400_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0400_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0400_20161'),

            # --- MFV neutralino, M = 600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0600_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0600_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0600_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0600_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0600_20161'),

            # --- MFV neutralino, M = 800 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0800_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0800_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0800_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0800_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0800_20161'),

            # --- MFV neutralino, M = 1200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1200_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M1200_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M1200_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M1200_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M1200_20161'),

            # --- MFV neutralino, M = 1600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1600_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M1600_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M1600_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M1600_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M1600_20161'),

            # --- MFV neutralino, M = 3000 ---
            getattr(Samples, 'mfv_neu_tau000100um_M3000_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M3000_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M3000_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M3000_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M3000_20161'),
        ]
        
        # Lepton-triggered samples
        
        samples = [

            # --- MFV neutralino, M = 200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0200_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0200_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0200_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0200_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0200_20161'),

            # --- MFV neutralino, M = 300 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0300_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0300_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0300_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0300_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0300_20161'),

            # --- MFV neutralino, M = 400 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0400_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0400_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0400_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0400_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0400_20161'),

            # --- MFV neutralino, M = 600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0600_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0600_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0600_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0600_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0600_20161'),

            # --- MFV neutralino, M = 800 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0800_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M0800_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M0800_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M0800_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M0800_20161'),

            # --- MFV neutralino, M = 1200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1200_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M1200_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M1200_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M1200_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M1200_20161'),

            # --- MFV neutralino, M = 1600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1600_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M1600_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M1600_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M1600_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M1600_20161'),

            # --- MFV neutralino, M = 3000 ---
            getattr(Samples, 'mfv_neu_tau000100um_M3000_20161'),
            getattr(Samples, 'mfv_neu_tau000300um_M3000_20161'),
            getattr(Samples, 'mfv_neu_tau001000um_M3000_20161'),
            getattr(Samples, 'mfv_neu_tau010000um_M3000_20161'),
            getattr(Samples, 'mfv_neu_tau030000um_M3000_20161'),

            # --- ZH (Z->LL), MS = 15 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M15_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M15_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M15_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M15_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M15_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M15_20161'),

            # --- ZH (Z->LL), MS = 40 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M40_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M40_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M40_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M40_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M40_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M40_20161'),

            # --- ZH (Z->LL), MS = 55 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M55_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M55_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M55_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M55_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M55_20161'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M55_20161'),

            # --- W+H (W->LNu), MS = 15 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M15_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M15_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M15_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M15_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M15_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M15_20161'),

            # --- W+H (W->LNu), MS = 40 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M40_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M40_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M40_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M40_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M40_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M40_20161'),

            # --- W+H (W->LNu), MS = 55 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M55_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M55_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M55_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M55_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M55_20161'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M55_20161'),

            # --- W-H (W->LNu), MS = 15 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M15_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M15_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M15_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M15_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M15_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M15_20161'),

            # --- W-H (W->LNu), MS = 40 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M40_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M40_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M40_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M40_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M40_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M40_20161'),

            # --- W-H (W->LNu), MS = 55 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M55_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M55_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M55_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M55_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M55_20161'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M55_20161'),
        ]
        '''
    if year == 20162:
        '''
        # ttH Private
        samples = [
            getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_20162'),
            getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_20162'),
        ]

        # Jet-triggered samples
        samples = [
            # --- ggH, MS = 15 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M15_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M15_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M15_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M15_20162'),

            # --- ggH, MS = 40 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M40_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M40_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M40_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M40_20162'),

            # --- ggH, MS = 55 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M55_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M55_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M55_20162'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M55_20162'),

            # --- MFV stop -> bbar bbar, M = 200 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0200_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0200_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0200_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0200_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0200_20162'),

            # --- MFV stop -> bbar bbar, M = 300 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0300_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0300_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0300_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0300_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0300_20162'),

            # --- MFV stop -> bbar bbar, M = 400 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0400_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0400_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0400_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0400_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0400_20162'),

            # --- MFV stop -> bbar bbar, M = 600 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0600_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0600_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0600_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0600_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0600_20162'),

            # --- MFV stop -> bbar bbar, M = 800 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0800_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0800_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0800_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0800_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0800_20162'),

            # --- MFV stop -> bbar bbar, M = 1200 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M1200_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M1200_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M1200_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M1200_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M1200_20162'),

            # --- MFV stop -> bbar bbar, M = 1600 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M1600_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M1600_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M1600_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M1600_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M1600_20162'),

            # --- MFV stop -> bbar bbar, M = 3000 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M3000_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M3000_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M3000_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M3000_20162'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M3000_20162'),

            # --- MFV stop -> dbar dbar, M = 200 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0200_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0200_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0200_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0200_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0200_20162'),

            # --- MFV stop -> dbar dbar, M = 300 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0300_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0300_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0300_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0300_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0300_20162'),

            # --- MFV stop -> dbar dbar, M = 400 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0400_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0400_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0400_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0400_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0400_20162'),

            # --- MFV stop -> dbar dbar, M = 600 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0600_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0600_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0600_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0600_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0600_20162'),

            # --- MFV stop -> dbar dbar, M = 800 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0800_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0800_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0800_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0800_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0800_20162'),

            # --- MFV stop -> dbar dbar, M = 1200 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M1200_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M1200_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1200_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M1200_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M1200_20162'),

            # --- MFV stop -> dbar dbar, M = 1600 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M1600_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M1600_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1600_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M1600_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M1600_20162'),

            # --- MFV stop -> dbar dbar, M = 3000 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M3000_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M3000_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M3000_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M3000_20162'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M3000_20162'),

            # --- MFV neutralino (gluino->neu neu->2T2B2S), M = 200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0200_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0200_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0200_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0200_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0200_20162'),

            # --- MFV neutralino, M = 300 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0300_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0300_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0300_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0300_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0300_20162'),

            # --- MFV neutralino, M = 400 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0400_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0400_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0400_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0400_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0400_20162'),

            # --- MFV neutralino, M = 600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0600_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0600_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0600_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0600_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0600_20162'),

            # --- MFV neutralino, M = 800 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0800_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0800_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0800_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0800_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0800_20162'),

            # --- MFV neutralino, M = 1200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1200_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M1200_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M1200_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M1200_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M1200_20162'),

            # --- MFV neutralino, M = 1600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1600_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M1600_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M1600_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M1600_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M1600_20162'),

            # --- MFV neutralino, M = 3000 ---
            getattr(Samples, 'mfv_neu_tau000100um_M3000_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M3000_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M3000_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M3000_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M3000_20162'),
        ]
        '''
        # Lepton-triggered samples
  
        samples = [
                # --- MFV neutralino, M = 200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0200_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0200_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0200_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0200_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0200_20162'),

            # --- MFV neutralino, M = 300 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0300_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0300_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0300_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0300_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0300_20162'),

            # --- MFV neutralino, M = 400 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0400_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0400_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0400_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0400_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0400_20162'),

            # --- MFV neutralino, M = 600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0600_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0600_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0600_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0600_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0600_20162'),

            # --- MFV neutralino, M = 800 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0800_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M0800_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M0800_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M0800_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M0800_20162'),

            # --- MFV neutralino, M = 1200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1200_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M1200_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M1200_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M1200_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M1200_20162'),

            # --- MFV neutralino, M = 1600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1600_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M1600_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M1600_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M1600_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M1600_20162'),

            # --- MFV neutralino, M = 3000 ---
            getattr(Samples, 'mfv_neu_tau000100um_M3000_20162'),
            getattr(Samples, 'mfv_neu_tau000300um_M3000_20162'),
            getattr(Samples, 'mfv_neu_tau001000um_M3000_20162'),
            getattr(Samples, 'mfv_neu_tau010000um_M3000_20162'),
            getattr(Samples, 'mfv_neu_tau030000um_M3000_20162'),

            # --- ZH (Z->LL), MS = 15 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M15_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M15_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M15_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M15_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M15_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M15_20162'),

            # --- ZH (Z->LL), MS = 40 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M40_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M40_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M40_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M40_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M40_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M40_20162'),

            # --- ZH (Z->LL), MS = 55 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M55_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M55_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M55_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M55_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M55_20162'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M55_20162'),

            # --- W+H (W->LNu), MS = 15 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M15_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M15_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M15_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M15_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M15_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M15_20162'),

            # --- W+H (W->LNu), MS = 40 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M40_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M40_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M40_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M40_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M40_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M40_20162'),

            # --- W+H (W->LNu), MS = 55 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M55_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M55_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M55_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M55_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M55_20162'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M55_20162'),

            # --- W-H (W->LNu), MS = 15 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M15_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M15_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M15_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M15_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M15_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M15_20162'),

            # --- W-H (W->LNu), MS = 40 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M40_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M40_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M40_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M40_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M40_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M40_20162'),

            # --- W-H (W->LNu), MS = 55 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M55_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M55_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M55_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M55_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M55_20162'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M55_20162'),
        ]


    if year == 2017:
        '''
        # ttH Private
        samples = [
            getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_2017'),
            getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_2017'),

            getattr(Samples, 'ttHToLLPs_dddd_tau000000100um_M0055_JOEY_2017'),
            getattr(Samples, 'ttHToLLPs_dddd_tau000001000um_M0055_JOEY_2017'),
            getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_JOEY_2017'),
            getattr(Samples, 'ttHToLLPs_dddd_tau000100000um_M0055_JOEY_2017'),
            
        ]

        # Jet-triggered samples
        samples = [
            # --- ggH, MS = 15 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M15_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M15_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M15_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M15_2017'),

            # --- ggH, MS = 40 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M40_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M40_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M40_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M40_2017'),

            # --- ggH, MS = 55 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M55_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M55_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M55_2017'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M55_2017'),

            # --- MFV stop -> bbar bbar, M = 200 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0200_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0200_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0200_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0200_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0200_2017'),

            # --- MFV stop -> bbar bbar, M = 300 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0300_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0300_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0300_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0300_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0300_2017'),

            # --- MFV stop -> bbar bbar, M = 400 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0400_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0400_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0400_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0400_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0400_2017'),

            # --- MFV stop -> bbar bbar, M = 600 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0600_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0600_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0600_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0600_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0600_2017'),

            # --- MFV stop -> bbar bbar, M = 800 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0800_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0800_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0800_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0800_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0800_2017'),

            # --- MFV stop -> bbar bbar, M = 1200 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M1200_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M1200_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M1200_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M1200_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M1200_2017'),

            # --- MFV stop -> bbar bbar, M = 1600 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M1600_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M1600_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M1600_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M1600_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M1600_2017'),

            # --- MFV stop -> bbar bbar, M = 3000 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M3000_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M3000_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M3000_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M3000_2017'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M3000_2017'),

            # --- MFV stop -> dbar dbar, M = 200 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0200_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0200_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0200_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0200_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0200_2017'),

            # --- MFV stop -> dbar dbar, M = 300 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0300_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0300_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0300_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0300_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0300_2017'),

            # --- MFV stop -> dbar dbar, M = 400 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0400_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0400_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0400_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0400_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0400_2017'),

            # --- MFV stop -> dbar dbar, M = 600 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0600_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0600_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0600_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0600_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0600_2017'),

            # --- MFV stop -> dbar dbar, M = 800 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0800_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0800_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0800_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0800_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0800_2017'),

            # --- MFV stop -> dbar dbar, M = 1200 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M1200_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M1200_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1200_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M1200_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M1200_2017'),

            # --- MFV stop -> dbar dbar, M = 1600 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M1600_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M1600_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1600_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M1600_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M1600_2017'),

            # --- MFV stop -> dbar dbar, M = 3000 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M3000_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M3000_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M3000_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M3000_2017'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M3000_2017'),

            # --- MFV neutralino (gluino->neu neu->2T2B2S), M = 200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0200_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0200_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0200_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0200_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0200_2017'),

            # --- MFV neutralino, M = 300 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0300_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0300_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0300_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0300_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0300_2017'),

            # --- MFV neutralino, M = 400 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0400_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0400_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0400_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0400_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0400_2017'),

            # --- MFV neutralino, M = 600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0600_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0600_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0600_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0600_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0600_2017'),

            # --- MFV neutralino, M = 800 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0800_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0800_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0800_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0800_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0800_2017'),

            # --- MFV neutralino, M = 1200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1200_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M1200_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M1200_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M1200_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M1200_2017'),

            # --- MFV neutralino, M = 1600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1600_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M1600_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M1600_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M1600_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M1600_2017'),

            # --- MFV neutralino, M = 3000 ---
            getattr(Samples, 'mfv_neu_tau000100um_M3000_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M3000_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M3000_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M3000_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M3000_2017'),
        ]
        '''
        # Lepton-triggered samples

        samples = [
            # --- MFV neutralino, M = 200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0200_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0200_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0200_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0200_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0200_2017'),

            # --- MFV neutralino, M = 300 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0300_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0300_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0300_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0300_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0300_2017'),

            # --- MFV neutralino, M = 400 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0400_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0400_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0400_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0400_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0400_2017'),

            # --- MFV neutralino, M = 600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0600_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0600_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0600_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0600_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0600_2017'),

            # --- MFV neutralino, M = 800 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0800_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M0800_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M0800_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M0800_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M0800_2017'),

            # --- MFV neutralino, M = 1200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1200_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M1200_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M1200_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M1200_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M1200_2017'),

            # --- MFV neutralino, M = 1600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1600_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M1600_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M1600_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M1600_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M1600_2017'),

            # --- MFV neutralino, M = 3000 ---
            getattr(Samples, 'mfv_neu_tau000100um_M3000_2017'),
            getattr(Samples, 'mfv_neu_tau000300um_M3000_2017'),
            getattr(Samples, 'mfv_neu_tau001000um_M3000_2017'),
            getattr(Samples, 'mfv_neu_tau010000um_M3000_2017'),
            getattr(Samples, 'mfv_neu_tau030000um_M3000_2017'),

            # Lepton-triggered VH
            # --- ZH (Z->LL), MS = 15 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M15_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M15_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M15_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M15_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M15_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M15_2017'),

            # --- ZH (Z->LL), MS = 40 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M40_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M40_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M40_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M40_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M40_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M40_2017'),

            # --- ZH (Z->LL), MS = 55 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M55_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M55_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M55_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M55_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M55_2017'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M55_2017'),

            # --- W+H (W->LNu), MS = 15 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M15_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M15_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M15_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M15_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M15_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M15_2017'),

            # --- W+H (W->LNu), MS = 40 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M40_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M40_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M40_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M40_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M40_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M40_2017'),

            # --- W+H (W->LNu), MS = 55 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M55_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M55_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M55_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M55_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M55_2017'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M55_2017'),

            # --- W-H (W->LNu), MS = 15 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M15_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M15_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M15_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M15_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M15_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M15_2017'),

            # --- W-H (W->LNu), MS = 40 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M40_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M40_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M40_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M40_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M40_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M40_2017'),

            # --- W-H (W->LNu), MS = 55 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M55_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M55_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M55_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M55_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M55_2017'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M55_2017'),
    ]


    if year == 2018:
        '''
        # ttH Private
        samples = [
            getattr(Samples, 'ttHToLLPs_bbbb_tau000010000um_M0055_2018'),
            getattr(Samples, 'ttHToLLPs_dddd_tau000010000um_M0055_2018'),
        ]

        # Jet-triggered samples
        samples = [
            # --- ggH, MS = 15 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M15_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M15_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M15_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M15_2018'),

            # --- ggH, MS = 40 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M40_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M40_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M40_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M40_2018'),

            # --- ggH, MS = 55 ---
            getattr(Samples, 'ggHToSSTodddd_tau000100um_M55_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau1mm_M55_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau10mm_M55_2018'),
            getattr(Samples, 'ggHToSSTodddd_tau100mm_M55_2018'),

            # --- MFV stop -> bbar bbar, M = 200 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0200_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0200_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0200_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0200_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0200_2018'),

            # --- MFV stop -> bbar bbar, M = 300 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0300_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0300_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0300_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0300_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0300_2018'),

            # --- MFV stop -> bbar bbar, M = 400 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0400_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0400_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0400_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0400_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0400_2018'),

            # --- MFV stop -> bbar bbar, M = 600 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0600_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0600_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0600_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0600_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0600_2018'),

            # --- MFV stop -> bbar bbar, M = 800 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M0800_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M0800_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M0800_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M0800_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M0800_2018'),

            # --- MFV stop -> bbar bbar, M = 1200 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M1200_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M1200_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M1200_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M1200_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M1200_2018'),

            # --- MFV stop -> bbar bbar, M = 1600 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M1600_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M1600_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M1600_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M1600_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M1600_2018'),

            # --- MFV stop -> bbar bbar, M = 3000 ---
            getattr(Samples, 'mfv_stopbbarbbar_tau000100um_M3000_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau000300um_M3000_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau001000um_M3000_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau010000um_M3000_2018'),
            getattr(Samples, 'mfv_stopbbarbbar_tau030000um_M3000_2018'),

            # --- MFV stop -> dbar dbar, M = 200 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0200_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0200_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0200_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0200_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0200_2018'),

            # --- MFV stop -> dbar dbar, M = 300 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0300_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0300_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0300_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0300_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0300_2018'),

            # --- MFV stop -> dbar dbar, M = 400 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0400_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0400_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0400_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0400_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0400_2018'),

            # --- MFV stop -> dbar dbar, M = 600 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0600_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0600_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0600_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0600_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0600_2018'),

            # --- MFV stop -> dbar dbar, M = 800 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M0800_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0800_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0800_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0800_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M0800_2018'),

            # --- MFV stop -> dbar dbar, M = 1200 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M1200_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M1200_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1200_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M1200_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M1200_2018'),

            # --- MFV stop -> dbar dbar, M = 1600 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M1600_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M1600_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M1600_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M1600_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M1600_2018'),

            # --- MFV stop -> dbar dbar, M = 3000 ---
            getattr(Samples, 'mfv_stopdbardbar_tau000100um_M3000_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau000300um_M3000_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau001000um_M3000_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau010000um_M3000_2018'),
            getattr(Samples, 'mfv_stopdbardbar_tau030000um_M3000_2018'),

            # --- MFV neutralino (gluino->neu neu->2T2B2S), M = 200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0200_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0200_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0200_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0200_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0200_2018'),

            # --- MFV neutralino, M = 300 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0300_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0300_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0300_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0300_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0300_2018'),

            # --- MFV neutralino, M = 400 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0400_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0400_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0400_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0400_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0400_2018'),

            # --- MFV neutralino, M = 600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0600_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0600_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0600_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0600_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0600_2018'),

            # --- MFV neutralino, M = 800 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0800_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0800_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0800_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0800_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0800_2018'),

            # --- MFV neutralino, M = 1200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1200_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M1200_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M1200_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M1200_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M1200_2018'),

            # --- MFV neutralino, M = 1600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1600_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M1600_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M1600_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M1600_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M1600_2018'),

            # --- MFV neutralino, M = 3000 ---
            getattr(Samples, 'mfv_neu_tau000100um_M3000_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M3000_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M3000_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M3000_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M3000_2018'),
        ]
        '''
        # Lepton-triggered samples
        samples = [

            # --- MFV neutralino, M = 200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0200_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0200_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0200_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0200_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0200_2018'),

            # --- MFV neutralino, M = 300 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0300_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0300_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0300_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0300_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0300_2018'),

            # --- MFV neutralino, M = 400 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0400_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0400_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0400_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0400_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0400_2018'),

            # --- MFV neutralino, M = 600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0600_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0600_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0600_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0600_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0600_2018'),

            # --- MFV neutralino, M = 800 ---
            getattr(Samples, 'mfv_neu_tau000100um_M0800_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M0800_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M0800_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M0800_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M0800_2018'),

            # --- MFV neutralino, M = 1200 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1200_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M1200_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M1200_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M1200_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M1200_2018'),

            # --- MFV neutralino, M = 1600 ---
            getattr(Samples, 'mfv_neu_tau000100um_M1600_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M1600_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M1600_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M1600_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M1600_2018'),

            # --- MFV neutralino, M = 3000 ---
            getattr(Samples, 'mfv_neu_tau000100um_M3000_2018'),
            getattr(Samples, 'mfv_neu_tau000300um_M3000_2018'),
            getattr(Samples, 'mfv_neu_tau001000um_M3000_2018'),
            getattr(Samples, 'mfv_neu_tau010000um_M3000_2018'),
            getattr(Samples, 'mfv_neu_tau030000um_M3000_2018'),

            # Lepton-triggered VH
            # --- ZH (Z->LL), MS = 15 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M15_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M15_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M15_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M15_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M15_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M15_2018'),

            # --- ZH (Z->LL), MS = 40 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M40_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M40_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M40_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M40_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M40_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M40_2018'),

            # --- ZH (Z->LL), MS = 55 ---
            getattr(Samples, 'ZHToSSTodddd_tau100um_M55_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau300um_M55_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau1mm_M55_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau3mm_M55_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau10mm_M55_2018'),
            getattr(Samples, 'ZHToSSTodddd_tau30mm_M55_2018'),

            # --- W+H (W->LNu), MS = 15 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M15_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M15_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M15_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M15_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M15_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M15_2018'),

            # --- W+H (W->LNu), MS = 40 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M40_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M40_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M40_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M40_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M40_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M40_2018'),

            # --- W+H (W->LNu), MS = 55 ---
            getattr(Samples, 'WplusHToSSTodddd_tau100um_M55_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau300um_M55_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau1mm_M55_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau3mm_M55_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau10mm_M55_2018'),
            getattr(Samples, 'WplusHToSSTodddd_tau30mm_M55_2018'),

            # --- W-H (W->LNu), MS = 15 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M15_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M15_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M15_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M15_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M15_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M15_2018'),

            # --- W-H (W->LNu), MS = 40 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M40_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M40_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M40_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M40_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M40_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M40_2018'),

            # --- W-H (W->LNu), MS = 55 ---
            getattr(Samples, 'WminusHToSSTodddd_tau100um_M55_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau300um_M55_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau1mm_M55_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau3mm_M55_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau10mm_M55_2018'),
            getattr(Samples, 'WminusHToSSTodddd_tau30mm_M55_2018'),
    ]

    
    ''' ## Old Stuff from repo
    if use_btag_triggers :
       samples = pick_samples(dataset, qcd=True, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
       #samples = pick_samples(dataset, qcd=False, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=True, DisplacedJet_data=True) #set settings.is_mc to False
    elif use_btag_vetoLepHT_triggers :
        #samples = [getattr(Samples, 'mfv_neu_tau001000um_M0400_2017')]
        #samples = [getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0400_2017')]
        #samples = [getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0200_2017')]
        #samples = [getattr(Samples, 'ggHToSSTodddd_tau1mm_M55_2017')]

        if settings.is_mc :
            #samples = [getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0400_2017')]
            samples = pick_samples(dataset, qcd=False, data=False, all_signal=True, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
            #samples = pick_samples(dataset, qcd=True, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
        else :
            samples = pick_samples(dataset, qcd=False, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=True, DisplacedJet_data=True) #set settings.is_mc to False

    elif use_MET_triggers :
       samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
    elif use_Lepton_triggers :
        #samples = pick_samples(dataset, qcd=True, data = False, all_signal=True, qcd_lep=True, leptonic=True, ttbar=True, diboson=True, Lepton_data=False) #bkg template
        samples = pick_samples(dataset, qcd=False, data = False, all_signal=True, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False) #trk ineff apply
        #samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, met=True, diboson=False, Lepton_data=True) #set settings.is_mc to False
    elif use_Muon_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=True)
    elif use_Electron_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=False)
    else :
        samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
    '''

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2016.json' if year in [20161, 20162] else 'ana_2017p8.json'), limit_ttbar=True)
    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)#, bjet_trigger_veto_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
