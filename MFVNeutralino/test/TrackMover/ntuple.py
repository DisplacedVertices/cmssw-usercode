#!/usr/bin/env python

from JMTucker.Tools.PATTuple_cfg import *

runOnMC = True # magic line, don't touch
process, common_seq = pat_tuple_process(runOnMC)
no_skimming_cuts(process)
process.patMuonsPF.embedTrack = False
process.patElectronsPF.embedTrack = False

process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService',
                                                   mfvMovedTracks = cms.PSet(initialSeed = cms.untracked.uint32(1220)))

process.out.dropMetaData = cms.untracked.string('ALL')
process.out.fileName = 'ntuple.root'
process.out.outputCommands = [
    'drop *',
    'keep MFVEvent_mfvEvent__*',
    'keep MFVVertexAuxs_mfvVerticesAux*__*',
    'keep *_mfvMovedTracks*_*_*',
    'keep recoPFCandidates_selectedPatJetsPF_pfCandidates_PAT',
    'keep *_generalTracks_*_*',
    ]

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.mfvMovedTracks = cms.EDProducer('MFVTrackMover',
                                        tracks_src = cms.InputTag('generalTracks'),
                                        primary_vertices_src = cms.InputTag('offlinePrimaryVertices'),
                                        jets_src = cms.InputTag('selectedPatJetsPF'),
                                        min_jet_pt = cms.double(50),
                                        min_jet_ntracks = cms.uint32(4),
                                        b_discriminator = cms.string('combinedSecondaryVertexBJetTags'),
                                        b_discriminator_veto = cms.double(0.244),
                                        b_discriminator_tag = cms.double(0.898),
                                        njets = cms.uint32(2),
                                        nbjets = cms.uint32(1),
                                        tau = cms.double(1),
                                        sig_theta = cms.double(0.2),
                                        sig_phi = cms.double(0.2),
                                        )

process.mfvVertices.track_src = 'mfvMovedTracks'
process.p = cms.Path(common_seq * process.mfvMovedTracks * process.mfvVertexSequence)

del process.outp
process.outp = cms.EndPath(process.mfvEvent * process.out)

import JMTucker.MFVNeutralino.TriggerFilter
JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)
