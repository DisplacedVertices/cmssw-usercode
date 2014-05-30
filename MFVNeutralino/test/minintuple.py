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
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

process.mfvAnalysisCuts.min_nvertex = 1
process.mfvAnalysisCuts.vertex_src = 'mfvSelectedVerticesMedium'
process.mfvWeight.histos = cms.untracked.bool(False)

process.mfvSampleInfo = cms.EDProducer('SampleInfoProducer',
                                       extra_weight_src = cms.InputTag('mfvWeight'),
                                       sample = cms.string(s.name),
                                       num_events = cms.int32(s.nevents),
                                       cross_section = cms.double(s.cross_section),
                                       int_lumi = cms.double(20000),
                                       )

process.p = cms.Path(process.mfvSelectedVerticesMedium * process.mfvAnalysisCuts * process.mfvWeight * process.mfvSampleInfo)

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

    run_half = True

    def modify(sample):
        to_add = []
        to_replace = []

        to_add.append('''
process.mfvSampleInfo.sample = '%s'
process.mfvSampleInfo.num_events = %s
process.mfvSampleInfo.cross_section = %g
''' % (sample.name,
       'int(%i*0.5)' % sample.nevents if (run_half and sample in Samples.ttbar_samples + Samples.qcd_samples) else sample.nevents,
       sample.cross_section)
                      )

        return to_add, to_replace

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MiniNtupleV18',
                       use_ana_dataset = True,
                       pset_modifier = modify,
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       get_edm_output = True,
                       data_retrieval = 'fnal',
                       publish_data_name = 'mfvminintuple_v18',
                       run_half_mc = run_half,
                       )
    cs.submit_all(samples)
