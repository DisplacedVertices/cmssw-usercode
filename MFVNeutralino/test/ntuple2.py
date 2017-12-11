#!/usr/bin/env python

from JMTucker.Tools.MiniAOD_cfg import cms, which_global_tag
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

is_mc = True
version = 'v16maod'
batch_name = 'Ntuple' + version.upper()

####

process = basic_process('Ntuple')
report_every(process, 1000000)
registration_warnings(process)
geometry_etc(process, which_global_tag(is_mc, year, H=False, repro=False))
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
process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.PATTupleSelection_cfi')
process.load('JMTucker.MFVNeutralino.UnpackedCandidateTracks_cfi')
process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'

process.selectedPatJets.src = 'slimmedJets'
process.selectedPatJets.cut = process.jtupleParams.jetCut

process.selectedPatMuons.src = 'slimmedMuons'
process.selectedPatMuons.cut = process.jtupleParams.muonCut

process.selectedPatElectrons.src = 'slimmedElectrons'
process.selectedPatElectrons.cut = process.jtupleParams.electronCut

process.mfvGenParticles.gen_particles_src = 'prunedGenParticles'

process.mfvVertices.track_src = 'mfvUnpackedCandidateTracks'

#process.mfvVerticesToJets.enable = False # have to figure out how to use daughters of slimmed jets and the map we make in UnpackedCandidateTracks
process.mfvVerticesToJets.input_is_miniaod = True
process.mfvVerticesAuxTmp.input_is_miniaod = True
process.mfvVerticesAuxPresel.input_is_miniaod = True

process.mfvEvent.gen_particles_src = 'prunedGenParticles' # no idea if this lets gen_flavor_code, gen_bquarks, gen_leptons work. I think for the latter you'd want the packed ones that have status 1 particles
process.mfvEvent.gen_jets_src = 'slimmedGenJets'
process.mfvEvent.pileup_info_src = 'slimmedAddPileupInfo'
process.mfvEvent.met_src = 'slimmedMETs'

process.p = cms.Path(process.goodOfflinePrimaryVertices *
                     process.selectedPatJets *
                     process.selectedPatMuons *
                     process.selectedPatElectrons *
                     process.mfvTriggerFloats *
                     process.mfvUnpackedCandidateTracks *
                     process.mfvVertexSequence *
                     process.mfvEvent)

process.options.wantSummary = True
process.maxEvents.input = -1
process.source.fileNames = ['file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/A00610B3-00B7-E611-8546-A0000420FE80.root']
file_event_from_argv(process)
