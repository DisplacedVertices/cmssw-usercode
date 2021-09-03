from DVCode.Tools.BasicAnalyzer_cfg import *

prints = 1

max_events(process, 100)
tfileservice(process, 'packedcands.root')
geometry_etc(process)
report_every(process, 1 if prints else 1000000)

input_files(process, 'itch:/store/mc/RunIIFall17MiniAOD/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/50000/7EF2B30C-37EA-E711-B605-0026B92785F6.root', ['itch:/store/mc/RunIIFall17DRPremix/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/AODSIM/94X_mc2017_realistic_v10-v1/50000/10757D90-12E9-E711-A588-1CB72C1B6C32.root', 'itch:/store/mc/RunIIFall17DRPremix/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/AODSIM/94X_mc2017_realistic_v10-v1/50000/B43D6EA3-F2E8-E711-8D8C-1CB72C1B649A.root'])

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
#process.goodOfflinePrimaryVertices.filter = True

process.mfvPackedCands = cms.EDAnalyzer('MFVPackedCandidates',
                                        tracks_src = cms.InputTag('generalTracks'),
                                        max_closest_cd_dist = cms.double(0.111e-3),
                                        prints = cms.int32(prints),
                                        )

process.load('DVCode.Tools.UnpackedCandidateTracks_cfi')
process.jmtUnpackedCandidateTracks.debug = prints
#process.mfvPackedCands.tracks_src = 'jmtUnpackedCandidateTracks'
process.p = cms.Path(process.goodOfflinePrimaryVertices * process.jmtUnpackedCandidateTracks * process.mfvPackedCands)

import DVCode.MFVNeutralino.EventFilter
DVCode.MFVNeutralino.EventFilter.setup_event_filter(process, path_name='p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from DVCode.Tools.Year import year
    import DVCode.Tools.Samples as Samples
    samples = [Samples.mfv_neu_tau10000um_M1600]
    for sample in samples:
        sample.set_curr_dataset('miniaod')
        sample.split_by = 'events'
        sample.events_per = 3000

    from DVCode.Tools.MetaSubmitter import *
    ms = MetaSubmitter('PackedCandsV2', dataset='miniaod')
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier, secondary_files_modifier('main'))
    ms.submit(samples)
