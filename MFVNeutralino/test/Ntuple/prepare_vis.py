# first run
#
# cmsRun pat.py keep_all [is_data] filename.root nevents
#  or
# cmsRun pat.py keep_all [is_data] filename.root run event
#  or
# cmsRun pat.py keep_all [is_data] filename.root run lumi event
# 
# where filename.root may be a local file, /store/**/*.root, or an xrootd url
# and nevents will set maxEvents.input = nevents
# or run,event or run,lumi,event is the specific event number you want
# and specify is_data if it's data.

from JMTucker.Tools.CMSSWTools import file_event_from_argv
from ntuple import *

process.source.fileNames = ['file:pat.root']
file_event_from_argv(process, warn=False)

process.out.fileName = ['ntuple4vis.root']
process.out.outputCommands = ['keep *']
process.mfvEvent.skip_event_filter = ''

process.mfvVertices.write_tracks = True
process.mfvSelectedVerticesTight.produce_vertices = True
process.mfvSelectedVerticesTight.produce_tracks = True
process.mfvSelectedVerticesTightLargeErr.produce_vertices = True
process.mfvSelectedVerticesTightLargeErr.produce_tracks = True

process.load('JMTucker.MFVNeutralino.VertexRefitter_cfi')
process.mfvVertexRefitsDrop0 = process.mfvVertexRefits.clone(n_tracks_to_drop = 0)
process.mfvVertexRefitsDrop2 = process.mfvVertexRefits.clone(n_tracks_to_drop = 2)
process.mfvVertexRefitsLargeErr = process.mfvVertexRefits.clone(vertex_src = 'mfvSelectedVerticesTightLargeErr')
process.mfvVertexRefitsLargeErrDrop2 = process.mfvVertexRefits.clone(vertex_src = 'mfvSelectedVerticesTightLargeErr', n_tracks_to_drop = 2)
process.p *= process.mfvVertexRefits * process.mfvVertexRefitsDrop2 *  process.mfvVertexRefitsDrop0 * process.mfvVertexRefitsLargeErr * process.mfvVertexRefitsLargeErrDrop2

if is_mc:
    process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                             gen_src = cms.InputTag('genParticles'),
                                             print_info = cms.bool(True),
                                             )
    process.load('JMTucker.Tools.ParticleListDrawer_cff')
    process.p *= process.mfvGenParticles * process.ParticleListDrawer
