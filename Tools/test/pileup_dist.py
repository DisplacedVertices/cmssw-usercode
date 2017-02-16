import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

from_miniaod = False

import JMTucker.Tools.SampleFiles as sf
sf.set_process(process, 'mfv_neu_tau10000um_M0800', 'main', 1)

process.TFileService.fileName = 'mc_pileup.root'

process.MCPileupDist = cms.EDAnalyzer('PileupDist',
                                      pileup_info_src = cms.InputTag('slimmedAddPileupInfo' if from_miniaod else 'addPileupInfo'),
                                      binning = cms.vdouble(100, 0, 100)
                                      )
process.MCPileupDistHLTPFHT = process.MCPileupDist.clone()

process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.hltHighLevel.HLTPaths = ['HLT_PFHT800_v*', 'HLT_PFHT900_v*']
process.hltHighLevel.andOr = True
process.hltHighLevel.throw = False

process.p = cms.Path(process.MCPileupDist * process.hltHighLevel * process.MCPileupDistHLTPFHT)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 

    if not from_miniaod:
        samples = [Samples.qcdht0500, Samples.qcdht0500ext, Samples.qcdht2000, Samples.qcdht2000ext,
                   Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau01000um_M1600]

        from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
        cs = CRABSubmitter('PileupDist_15_aod',
                           splitting = 'EventAwareLumiBased',
                           units_per_job = 200000,
                           total_units = -1,
                           )
        cs.submit_all(samples)
    else:
        samples = [Samples.qcdht0500, Samples.qcdht0500ext, Samples.qcdht2000, Samples.qcdht2000ext]

        from JMTucker.Tools.CondorSubmitter import CondorSubmitter
        cs = CondorSubmitter('PileupDist_15_miniaod',
                             dataset = 'miniaod',
                             pfn_prefix = 'root://cmseos.fnal.gov/', # if the files are at FNAL not just accessible by xrootd
                             events_per = 200000,
                             )
        cs.submit_all(condor_samples)
