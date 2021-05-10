#!/usr/bin/env python

from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.Tools.Year import year
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

settings = CMSSWSettings()
settings.is_mc = True
settings.cross = '' # 2017to2018' # 2017to2017p8'

version = '2017v11_MET'

mu_thresh_hlt = 27
mu_thresh_offline = 35
ele_thresh_hlt = 27
ele_thresh_offline = 35
weight_l1ecal = ''

tfileservice(process, 'eff.root')
global_tag(process, which_global_tag(settings))
#want_summary(process)
#report_every(process, 1)
max_events(process, -1)
dataset = 'miniaod'
sample_files(process, 'wjetstolnu_2017', dataset, 1)
#input_files(process,[
#                    '/store/mc/RunIIFall17MiniAODv2/TTJets_DiLept_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/028BAF0D-85A0-E811-8B96-D4AE526A0C89.root',
#                    '/store/mc/RunIIFall17MiniAODv2/TTJets_DiLept_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/242B88DC-84A0-E811-8028-B083FED43140.root',
#                    '/store/mc/RunIIFall17MiniAODv2/TTJets_DiLept_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/5AFC83DA-83A0-E811-99CC-0025905A48C0.root',
#            ])

from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runVID=True, #saves CPU time by not needlessly re-running VID, if you want the Fall17V2 IDs, set this to True or remove (default is True)
                       era='2017-Nov17ReReco')  
#a sequence egammaPostRecoSeq has now been created and should be added to your path, eg process.p=cms.Path(process.egammaPostRecoSeq)
process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.UpdatedJets_cff')
process.load('JMTucker.Tools.WeightProducer_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff") 

process.selectedPatJets.src = 'updatedJetsMiniAOD'
process.selectedPatJets.cut = jtupleParams.jetCut
process.mfvTriggerFloats.met_src = cms.InputTag('slimmedMETs', '', 'BasicAnalyzer') # BasicAnalyzer
process.mfvTriggerFloats.isMC = settings.is_mc
process.mfvTriggerFloats.year = settings.year


from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu%i_v*' % mu_thresh_hlt]

process.eletrig = hltHighLevel.clone()
process.eletrig.HLTPaths = ['HLT_Ele%i_WPTight_Gsf_v*' % ele_thresh_hlt]

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

# MET correction
runMetCorAndUncFromMiniAOD(process,
                           isData = not settings.is_mc,
                           )

process.load('RecoMET.METFilters.ecalBadCalibFilter_cfi')

baddetEcallist = cms.vuint32(
    [872439604,872422825,872420274,872423218,872423215,872416066,872435036,872439336,
    872420273,872436907,872420147,872439731,872436657,872420397,872439732,872439339,
    872439603,872422436,872439861,872437051,872437052,872420649,872421950,872437185,
    872422564,872421566,872421695,872421955,872421567,872437184,872421951,872421694,
    872437056,872437057,872437313,872438182,872438951,872439990,872439864,872439609,
    872437181,872437182,872437053,872436794,872436667,872436536,872421541,872421413,
    872421414,872421031,872423083,872421439])

process.ecalBadCalibReducedMINIAODFilter = cms.EDFilter(
    "EcalBadCalibFilter",
    EcalRecHitSource = cms.InputTag("reducedEgamma:reducedEERecHits"),
    ecalMinEt        = cms.double(50.),
    baddetEcal    = baddetEcallist, 
    taggingMode = cms.bool(True),
    debug = cms.bool(False)
    )

process.den = cms.EDAnalyzer('MFVTriggerEfficiency',
                             use_jetpt_weights = cms.int32(0),
                             require_hlt = cms.int32(-1),
                             require_l1 = cms.int32(-1),
                             require_muon = cms.bool(False),
                             require_electron = cms.bool(True),
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
process.p = cms.Path(process.egammaPostRecoSeq * process.ecalBadCalibReducedMINIAODFilter * process.weightSeq * process.mutrig * process.updatedJetsSeqMiniAOD * process.fullPatMetSequence * process.selectedPatJets * process.mfvTriggerFloats * process.den)

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
        #samples = [Samples.met_samples_2017[0]]
        samples = Samples.auxiliary_data_samples_2017 + Samples.leptonic_samples_2017 + Samples.met_samples_2017[0:2] + [Samples.met_samples_2017[-1]]
        samples += Samples.mfv_splitSUSY_samples_2017
        #masses = (400, 800, 1200, 1600)
        #samples += [getattr(Samples, 'mfv_neu_tau001000um_M%04i_2017' % m) for m in masses] + [Samples.mfv_neu_tau010000um_M0800_2017]
    elif year == 2018:
        samples = Samples.auxiliary_data_samples_2018
    
    samples = [s for s in samples if s.has_dataset(dataset) and (s.is_mc or not settings.cross)]
    set_splitting(samples, dataset, 'default', json_path('ana_2017p8.json'), 5)

    ms = MetaSubmitter('TrigEff%s%s' % (version, '_' + settings.cross if settings.cross else ''), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier(cross=settings.cross))
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
