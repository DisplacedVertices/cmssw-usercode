#!/usr/bin/env python

from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
repro = False

####

process = pat_tuple_process(None, is_mc, year, H, repro)

process.out.fileName = 'miniaod.root'
process.out.outputCommands += [
    'drop *',
    'keep *_mcStat_*_*',
    'keep *_skimmedGeneralTracks_*_*',
    'keep recoGenParticles_genParticles_*_*',
    'keep *_selectedPatJets_*_*',
    'keep patMuons_selectedPatMuons_*_*',
    'keep patElectrons_selectedPatElectrons_*_*',
    'keep *_patMETsNoHF_*_*',
    'keep recoBeamSpot_offlineBeamSpot_*_*',
    'keep recoVertexs_offlinePrimaryVertices_*_*',
    'keep *_mfvTriggerFloats_*_*',
    'keep *_mfvCleaningBits_*_*',
    'keep GenEventInfoProduct_generator_*_*',
    'keep *_addPileupInfo_*_*',
    ]

process.skimmedGeneralTracks = cms.EDProducer('MFVSkimmedTracks')

process.patJets.embedPFCandidates = True

process.patMuons.embedTrack = True
process.patMuons.embedCaloMETMuonCorrs   = False
process.patMuons.embedHighLevelSelection = False
process.patMuons.embedCombinedMuon       = False
process.patMuons.embedMuonBestTrack      = False
process.patMuons.embedPFCandidate        = False
process.patMuons.embedPfEcalEnergy       = False
process.patMuons.embedStandAloneMuon     = False
process.patMuons.embedTunePMuonBestTrack = False
process.patMuons.isolationValues = cms.PSet()

process.patElectrons.embedTrack = True
process.patElectrons.embedGsfElectronCore = True
process.patElectrons.embedHighLevelSelection = False
process.patElectrons.addElectronID = False
process.patElectrons.embedPFCandidate = False
process.patElectrons.addPFClusterIso  = False
process.patElectrons.isolationValues = cms.PSet()
process.patElectrons.isolationValuesNoPFId = cms.PSet()
process.patElectrons.electronIDSources = cms.PSet()

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.CleaningBits_cff')

import JMTucker.MFVNeutralino.EventFilter
JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, event_filter=True)

process.maxEvents.input = 500
file_event_from_argv(process)
