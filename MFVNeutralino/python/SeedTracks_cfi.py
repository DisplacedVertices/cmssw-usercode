import FWCore.ParameterSet.Config as cms

mfvSeedTracks = cms.EDProducer('MFVSeedTracksProducer', 
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               mci_src = cms.InputTag('mfvGenParticles'),
                               seed_tracks_src = cms.InputTag('mfvVertexTracks', 'seed'),
                               muon_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'museed'),
                               electron_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'eleseed'), # these two are used just to check if the seed track is a lepton or not )
                               )
