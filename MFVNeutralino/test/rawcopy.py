#!/usr/bin/env python

import sys
from JMTucker.Tools.Merge_cfg import cms, process
process.out.outputCommands = ['keep *']

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/162F7B5B-579A-E111-8EAD-BCAEC518FF68.root'))

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
process.triggerFilter.andOr = True # = OR
process.ptrig = cms.Path(process.triggerFilter)

process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('ptrig'))

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = [
        Samples.DataSample('MultiJetPk2012B', '/MultiJet1Parked/Run2012B-v1/RAW'),
        Samples.DataSample('MultiJetPk2012C', '/MultiJet1Parked/Run2012C-v1/RAW'),
        Samples.DataSample('MultiJetPk2012D', '/MultiJet1Parked/Run2012D-v1/RAW'),
        ]

    for sample in samples:
        sample.lumis_per = 100

    def modify(sample):
        to_add = []
        to_replace = []

        to_add.append('process.dummyToMakeDiffHash = cms.PSet(sampleName = cms.string("%s"))' % sample.name)

        return to_add, to_replace

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('RawQuadJet50',
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       get_edm_output = True,
                       data_retrieval = 'cornell',
                       max_threads = 1,
                       publish_data_name = 'RawQuadJet50',
                       GRID_data_location_override = 'T2_US',
                       USER_jmt_skip_input_files = 'src/EgammaAnalysis/ElectronTools/data/*,src/CMGTools/External/data/TMVAClassificationCategory_JetID_53X_chs_Dec2012.weights.xml,lib/slc5_amd64_gcc462/libCMGToolsExternal.so',
                       )

    cs.submit_all(samples[:1])
