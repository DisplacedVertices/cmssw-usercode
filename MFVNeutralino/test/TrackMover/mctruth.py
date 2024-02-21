#!/usr/bin/env python 

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
#settings.event_filter = 'electrons only novtx'
settings.event_filter = 'muons only novtx' #FIXME miss leading because there is no process.mfvEventFilterSequence applied nor signals_no_event_filter_modifier  
version = settings.version + 'v5'

process = ntuple_process(settings)
tfileservice(process, 'mctruth.root')
dataset = 'miniaod' if settings.is_miniaod else 'main'
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/0BD790C6-883F-0147-A66E-8EC9DC53750F.root')
#max_events(process, 1000)
cmssw_from_argv(process)


from JMTucker.MFVNeutralino.Vertexer_cff import modifiedVertexSequence
from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset
from JMTucker.Tools.TrackRefGetter_cff import jmtTrackRefGetter
jmtTrackRefGetter.input_is_miniaod = settings.is_miniaod

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
process.mfvGenParticles.histos = True
if dataset == 'miniaod':
    process.mfvGenParticles.last_flag_check = False
    process.mfvGenParticles.gen_particles_src = 'prunedGenParticles'

process.p = cms.Path(process.mfvEventFilterSequence *process.mfvGenParticles*process.BadPFMuonFilterUpdateDz * process.fullPatMetSequence * process.mfvTriggerFloats)


tree = cms.EDAnalyzer('MFVMovedTracksTreer',
                                             jmtNtupleFiller_pset(settings.is_miniaod, True, False),
                                             sel_tracks_src = cms.InputTag('mfvVertexTracks','all'),
                                             mover_src = cms.string(''),
                                             vertices_src = cms.InputTag('mfvVerticesAux'),
                                             max_dist2move = cms.double(-1),
                                             apply_presel = cms.bool(False), #not a usual preselection cuts -- TM moved-jet cuts 
                                             njets_req = cms.uint32(0),
                                             nbjets_req = cms.uint32(0),
                                             for_mctruth = cms.bool(True),
                                             )

setattr(process, 'mfvMovedTreeMCTruth', tree)
process.p *= tree 
ReferencedTagsTaskAdder(process)('p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=False, leptonic=False, met=False, diboson=False, Lepton_data=False)
    #samples = pick_samples(dataset, all_signal='only')
    
    #samples = [getattr(Samples, 'WplusHToSSTodddd_tau1mm_M55_2017')] 
    set_splitting(samples, dataset, 'ntuple')
    ms = MetaSubmitter('TrackMoverMCTruth' + version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
