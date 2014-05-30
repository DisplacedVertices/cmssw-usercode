import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
process.setName_('Mini')
del process.TFileService

import JMTucker.Tools.Samples as Samples
s = Samples.qcdht1000

from JMTucker.Tools import SampleFiles
SampleFiles.setup(process, 'MFVNtupleV18', s.name, 50000)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.mfvAnalysisCuts.min_nvertex = 1

process.mfvSampleInfo = cms.EDProducer('SampleInfoProducer',
                                       sample = cms.string(s.name),
                                       numEvents = cms.int32(s.nevents),
                                       crossSection = cms.double(s.cross_section),
                                       intLumi = cms.double(20000),
                                       )

process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvAnalysisCuts * process.mfvSampleInfo)

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('minintuple.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep MFVEvent_mfvEvent__*',
                                   'keep MFVVertexAuxs_mfvSelectedVerticesMedium__*',
                                   'keep *_mfvSampleInfo_*_*',
                                   )
                               )
process.outp = cms.EndPath(process.out)

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.inputCommands = cms.untracked.vstring('keep *', 'drop *_MEtoEDMConverter_*_*')
process.out.outputCommands += ['drop LumiDetails_lumiProducer_*_*', 'drop LumiSummary_lumiProducer_*_*', 'drop RunSummary_lumiProducer_*_*']
process.out.dropMetaData = cms.untracked.string('ALL')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
                                 Samples.mfv_neutralino_tau1000um_M0400,
                                 Samples.mfv_neutralino_tau0300um_M0400,
                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples)

    def modify(sample):
        to_add = []
        to_replace = []

        to_add.append('''
process.mfvSampleInfo.sample = %(name)s
process.mfvSampleInfo.numEvents = %(nevents)i
process.mfvSampleInfo.crossSection = %(cross_section)g
''' % sample)

        return to_add, to_replace

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MiniNtupleV18',
                       pset_modifier = modify,
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       get_edm_output = True,
                       data_retrieval = 'fnal',
                       )
    cs.submit_all(samples)
