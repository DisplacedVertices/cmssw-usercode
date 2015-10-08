#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = False

global_tag(process, '74X_dataRun2_Prompt_v2')
process.maxEvents.input = 100
process.source.fileNames = ['/store/data/Run2015D/SingleMuon/MINIAOD/PromptReco-v3/000/256/630/00000/BCD78EF7-2B5F-E511-A3A3-02163E0170B5.root']
process.TFileService.fileName = 'eff.root'
from FWCore.PythonUtilities.LumiList import LumiList
process.source.lumisToProcess = LumiList('../Cert_246908-257599_13TeV_PromptReco_Collisions15_25ns_JSON.txt').getVLuminosityBlockRange()

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.mutrig = hltHighLevel.clone()
process.mutrig.HLTPaths = ['HLT_IsoMu18_v*']
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
    from JMTucker.Tools.Sample import anon_samples
    samples = anon_samples('''
/SingleMuon/Run2015D-PromptReco-v3/MINIAOD
''')

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('TrigEff_v0',
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 100000,
                       total_units = -1,
                       crab_cfg_Data_lumiMask = '../Cert_246908-257599_13TeV_PromptReco_Collisions15_25ns_JSON.txt',
                       )
    cs.submit_all(samples)
