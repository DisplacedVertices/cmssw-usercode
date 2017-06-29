from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.MFVNeutralino.Year import year

is_mc = False
H = False

global_tag(process, which_global_tag(is_mc, year, H))
process.TFileService.fileName = 'v0histos.root'

process.source.fileNames = ['file:v0ntuple.root']

process.load('JMTucker.MFVNeutralino.TriggerFloatsFilter_cfi')
process.mfvTriggerFloatsFilter.require_hlt = -5 if H else 1
process.mfvTriggerFloatsFilter.ht_cut = 1000
process.mfvTriggerFloatsFilter.min_njets = 4

process.v0eff = cms.EDAnalyzer('MFVV0Efficiency',
                               vertices_src = cms.InputTag('mfvV0Vertices'),
                               pileup_weights = cms.vdouble(*pileup_weights[year]),
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               primary_vertex_src = cms.InputTag('firstGoodPrimaryVertex'),
                               tracks_src = cms.InputTag('mfvSkimmedTracks'),
                               min_track_pt = cms.double(1),
                               min_track_nsigmadxybs = cms.double(4),
                               max_chi2ndf = cms.double(7),
                               min_p = cms.double(0),
                               max_p = cms.double(1e9),
                               mass_window_lo = cms.double(1e9),
                               mass_window_hi = cms.double(1e9),
                               min_costh3 = cms.double(-2),
                               debug = cms.untracked.bool(True)
                               )

process.p = cms.Path(process.mfvTriggerFloatsFilter * process.v0eff)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    samples = Samples.data_samples + [s for s in Samples.auxiliary_data_samples if s.name.startswith('ZeroBias')]
    for s in samples:
        s.files_per = 50

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('V0EfficiencyV1')
    ms.common.ex = year
    ms.common.pset_modifier = H_modifier #chain_modifiers(is_mc_modifier, H_modifier)
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
