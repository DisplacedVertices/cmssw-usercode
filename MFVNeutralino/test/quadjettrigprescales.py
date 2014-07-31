#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.TFileService.fileName = 'quadjettrigprescales.root'

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'FT53_V21A_AN6::All'

process.source.fileNames = [
    '/store/data/Run2012B/MultiJet1Parked/AOD/05Nov2012-v2/10000/2A072028-5949-E211-947E-00304866C368.root',
    '/store/data/Run2012C/MultiJet1Parked/AOD/part1_05Nov2012-v2/10000/1E337BCE-2D4E-E211-8B97-003048D47A7C.root',
    '/store/data/Run2012C/MultiJet1Parked/AOD/part2_05Nov2012-v2/10012/70E96449-E65F-E211-B550-003048D45FB0.root',
    ]

add_analyzer('QuadJetTrigPrescales')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('QuadJetTrigPrescales',
                       total_number_of_lumis = -1,
                       lumis_per_job = 500,
                       skip_common = True,
                       )
    cs.submit_all(Samples.data_samples_orig)
