#!/usr/bin/env python

from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.Tools.Year import year
from JMTucker.MFVNeutralino.NtupleCommon import use_MET_triggers
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

useElectron = False # True: use electron trigger as reference; False: use muon trigger as reference
settings = CMSSWSettings()
settings.is_mc = True
settings.cross = '' # 2017to2018' # 2017to2017p8'

version = '2017ULv1_METNoMu'
version += '_ele' if useElectron else '_mu'

trig_id = -1 # the require_hlt number for the trigger we want to measure
mu_thresh_hlt = 27
mu_thresh_offline = 35
ele_thresh_hlt = 35
ele_thresh_offline = 38
weight_l1ecal = ''

tfileservice(process, 'eff.root')
global_tag(process, which_global_tag(settings))
max_events(process, 10000)
dataset = 'miniaod'
sample_files(process, 'wjetstolnu_2017', dataset, 1)

process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.UpdatedJets_cff')
process.load('JMTucker.Tools.WeightProducer_cfi')
#process.load('JMTucker.Tools.GoodPrimaryVertices_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff") 

#process.goodOfflinePrimaryVertices.input_is_miniaod = True
process.selectedPatJets.src = 'updatedJetsMiniAOD'
process.selectedPatJets.cut = jtupleParams.jetCut
process.mfvTriggerFloats.met_src = cms.InputTag('slimmedMETs', '', 'BasicAnalyzer') # BasicAnalyzer
process.mfvTriggerFloats.isMC = settings.is_mc
process.mfvTriggerFloats.year = settings.year
if not settings.is_mc:
  process.mfvTriggerFloats.met_filters_src = cms.InputTag('TriggerResults', '', 'RECO')


from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.reftrig = hltHighLevel.clone()
if useElectron:
  process.reftrig.HLTPaths = ['HLT_Ele%i_WPTight_Gsf_v*' % ele_thresh_hlt]
else:
  process.reftrig.HLTPaths = ['HLT_IsoMu%i_v*' % mu_thresh_hlt]

process.weightSeq = cms.Sequence(process.jmtWeightMiniAOD)

if weight_l1ecal and settings.is_mc and settings.year == 2017 and settings.cross == '':
    process.load('JMTucker.Tools.L1ECALPrefiringWeightProducer_cfi')
    if 'separate' in weight_l1ecal:
        w = process.jmtWeightMiniAODL1Ecal = process.jmtWeightMiniAOD.clone()
        process.weightSeq.insert(0, process.prefiringweight * process.jmtWeightMiniAODL1Ecal)
    else:
        w = process.jmtWeightMiniAOD
    which = 'nonPrefiringProb'
    if 'up' in weight_l1ecal:
        which += 'Up'
    elif 'down' in weight_l1ecal:
        which += 'Down'
    w.weight_misc = True
    w.misc_srcs = cms.VInputTag(cms.InputTag('prefiringweight', which, 'BasicAnalyzer'))

# MET correction
runMetCorAndUncFromMiniAOD(process,
                           isData = not settings.is_mc,
                           )

process.load('JMTucker.Tools.METBadPFMuonDzFilter_cfi')

process.den = cms.EDAnalyzer('MFVTriggerEfficiency',
                             use_jetpt_weights = cms.int32(0),
                             require_hlt = cms.int32(-1),
                             require_l1 = cms.int32(-1),
                             require_muon = cms.bool(False),
                             require_electron = cms.bool(False),
                             require_metfilters = cms.bool(False),
                             require_1jet = cms.bool(True),#for MET trigger
                             require_4jets = cms.bool(False),#for MET trigger
                             require_6jets = cms.bool(False),
                             require_1stjetpt = cms.double(80.),
                             require_4thjetpt = cms.double(0.),
                             require_6thjetpt = cms.double(0.),
                             require_ht = cms.double(-1),
                             weight_src = cms.InputTag('jmtWeightMiniAOD'),
                             muons_src = cms.InputTag('slimmedMuons'),
                             muon_cut = cms.string(jtupleParams.muonCut.value() + ' && pt > %i' % mu_thresh_offline),
                             electrons_src = cms.InputTag('slimmedElectrons'),
                             electron_cut = cms.string('pt > %i && abs(eta) < 2.5' % ele_thresh_offline),
                             genjets_src = cms.InputTag(''), #'ak4GenJets' if is_mc else ''),
                             )

if use_MET_triggers:
  process.den.require_metfilters = cms.bool(True)
  trig_id = 20
if useElectron:
  process.den.require_electron = cms.bool(True)
else:
  process.den.require_muon = cms.bool(True)
process.denht1000 = process.den.clone(require_ht = 1000)
process.denjet6pt75 = process.den.clone(require_6thjetpt = 75)
process.denht1000jet6pt75 = process.den.clone(require_ht = 1000, require_6thjetpt = 75)
process.p = cms.Path(process.weightSeq * process.reftrig * process.updatedJetsSeqMiniAOD * process.BadPFMuonFilterUpdateDz * process.fullPatMetSequence * process.selectedPatJets * process.mfvTriggerFloats * process.den)

for x in ['']:
    num = getattr(process, 'den%s' % x).clone(require_hlt = trig_id)
    if 'separate' in weight_l1ecal:
        num.weight_src = 'jmtWeightMiniAODL1Ecal'
    setattr(process, 'num%s' % x, num)
    if 'nomu' in x:
        process.pnomu *= num
    else:
        process.p *= num

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.MetaSubmitter import *

    if year == 2017:
        samples = Samples.leptonic_samples_2017 + Samples.met_samples_2017
        if useElectron:
          samples += Samples.singleelectron_data_samples_2017
        else:
          samples += Samples.auxiliary_data_samples_2017
        samples += Samples.mfv_splitSUSY_samples_2017
    elif year == 2018:
        samples = Samples.leptonic_samples_2018 + Samples.met_samples_2018
        if useElectron:
          samples += Samples.egamma_data_samples_2018
        else:
          samples += Samples.auxiliary_data_samples_2018
    
    samples = [s for s in samples if s.has_dataset(dataset) and (s.is_mc or not settings.cross)]
    set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'), 5)

    ms = MetaSubmitter('TrigEff%s%s' % (version, '_' + settings.cross if settings.cross else ''), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier(cross=settings.cross))
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
