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

del process.outp
process.outp = cms.EndPath(process.mfvEvent * process.out)

process.p = cms.Path(common_seq * process.mfvGenVertices)

import JMTucker.MFVNeutralino.TriggerFilter
JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)

for njets in xrange(1,5):
    for nbjets in xrange(0,3):
        if njets == 1 and nbjets == 0:
            continue
        ex = '%i%i' % (njets, nbjets)

        def app(name, obj):
            setattr(process, name, obj)
            process.p *= obj

        mover = cms.EDProducer('MFVTrackMover',
                               tracks_src = cms.InputTag('generalTracks'),
                               primary_vertices_src = cms.InputTag('offlinePrimaryVertices'),
                               jets_src = cms.InputTag('selectedPatJetsPF'),
                               min_jet_pt = cms.double(50),
                               min_jet_ntracks = cms.uint32(4),
                               b_discriminator = cms.string('combinedSecondaryVertexBJetTags'),
                               b_discriminator_veto = cms.double(0.244),
                               b_discriminator_tag = cms.double(0.898),
                               njets = cms.uint32(njets),
                               nbjets = cms.uint32(nbjets),
                               tau = cms.double(1),
                               sig_theta = cms.double(0.2),
                               sig_phi = cms.double(0.2),
                               )

        mover_name = 'mfvMovedTracks' + ex
        app(mover_name, mover)

        setattr(process.RandomNumberGeneratorService, mover_name, cms.PSet(initialSeed = cms.untracked.uint32(1220 + njets*10 + nbjets)))

        vertices_name = 'mfvVertices' + ex
        app(vertices_name, process.mfvVertices.clone(track_src = mover_name))

        auxtmp_name = 'mfvVerticesAuxTmp' + ex
        app(auxtmp_name, process.mfvVerticesAuxTmp.clone(vertex_src = vertices_name))

        seltmp_name = 'mfvSelectedVerticesTmp' + ex
        app(seltmp_name, process.mfvSelectedVerticesTmp.clone(vertex_src = vertices_name,
                                                              vertex_aux_src = auxtmp_name))

        jet2vtx_name = 'mfvVerticesToJets' + ex
        app(jet2vtx_name, process.mfvVerticesToJets.clone(vertex_src = seltmp_name))

        aux_name = 'mfvVerticesAux' + ex
        app(aux_name, process.mfvVerticesAux.clone(vertex_src = vertices_name,
                                                   sv_to_jets_src = jet2vtx_name))
