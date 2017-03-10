#!/usr/bin/env python

from JMTucker.Tools.MiniAOD_cfg import cms, which_global_tag
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

is_mc = True
version = 'v9'
batch_name = 'Ntuple' + version.upper()

####

process = basic_process('Ntuple')
report_every(process, 1000000)
registration_warnings(process)
geometry_etc(process, which_global_tag(is_mc, year))
random_service(process, {'mfvVertices': 1222})
tfileservice(process, 'vertex_histos.root')
output_file(process, 'ntuple.root', [
        'drop *',
        'keep *_mcStat_*_*',
        'keep MFVVertexAuxs_mfvVerticesAux_*_*',
        'keep MFVEvent_mfvEvent__*',
        ])

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi')
process.load('JMTucker.Tools.PATTupleSelection_cfi')
process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.selectedPatJets.cut = process.jtupleParams.jetCut
process.selectedPatJets.src = 'preselectedPatJets'
process.selectedPatMuons.cut = process.jtupleParams.muonCut
process.selectedPatElectrons.cut = process.jtupleParams.electronCut

process.mfvVertices.track_src = 'skimmedGeneralTracks'

process.p = cms.Path(process.goodOfflinePrimaryVertices *
                     process.selectedPatJets *
                     process.selectedPatMuons *
                     process.selectedPatElectrons *
                     process.mfvVertices *
                     process.mfvEvent *
                     process.mfvGenVertices *
                     process.mfvVerticesAuxTmp *
                     process.mfvSelectedVerticesTmp *
                     process.mfvVerticesToJets *
                     process.mfvVerticesAux)

#process.options.wantSummary = True
process.maxEvents.input = 100
process.source.fileNames = ['file:miniaod.root']
file_event_from_argv(process)
