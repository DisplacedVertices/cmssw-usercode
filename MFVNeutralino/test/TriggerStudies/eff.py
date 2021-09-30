#!/usr/bin/env python

from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.Tools.Year import year
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

settings = CMSSWSettings()
settings.is_mc = True
#settings.is_mc = False
settings.cross = '' # 2017to2018' # 2017to2017p8'

version = '2017ULv1_mu_METNoMu'

mu_thresh_hlt = 27
mu_thresh_offline = 35
ele_thresh_hlt = 27
ele_thresh_offline = 35
weight_l1ecal = ''

tfileservice(process, 'eff.root')
global_tag(process, which_global_tag(settings))
#want_summary(process)
#report_every(process, 1)
max_events(process, 10000)
dataset = 'miniaod'
#sample_files(process, 'wjetstolnu_2017', dataset, 1)
input_files(process,[
                    #'/store/mc/RunIISummer20UL17MiniAOD/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/260000/07B5521B-4BD8-CF46-B11D-E220B439B5C1.root',
                    'root://pubxrootd.hep.wisc.edu//store/mc/RunIISummer20UL17MiniAOD/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/270000/C94F54BD-07CE-6F4B-B3BD-90B21F08F40A.root'
                    #'/store/data/Run2017B/SingleMuon/MINIAOD/09Aug2019_UL2017-v1/130000/D10B713B-5923-6548-BCC1-B4671179D853.root'
            ])

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
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu%i_v*' % mu_thresh_hlt]

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
                             require_muon = cms.bool(True),
                             require_electron = cms.bool(False),
                             require_metfilters = cms.bool(True),
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

process.denht1000 = process.den.clone(require_ht = 1000)
process.denjet6pt75 = process.den.clone(require_6thjetpt = 75)
process.denht1000jet6pt75 = process.den.clone(require_ht = 1000, require_6thjetpt = 75)
#process.p = cms.Path(process.weightSeq * process.mutrig * process.updatedJetsSeqMiniAOD * process.selectedPatJets * process.mfvTriggerFloats * process.den * process.denht1000 * process.denjet6pt75 * process.denht1000jet6pt75)
process.p = cms.Path(process.weightSeq * process.mutrig * process.updatedJetsSeqMiniAOD * process.BadPFMuonFilterUpdateDz * process.fullPatMetSequence * process.selectedPatJets * process.mfvTriggerFloats * process.den)

#process.dennomu = process.den.clone(require_muon = False)
#process.dennomuht1000 = process.den.clone(require_muon = False, require_ht = 1000)
#process.dennomujet6pt75 = process.den.clone(require_muon = False, require_6thjetpt = 75)
#process.dennomuht1000jet6pt75 = process.den.clone(require_muon = False, require_ht = 1000, require_6thjetpt = 75)
#process.pnomu = cms.Path(process.weightSeq * process.updatedJetsSeqMiniAOD * process.selectedPatJets * process.mfvTriggerFloats * process.dennomu * process.dennomuht1000 * process.dennomujet6pt75 * process.dennomuht1000jet6pt75)

#for x in '', 'ht1000', 'jet6pt75', 'ht1000jet6pt75', 'nomu', 'nomuht1000', 'nomujet6pt75', 'nomuht1000jet6pt75':
for x in ['']:
    num = getattr(process, 'den%s' % x).clone(require_hlt = 20)
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
        samples = Samples.auxiliary_data_samples_2017 + Samples.leptonic_samples_2017 + Samples.met_samples_2017
        samples += Samples.mfv_splitSUSY_samples_2017
    elif year == 2018:
        samples = Samples.auxiliary_data_samples_2018 + Samples.leptonic_samples_2018 + Samples.met_samples_2018
    
    samples = [s for s in samples if s.has_dataset(dataset) and (s.is_mc or not settings.cross)]
    set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'), 5)

    ms = MetaSubmitter('TrigEff%s%s' % (version, '_' + settings.cross if settings.cross else ''), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier(cross=settings.cross))
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
