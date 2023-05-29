from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.event_filter = 'leptons only novtx'

version = settings.version + 'v2'

process = ntuple_process(settings)
remove_output_module(process)
tfileservice(process, 'mctruth.root')
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'WplusHToSSTodddd_tau1mm_M55_year', dataset, 1)
cmssw_from_argv(process)

from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset

process.mfvMovedTreeMCTruth = cms.EDAnalyzer('MFVMovedTracksTreer',
                                             jmtNtupleFiller_pset(settings.is_miniaod),
                                             sel_tracks_src = cms.InputTag('mfvVertexTracks','seed'),
                                             mover_src = cms.string(''),
                                             vertices_src = cms.InputTag('mfvVerticesAux'),
                                             max_dist2move = cms.double(-1),
                                             apply_presel = cms.bool(False), #FIXME ?
                                             njets_req = cms.uint32(0),
                                             nbjets_req = cms.uint32(0),
                                             for_mctruth = cms.bool(True),
                                             )

process.p = cms.Path(process.mfvMovedTreeMCTruth)
ReferencedTagsTaskAdder(process)('p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    #samples = pick_samples(dataset, all_signal='only')
    samples = [getattr(Samples, 'WplusHToSSTodddd_tau1mm_M55_2017')] 
    set_splitting(samples, dataset, 'ntuple')

    cs = CondorSubmitter('TrackMoverMCTruth' + version,
                         ex = year,
                         dataset = dataset,
                         stageout_files = 'all'
                         )
    cs.submit_all(samples)
