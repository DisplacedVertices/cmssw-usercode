#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True
htskim = True
version = 'v6'

global_tag(process, 'MCRUN2_74_V9' if is_mc else '74X_dataRun2_Prompt_v2')
process.maxEvents.input = 1000
process.source.fileNames = ['/store/mc/RunIISpring15DR74/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/80000/CA0ABB76-43FC-E411-A207-1CC1DE1CEDB2.root' if is_mc else '/store/data/Run2015D/SingleMuon/MINIAOD/PromptReco-v3/000/256/630/00000/BCD78EF7-2B5F-E511-A3A3-02163E0170B5.root']
#process.source.fileNames = ['/store/user/tucker/SingleMuon/trigeff_htskim_v5/151120_145239/0000/htskim_7.root']
#process.options.wantSummary = True
process.TFileService.fileName = 'eff.root'

if not is_mc:
    from JMTucker.Tools.Sample import DataSample
    from FWCore.PythonUtilities.LumiList import LumiList
    process.source.lumisToProcess = LumiList(DataSample.JSON).getVLuminosityBlockRange()

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu20_v*']
process.mutrig.andOr = True # = OR

process.emu = cms.EDFilter('MFVEmulateHT800',
                           trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                           trigger_objects_src = cms.InputTag('selectedPatTrigger'),
                           throw_not_found = cms.bool(False),
                           return_actual = cms.bool(True),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(False),
                           )

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

process.num = cms.EDFilter('MFVTriggerEfficiency',
                             require_trigger = cms.bool(False), # just from EmulateHT800 filter, need to split out
                             require_muon = cms.bool(True),
                             muons_src = cms.InputTag('slimmedMuons'),
                             muon_cut = cms.string(jtupleParams.semilepMuonCut.value() + ' && pt > 24'),
                             jets_src = cms.InputTag('slimmedJets'),
                             jet_cut = jtupleParams.jetCut,
                             jet_ht_cut = cms.double(0),
                             genjets_src = cms.InputTag(''), #'ak4GenJets' if is_mc else ''),
                             )
process.den = process.num.clone(require_trigger = False)

process.p = cms.Path(process.mutrig * cms.ignore(process.emu) * cms.ignore(process.den) * process.emu * cms.ignore(process.num))

if htskim:
    process.setName_('EffHtSkim')
    process.htskim = process.den.clone(jet_ht_cut = 800)
    process.phtskim = cms.Path(process.mutrig * process.htskim)
    process.load('Configuration.EventContent.EventContent_cff')
    process.out = cms.OutputModule('PoolOutputModule',
                                   fileName = cms.untracked.string('htskim.root'),
                                   compressionLevel = cms.untracked.int32(4),
                                   compressionAlgorithm = cms.untracked.string('LZMA'),
                                   eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
                                   outputCommands = process.MINIAODSIMEventContent.outputCommands,
                                   dropMetaData = cms.untracked.string('ALL'),
                                   fastCloning = cms.untracked.bool(False),
                                   overrideInputFileSplitLevels = cms.untracked.bool(True),
                                   SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('phtskim')),
                                   )
    process.outp = cms.EndPath(process.out)

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)
random_service(process, {'SimpleTriggerEfficiency': 1222})


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    from JMTucker.Tools.Sample import anon_samples
    samples = Samples.auxiliary_data_samples + Samples.leptonic_background_samples + Samples.ttbar_samples
    for sample in samples:
        if sample.is_mc:
            sample.events_per = 100000
        else:
            sample.lumis_per = 30 # ?

    def pset_modifier(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'is_mcX=XTrue'.replace('X', ' ')
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))

        return to_add, to_replace

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('TrigEff' + version,
                       pset_modifier = pset_modifier,
                       job_control_from_sample = True,
                       dataset = 'miniaod',
                       publish_name = 'trigeff_htskim_' + version  # if htskim False, then crab will just complain?
                       )
    cs.submit_all(samples)
 
