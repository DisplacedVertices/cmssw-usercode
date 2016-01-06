import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.fileNames = ['/store/user/dquach/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ntuplev3_25ns/151124_021541/0000/ntuple_1.root']
process.source.noEventSort = cms.untracked.bool(True)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
process.TFileService.fileName = 'minitree.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.mfvAnalysisCuts.min_nvertex = 1

process.mfvMiniTree = cms.EDAnalyzer('MFVMiniTreer',
                                     event_src = cms.InputTag('mfvEvent'),
                                     vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                     weight_src = cms.InputTag('mfvWeight'),
                                     )

process.p = cms.Path(process.mfvWeight * process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.mfvMiniTree)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    samples = Samples.ttbar_samples + Samples.qcd_samples[3:]

    cs = CRABSubmitter('MinitreeV4',
                       dataset = 'ntuplev4',
                       splitting = 'FileBased',
                       units_per_job = 5,
                       total_units = -1,
                       aaa = True,
                       )

    cs.submit_all(samples)
