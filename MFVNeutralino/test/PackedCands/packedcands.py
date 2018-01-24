from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.CMSSWTools import which_global_tag
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
repro = False
prints = False

####

process.source.fileNames = ['file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/A00610B3-00B7-E611-8546-A0000420FE80.root']
process.source.secondaryFileNames = cms.untracked.vstring(*['file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/%s.root'%x for x in '2A6D6695-3BB2-E611-BA91-24BE05C626B1','04E63C02-A4B3-E611-B32A-5065F37D7121','76CA2BA8-C1B4-E611-8E26-A0000420FE80','F2F5FB71-B2B4-E611-965D-5065F381A2F1','729AA0EC-60B3-E611-8CC1-A0000420FE80','74F234FF-19B3-E611-8BD2-A0369F3102F6','AAF9AAEF-A3B2-E611-B303-A0000420FE80','CAA8DC11-2FB4-E611-AFF1-5065F381B271','FC0B2D33-7AB2-E611-A0BB-A0369F3016EC','82DA3659-6CB4-E611-B34A-A0000420FE80','F6D152BB-C4B3-E611-9D2A-5065F382B261','14869E2D-1BB4-E611-AF08-24BE05CEADD1','9E6E0612-68B2-E611-A1F3-5065F37D2182'])

process.TFileService.fileName = 'packedcands.root'
geometry_etc(process, which_global_tag(is_mc, year, H, repro))
report_every(process, 1 if prints else 1000000)

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
process.goodOfflinePrimaryVertices.filter = True

process.mfvPackedCands = cms.EDAnalyzer('MFVPackedCandidates',
                                        max_closest_cd_dist = cms.double(0.111e-3),
                                        prints = cms.bool(prints),
                                        )
process.p = cms.Path(process.goodOfflinePrimaryVertices * process.mfvPackedCands)

import JMTucker.MFVNeutralino.EventFilter
JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, 'p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = [Samples.mfv_neu_tau10000um_M1600]
    for sample in samples:
        sample.set_curr_dataset('miniaod')
        sample.split_by = 'events'
        sample.events_per = 3000

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('PackedCandsV1')
    ms.common.ex = year
    ms.common.dataset = 'miniaod'
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier, secondary_files_modifier('main'))
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
