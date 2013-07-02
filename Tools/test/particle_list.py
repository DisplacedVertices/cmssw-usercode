import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

del process.TFileService
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
add_analyzer('JMTParticleListDrawer',
             src = cms.InputTag('genParticles'),
             printVertex = cms.untracked.bool(True),
             )

file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import background_samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('BkgsParticleList',
                       total_number_of_events = 3,
                       number_of_jobs = 1,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*',
                       )
    cs.submit_all([s for s in background_samples if s.name != 'ttbarhadronic'])
