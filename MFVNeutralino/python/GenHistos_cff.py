import FWCore.ParameterSet.Config as cms

from SimGeneral.HepPDTESSource.pythiapdt_cfi import *

mfvGenHistos = cms.EDAnalyzer('MFVGenHistos',
                              gen_src = cms.InputTag('genParticles'),
                              print_info = cms.untracked.int32(0),
                              )
