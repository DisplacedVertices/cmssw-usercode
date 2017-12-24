#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
repro = False
input_is_aod = False
to_do = (800, 900)
if year == 2015:
    to_do = (800,)
    if H:
        print 'H does nothing in 2015'
elif year == 2016 and H:
    to_do = (900,)
use_ak8450 = True and year == 2016

version = 'v8'
batch_name = 'TrigEff%s' % version

if year == 2015:
    mu_thresh_hlt = 20
    mu_thresh_offline = 23
elif year == 2016:
    mu_thresh_hlt = 24
    mu_thresh_offline = 27

if input_is_aod:
    process = pat_tuple_process(None, is_mc, year, H, repro)
    remove_met_filters(process)
    remove_output_module(process)
    tfileservice(process, 'eff.root')

process.TFileService.fileName = 'eff.root'
global_tag(process, which_global_tag(is_mc, year, H, repro))
#process.options.wantSummary = True
process.maxEvents.input = 1000
process.source.fileNames = {
    (2015,True):  ['/store/mc/RunIIFall15MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/50000/2018871D-CABC-E511-95C1-A4BADB0F4C29.root'],
    (2015,False): ['/store/data/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/10000/7C7A3D21-C0A8-E511-94E7-0025905A60DE.root'],
    (2016,True):  ['root://dcache-cms-xrootd.desy.de//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/163E57C9-7ABE-E611-A73A-0025905B857E.root'],
    (2016,False): ['/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/283/283/00000/780D7FAA-FF95-E611-AC56-02163E011B49.root' if H else '/store/data/Run2016G/SingleMuon/MINIAOD/23Sep2016-v1/90000/94F15529-0694-E611-9B67-848F69FD4FC1.root'],
    }[(year, is_mc)]
#process.source.fileNames = ['/store/data/Run2016B/SingleMuon/MINIAOD/23Sep2016-v3/120000/58678DBC-1599-E611-AE77-FA163E4986BD.root']
if input_is_aod:
    process.source.fileNames = ['/store/user/wsun/croncopyeos/mfv_ddbar_tau10000um_M0800/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6/170322_122934/0000/reco_1.root']

process.load('JMTucker.Tools.MCStatProducer_cff')

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu%i_v*' % mu_thresh_hlt]

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.mfvTriggerFloats.jets_src = 'slimmedJets'

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
                             muon_cut = cms.string(jtupleParams.semilepMuonCut.value() + ' && pt > %i' % mu_thresh_offline),
                             genjets_src = cms.InputTag(''), #'ak4GenJets' if is_mc else ''),
                             )

process.denht1000 = process.den.clone(require_ht = 1000)
process.denjet6pt75 = process.den.clone(require_6thjetpt = 75)
process.denht1000jet6pt75 = process.den.clone(require_ht = 1000, require_6thjetpt = 75)
process.p = cms.Path(process.mutrig * process.mfvTriggerFloats * process.den * process.denht1000 * process.denjet6pt75 * process.denht1000jet6pt75)

process.dennomu = process.den.clone(require_muon = False)
process.dennomuht1000 = process.den.clone(require_muon = False, require_ht = 1000)
process.dennomujet6pt75 = process.den.clone(require_muon = False, require_6thjetpt = 75)
process.dennomuht1000jet6pt75 = process.den.clone(require_muon = False, require_ht = 1000, require_6thjetpt = 75)
process.pforsig = cms.Path(process.mfvTriggerFloats * process.dennomu * process.dennomuht1000 * process.dennomujet6pt75 * process.dennomuht1000jet6pt75)

def a(name, obj, p=process.p):
    setattr(process, name, obj)
    p *= obj

