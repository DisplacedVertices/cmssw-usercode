from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.general import typed_from_argv

debug = False
is_mc = True
which_event = None
rest_of_event = False
dz_true_max = 1e9
min_ntracks = 3
found_dist = 0.008
z_model = 'deltasvgaus'
z_width = 0.02

if which_event is None:
    which_event = typed_from_argv(int)
    if which_event is None:
        raise ValueError('which_event from argv but no int found')
    print 'which_event from argv:', which_event

out_fn = 'overlay%s_Z%s%s_dist%s_%i.root' % ('_wevent' if rest_of_event else '',
                                             z_model,
                                             ('%.3f' % z_width).replace('.', 'p') if 'gaus' in z_model else '',
                                             ('%.3f' % found_dist).replace('.', 'p'),
                                             which_event)

process = basic_process('Overlay')
geometry_etc(process, which_global_tag(is_mc))
tfileservice(process, out_fn)
random_service(process, {'mfvVertices': 12179, 'mfvOverlayTracks': 12180})

if is_mc:
    process.load('JMTucker.Tools.MCStatProducer_cff')
    process.mcStat.histos = True

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('JMTucker.MFVNeutralino.Vertexer_cfi')

process.mfvVertices.verbose = debug
#process.mfvVertices.track_src = 'mfvOverlayTracks'
#process.mfvVertices.no_track_cuts = True
process.mfvVertices.use_second_tracks = True
process.mfvVertices.second_track_src = 'mfvOverlayTracks'
if not rest_of_event:
    process.mfvVertices.disregard_event = True

process.mfvOverlayTracks = cms.EDFilter('MFVOverlayVertexTracks',
                                        minitree_fn = cms.string('minitree.root'),
                                        which_event = cms.int32(which_event),
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

process.mfvOverlayTracks.minitree_fn = '/uscms_data/d2/tucker/crab_dirs/MinitreeV9_temp/ttbar.root'
process.maxEvents.input = -1
process.source.fileNames = ['/store/user/tucker/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/pick1vtx/161020_194226/0000/' + x.strip() for x in \
'''
pick_1.root
pick_2.root
pick_3.root
pick_4.root
pick_5.root
pick_7.root
pick_8.root
pick_10.root
pick_14.root
pick_16.root
pick_17.root
pick_18.root
pick_23.root
pick_25.root
pick_26.root
pick_27.root
'''.split('\n') if x.strip()]

report_every(process, 100)
