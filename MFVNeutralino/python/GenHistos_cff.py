import FWCore.ParameterSet.Config as cms

from SimGeneral.HepPDTESSource.pythiapdt_cfi import *

mfvGenHistos = cms.EDAnalyzer('MFVGenHistos',
                              gen_src = cms.InputTag('genParticles'),
                              check_all_gen_particles = cms.bool(False),
                              )
