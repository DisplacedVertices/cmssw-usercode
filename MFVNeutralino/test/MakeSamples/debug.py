import sys
from gensimhlt import cms, process

if 'replay' in sys.argv:
    from JMTucker.Tools.CMSSWTools import replay_event
    replay_event(process, filename=None, rle=None)

process.maxEvents.input = 1
process.options.wantSummary = True
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.generator.maxEventsToPrint = 2
process.generator.pythiaPylistVerbosity = 13
process.generator.pythiaHepMCVerbosity = True
process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                   src = cms.InputTag('genParticles'),
                                   printVertex = cms.untracked.bool(True),
                                   )
process.dumpGraph = cms.EDAnalyzer('GenParticlesGraphDumper',
                                   src = cms.InputTag('genParticles'),
                                   use_mothers = cms.bool(True),
                                   use_daughters = cms.bool(False),
                                   include_id_and_stat = cms.bool(True),
                                   )
process.pprint = cms.Path(process.printList) # * process.dumpGraph)
process.schedule.extend([process.pprint])
