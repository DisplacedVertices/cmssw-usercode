#!/usr/bin/env python

from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.general import bool_from_argv 
from JMTucker.Tools.MiniAOD_cfg import global_tag

is_mc = not bool_from_argv('is_data')

process = basic_process('MFVNtuple')

process.source.fileNames = ['file:pat.root']
#process.source.fileNames = ['/store/user/tucker/F47E7F59-8A29-E511-8667-002590A52B4A.pat500evt.root']
#process.source.fileNames = ['/store/user/tucker/mfv_neu_tau01000um_M0800_reco25ns_10k_150813_011937_0000_reco_1.pat100evt.root']
#set_events_to_process(process, [(1, 149765, 37404137)])
process.maxEvents.input = 10
process.options.wantSummary = True

registration_warnings(process)
geometry_etc(process, global_tag(is_mc))
tfileservice(process, 'vertex_histos.root')
random_service(process, {'mfvVertices': 1222})

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.p = cms.Path(process.mfvVertexSequence * process.mfvEvent)

output_commands = [
    'drop *',
    'keep *_mcStat_*_*',
    'keep MFVVertexAuxs_mfvVerticesAux_*_*',
    'keep MFVEvent_mfvEvent__*',
    'keep edmTriggerResults_TriggerResults__HLT',
    ]
output_file(process, 'ntuple.root', output_commands)

#process.mfvVertices.jumble_tracks = True
#process.mfvVertices.remove_tracks_frac = 0.1
#process.mfvVertices.use_tracks = False
#process.mfvVertices.use_non_pv_tracks = True
#process.mfvVertices.use_non_pvs_tracks = True
