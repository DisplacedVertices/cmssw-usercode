import FWCore.ParameterSet.Config as cms

from SimGeneral.HepPDTESSource.pythiapdt_cfi import *

mfvGenHistos = cms.EDAnalyzer('MFVGenHistos',
                              gen_src = cms.InputTag('genParticles'),
                              gen_jet_src = cms.InputTag('ak4GenJets'),
                              check_all_gen_particles = cms.bool(False),
                              mci_mode = cms.string('mfv3j')
                              )
