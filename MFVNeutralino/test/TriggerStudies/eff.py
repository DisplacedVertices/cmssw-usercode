#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.MFVNeutralino.Year import year

# 1st two magic
is_mc = True
to_do = (800, 900)
H_for_test = False
if year == 2015:
    to_do = (800,)
    if H_for_test:
        print 'H_for_test does nothing in 2015'
elif year == 2016 and H_for_test:
    to_do = (900,)
use_ak8450 = True and year == 2016

htskim = False
ht_skim_cut = min(to_do) if htskim else -1

version = 'v6'
json = '../ana_2015p6.json'
batch_name = 'TrigEff%s' % version

if year == 2015:
    mu_thresh_hlt = 20
    mu_thresh_offline = 23
elif year == 2016:
    mu_thresh_hlt = 24
    mu_thresh_offline = 27

process.TFileService.fileName = 'eff.root'
global_tag(process, which_global_tag(is_mc, year))
#process.options.wantSummary = True
process.maxEvents.input = 1000
process.source.fileNames = {
    (2015,True):  ['/store/mc/RunIIFall15MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/50000/2018871D-CABC-E511-95C1-A4BADB0F4C29.root'],
    (2015,False): ['/store/data/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/10000/7C7A3D21-C0A8-E511-94E7-0025905A60DE.root'],
    (2016,True):  ['root://dcache-cms-xrootd.desy.de//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/163E57C9-7ABE-E611-A73A-0025905B857E.root'],
    (2016,False): ['/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/283/283/00000/780D7FAA-FF95-E611-AC56-02163E011B49.root' if H_for_test else '/store/data/Run2016G/SingleMuon/MINIAOD/23Sep2016-v1/90000/94F15529-0694-E611-9B67-848F69FD4FC1.root'],
    }[(year, is_mc)]
#process.source.fileNames = ['/store/data/Run2016B/SingleMuon/MINIAOD/23Sep2016-v3/120000/58678DBC-1599-E611-AE77-FA163E4986BD.root']

if is_mc:
    process.load('JMTucker.Tools.MCStatProducer_cff')
    process.mcStat.histos = True
else:
    from FWCore.PythonUtilities.LumiList import LumiList
    process.source.lumisToProcess = LumiList(json).getVLuminosityBlockRange()

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu%i_v*' % mu_thresh_hlt]

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.mfvTriggerFloats.ht_cut = ht_skim_cut

process.den = cms.EDAnalyzer('MFVTriggerEfficiency',
                             require_hlt = cms.int32(-1),
                             require_l1 = cms.int32(-1),
                             require_muon = cms.bool(True),
                             require_4jets = cms.bool(True),
                             require_ht = cms.double(-1),
                             muons_src = cms.InputTag('slimmedMuons'),
                             muon_cut = cms.string(jtupleParams.semilepMuonCut.value() + ' && pt > %i' % mu_thresh_offline),
                             jets_src = cms.InputTag('slimmedJets'),
                             jet_cut = jtupleParams.jetCut,
                             genjets_src = cms.InputTag(''), #'ak4GenJets' if is_mc else ''),
                             )

process.denht1000 = process.den.clone(require_ht = 1000)
process.p = cms.Path(process.mutrig * cms.ignore(process.mfvTriggerFloats) * process.den * process.denht1000)

process.dennomu = process.den.clone(require_muon = False)
process.dennomuht1000 = process.den.clone(require_muon = False, require_ht = 1000)
process.pforsig = cms.Path(cms.ignore(process.mfvTriggerFloats) * process.dennomu * process.dennomuht1000)

if 800 in to_do:
    process.num800 = process.den.clone(require_hlt = 1)
    process.num800450 = process.den.clone(require_hlt = -2)
    process.p *= process.num800 * process.num800450
    if use_ak8450:
        process.num800450ak = process.den.clone(require_hlt = -3)
        process.p *= process.num800450ak

    process.num800nomu = process.dennomu.clone(require_hlt = 1)
    process.num800nomuht1000 = process.dennomuht1000.clone(require_hlt = 1)
    process.pforsig *= process.num800nomu * process.num800nomuht1000

if 900 in to_do:
    process.num900 = process.den.clone(require_hlt = 2)
    process.num900450 = process.den.clone(require_hlt = -4)
    process.p *= process.num900 * process.num900450
    if use_ak8450:
        process.num900450ak = process.den.clone(require_hlt = -5)
        process.p *= process.num900450ak

    process.num900nomu = process.dennomu.clone(require_hlt = 2)
    process.num900nomuht1000 = process.dennomuht1000.clone(require_hlt = 2)
    process.pforsig *= process.num900nomu * process.num900nomuht1000

if htskim:
    process.setName_('EffHtSkim')
    process.phtskim = cms.Path(process.mutrig * process.mfvTriggerFloats)
    process.load('Configuration.EventContent.EventContent_cff')
    output_file(process, 'htskim.root', process.MINIAODSIMEventContent.outputCommands)
    process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('phtskim'))

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    if year == 2015:
        samples = Samples.auxiliary_data_samples_2015 + Samples.leptonic_background_samples_2015 + Samples.ttbar_samples_2015
    elif year == 2016:
        samples = Samples.auxiliary_data_samples + Samples.leptonic_background_samples + Samples.ttbar_samples
        samples += [getattr(Samples, 'official_mfv_neu_tau01000um_M%04i' % m) for m in (300, 400, 800, 1200, 1600)] + [Samples.official_mfv_neu_tau10000um_M0800]

    for sample in samples:
        if not sample.is_mc:
            sample.json = json

    def pset_modifier(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'is_mcX=XTrue'.replace('X', ' ')
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))

        if '2016B3' in sample.name:
            magic = 'use_ak8450 =XTrue'.replace('X', ' ')
            err = "trying to submit on B3 and want to kill ak8450 but can't find magic"
            to_replace.append((magic, 'use_ak8450 = False', err))

        if year == 2015 or (year == 2016 and not sample.is_mc and sample.name.split('2016')[1].startswith('H')):
            magic = 'to_doX=X(800,X900)'.replace('X', ' ')
            repwith = 'to_do = (%i,)' % (800 if year == 2015 else 900)
            err = 'trying to submit on data, and need to change to_do but no magic string'
            to_replace.append((magic, repwith, err))

        return to_add, to_replace

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter(batch_name,
                       pset_modifier = pset_modifier,
                       splitting = 'FileBased',
                       units_per_job = 10,
                       total_units = -1,
                       dataset = 'miniaod',
                       publish_name = 'trigeff_htskim_' + version,
                       )
    cs.submit_all(samples)
