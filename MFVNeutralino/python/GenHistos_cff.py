import FWCore.ParameterSet.Config as cms

from SimGeneral.HepPDTESSource.pythiapdt_cfi import *

mfvGenHistos = cms.EDAnalyzer('MFVGenHistos',
                              gen_src = cms.InputTag('genParticles'),
                              gen_jet_src = cms.InputTag('ak5GenJets'),
                              check_all_gen_particles = cms.bool(False),
                              mci_bkg = cms.bool(False)
                              )
