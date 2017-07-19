from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
zerobias = False
repro = False
meatloverssupreme = True
dataset_version = 1
dataset = 'v0ntuplev%i' % dataset_version

geometry_etc(process, which_global_tag(is_mc, year, H, repro))
process.TFileService.fileName = 'v0histos.root'

process.source.fileNames = ['file:v0ntuple.root']
process.source.fileNames = ['/store/user/tucker/V0NtupleV1_qcdht1000_hip1p0_mit.root']
report_every(process, 100)
process.maxEvents.input = 10000

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
                               min_track_dxybs = cms.double(-1),
                               max_track_dxybs = cms.double(-1),
                               min_track_nsigmadxybs = cms.double(4),
                               min_track_npxlayers = cms.int32(0),
                               max_track_npxlayers = cms.int32(1000000),
                               min_track_nstlayers = cms.int32(0),
                               max_track_nstlayers = cms.int32(1000000),
                               min_track_nstlayersstereo = cms.int32(0),
                               max_track_nstlayersstereo = cms.int32(1000000),
                               track_inpv_req = cms.int32(0),
                               max_chi2ndf = cms.double(5),
                               min_p = cms.double(0),
                               max_p = cms.double(1e9),
                               min_eta = cms.double(-1e9),
                               max_eta = cms.double(1e9),
                               abs_eta_cut = cms.bool(False),
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

process.v0effbkglo = process.v0eff.clone(mass_window_lo = -0.420, mass_window_hi = -0.460)
process.v0effbkghi = process.v0eff.clone(mass_window_lo = -0.540, mass_window_hi = -0.600)
process.v0effon = process.v0eff.clone(mass_window_lo = -0.490, mass_window_hi = -0.505)
process.p *= process.v0effbkglo * process.v0effbkghi * process.v0effon

if meatloverssupreme:
    def addmodified(tag, code):
        al = eval('process.v0eff     .clone(%s)' % code)
        lo = eval('process.v0effbkglo.clone(%s)' % code)
        hi = eval('process.v0effbkghi.clone(%s)' % code)
        on = eval('process.v0effon   .clone(%s)' % code)
        setattr(process, 'v0eff' + tag, al)
        setattr(process, 'v0effbkglo' + tag, lo)
        setattr(process, 'v0effbkghi' + tag, hi)
        setattr(process, 'v0effon' + tag, on)
        process.p *= al * lo * hi * on

    if dataset_version >= 2:
        addmodified('loose', 'min_track_nsigmadxybs = 1')
        addmodified('loosenocos', 'min_track_nsigmadxybs = 1, min_costh2 = -2')

    addmodified('nsigdxy3', 'min_track_nsigmadxybs = 3')
    addmodified('nsigdxy5', 'min_track_nsigmadxybs = 5')

    addmodified('dxybslt500um',      'max_track_dxybs = 0.05')
    addmodified('dxybsgt500umlt1mm', 'min_track_dxybs = 0.05, max_track_dxybs = 0.1')
    addmodified('dxybsgt1mm',        'min_track_dxybs = 0.1')

    n = 3
    for i in xrange(n):
        min_eta = 0 + 2.5/n * i
        max_eta = 0 + 2.5/n * (i+1)
        addmodified('aeta%i' % i, 'abs_eta_cut = True, min_eta = %.1f, max_eta = %.1f' % (min_eta, max_eta))

    addmodified('npxlaymin3', 'min_track_npxlayers = 3')
    addmodified('nstlaymin10', 'min_track_nstlayers = 10')

    supertracks = 'min_track_pt = 3.5, min_track_npxlayers = 3, min_track_nstlayers = 10'
    addmodified('supertracks',       supertracks)
    addmodified('supertracksbarrel', supertracks + ', abs_eta_cut = True, min_eta = 0, max_eta = 0.833')
    addmodified('supertracksendcap', supertracks + ', abs_eta_cut = True, min_eta = 1.666, max_eta = 2.5')

    addmodified('inpv1', 'track_inpv_req = 1')
    addmodified('inpv2', 'track_inpv_req = 2')

    addmodified('costh2tight', 'min_costh2 = 0.9998')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples 

    samples = [s for s in Samples.registry.all() if s.has_dataset(dataset)]
    samples = [Samples.JetHT2016D, Samples.JetHT2016G, Samples.JetHT2016G, Samples.qcdht1000, Samples.qcdht1500, Samples.qcdht1000_hip1p0_mit, Samples.qcdht1500_hip1p0_mit]
    set_splitting(samples, dataset, 'default', '../ana_2015p6.json', 2)

    cs = CondorSubmitter('V0EfficiencyV%i_v19' % dataset_version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(is_mc_modifier, H_modifier, zerobias_modifier, repro_modifier),
                         )
    cs.submit_all(samples)
