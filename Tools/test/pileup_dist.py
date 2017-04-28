import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

from_miniaod = False

import JMTucker.Tools.SampleFiles as sf
sf.set_process(process, 'qcdht1500', 'main', 10)

process.TFileService.fileName = 'pileup_mc.root'

process.MCPileupDist = cms.EDAnalyzer('PileupDist',
                                      primary_vertices_src = cms.InputTag('offlinePrimaryVertices'),
                                      pileup_info_src = cms.InputTag('addPileupInfo')
                                      )

if from_miniaod:
    process.MCPileupDist.primary_vertices_src = cms.InputTag('offlineSlimmedPrimaryVertices')
    process.MCPileupDist.pileup_info_src = cms.InputTag('slimmedAddPileupInfo')

process.MCPileupDistHLT = process.MCPileupDist.clone()

process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.hltHighLevel.HLTPaths = ['HLT_PFHT800_v*', 'HLT_PFHT900_v*', 'HLT_PFJet450_v*', 'HLT_AK8PFJet450_v*']
process.hltHighLevel.andOr = True
process.hltHighLevel.throw = False

process.p = cms.Path(process.MCPileupDist * process.hltHighLevel * process.MCPileupDistHLT)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
   from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples 

    if year == 2015:
        samples = Samples.data_samples_2015 + Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    for s in samples:
        if not s.is_mc:
            s.json = 'ana_2015p6.json'
        s.split_by = 'files'
        s.files_per = 200

    ms = MetaSubmitter('PileupDistV3')
    ms.common.ex = year
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
