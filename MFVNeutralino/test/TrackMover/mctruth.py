from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.event_filter = 'jets only novtx'

version = settings.version + 'v3'

process = ntuple_process(settings)
remove_output_module(process)
tfileservice(process, 'mctruth.root')
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'mfv_neu_tau010000um_M0800_2017', dataset, 1)
cmssw_from_argv(process)

from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset

process.mfvMovedTreeMCTruth = cms.EDAnalyzer('MFVMovedTracksTreer',
                                             jmtNtupleFiller_pset(settings.is_miniaod),
                                             sel_tracks_src = cms.InputTag(''),
                                             mover_src = cms.string(''),
                                             vertices_src = cms.InputTag('mfvVerticesAux'),
                                             max_dist2move = cms.double(-1),
                                             apply_presel = cms.bool(False),
                                             njets_req = cms.uint32(0),
                                             nbjets_req = cms.uint32(0),
                                             for_mctruth = cms.bool(True),
                                             )

process.p = cms.Path(process.mfvMovedTreeMCTruth)
ReferencedTagsTaskAdder(process)('p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    assert year == 2017
    if year == 2017:
        samples = Samples.all_signal_samples_2017

    #samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'ntuple')

    cs = CondorSubmitter('TrackMoverMCTruth' + version,
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)
