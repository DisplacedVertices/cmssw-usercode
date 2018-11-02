import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

del process.TFileService
process.MessageLogger.cerr.FwkReport.reportEvery = 1
file_event_from_argv(process)

process.load('JMTucker.Tools.ParticleListDrawer_cff')
process.ParticleListDrawer.maxEventsToPrint = -1
process.p = cms.Path(process.ParticleListDrawer)

#process.ParticleListDrawer.src = 'prunedGenParticles'
