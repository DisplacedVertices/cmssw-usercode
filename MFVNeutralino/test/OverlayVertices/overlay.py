#!/usr/bin/env python

from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.CMSSWTools import *
import JMTucker.Tools.SampleFiles as SampleFiles
import JMTucker.Tools.Samples as Samples
from JMTucker.MFVNeutralino.Year import year

allowed_samples = Samples.ttbar_samples + Samples.qcd_samples_sum + Samples.ttbar_samples_2015 + Samples.qcd_samples_sum_2015

parser, args_printer = friendly_argparse(description='Overlay tracks from pairs of 1-vertex events')
parser.add_argument('+which-event', '+e', type=int, help='which event from minitree to use', required=True)
parser.add_argument('+sample', help='which sample to use', choices=[s.name for s in allowed_samples], default='qcdht1500sum')
parser.add_argument('+ntracks', type=int, help='ntracks to use', default=3, choices=[3,4,5])
parser.add_argument('+no-rest-of-event', action='store_false', dest='rest_of_event', help='whether to use the rest of the tracks in the edm event')
parser.add_argument('+z-model', help='z model', choices=['deltasv', 'deltasvgaus', 'deltapv', 'none'], default='deltasvgaus')
parser.add_argument('+z-width', type=float, help='width of gaus used in z model (cm)', default=99)
parser.add_argument('+dz-true-max', type=float, help='max dz allowed for z model (cm)', default=1e9)
parser.add_argument('+found-dist', type=float, help='3D distance for matching by position (cm)', default=0.008)
parser.add_argument('+rotate-x', action='store_true', help='azimuthally rotate x of tracks (around beam line)')
parser.add_argument('+rotate-p', action='store_true', help='azimuthally rotate p of tracks')
parser.add_argument('+is-data', action='store_true', help='whether input is data / MC')
parser.add_argument('+is-H', action='store_true', help='if data, whether input is the H dataset')
parser.add_argument('+debug', action='store_true', help='turn on debug prints')
parser.add_argument('+debug-timing', action='store_true', help='turn on want summary to see the time report')
parser.add_argument('+in-path', help='override input path', default='root://cmsxrootd.fnal.gov//store/user/tucker/skimpickv14')
parser.add_argument('+in-fn', help='override input fn')
parser.add_argument('+out-fn', help='override output fn')
parser.add_argument('+minitree-path', help='override minitree path', default='root://cmsxrootd.fnal.gov//store/user/tucker/MiniTreeV14_forpick')
parser.add_argument('+minitree-fn', help='override minitree fn')
parser.add_argument('+minitree-treepath', help='override minitree tree path')
parser.add_argument('+max-events', type=int, help='max edm events to run on', default=-1)

args = parser.parse_args()

if args.in_fn is None:
    args.in_fn = '%s/%s.root' % (args.in_path, args.sample)
if args.out_fn is None:
    args.out_fn = 'overlay_%i.root' % args.which_event
if args.minitree_fn is None:
    args.minitree_fn = '%s/%s.root' % (args.minitree_path, args.sample)
if args.minitree_treepath is None:
    args.minitree_treepath = 'mfvMiniTreeNtk%i/t' % args.ntracks if args.ntracks != 5 else 'mfvMiniTree/t'

if args.z_width == 99:
    args.z_width = 0.03 if args.ntracks == 3 else 0.02
    
args_printer('overlay args', args)

####

process = basic_process('Overlay')
process.source.fileNames = [args.in_fn]
process.maxEvents.input = args.max_events
want_summary(process, args.debug or args.debug_timing)
silence_messages(process, ['TwoTrackMinimumDistanceHelixLine'])
report_every(process, 1 if args.debug else 1000 if args.debug_timing else 1000000)
geometry_etc(process, which_global_tag(not args.is_data, year, args.is_H))
tfileservice(process, args.out_fn)
random_service(process, {'mfvVertices':      12179 + args.which_event,
                         'mfvOverlayTracks': 12180 + args.which_event})

process.load('JMTucker.MFVNeutralino.Vertexer_cfi')
process.mfvVertices.histos = False
process.mfvVertices.verbose = args.debug
process.mfvVertices.track_src = 'mfvSkimmedTracks'
process.mfvVertices.primary_vertices_src = '' #firstGoodPrimaryVertex
process.mfvVertices.use_second_tracks = True
process.mfvVertices.second_track_src = 'mfvOverlayTracks'

if not args.rest_of_event:
    process.mfvVertices.disregard_event = True

process.mfvOverlayTracks = cms.EDFilter('MFVOverlayVertexTracks',
                                        minitree_fn = cms.string(args.minitree_fn),
                                        minitree_treepath = cms.string(args.minitree_treepath),
                                        which_event = cms.int32(args.which_event),
                                        rotate_x = cms.bool(args.rotate_x),
                                        rotate_p = cms.bool(args.rotate_p),
                                        z_model = cms.string(args.z_model),
                                        z_width = cms.double(args.z_width),
                                        rest_of_event = cms.bool(args.rest_of_event),
                                        only_other_tracks = cms.bool(args.rest_of_event),
                                        verbose = cms.bool(args.debug),
                                        )

process.mfvOverlayHistos = cms.EDAnalyzer('MFVOverlayVertexHistos',
                                          truth_src = cms.InputTag('mfvOverlayTracks'),
                                          beamspot_src = cms.InputTag('offlineBeamSpot'),
                                          vertices_src = cms.InputTag('mfvVertices'),
                                          dz_true_max = cms.double(args.dz_true_max),
                                          min_ntracks = cms.int32(args.ntracks),
                                          found_dist = cms.double(args.found_dist),
                                          debug = cms.bool(args.debug),
                                          )

process.p = cms.Path(process.mfvOverlayTracks * process.mfvVertices * process.mfvOverlayHistos)
