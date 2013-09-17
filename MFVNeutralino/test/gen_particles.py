import sys, FWCore.ParameterSet.Config as cms

process = cms.Process('MFVGenParticles')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

process.load('JMTucker.Tools.ParticleListDrawer_cff')
process.load('JMTucker.MFVNeutralino.GenParticles_cff')

#process.mfvGenParticles.print_info = True
process.mfvGenVertices.print_info = True

process.ParticleListDrawer2 = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'All'))
process.ParticleListDrawer3 = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'Visible'))

process.p = cms.Path(process.ParticleListDrawer * process.mfvGenParticles * process.mfvGenVertices)
#process.p = cms.Path(process.mfvGenParticles * process.ParticleListDrawer2 * process.ParticleListDrawer3)

if 'out' in sys.argv:
    process.out = cms.OutputModule('PoolOutputModule',
                                   fileName = cms.untracked.string('gen_particles.root'),
                                   outputCommands = cms.untracked.vstring('drop *', 'keep recoGenParticles_*_*_MFVGenParticles'),
                                   )
    process.outp = cms.EndPath(process.out)

