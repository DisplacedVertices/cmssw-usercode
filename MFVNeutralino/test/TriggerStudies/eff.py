#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = False

global_tag(process, 'MCRUN2_74_V9' if is_mc else '74X_dataRun2_Prompt_v2')
process.maxEvents.input = 100
process.source.fileNames = ['/store/mc/RunIISpring15DR74/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/80000/CA0ABB76-43FC-E411-A207-1CC1DE1CEDB2.root' if is_mc else '/store/data/Run2015D/SingleMuon/MINIAOD/PromptReco-v3/000/256/630/00000/BCD78EF7-2B5F-E511-A3A3-02163E0170B5.root']
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

process.p = cms.Path(process.mutrig * process.den * process.num)

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

    def cfg_modifier(cfg, sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'is_mc = True'
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))

        return to_add, to_replace

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('TrigEff_v2',
                       cfg_modifier = cfg_modifier,
                       job_control_from_sample = True,
                       dataset = 'miniaod',
                       )
    cs.submit_all(samples)
