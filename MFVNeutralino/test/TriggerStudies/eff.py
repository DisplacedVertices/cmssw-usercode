#!/usr/bin/env python

from DVCode.Tools.BasicAnalyzer_cfg import *
from DVCode.Tools.PATTupleSelection_cfi import jtupleParams
from DVCode.Tools.Year import year

settings = CMSSWSettings()
settings.is_mc = True
settings.cross = '' # 2017to2018' # 2017to2017p8'

version = '2017p8v4'

mu_thresh_hlt = 27
mu_thresh_offline = 30
weight_l1ecal = ''

tfileservice(process, 'eff.root')
global_tag(process, which_global_tag(settings))
#want_summary(process)
#report_every(process, 1)
max_events(process, -1)
dataset = 'miniaod'
sample_files(process, 'wjetstolnu_2017', dataset, 1)

process.load('DVCode.Tools.MCStatProducer_cff')
process.load('DVCode.Tools.UpdatedJets_cff')
process.load('DVCode.Tools.WeightProducer_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('DVCode.MFVNeutralino.TriggerFloats_cff')

process.selectedPatJets.src = 'updatedJetsMiniAOD'
process.selectedPatJets.cut = jtupleParams.jetCut

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu%i_v*' % mu_thresh_hlt]

process.weightSeq = cms.Sequence(process.jmtWeightMiniAOD)

if weight_l1ecal and settings.is_mc and settings.year == 2017 and settings.cross == '':
    process.load('DVCode.Tools.L1ECALPrefiringWeightProducer_cfi')
    if 'separate' in weight_l1ecal:
        w = process.jmtWeightMiniAODL1Ecal = process.jmtWeightMiniAOD.clone()
        process.weightSeq.insert(0, process.prefiringweight * process.jmtWeightMiniAODL1Ecal)
    else:
        w = process.jmtWeightMiniAOD
    which = 'NonPrefiringProb'
    if 'up' in weight_l1ecal:
        which += 'Up'
    elif 'down' in weight_l1ecal:
        which += 'Down'
    w.weight_misc = True
    w.misc_srcs = cms.VInputTag(cms.InputTag('prefiringweight', which))

process.den = cms.EDAnalyzer('MFVTriggerEfficiency',
                             use_jetpt_weights = cms.int32(0),
                             require_hlt = cms.int32(-1),
                             require_l1 = cms.int32(-1),
                             require_muon = cms.bool(True),
                             require_4jets = cms.bool(True),
                             require_6jets = cms.bool(False),
                             require_4thjetpt = cms.double(0.),
                             require_6thjetpt = cms.double(0.),
                             require_ht = cms.double(-1),
                             weight_src = cms.InputTag('jmtWeightMiniAOD'),
                             muons_src = cms.InputTag('slimmedMuons'),
                             muon_cut = cms.string(jtupleParams.muonCut.value() + ' && pt > %i' % mu_thresh_offline),
                             genjets_src = cms.InputTag(''), #'ak4GenJets' if is_mc else ''),
                             )

process.denht1000 = process.den.clone(require_ht = 1000)
process.denjet6pt75 = process.den.clone(require_6thjetpt = 75)
process.denht1000jet6pt75 = process.den.clone(require_ht = 1000, require_6thjetpt = 75)
process.p = cms.Path(process.weightSeq * process.mutrig * process.updatedJetsSeqMiniAOD * process.selectedPatJets * process.mfvTriggerFloats * process.den * process.denht1000 * process.denjet6pt75 * process.denht1000jet6pt75)

process.dennomu = process.den.clone(require_muon = False)
process.dennomuht1000 = process.den.clone(require_muon = False, require_ht = 1000)
process.dennomujet6pt75 = process.den.clone(require_muon = False, require_6thjetpt = 75)
process.dennomuht1000jet6pt75 = process.den.clone(require_muon = False, require_ht = 1000, require_6thjetpt = 75)
process.pnomu = cms.Path(process.weightSeq * process.updatedJetsSeqMiniAOD * process.selectedPatJets * process.mfvTriggerFloats * process.dennomu * process.dennomuht1000 * process.dennomujet6pt75 * process.dennomuht1000jet6pt75)

for x in '', 'ht1000', 'jet6pt75', 'ht1000jet6pt75', 'nomu', 'nomuht1000', 'nomujet6pt75', 'nomuht1000jet6pt75':
    num = getattr(process, 'den%s' % x).clone(require_hlt = 0)
    if 'separate' in weight_l1ecal:
        num.weight_src = 'jmtWeightMiniAODL1Ecal'
    setattr(process, 'num%s' % x, num)
    if 'nomu' in x:
        process.pnomu *= num
    else:
        process.p *= num

import DVCode.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import DVCode.Tools.Samples as Samples
    from DVCode.Tools.MetaSubmitter import *

    if year == 2017:
        samples = Samples.auxiliary_data_samples_2017 + Samples.leptonic_samples_2017
        masses = (400, 800, 1200, 1600)
        samples += [getattr(Samples, 'mfv_neu_tau001000um_M%04i_2017' % m) for m in masses] + [Samples.mfv_neu_tau010000um_M0800_2017]
    elif year == 2018:
        samples = Samples.auxiliary_data_samples_2018
    
    samples = [s for s in samples if s.has_dataset(dataset) and (s.is_mc or not settings.cross)]
    set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'), 50)

    ms = MetaSubmitter('TrigEff%s%s' % (version, '_' + settings.cross if settings.cross else ''), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier(cross=settings.cross))
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
