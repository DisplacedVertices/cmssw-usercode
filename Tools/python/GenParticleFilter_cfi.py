import FWCore.ParameterSet.Config as cms
from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import Realistic25ns13TeVEarly2017CollisionVtxSmearingParameters as bs

jmtGenParticleFilter = cms.EDFilter('JMTGenParticleFilter',
                                    gen_particles_src = cms.InputTag('genParticles'),
                                    bsx = bs.X0,
                                    bsy = bs.Y0,
                                    bsz = bs.Z0,
                                    min_pvrho = cms.double(0),
                                    max_pvrho = cms.double(1e9),
                                    min_flavor_code = cms.int32(0),
                                    max_flavor_code = cms.int32(1000),
                                    )
