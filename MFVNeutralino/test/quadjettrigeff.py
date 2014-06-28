#!/usr/bin/env python

import sys
from JMTucker.Tools.PATTuple_cfg import *

runOnMC = True # magic line, don't touch
process, common_seq = pat_tuple_process(runOnMC)

process.source.fileNames = ['/store/user/tucker/Run2012D_SingleMu_AOD_22Jan2013-v1_10000_0015EC7D-EAA7-E211-A9B9-E0CB4E5536A7.root']
del process.out
del process.outp

process.TFileService = cms.Service('TFileService', fileName = cms.string('quadjettrigeff.root'))

process.patJetCorrFactors.primaryVertices = 'goodOfflinePrimaryVertices'
process.patJets.addJetCharge = False
process.selectedPatJets.cut = ''
common_seq *= process.patJetCorrFactors * process.patJets * process.selectedPatJets

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.QuadJet50 = hltHighLevel.clone()
process.QuadJet50.HLTPaths = ['HLT_QuadJet50_v*']
process.QuadJet50.andOr = True # = OR
process.IsoMu25Eta2p1 = process.QuadJet50.clone(HLTPaths = ['HLT_IsoMu24_eta2p1_v*'])
for name, path in process.paths.items():
    if not name.startswith('eventCleaning'):
        path.insert(0, process.IsoMu25Eta2p1)

for no_prescale in (True, False):
    for kind in ('pf', 'cl', 0, 1, 2, 3):
        if type(kind) == int:
            sel = kind
            kind = 'cl'
        else:
            sel = -1

        src = 'selectedPatJets'
        if kind == 'pf':
            src += 'PF'

        num = cms.EDAnalyzer('QuadJetTrigEff', jets_src = cms.InputTag(src), sel = cms.int32(sel), no_prescale = cms.bool(no_prescale))
        den = num.clone()

        name = '%s%s' % (kind, '' if sel == -1 else sel)
        setattr(process, name + 'num', num)
        setattr(process, name + 'den', den)
        setattr(process, 'p' + name + 'num', cms.Path(process.IsoMu25Eta2p1 * process.QuadJet50 * common_seq * num))
        setattr(process, 'p' + name + 'den', cms.Path(process.IsoMu25Eta2p1 *                     common_seq * den))

process.options.wantSummary = True

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

    datasamples = [
        Samples.DataSample('SingleMu2012A', '/SingleMu/Run2012A-22Jan2013-v1/AOD'),
        Samples.DataSample('SingleMu2012B', '/SingleMu/Run2012B-22Jan2013-v1/AOD'),
        Samples.DataSample('SingleMu2012C', '/SingleMu/Run2012C-22Jan2013-v1/AOD'),
        Samples.DataSample('SingleMu2012D', '/SingleMu/Run2012D-22Jan2013-v1/AOD'),
        ]
        
    samples = Samples.from_argv([Samples.qcdmupt15] +
                                Samples.ttbar_samples +
                                Samples.leptonic_background_samples +
                                datasamples)

    cs.submit_all(samples)



