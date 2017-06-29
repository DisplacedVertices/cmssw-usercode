from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.MFVNeutralino.Year import year

is_mc = False
H = False

process = pat_tuple_process(None, is_mc, year, H)
jets_only(process)

process.source.fileNames = ['/store/data/Run2016E/ZeroBias/AOD/23Sep2016-v1/100000/18151C77-4486-E611-84FD-0CC47A7C357A.root']

process.firstGoodPrimaryVertex = cms.EDFilter('JMTFirstGoodPrimaryVertex', cut = cms.bool(True))

process.load('JMTucker.MFVNeutralino.SkimmedTracks_cfi')
process.mfvSkimmedTracks.min_pt = 0.9
process.mfvSkimmedTracks.min_nsigmadxybs = 3
process.mfvSkimmedTracks.cut = True

from JMTucker.MFVNeutralino.Vertexer_cfi import kvr_params
process.mfvV0Vertices = cms.EDFilter('MFVV0Vertexer',
                                     kvr_params = kvr_params,
                                     tracks_src = cms.InputTag('mfvSkimmedTracks'),
                                     max_chi2ndf = cms.double(10),
                                     cut = cms.bool(True),
                                     #debug = cms.untracked.bool(True)
                                     )

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')

process.p = cms.Path(process.firstGoodPrimaryVertex * process.mfvSkimmedTracks * process.mfvTriggerFloats * process.mfvV0Vertices)

output_commands = [
    'drop *',
    'keep *_mfvSkimmedTracks_*_*',
    'keep *_mfvV0Vertices_*_*',
    'keep *_mfvTriggerFloats_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_slimmedAddPileupInfo_*_*',
    'keep *_firstGoodPrimaryVertex_*_*',
    'keep *_TriggerResults_*_HLT', # for ZeroBias since I don't wanna mess with MFVTriggerFloats for it
    ]
output_file(process, 'v0ntuple.root', output_commands)

import JMTucker.MFVNeutralino.EventFilter as ef
ef.setup_event_filter(process, path_name='p')
process.triggerFilter.HLTPaths.append('HLT_ZeroBias_v*') # what are the ZeroBias_part* paths?

process.maxEvents.input = 10000
set_lumis_to_process_from_json(process, 'ana_2016.json')
#report_every(process, 1)
want_summary(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    samples = Samples.data_samples + [s for s in Samples.auxiliary_data_samples if s.name.startswith('ZeroBias')]
    for s in samples:
        s.files_per = 50

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('V0NtupleV1')
    ms.common.ex = year
    ms.common.pset_modifier = H_modifier #chain_modifiers(is_mc_modifier, H_modifier)
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
