#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.MFVNeutralino.Year import year

# 1st two magic
is_mc = True
to_do = (800, 900)
htskim = True
ht_skim_cut = min(to_do)
version = 'v2'
batch_name = 'TrigEff%s/%i' % (version, year)
json = '../ana_2015p6.json'

if year == 2015:
    mu_thresh_hlt = 20
    mu_thresh_offline = 23
elif year == 2016:
    mu_thresh_hlt = 24
    mu_thresh_offline = 27

global_tag(process, which_global_tag(is_mc, year))
process.maxEvents.input = 1000
process.source.fileNames = ['/store/user/tucker/temp/wjetstolnu.miniaod.163E57C9-7ABE-E611-A73A-0025905B857E.root' if is_mc else
         #                   '/store/data/Run2016G/SingleMuon/MINIAOD/23Sep2016-v1/90000/94F15529-0694-E611-9B67-848F69FD4FC1.root']
                            '/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/283/283/00000/780D7FAA-FF95-E611-AC56-02163E011B49.root']
#process.options.wantSummary = True
process.TFileService.fileName = 'eff.root'

if is_mc:
    process.load('JMTucker.Tools.MCStatProducer_cff')
else:
    from FWCore.PythonUtilities.LumiList import LumiList
    process.source.lumisToProcess = LumiList(json).getVLuminosityBlockRange()

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu%i_v*' % mu_thresh_hlt]

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.mfvTriggerFloats.ht_cut = ht_skim_cut

process.den = cms.EDProducer('MFVTriggerEfficiency',
                             require_hlt = cms.int32(-1),
                             require_l1 = cms.int32(-1),
                             require_muon = cms.bool(True),
                             require_4jets = cms.bool(True),
                             muons_src = cms.InputTag('slimmedMuons'),
                             muon_cut = cms.string(jtupleParams.semilepMuonCut.value() + ' && pt > %i' % mu_thresh_offline),
                             jets_src = cms.InputTag('slimmedJets'),
                             jet_cut = jtupleParams.jetCut,
                             genjets_src = cms.InputTag(''), #'ak4GenJets' if is_mc else ''),
                             )

process.p = cms.Path(process.mutrig * cms.ignore(process.mfvTriggerFloats) * process.den)

if 800 in to_do:
    process.num800 = process.den.clone(require_hlt = 1)
    process.p *= process.num800
if 900 in to_do:
    process.num900 = process.den.clone(require_hlt = 2)
    process.p *= process.num900

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

    for sample in samples:
        if sample.is_mc:
            sample.events_per = 100000
        else:
            sample.lumis_per = 50
            sample.json = json

    def pset_modifier(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'is_mcX=XTrue'.replace('X', ' ')
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))

        if year == 2015 or (year == 2016 and not sample.is_mc and sample.name.split('2016')[1].startswith('H'))
            magic = 'to_doX=X(800,X900)'.replace('X', ' ')
            repwith = 'to_do = (%i,)' % (800 if year == 2015 else 900)
            err = 'trying to submit on data, and need to change to_do but no magic string'
            to_replace.append((magic, repwith, err))

        return to_add, to_replace

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter(batch_name,
                       pset_modifier = pset_modifier,
                       job_control_from_sample = True,
                       dataset = 'miniaod',
                       publish_name = 'trigeff_htskim_' + version,
                       )
    cs.submit_all(samples)
