#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.CMSSWTools import *

is_mc = True

global_tag(process, 'MCRUN2_74_V9' if is_mc else '74X_dataRun2_Prompt_v2')
process.maxEvents.input = 1000
process.source.fileNames = ['/store/mc/RunIISpring15DR74/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/80000/CA0ABB76-43FC-E411-A207-1CC1DE1CEDB2.root' if is_mc else '/store/data/Run2015D/SingleMuon/MINIAOD/PromptReco-v3/000/256/630/00000/BCD78EF7-2B5F-E511-A3A3-02163E0170B5.root']
#process.source.fileNames = ['/store/mc/RunIISpring15DR74/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/0270C6BA-AE17-E511-9D04-549F358EB755.root']
#process.source.fileNames = ['/store/mc/RunIISpring15DR74/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/00000/00F9B1F1-3B18-E511-B17D-A0369F30FFD2.root']
#process.source.fileNames = ['/store/mc/RunIISpring15DR74/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/70000/AAC7A1D1-F6FB-E411-AFC9-E0CB4E1A114B.root']
#set_events_to_process(process, [(1, 205534, 50556064)])
process.TFileService.fileName = 'eff.root'
if not is_mc:
    from JMTucker.Tools.Sample import DataSample
    from FWCore.PythonUtilities.LumiList import LumiList
    process.source.lumisToProcess = LumiList(DataSample.JSON).getVLuminosityBlockRange()

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu20_v*']
process.mutrig.andOr = True # = OR

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')
process.RandomNumberGeneratorService.SimpleTriggerEfficiency = cms.PSet(initialSeed = cms.untracked.uint32(1219))

process.emu = cms.EDFilter('MFVEmulateHT800',
                             trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                             trigger_objects_src = cms.InputTag('selectedPatTrigger'),
                             throw_not_found = cms.bool(False),
                             prints = cms.untracked.bool(False),
                             )

process.num = cms.EDAnalyzer('MFVTriggerEfficiency',
                             require_trigger = cms.bool(True),
                             require_muon = cms.bool(True),
                             muons_src = cms.InputTag('slimmedMuons'),
                             muon_cut = cms.string(jtupleParams.semilepMuonCut.value() + ' && pt > 24'),
                             jets_src = cms.InputTag('slimmedJets'),
                             jet_cut = jtupleParams.jetCut,
                             genjets_src = cms.InputTag('ak4GenJets' if is_mc else ''),
                             )
process.den = process.num.clone(require_trigger = False)

process.p = cms.Path(process.emu) # * process.mutrig * process.den * process.num)

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)

#process.options.wantSummary = True

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
            magic = 'is_mc = True'
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))

        return to_add, to_replace

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('TestEmu800v2',
                       pset_modifier = pset_modifier,
                       job_control_from_sample = True,
                       dataset = 'miniaod',
                       )
    cs.submit_all(samples)
 
