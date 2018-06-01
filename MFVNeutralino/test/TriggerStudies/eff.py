#!/usr/bin/env python

from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.Tools.Year import year

cmssw_settings = CMSSWSettings()
cmssw_settings.is_mc = True

version = '2017v1'
batch_name = 'TrigEff%s' % version

mu_thresh_hlt = 27
mu_thresh_offline = 30

tfileservice(process, 'eff.root')
global_tag(process, which_global_tag(cmssw_settings))
#want_summary(process)
#report_every(process, 1)
max_events(process, 10000)
input_files(process, {
    (2017,True): '/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/mc/RunIIFall17MiniAOD/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/20000/FA596B3F-C303-E811-B69C-20CF3027A6DC.root',
    (2017,False):'/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/store/data/Run2017F/SingleMuon/MINIAOD/17Nov2017-v1/70001/DC73F8F1-A5EA-E711-A5F3-141877410B4D.root',
    }[(year, cmssw_settings.is_mc)])

process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')

process.selectedPatJets.src = 'slimmedJets'
process.selectedPatJets.cut = jtupleParams.jetCut

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu%i_v*' % mu_thresh_hlt]

process.den = cms.EDAnalyzer('MFVTriggerEfficiency',
                             use_weight = cms.int32(0),
                             require_hlt = cms.int32(-1),
                             require_l1 = cms.int32(-1),
                             require_muon = cms.bool(True),
                             require_4jets = cms.bool(True),
                             require_6jets = cms.bool(False),
                             require_4thjetpt = cms.double(0.),
                             require_6thjetpt = cms.double(0.),
                             require_ht = cms.double(-1),
                             muons_src = cms.InputTag('slimmedMuons'),
                             muon_cut = cms.string(jtupleParams.muonCut.value() + ' && pt > %i' % mu_thresh_offline),
                             genjets_src = cms.InputTag(''), #'ak4GenJets' if is_mc else ''),
                             )

process.denht1000 = process.den.clone(require_ht = 1000)
process.denjet6pt75 = process.den.clone(require_6thjetpt = 75)
process.denht1000jet6pt75 = process.den.clone(require_ht = 1000, require_6thjetpt = 75)
process.p = cms.Path(process.mutrig * process.selectedPatJets * process.mfvTriggerFloats * process.den * process.denht1000 * process.denjet6pt75 * process.denht1000jet6pt75)

process.dennomu = process.den.clone(require_muon = False)
process.dennomuht1000 = process.den.clone(require_muon = False, require_ht = 1000)
process.dennomujet6pt75 = process.den.clone(require_muon = False, require_6thjetpt = 75)
process.dennomuht1000jet6pt75 = process.den.clone(require_muon = False, require_ht = 1000, require_6thjetpt = 75)
process.pnomu = cms.Path(process.selectedPatJets * process.mfvTriggerFloats * process.dennomu * process.dennomuht1000 * process.dennomujet6pt75 * process.dennomuht1000jet6pt75)

for x in '', 'ht1000', 'jet6pt75', 'ht1000jet6pt75', 'nomu', 'nomuht1000', 'nomujet6pt75', 'nomuht1000jet6pt75':
    num = getattr(process, 'den%s' % x).clone(require_hlt = 0)
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
        samples = Samples.auxiliary_data_samples_2017 + Samples.leptonic_samples_2017 + Samples.ttbar_samples_2017
        masses = (400, 800, 1200, 1600)
        samples += [getattr(Samples, 'mfv_neu_tau01000um_M%04i_2017' % m) for m in masses] + [Samples.mfv_neu_tau10000um_M0800_2017]
    
    dataset = 'miniaod'
    set_splitting(samples, dataset, 'default', json_path('ana_2017.json'), 50)

    ms = MetaSubmitter(batch_name)
    ms.common.dataset = dataset
    ms.common.ex = year
    ms.common.pset_modifier = is_mc_modifier
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
