import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

del process.TFileService
process.MessageLogger.cerr.FwkReport.reportEvery = 1
file_event_from_argv(process)

process.load('JMTucker.Tools.ParticleListDrawer_cff')
process.ParticleListDrawer.maxEventsToPrint = -1
process.p = cms.Path(process.ParticleListDrawer)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import background_samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('BkgsParticleList',
                       total_number_of_events = 3,
                       number_of_jobs = 1,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*',
                       )
    cs.submit_all([s for s in background_samples if s.name != 'ttbarhadronic'])
