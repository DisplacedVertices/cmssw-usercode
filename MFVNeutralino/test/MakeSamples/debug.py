from gensimhlt import cms, process

if 'replay' in sys.argv:
    from JMTucker.Tools.CMSSWTools import replay_event
    replay_event(process, '/store/user/tucker/mfv_gensimhlt_gluino_tau1000um_M0400/mfv_gensimhlt_gluino_tau1000um_M0400/11e502b9027fe454bec38485095c4f53/gensimhlt_7_1_mcS.root', (1,7,35))

process.options.wantSummary = True
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.generator.maxEventsToPrint = 2
process.generator.pythiaPylistVerbosity = 13
process.generator.pythiaHepMCVerbosity = True
process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                   maxEventsToPrint = cms.untracked.int32(100),
                                   src = cms.InputTag('genParticles'),
                                   printOnlyHardInteraction = cms.untracked.bool(False),
                                   useMessageLogger = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(True),
                                   )
process.dumpGraph = cms.EDAnalyzer('GenParticlesGraphDumper',
                                   src = cms.InputTag('genParticles'),
                                   use_mothers = cms.bool(True),
                                   use_daughters = cms.bool(False),
                                   include_id_and_stat = cms.bool(True),
                                   )
process.pprint = cms.Path(process.printList * process.dumpGraph)
process.schedule.extend([process.pprint])
