#!/usr/bin/env python

import sys
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.TFileService.fileName = 'mctruth.root'

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

process.mfvMovedTree = cms.EDAnalyzer('MFVMovedTracksTreer',
                                      event_src = cms.InputTag('mfvEvent'),
                                      weight_src = cms.InputTag('mfvWeight'),
                                      mover_src = cms.string(''),
                                      vertices_src = cms.InputTag('mfvVerticesAux'),
                                      max_dist2move = cms.double(-1),
                                      apply_presel = cms.bool(False),
                                      njets_req = cms.uint32(0),
                                      nbjets_req = cms.uint32(0),
                                      for_mctruth = cms.bool(True),
                                      )

process.p = cms.Path(process.mfvWeight * process.mfvMovedTree)

file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    import JMTucker.Tools.Samples as Samples
    if year == 2015:
        samples = Samples.mfv_signal_samples_2015
    elif year == 2016:
        samples = Samples.mfv_signal_samples + Samples.mfv_ddbar_samples

    dataset = 'ntuplev14'
    for sample in samples:
        sample.datasets[dataset].files_per = 2

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('TrackMoverMCTruthV14',
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)
