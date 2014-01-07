import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

process.options.wantSummary = True
SampleFiles.setup(process, 'MFVNtupleV13', 'qcdht0250', 10000)
process.TFileService.fileName = 'events_cutplay.root'

from JMTucker.MFVNeutralino.AnalysisCuts_cfi import mfvAnalysisCuts as cuts
cuts.apply_vertex_cuts = False

process.trignjets = cuts.clone()
process.trignjetsht500 = cuts.clone(min_sumht = 500)
process.trignjetsht750 = cuts.clone(min_sumht = 750)
process.trigmu = cuts.clone(trigger_bit = 3, min_4th_jet_pt = 20)
process.trigmuht500 = cuts.clone(trigger_bit = 3, min_4th_jet_pt = 20, min_sumht = 500)
process.trigtopmu = cuts.clone(trigger_bit = 4, min_4th_jet_pt = 20)
process.trigtopmunmu = cuts.clone(trigger_bit = 4, min_4th_jet_pt = 20, min_nsemilepmuons = 1)
process.trigtopmunmuht500 = cuts.clone(trigger_bit = 4, min_4th_jet_pt = 20, min_nsemilepmuons = 1, min_sumht = 500)
process.trignjetsslep = cuts.clone(min_nsemileptons = 1)

for name in process.filters.keys():
    setattr(process, 'p' + name, cms.Path(getattr(process,name)))

process.effs = cms.EDAnalyzer('SimpleTriggerEfficiency', trigger_results_src = cms.InputTag('TriggerResults', '', process.name_()))
process.p = cms.EndPath(process.effs)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.qcd_samples + Samples.ttbar_samples + Samples.mfv_signal_samples + Samples.leptonic_background_samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('EventsCutplay',
                       total_number_of_events = -1,
                       events_per_job = 1000000,
                       manual_datasets = SampleFiles['MFVNtupleV13'],
                       )
    cs.submit_all(samples)
