#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.CMSSWTools import which_global_tag
from JMTucker.Tools.Year import year

H = False
repro = False

process.TFileService.fileName = 'prescales.root'
global_tag(process, which_global_tag(is_mc=False, year=year, H=H, repro=repro))

process.source.fileNames = ['/store/data/Run2015D/JetHT/AOD/PromptReco-v4/000/260/627/00000/78D8E6A7-6484-E511-89B4-02163E0134F6.root']

from JMTucker.Tools.L1GtUtils_cff import l1GtUtilsTags
add_analyzer(process, 'MFVTriggerPrescales', l1GtUtilsTags)

process.maxEvents.input = -1

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('TriggerPrescalesV0',
                       pset_modifier = chain_modifiers(H_modifier, repro_modifier),
                       splitting = 'FileBased',
                       units_per_job = 20,
                       total_units = -1,
                       )
    cs.submit_all(Samples.data_samples)
