import sys
from DVCode.Tools.BasicAnalyzer_cfg import cms, process
from DVCode.Tools import SampleFiles

raise NotImplementedError('V15 samples have trigger selection already')

use_weights = True

process.options.wantSummary = True
SampleFiles.setup(process, 'MFVNtupleV15', 'qcdht0250', 10000)
process.TFileService.fileName = 'events_cutplay.root'

from DVCode.MFVNeutralino.AnalysisCuts_cfi import mfvAnalysisCuts as cuts
cuts.apply_vertex_cuts = False

process.trignjets = cuts.clone()
process.trignjetsht500 = cuts.clone(min_ht = 500)
process.trignjetsht750 = cuts.clone(min_ht = 750)
process.trigmu = cuts.clone(trigger_bit = 3, min_4th_jet_pt = 20)
process.trigmuht500 = cuts.clone(trigger_bit = 3, min_4th_jet_pt = 20, min_ht = 500)
process.trigtopmu = cuts.clone(trigger_bit = 4, min_4th_jet_pt = 20)
process.trigtopmunmu = cuts.clone(trigger_bit = 4, min_4th_jet_pt = 20, min_nsemilepmuons = 1)
process.trigtopmunmuht500 = cuts.clone(trigger_bit = 4, min_4th_jet_pt = 20, min_nsemilepmuons = 1, min_ht = 500)
process.trignjetsslep = cuts.clone(min_nsemileptons = 1)
process.trigonly = cuts.clone(min_njets = 0, min_4th_jet_pt = 0)

for name in process.filters.keys():
    setattr(process, 'p' + name, cms.Path(getattr(process,name)))

if use_weights:
    process.load('DVCode.MFVNeutralino.WeightProducer_cfi')

import DVCode.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process, weight_src='mfvWeight' if use_weights else '')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import DVCode.Tools.Samples as Samples
    samples = Samples.qcd_samples + Samples.ttbar_samples + Samples.mfv_signal_samples + Samples.leptonic_background_samples

    from DVCode.Tools.CRABSubmitter import CRABSubmitter
    from DVCode.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('EventsCutplay',
                       total_number_of_events = 1000000,
                       events_per_job = 500000,
                       manual_datasets = SampleFiles['MFVNtupleV15'],
                       )
    cs.submit_all(samples)
