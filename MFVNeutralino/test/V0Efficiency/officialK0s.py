from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
repro = False
zerobias = False

process = pat_tuple_process(None, is_mc, year, H, repro)
jets_only(process)

#report_every(process, 100)
process.maxEvents.input = 10000
if is_mc:
    process.source.fileNames = ['/store/user/wsun/croncopyeos/qcdht1000/RunIISummer16DR80-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6/170606_165644/0000/reco_%i.root' % i for i in xrange(1,11)]
else:
    process.source.fileNames = ['/store/data/Run2016E/ZeroBias/AOD/23Sep2016-v1/100000/18151C77-4486-E611-84FD-0CC47A7C357A.root']

tfileservice(process, 'officialK0s.root')

process.goodOfflinePrimaryVertices.filter = True
process.p = cms.Path(process.goodOfflinePrimaryVertices)

if not zerobias:
    process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
    process.load('JMTucker.MFVNeutralino.TriggerFloatsFilter_cfi')
    process.mfvTriggerFloatsFilter.require_hlt = -5 if H else 1
    process.mfvTriggerFloatsFilter.ht_cut = 1000
    process.mfvTriggerFloatsFilter.min_njets = 4
    process.p *= process.mfvTriggerFloats * process.mfvTriggerFloatsFilter

process.v0eff = cms.EDAnalyzer('MFVOfficialK0s',
                               pileup_weights = cms.vdouble(*pileup_weights[year]),
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                               tracks_src = cms.InputTag('generalTracks'),
                               limit_set = cms.bool(True),
                               min_track_pt = cms.double(1),
                               min_track_nsigmadxybs = cms.double(4),
                               min_track_npxlayers = cms.int32(0),
                               max_track_npxlayers = cms.int32(1000000),
                               min_track_nstlayers = cms.int32(6),
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

process.v0effbkglo = process.v0eff.clone(mass_window_lo = -0.420, mass_window_hi = -0.460)
process.v0effbkghi = process.v0eff.clone(mass_window_lo = -0.540, mass_window_hi = -0.600)
process.v0effon = process.v0eff.clone(mass_window_lo = -0.490, mass_window_hi = -0.505)
process.p *= process.v0eff * process.v0effbkglo * process.v0effbkghi * process.v0effon

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

addmodified('nocut', 'min_track_pt = 0, min_track_nsigmadxybs = 0, min_track_nstlayers = 0, min_costh2 = -2')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    samples = Samples.data_samples + [s for s in Samples.auxiliary_data_samples if s.name.startswith('ZeroBias')]
    samples += [s for s in Samples.qcd_samples + Samples.qcd_samples_ext if '1000' in s.name or '1500' in s.name]
    samples += Samples.qcd_hip_samples[-2:]

    for s in samples:
        s.files_per = 20

    from JMTucker.Tools.MetaSubmitter import *
    batch_name = 'V0OfficialK0sV1'
    ms = MetaSubmitter(batch_name)
    ms.common.ex = year
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier, zerobias_modifier)
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