for require_l1, l1_threshold in (-1, 0), (-2, 240), (-3, 255), (-4, 280), (-5, 300), (-6, 320):
    l1_ex = 'bugL1%i' % l1_threshold if require_l1 != -1 else ''
    for ht_threshold, hlt1, hlt2, hlt3 in (800, 1, -2, -3), (900, 2, -4, -5):
        if ht_threshold in to_do:
            z = (ht_threshold, l1_ex)
            a('num%i%s'    % z, process.den.clone(require_hlt = hlt1, require_l1 = require_l1))
            a('num%i450%s' % z, process.den.clone(require_hlt = hlt2, require_l1 = require_l1))
            if use_ak8450:
                a('num%i450ak%s' % z, process.den.clone(require_hlt = hlt3, require_l1 = require_l1))

            a('num%inomu%s' % z, process.dennomu.clone(require_hlt = hlt1, require_l1 = require_l1), process.pforsig)
            a('num%inomuht1000%s' % z, process.dennomuht1000.clone(require_hlt = hlt1, require_l1 = require_l1), process.pforsig)
            a('num%inomujet6pt75%s' % z, process.dennomujet6pt75.clone(require_hlt = hlt1, require_l1 = require_l1), process.pforsig)
            a('num%inomuht1000jet6pt75%s' % z, process.dennomuht1000jet6pt75.clone(require_hlt = hlt1, require_l1 = require_l1), process.pforsig)

            a('num%ijet6pt75%s'    % z, process.denjet6pt75.clone(require_hlt = hlt1, require_l1 = require_l1))
            a('num%i450jet6pt75%s' % z, process.denjet6pt75.clone(require_hlt = hlt2, require_l1 = require_l1))
            if use_ak8450:
                a('num%i450akjet6pt75%s' % z, process.denjet6pt75.clone(require_hlt = hlt3, require_l1 = require_l1))

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    if year == 2015:
        samples = Samples.auxiliary_data_samples_2015 + Samples.leptonic_background_samples_2015 + Samples.ttbar_samples_2015
    elif year == 2016:
        muon_data_samples = [s for s in Samples.auxiliary_data_samples if s.name.startswith('SingleMuon')]
        samples = muon_data_samples + Samples.leptonic_background_samples + Samples.ttbar_samples
        masses = (300, 400, 800, 1200, 1600)
        samples += [getattr(Samples, 'mfv_neu_tau01000um_M%04i'   % m) for m in masses] + [Samples.mfv_neu_tau10000um_M0800]

    if input_is_aod:
        dataset = 'main'
        samples = [Samples.mfv_neu_tau01000um_M0600, Samples.mfv_ddbar_tau10000um_M0800] + [getattr(Samples, 'mfv_ddbar_tau01000um_M%04i' % m) for m in masses]
    else:
        dataset = 'miniaod'

    for sample in samples:
        if not sample.is_mc:
            sample.json = '../ana_2015p6.json'
        sample.set_curr_dataset(dataset)
        sample.split_by = 'files'
        sample.files_per = 30

    def pset_modifier(sample):
        to_add = []
        to_replace = []

        if sample.name.startswith('Repro'):
            raise NotImplementedError('reprocessing?')

        if not sample.is_mc:
            magic = 'is_mcX=XTrue'.replace('X', ' ')
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))

        if '2016B3' in sample.name:
            magic = 'use_ak8450 =XTrue'.replace('X', ' ')
            err = "trying to submit on B3 and want to kill ak8450 but can't find magic"
            to_replace.append((magic, 'use_ak8450 = False', err))

        sample_is_2016H = year == 2016 and not sample.is_mc and sample.name.split('2016')[1].startswith('H')
        if year == 2015 or sample_is_2016H:
            magic = 'to_doX=X(800,X900)'.replace('X', ' ')
            repwith = 'to_do = (%i,)' % (800 if year == 2015 else 900)
            err = 'trying to submit on data, and need to change to_do but no magic string'
            to_replace.append((magic, repwith, err))

        if sample_is_2016H:
            magic = 'H =XFalse'.replace('X', ' ')
            to_replace.append((magic, 'H = True', 'trying to submit on 2016H and no magic string "%s"' % magic))

        return to_add, to_replace

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter(batch_name)
    ms.common.dataset = dataset
    ms.common.ex = year
    ms.common.pset_modifier = pset_modifier
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
