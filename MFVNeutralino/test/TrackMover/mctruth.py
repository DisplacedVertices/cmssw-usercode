from JMTucker.Tools.BasicAnalyzer_cfg import *

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset
sample_files(process, 'mfv_neu_tau010000um_M0800_2017', dataset, 1)
tfileservice(process, 'mctruth.root')
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

process.mfvMovedTree = cms.EDAnalyzer('MFVMovedTracksTreer',
                                      event_src = cms.InputTag('mfvEvent'),
                                      weight_src = cms.InputTag('mfvWeight'),
                                      sel_tracks_src = cms.InputTag(''),
                                      mover_src = cms.string(''),
                                      vertices_src = cms.InputTag('mfvVerticesAux'),
                                      max_dist2move = cms.double(-1),
                                      apply_presel = cms.bool(False),
                                      njets_req = cms.uint32(0),
                                      nbjets_req = cms.uint32(0),
                                      for_mctruth = cms.bool(True),
                                      )

process.p = cms.Path(process.mfvWeight * process.mfvMovedTree)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    assert year == 2017
    if year == 2017:
        samples = Samples.all_signal_samples_2017

    #samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'minitree')

    cs = CondorSubmitter('TrackMoverMCTruth' + version,
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)
