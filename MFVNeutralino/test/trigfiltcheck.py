import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, file_event_from_argv

file_event_from_argv(process)
process.TFileService.fileName = 'simple_trigger_efficiency.root'

from JMTucker.MFVNeutralino.TriggerFilter import setup_trigger_filter
setup_trigger_filter(process, 'pmfvfilt')

process.load('JMTucker.Tools.SimpleTriggerEfficiency_cfi')
process.SimpleTriggerEfficiency.trigger_results_src = cms.InputTag('TriggerResults', '', process.name_())
process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')
process.RandomNumberGeneratorService.SimpleTriggerEfficiency = cms.PSet(initialSeed = cms.untracked.uint32(1219))

process.ep = cms.EndPath(process.SimpleTriggerEfficiency)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    from JMTucker.Tools.Sample import anon_samples
    from JMTucker.Tools.Samples import *

    samples = ttbar_mgnlo_25ns_samples + qcd_ht_mg_25ns_samples + ttbar_mgnlo_50ns_samples

    cs = CRABSubmitter('TriggerFilterCheck',
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 100000,
                       total_units = -1,
                       )
    cs.submit_all(samples)
