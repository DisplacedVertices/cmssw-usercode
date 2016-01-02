#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag

process.TFileService.fileName = 'prescales.root'
global_tag(process, which_global_tag(is_mc=False))

process.source.fileNames = ['/store/data/Run2015D/JetHT/AOD/PromptReco-v4/000/260/627/00000/78D8E6A7-6484-E511-89B4-02163E0134F6.root']

add_analyzer(process, 'MFVTriggerPrescales')
process.maxEvents.input = -1

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('QuadJetTrigPrescales',
                       total_number_of_lumis = -1,
                       lumis_per_job = 500,
                       skip_common = True,
                       )
    cs.submit_all(Samples.data_samples_orig + Samples.auxiliary_data_samples)
