import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.TrackRefGetter_cff import jmtTrackRefGetter
from JMTucker.MFVNeutralino.Vertexer_cfi import kvr_params

mfvVerticesAuxTmp = cms.EDProducer('MFVVertexAuxProducer',
                                   kvr_params = kvr_params,
                                   beamspot_src = cms.InputTag('offlineBeamSpot'),
                                   primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                   gen_vertices_src = cms.InputTag('mfvGenParticles', 'decays'),
                                   vertex_src = cms.InputTag('mfvVertices'),
                                   sv_to_jets_src = cms.string('dummy'),
                                   track_ref_getter = jmtTrackRefGetter,
                                   sv_to_muons_src = cms.string('dummy'),
                                   sv_to_ele_src = cms.string('dummy'),
                                   muons_src = cms.InputTag('selectedPatMuons'),
                                   electrons_src = cms.InputTag('selectedPatElectrons'),
                                   rho_src = cms.InputTag('fixedGridRhoFastjetAll'),
                                   electron_effective_areas = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt'),
                                   sort_by = cms.string('ntracks_then_mass'),
                                   verbose = cms.untracked.bool(False),
                                   )

mfvVerticesAux = mfvVerticesAuxTmp.clone(sv_to_jets_src = 'mfvVerticesToJets', 
                                         sv_to_muons_src = 'mfvVerticesToLeptons',
                                         sv_to_ele_src = 'mfvVerticesToLeptons')
