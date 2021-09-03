from DVCode.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/tucker/sstop_genfsimreco_test/sstop_genfsimreco_test//15c4250952b10a469cc6da8beaecd65e/fastsim_9_1_Ziq.root']
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.ParticleListDrawer = cms.EDAnalyzer('ParticleListDrawer',
                                            maxEventsToPrint = cms.untracked.int32(1000000),
                                            src = cms.InputTag('genParticles'),
                                            printOnlyHardInteraction = cms.untracked.bool(False),
                                            useMessageLogger = cms.untracked.bool(False)
                                            )

process.a = cms.EDAnalyzer('MCInteractionTest')
process.p = cms.Path(process.ParticleListDrawer * process.a)
