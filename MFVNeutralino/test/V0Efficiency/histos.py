from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
zerobias = False

global_tag(process, which_global_tag(is_mc, year, H))
process.TFileService.fileName = 'v0histos.root'

process.source.fileNames = ['file:v0ntuple.root']
process.source.fileNames = ['/store/user/tucker/V0NtupleV1_qcdht1000_hip1p0_mit.root']
report_every(process, 100)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.mfvWeight.enable = False # just do mcStat

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
                               max_chi2ndf = cms.double(5),
                               min_p = cms.double(0),
                               max_p = cms.double(1e9),
                               mass_window_lo = cms.double(1e9),
                               mass_window_hi = cms.double(1e9),
                               min_costh2 = cms.double(0.995),
                               min_costh3 = cms.double(-2),
                               max_geo2ddist = cms.double(2),
                               debug = cms.untracked.bool(False)
                               )

process.p = cms.Path(process.mfvWeight * process.v0eff)
if not zerobias:
    process.p.insert(0, process.mfvTriggerFloatsFilter)

process.v0effbkglo = process.v0eff.clone(mass_window_lo = -0.380, mass_window_hi = -0.440)
process.v0effbkghi = process.v0eff.clone(mass_window_lo = -0.550, mass_window_hi = -0.600)
process.v0effon = process.v0eff.clone(mass_window_lo = -0.490, mass_window_hi = -0.505)
process.p *= process.v0effbkglo * process.v0effbkghi * process.v0effon

process.v0effonloose = process.v0effon.clone(min_track_nsigmadxybs = 3, min_track_pt = 0.)
process.p *= process.v0effonloose

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples 

    dataset = 'v0ntuplev1'
    samples = [s for s in Samples.registry.all() if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'default', '../ana_2015p6.json', 2)

    def zerobias_modifier(sample):
        return [], [('zerobias =XFalse'.replace('X', ' '), 'zerobias = True', 'no magic zerobias?')]

    cs = CondorSubmitter('V0EfficiencyV1_v8',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(is_mc_modifier, H_modifier, zerobias_modifier),
                         )
    cs.submit_all(samples)