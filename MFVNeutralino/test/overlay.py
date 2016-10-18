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
#process.mfvVertices.disregard_event = True
#process.mfvVertices.no_track_cuts = True
process.mfvVertices.verbose = True

process.mfvOverlayTracks = cms.EDProducer('MFVOverlayVertexTracks',
                                          minitree_fn = cms.string('minitree.root'),
                                          which_event = cms.int32(0),
                                          only_other_tracks = cms.bool(True),
                                          verbose = cms.bool(True),
                                          )

process.p = cms.Path(process.goodOfflinePrimaryVertices * process.mfvOverlayTracks * process.mfvVertices)

process.maxEvents.input = 2
process.source.fileNames = ['/store/mc/RunIIFall15DR76/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/0039E642-58BD-E511-B773-002590DE7230.root']
file_event_from_argv(process)

set_events_to_process(process, [ (1, 374886, 93627873), (1, 529143, 132153748)])


