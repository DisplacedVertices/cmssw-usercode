from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.Tools.CMSSWTools import *

is_mc = True
process = basic_process('Overlay')
geometry_etc(process, which_global_tag(is_mc))
tfileservice(process, 'overlay.root')
random_service(process, {'mfvVertices': 12179})

if is_mc:
    process.load('JMTucker.Tools.MCStatProducer_cff')
    process.mcStat.histos = True

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('JMTucker.MFVNeutralino.Vertexer_cfi')

process.mfvVertices.use_second_tracks = True
process.mfvVertices.second_track_src = 'mfvOverlayTracks'
process.mfvVertices.disregard_event = True
#process.mfvVertices.no_track_cuts = True
process.mfvVertices.verbose = True

process.veto = cms.EDFilter('EventIdVeto',
                         use_run = cms.bool(False),
                         list_fn = cms.string('veto.gz'),
                         debug = cms.untracked.bool(False),
                         )

process.mfvOverlayTracks = cms.EDProducer('MFVOverlayVertexTracks',
                                          minitree_fn = cms.string('minitree.root'),
                                          which_event = cms.int32(0),
                                          only_other_tracks = cms.bool(False),
                                          verbose = cms.bool(True),
                                          )

process.mfvOverlayHistos = cms.EDAnalyzer('MFVOverlayVertexHistos',
                                          truth_src = cms.InputTag('mfvOverlayTracks'),
                                          vertices_src = cms.InputTag('mfvVertices'),
                                          min_ntracks = cms.int32(3),
                                          )

process.p = cms.Path(~process.veto * process.goodOfflinePrimaryVertices * process.mfvOverlayTracks * process.mfvVertices * process.mfvOverlayHistos)

process.mfvOverlayTracks.minitree_fn = '/uscms_data/d2/tucker/crab_dirs/MinitreeV9_temp/ttbar.root'
process.veto.list_fn = 'veto_ttbar_temp'
process.maxEvents.input = -1
process.source.fileNames = ['/store/user/tucker/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/pick1vtx/161020_194226/0000/pick_1.root']
report_every(process, 1)
