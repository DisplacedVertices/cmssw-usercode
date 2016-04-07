#!/usr/bin/env python

import sys
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.TFileService.fileName = 'mctruth.root'

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.p = cms.Path(process.mfvWeight)

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

process.p *= process.mfvMovedTree
file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    cs = CRABSubmitter('TrackMoverMCTruthV6p1_76X',
                       dataset = 'ntuplev6p1_76x_nstlays3',
                       job_control_from_sample = True,
                       max_threads = 3,
                       )

    samples = Samples.registry.from_argv(Samples.mfv_signal_samples)
    cs.submit_all(samples)
