import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

from_miniaod = False

import JMTucker.Tools.SampleFiles as sf
sf.set_process(process, 'qcdht1000_2015', 'main', 5)

process.TFileService.fileName = 'mc_pileup.root'

process.MCPileupDist = cms.EDAnalyzer('PileupDist',
                                      pileup_info_src = cms.InputTag('slimmedAddPileupInfo' if from_miniaod else 'addPileupInfo'),
                                      binning = cms.vdouble(100, 0, 100)
                                      )
process.MCPileupDistHLT = process.MCPileupDist.clone()

process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.hltHighLevel.HLTPaths = ['HLT_PFHT800_v*', 'HLT_PFHT900_v*', 'HLT_PFJet450_v*', 'HLT_AK8PFJet450_v*']
process.hltHighLevel.andOr = True
process.hltHighLevel.throw = False

process.p = cms.Path(process.MCPileupDist * process.hltHighLevel * process.MCPileupDistHLT)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 

    # looks like it's OK to read older samples here just to get the addPileupInfo object
    samples = [
        Samples.qcdht0500, Samples.qcdht0500ext, Samples.qcdht2000, Samples.qcdht2000ext,
        Samples.qcdht0500_2015, Samples.qcdht0500ext_2015, Samples.qcdht2000_2015, Samples.qcdht2000ext_2015,
        Samples.mfv_neu_tau10000um_M0800_2015, Samples.official_mfv_neu_tau10000um_M0800
        ]

    for s in samples:
        s.files_per = 10

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('PileupDistV2')
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
