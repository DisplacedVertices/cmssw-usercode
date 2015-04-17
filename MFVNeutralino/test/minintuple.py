import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
process.setName_('Mini')
del process.TFileService

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

process.mfvAnalysisCuts.min_nvertex = 1
process.mfvWeight.histos = cms.untracked.bool(False)

import JMTucker.MFVNeutralino.AnalysisConstants as ac

process.mfvSampleInfo = cms.EDProducer('SampleInfoProducer',
                                       extra_weight_src = cms.InputTag('mfvWeight'),
                                       sample = cms.string('none'),
                                       num_events = cms.int32(-1),
                                       cross_section = cms.double(-1),
                                       int_lumi = cms.double(ac.int_lumi * ac.scale_factor),
                                       )

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.mfvWeight * process.mfvSampleInfo)

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('minintuple.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep MFVEvent_mfvEvent__*',
                                   'keep MFVVertexAuxs_mfvSelectedVerticesTight__*',
                                   'keep *_mfvSampleInfo_*_*',
                                   )
                               )
process.outp = cms.EndPath(process.out)

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.inputCommands = cms.untracked.vstring('keep *', 'drop *_MEtoEDMConverter_*_*')
process.out.outputCommands += ['drop LumiDetails_lumiProducer_*_*', 'drop LumiSummary_lumiProducer_*_*', 'drop RunSummary_lumiProducer_*_*']
process.out.dropMetaData = cms.untracked.string('ALL')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
                                 Samples.mfv_neutralino_tau1000um_M0400,
                                 Samples.mfv_neutralino_tau0300um_M0400,
                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples)

    for s in Samples.data_samples:
        s.json = 'ana_all.json'

    def modify(sample):
        to_add = []
        to_replace = []

        if sample.is_mc:
            to_add.append('''
process.mfvSampleInfo.sample = '%s'
process.mfvSampleInfo.num_events = %s
process.mfvSampleInfo.cross_section = %g
''' % (sample.name,
       sample.nevents,
       sample.cross_section)
                          )

        return to_add, to_replace

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MiniNtupleV20',
                       use_ana_dataset = True,
                       pset_modifier = modify,
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       get_edm_output = True,
                       data_retrieval = 'fnal',
                       publish_data_name = 'mfvminintuple_v20',
                       )
    cs.submit_all(samples)
