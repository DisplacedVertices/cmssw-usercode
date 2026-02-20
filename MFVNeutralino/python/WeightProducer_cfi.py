import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PileupWeights import get_pileup_weights
from JMTucker.Tools.Year import year
from JMTucker.MFVNeutralino.NtupleCommon import use_Lepton_triggers,use_Muon_triggers,use_Electron_triggers
import os

if (year == 20161) :
    # #20161 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/161UL/puWeights.json.gz')
    mujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/muon161UL_Z.json.gz')
    elejson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/electron161UL.json.gz')
    muSFjson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lepSF_json/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_SingleMuonTriggers_schemaV2.json')
    eleSFjson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lepSF_json/electron_trigsf_runII.json')
elif (year == 20162) : 
    # #20162 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/162UL/puWeights.json.gz')
    mujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/muon162UL_Z.json.gz')
    elejson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/electron162UL.json.gz')
    muSFjson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lepSF_json/Efficiencies_muon_generalTracks_Z_Run2016_UL_SingleMuonTriggers_schemaV2.json')
    eleSFjson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lepSF_json/electron_trigsf_runII.json')
elif (year == 2017) :
    #2017 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/17UL/puWeights.json.gz')
    mujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/muon17UL_Z.json.gz')
    elejson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/electron17UL.json.gz')
    muSFjson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lepSF_json/Efficiencies_muon_generalTracks_Z_Run2017_UL_SingleMuonTriggers_schemaV2.json')
    eleSFjson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lepSF_json/electron_trigsf_runII.json')
elif (year == 2018) :
    # #2018 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/18UL/puWeights.json.gz')
    mujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/muon18UL_Z.json.gz')
    elejson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/electron18UL.json.gz')
    muSFjson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lepSF_json/Efficiencies_muon_generalTracks_Z_Run2018_UL_SingleMuonTriggers_schemaV2.json')
    eleSFjson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lepSF_json/electron_trigsf_runII.json')
else :
    print("NO YEAR MATCHED; YEARS ARE 2018, 2017, 20161, and 20162")

mfvWeight = cms.EDProducer('MFVWeightProducer',
                           throw_if_no_mcstat = cms.bool(True),
                           mevent_src = cms.InputTag('mfvEvent'),
                           vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                           enable = cms.bool(True),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(True),
                           partial_mc_stats_weight = cms.double(1),
                           weight_gen = cms.bool(True),
                           weight_gen_sign_only = cms.bool(False),
                           weight_pileup = cms.bool(True), #using central values from json
                           pileup_weights = cms.vdouble(*get_pileup_weights('default')),
                           weight_npv = cms.bool(False),
                           npv_weights = cms.vdouble(),
                           misc_weight_indices = cms.vint32(),
                           apply_lepsf = cms.bool(True) if (use_Lepton_triggers or use_Muon_triggers or use_Electron_triggers) else cms.bool(False),
                           apply_roccor = cms.bool(False), # cms.bool(True) if use_Lepton_triggers else cms.bool(False), #rochester corrections for muons: we turned this off after seeing large weights; we're insensitive to muon momentum anyway
                           pujson = cms.string(pujson_path),
                           elejson = cms.string(elejson_path),
                           mujson = cms.string(mujson_path),
                           muSFjson = cms.string(muSFjson_path),
                           eleSFjson = cms.string(eleSFjson_path),
                           )

def half_mc_by_lumi(process, first=True):
    assert hasattr(process, 'mfvWeight')
    process.load('JMTucker.Tools.HalfMCByLumi_cfi')
    process.HalfMCByLumi.first = first
    for p in process.paths.itervalues():
        p.replace(process.mfvWeight, process.HalfMCByLumi * process.mfvWeight)
    process.mfvWeight.partial_mc_stats_weight = 0.5 # generally not different by more than 0.1%

def quarter_mc_by_lumi(process, first=True, second=False, third=False, fourth=False):
    assert hasattr(process, 'mfvWeight')
    process.load('JMTucker.Tools.QuarterMCByLumi_cfi')
    process.QuarterMCByLumi.first = first
    process.QuarterMCByLumi.second = second
    process.QuarterMCByLumi.third = third
    process.QuarterMCByLumi.fourth = fourth
    nquarters = [first,second,third,fourth].count(True)
    for p in process.paths.itervalues():
        p.replace(process.mfvWeight, process.QuarterMCByLumi * process.mfvWeight)
    process.mfvWeight.partial_mc_stats_weight = 0.25 * nquarters 
