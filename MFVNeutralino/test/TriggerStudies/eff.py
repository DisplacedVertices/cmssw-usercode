#!/usr/bin/env python

from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.Tools.Year import year

settings = CMSSWSettings()
settings.is_mc = True
settings.cross = '' # 2017to2018' # 2017to2017p8'

version = '2017v0p6'
#version = '2017v0p6_tighterbjetpt'

mu_thresh_hlt = 27
mu_thresh_offline = 30
el_thresh_offline = 30
weight_l1ecal = ''

tfileservice(process, 'eff.root')
global_tag(process, which_global_tag(settings))
#want_summary(process)
#report_every(process, 1)
max_events(process, -1)
dataset = 'miniaod'
#sample_files(process, 'wjetstolnu_2017', dataset, 1)
sample_files(process, 'mfv_neu_tau001000um_M0400_2017', dataset, 1)

process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.UpdatedJets_cff')
process.load('JMTucker.Tools.WeightProducer_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')

process.selectedPatJets.src = 'updatedJetsMiniAOD'
process.selectedPatJets.cut = jtupleParams.jetCut

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
                             require_electron = cms.bool(False),
                             do_ttbar_selection = cms.bool(False),
                             require_2jets = cms.bool(False),
                             require_4jets = cms.bool(True),
                             require_6jets = cms.bool(False),
                             require_1stjetpt = cms.double(0.),
                             require_2ndjetpt = cms.double(0.),
                             require_3rdjetpt = cms.double(0.),
                             require_4thjetpt = cms.double(0.),
                             require_6thjetpt = cms.double(0.),
                             require_maxdeta1p6pt = cms.double(0.),
                             require_maxdeta1p6maxeta = cms.double(0.),
                             min_bjet_pt = cms.double(0.),
                             max_bjet_eta = cms.double(0.),
                             require_2btags = cms.bool(False),
                             require_3btags = cms.bool(False),
                             require_ht = cms.double(-1),
                             require_ht30 = cms.double(-1),
                             require_trig_match_all = cms.bool(False),
                             require_trig_match_nm1_idx = cms.int32(-1),
                             weight_src = cms.InputTag('jmtWeightMiniAOD'),
                             muons_src = cms.InputTag('slimmedMuons'),
                             muon_cut = cms.string(jtupleParams.muonCut.value() + ' && pt > %i' % mu_thresh_offline),
                             electrons_src = cms.InputTag('slimmedElectrons'),
                             electron_cut = cms.string(jtupleParams.electronCut.value() + ' && pt > %i' % el_thresh_offline),
                             genjets_src = cms.InputTag(''), #'ak4GenJets' if is_mc else ''),
                             )

process.denht1000 = process.den.clone(require_ht = 1000)

process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc = process.den.clone(require_4jets = False, require_2jets = True, require_2ndjetpt = 100, require_maxdeta1p6pt = 100, require_maxdeta1p6maxeta = 2.3, min_bjet_pt = 100, max_bjet_eta = 2.3, require_2btags = True)
process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc = process.den.clone(require_ht30 = 300, require_4jets = True, require_1stjetpt = 75, require_2ndjetpt = 60, require_3rdjetpt = 45, require_4thjetpt = 40, min_bjet_pt = 30, require_3btags = True)

# FIXME may be able to do something like nm1_pt and set the nominal pt for the other legs. Just have to be careful in the nbtag counting though!!
dibjet_minbjetpt = 100
tribjet_minbjetpt = 30
if "tighterbjetpt" in version :
    dibjet_minbjetpt = 140
    tribjet_minbjetpt = 70

process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight = process.den.clone(require_4jets = False, require_2jets = True, require_2ndjetpt = 140, require_maxdeta1p6pt = 140, require_maxdeta1p6maxeta = 2.3, min_bjet_pt = dibjet_minbjetpt, max_bjet_eta = 2.3, require_2btags = True)
process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight = process.den.clone(require_ht30 = 450, require_4jets = True, require_1stjetpt = 115, require_2ndjetpt = 100, require_3rdjetpt = 85, require_4thjetpt = 80, min_bjet_pt = tribjet_minbjetpt, require_3btags = True)

#process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_ttbar_tight = process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight.clone(do_ttbar_selection = True)
#process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_ttbar_tight = process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight.clone(do_ttbar_selection = True)

process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg0 = process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight.clone(require_trig_match_nm1_idx = 0)
process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg0 = process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight.clone(require_trig_match_nm1_idx = 0)

process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg1 = process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight.clone(require_trig_match_nm1_idx = 1)
process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg1 = process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight.clone(require_trig_match_nm1_idx = 1)

process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg2 = process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight.clone(require_trig_match_nm1_idx = 2)

process.p = cms.Path(process.weightSeq * process.mutrig * process.updatedJetsSeqMiniAOD * process.selectedPatJets * process.mfvTriggerFloats * process.den * process.denht1000 * process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc * process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc * process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight * process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight * process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg0 * process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg0 * process.denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg1 * process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg1 * process.denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg2)

for x in '', 'ht1000', 'DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc', 'PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc', 'DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight','PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight', 'DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg0', 'PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg0', 'DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg1', 'PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg1', 'PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg2' :

    hlt_bit = 0
    if 'DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV' in x:
        hlt_bit = 8
    elif 'PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV' in x:
        hlt_bit = 9

    num = getattr(process, 'den%s' % x).clone(require_hlt = hlt_bit, require_trig_match_all = True if 'Btag' in x else False)
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
        samples = Samples.auxiliary_data_samples_2017 + Samples.leptonic_samples_2017 + [Samples.ttbar_2017]
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
