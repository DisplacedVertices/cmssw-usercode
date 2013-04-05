from Configuration.StandardSequences.RawToDigi_cff import *
from Configuration.StandardSequences.Reconstruction_cff import *

redotracking = cms.Sequence(RawToDigi * trackerlocalreco * recopixelvertexing * trackingGlobalReco)

mfvMatchedTracks = cms.EDProducer('MFVTracksMatchedToSim',
                                  gen_particles_src = cms.InputTag('genParticles'),
                                  tracking_particles_src = cms.InputTag('mergedtruth','MergedTrackTruth'),
                                  tracks_src = cms.InputTag('generalTracks'),
                                  produce_nonmatched = cms.bool(True),
                                  min_match_quality = cms.double(0),
                                  min_track_pt = cms.double(2),
                                  )

mfvTrackMatching = cms.Sequence(redotracking * mfvMatchedTracks)
