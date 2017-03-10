#!/usr/bin/env python

from JMTucker.Tools.MiniAOD_cfg import cms, pat_tuple_process
from JMTucker.Tools.CMSSWTools import file_event_from_argv
from JMTucker.MFVNeutralino.Year import year

is_mc = True

####

def customize_before_unscheduled(process):
    process.out.outputCommands = [
        'drop *',
        'keep *_mcStat_*_*',
        'keep *_skimmedGeneralTracks_*_*',
        'keep recoGenParticles_genParticles_*_*',
        'keep *_preselectedPatJets_*_*',
        'keep patMuons_patMuons_*_*',
        'keep patElectrons_patElectrons_*_*',
        'keep *_patMETsNoHF_*_*',
        'keep recoBeamSpot_offlineBeamSpot_*_*',
        'keep recoVertexs_offlinePrimaryVertices_*_*',
        'keep *_TriggerResults_*_HLT',
        'keep *_TriggerResults_*_PAT',
        'keep GenEventInfoProduct_generator_*_*',
        'keep *_addPileupInfo_*_*',
        ]

process = pat_tuple_process(customize_before_unscheduled, is_mc, year)
process.out.fileName = 'miniaod.root'

process.out.outputCommands += [
    # these three get added to the end somehow
    'drop patMETs_patPFMetPuppi__PAT',
    'drop patMETs_patCaloMet__PAT',
    'drop patMETs_patMETPuppi__PAT',
    ]

process.skimmedGeneralTracks = cms.EDProducer('MFVSkimmedTracks')

process.patJets.embedPFCandidates = True
process.preselectedPatJets = process.selectedPatJets.clone(cut = process.jtupleParams.jetPresel)
process.patMuons.embedTrack = True
process.patElectrons.embedTrack = True
process.patElectrons.embedGsfElectronCore = True

import JMTucker.MFVNeutralino.TriggerFilter
JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)

process.maxEvents.input = 100
file_event_from_argv(process)
