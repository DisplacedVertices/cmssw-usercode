import FWCore.ParameterSet.Config as cms

process = cms.Process('MFVGenParticles')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/fastsim_313_2_yIN.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                         gen_src = cms.InputTag('genParticles'),
                                         gen_jet_src = cms.InputTag('ak5GenJets'),
                                         gen_met_src = cms.InputTag('genMetTrue'),
                                         print_info = cms.bool(True),
                                         )

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')

process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                   maxEventsToPrint = cms.untracked.int32(100),
                                   src = cms.InputTag('genParticles'),
                                   printOnlyHardInteraction = cms.untracked.bool(False),
                                   useMessageLogger = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(True),
                                   )

process.printList2 = process.printList.clone(src = cms.InputTag('mfvGenParticles', 'All'))
process.printList3 = process.printList.clone(src = cms.InputTag('mfvGenParticles', 'Visible'))

process.p = cms.Path(process.mfvGenParticles * process.printList2 * process.printList3)

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('gen_particles.root'),
                               outputCommands = cms.untracked.vstring('drop *', 'keep recoGenParticles_*_*_MFVGenParticles'),
                               )
process.outp = cms.EndPath(process.out)

