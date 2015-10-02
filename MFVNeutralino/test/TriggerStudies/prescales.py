#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.TFileService.fileName = 'prescales.root'

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v2', '')

process.source.fileNames = [
    '/store/data/Run2015D/SingleMuon/AOD/PromptReco-v3/000/256/729/00000/0283F591-A25F-E511-93AB-02163E011BBE.root'
    ]

add_analyzer(process, 'MFVTriggerPrescales')
process.maxEvents.input = 100

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('QuadJetTrigPrescales',
                       total_number_of_lumis = -1,
                       lumis_per_job = 500,
                       skip_common = True,
                       )
    cs.submit_all(Samples.data_samples_orig + Samples.auxiliary_data_samples)
