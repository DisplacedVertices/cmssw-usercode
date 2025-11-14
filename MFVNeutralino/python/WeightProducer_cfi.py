import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PileupWeights import get_pileup_weights
from JMTucker.Tools.Year import year #Abby change
import os #Abby change

if (year == 20161) : #Abby changes begin
    # #20161 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/161UL/puWeights.json.gz')
    mujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/muon161UL_Z.json.gz')
    elejson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/electron161UL.json.gz')
elif (year == 20162) : 
    # #20162 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/162UL/puWeights.json.gz')
    mujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/muon162UL_Z.json.gz')
    elejson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/electron162UL.json.gz')
elif (year == 2017) :
    #2017 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/17UL/puWeights.json.gz')
    mujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/muon17UL_Z.json.gz')
    elejson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/electron17UL.json.gz')
elif (year == 2018) :
    # #2018 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/18UL/puWeights.json.gz')
    mujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/muon18UL_Z.json.gz')
    elejson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/lep_eff/electron18UL.json.gz')
else :
    print("NO YEAR MATCHED; YEARS ARE 2018, 2017, 20161, and 20162") #Abby changes end

mfvWeight = cms.EDProducer('MFVWeightProducer',
                           throw_if_no_mcstat = cms.bool(True),
                           mevent_src = cms.InputTag('mfvEvent'),
                           vertex_src = cms.InputTag('mfvSelectedVerticesTight'), #Abby change #Alec then changed to tight
                           enable = cms.bool(True),
                           prints = cms.untracked.bool(False), #Alec changed to true
                           histos = cms.untracked.bool(True),
                           partial_mc_stats_weight = cms.double(1),
                           weight_gen = cms.bool(True),
                           weight_gen_sign_only = cms.bool(False),
                           weight_pileup_2 = cms.bool(True), #using central values from json #Abby change
                           pileup_weights = cms.vdouble(*get_pileup_weights('default')),
                           weight_npv = cms.bool(False),
                           npv_weights = cms.vdouble(),
                           misc_weight_indices = cms.vint32(),
                           apply_lepsf = cms.bool(True), #Abby changes begin
                           apply_roccor = cms.bool(True), #rocchester corrections for muons
                           pujson = cms.string(pujson_path),
                           elejson = cms.string(elejson_path), 
                           mujson = cms.string(mujson_path), #Abby changes end
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
