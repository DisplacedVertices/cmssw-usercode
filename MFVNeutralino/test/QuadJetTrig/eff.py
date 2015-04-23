#!/usr/bin/env python

import sys
from JMTucker.Tools.PATTuple_cfg import *

runOnMC = True # magic line, don't touch
process, common_seq = pat_tuple_process(runOnMC)
for name, path in process.paths.items():
    delattr(process, name)

process.source.fileNames = ['/store/mc/Summer12_DR53X/TTJets_SemiLeptMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A_ext-v1/00000/FEDD73E4-5424-E211-8271-001E67398142.root' if runOnMC else '/store/data/Run2012D/SingleMu/AOD/22Jan2013-v1/10000/0015EC7D-EAA7-E211-A9B9-E0CB4E5536A7.root']

del process.out
del process.outp

process.TFileService = cms.Service('TFileService', fileName = cms.string('eff.root'))

process.patJetCorrFactors.primaryVertices = 'goodOfflinePrimaryVertices'
for attr in 'embedGenJetMatch addGenJetMatch embedGenPartonMatch addGenPartonMatch getJetMCFlavour addJetCharge'.split():
    setattr(process.patJets, attr, False)
process.selectedPatJets.cut = ''
common_seq *= process.patJetCorrFactors * process.patJets * process.selectedPatJets

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.IsoMu24Eta2p1 = hltHighLevel.clone()
process.IsoMu24Eta2p1.HLTPaths = ['HLT_IsoMu24_eta2p1_v*']
process.IsoMu24Eta2p1.andOr = True # = OR

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

for require_4calo in (0, 50, 60):
    for require_muon in (True, False):
        for kind in ('pf', 'cl', 0, 1, 2, 3):
            if type(kind) == int:
                sel = kind
                kind = 'cl'
            else:
                sel = -1

            src = 'selectedPatJets'
            if kind == 'pf':
                src += 'PF'

            num = cms.EDAnalyzer('QuadJetTrigEff',
                                 require_trigger = cms.bool(True),
                                 require_muon = cms.bool(require_muon),
                                 muons_src = cms.InputTag('selectedPatMuonsPF'),
                                 muon_cut = jtupleParams.semilepMuonCut,
                                 require_4calo = cms.int32(require_4calo),
                                 calojets_src = cms.InputTag('selectedPatJets'),
                                 jets_src = cms.InputTag(src),
                                 jet_sel_num = cms.int32(sel),
                                 genjets_src = cms.InputTag('ak5GenJets' if runOnMC else ''),
                                 )
            den = num.clone(require_trigger = False)

            name = 'Mu%i' % int(require_muon)
            name += '4C%i' % require_4calo
            name += '%s%s' % (kind, '' if sel == -1 else sel)
            setattr(process, name + 'num', num)
            setattr(process, name + 'den', den)
            setattr(process, 'p' + name, cms.Path(process.IsoMu24Eta2p1 * common_seq * num * den))

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)

#process.options.wantSummary = True

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    def modify(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'runOnMC = True'
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'runOnMC = False', err))
            to_add.append('process.dummyToMakeDiffHash = cms.PSet(sampleName = cms.string("%s"))' % sample.name)
            to_add.append('process.patJetCorrFactors.levels.append("L2L3Residual")')

        return to_add, to_replace

    cs = CRABSubmitter('QuadJetTrigEff',
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       max_threads = 2,
                       )

    mc_samples = [Samples.qcdmupt15] + Samples.ttbar_samples + Samples.leptonic_background_samples

    data_samples = Samples.auxiliary_data_samples[1:]

    for sample in mc_samples:
        sample.events_per = 25000
    for sample in data_samples:
        sample.lumis_per = 75
        sample.json = '../ana_all.json'

    samples = Samples.from_argv(mc_samples + data_samples)

    cs.submit_all(samples)
