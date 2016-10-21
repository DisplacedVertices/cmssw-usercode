#!/usr/bin/env python

from JMTucker.Tools.BasicAnalyzer_cfg import *
del process.TFileService

process.veto = cms.EDFilter('EventIdVeto',
                         use_run = cms.bool(False),
                         list_fn = cms.string('veto.gz'),
                         debug = cms.untracked.bool(False),
                         )

process.p = cms.Path(~process.veto)

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('pick.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                               )

process.outp = cms.EndPath(process.out)

file_event_from_argv(process)

if 'debug' in sys.argv:
    process.options.wantSummary = True
    process.veto.debug = True

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.registry.from_argv(
        Samples.data_samples + \
        Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
        Samples.auxiliary_background_samples[:1] + \
        Samples.qcdpt_samples + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        Samples.xx4j_samples
        )

    samples = Samples.ttbar_samples

    def pset_modifier(sample):
        assert sample.name == 'ttbar'  # fix this 
        return ['process.veto.list_fn = "vetolist.%s.gz"' % sample.name], []

    def cfg_modifier(cfg, sample):
        assert sample.name == 'ttbar'  # fix this 
        cfg.JobType.inputFiles = ['vetolist.%s.gz' % sample.name]

    cs = CRABSubmitter('Pick1Vtx',
                       pset_modifier = pset_modifier,
                       cfg_modifier = cfg_modifier,
                       splitting = 'FileBased',
                       units_per_job = 30,
                       total_units = -1,
                       publish_name = 'pick1vtx',
                       )

    cs.submit_all(samples)

'''
ttbar 38475776 events in 2762 files
'''
