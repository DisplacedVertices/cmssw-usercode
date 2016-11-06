#!/usr/bin/env python

max_events = -1
debug = False
is_mc = True
which_event = None
rest_of_event = False
dz_true_max = 1e9
min_ntracks = 3
found_dist = 0.008
z_model = 'deltasv'
z_width = 0.02
rotate_x = False
rotate_p = False
sample = 'ttbar'
minitree_path = 'root://cmsxrootd.fnal.gov//store/user/tucker/MinitreeV9/ntk%i' % min_ntracks

####

from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.general import typed_from_argv

batch = 'batch' in sys.argv

if which_event is None:
    which_event = typed_from_argv(int)
    if which_event is None:
        raise ValueError('which_event from argv but no int found')
    print 'which_event from argv:', which_event

rest_of_event_s = '_wevent' if rest_of_event else ''
z_width_s = ('%.3f' % z_width).replace('.', 'p') if 'gaus' in z_model else ''
found_dist_s = ('%.3f' % found_dist).replace('.', 'p')
rotate_s = ''
if rotate_x and rotate_p:
    rotate_s = '_rotateXP'
elif rotate_x:
    rotate_s = '_rotateX'
elif rotate_p:
    rotate_s = '_rotateP'

out_fn = 'overlay%(rest_of_event_s)s_%(sample)s_Z%(z_model)s%(z_width_s)s_dist%(found_dist_s)s%(rotate_s)s_%(which_event)i.root' % locals()

minitree_fn = '%s/%s.root' % (minitree_path, sample)

if sample == 'ttbar':
    file_base = '/store/user/tucker/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/pick1vtx/161104_153826/0000'
    file_nums = range(1,94)
elif sample == 'qcdht1500':
    file_base = '/store/user/tucker/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/pick1vtx/161104_153718/0000'
    file_nums = range(1,15)
    file_nums.remove(9)
else:
    raise ValueError('bad sample %s' % sample)

in_fns = [os.path.join(file_base, 'pick_%i.root' % i) for i in file_nums]

####

process = basic_process('Overlay')
process.source.fileNames = in_fns
process.maxEvents.input = max_events
report_every(process, 1000000 if batch else 100)
geometry_etc(process, which_global_tag(is_mc))
tfileservice(process, out_fn)
random_service(process, {'mfvVertices': 12179, 'mfvOverlayTracks': 12180})

if is_mc:
    process.load('JMTucker.Tools.MCStatProducer_cff')
    process.mcStat.histos = True

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('JMTucker.MFVNeutralino.Vertexer_cfi')

process.mfvVertices.histos = False
process.mfvVertices.verbose = debug
process.mfvVertices.use_second_tracks = True
process.mfvVertices.second_track_src = 'mfvOverlayTracks'
if not rest_of_event:
    process.mfvVertices.disregard_event = True

process.mfvOverlayTracks = cms.EDFilter('MFVOverlayVertexTracks',
                                        minitree_fn = cms.string(minitree_fn),
                                        which_event = cms.int32(which_event),
                                        rotate_x = cms.bool(rotate_x),
                                        rotate_p = cms.bool(rotate_p),
                                        z_model = cms.string(z_model),
                                        z_width = cms.double(z_width),
                                        only_other_tracks = cms.bool(rest_of_event),
                                        verbose = cms.bool(debug),
                                        )

process.mfvOverlayHistos = cms.EDAnalyzer('MFVOverlayVertexHistos',
                                          truth_src = cms.InputTag('mfvOverlayTracks'),
                                          beamspot_src = cms.InputTag('offlineBeamSpot'),
                                          vertices_src = cms.InputTag('mfvVertices'),
                                          dz_true_max = cms.double(dz_true_max),
                                          min_ntracks = cms.int32(min_ntracks),
                                          found_dist = cms.double(found_dist),
                                          debug = cms.bool(debug),
                                          )

process.p = cms.Path(process.goodOfflinePrimaryVertices * process.mfvOverlayTracks * process.mfvVertices * process.mfvOverlayHistos)
