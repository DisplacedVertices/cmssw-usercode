import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.fileNames = ['/store/user/tucker/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/mfvntuple_v18/c761ddfa7f093d8f86a338439e06a1d4/ntuple_1_1_URD.root']
process.source.noEventSort = cms.untracked.bool(True)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
process.TFileService.fileName = 'minitree.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCuts.min_nvertex = 1

process.mfvMiniTree = cms.EDAnalyzer('MFVMiniTreer',
                                     event_src = cms.InputTag('mfvEvent'),
                                     force_bs = cms.vdouble(),
                                     vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                     )

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.mfvMiniTree)
        
if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv(Samples.mfv_signal_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples)

    for s in Samples.data_samples:
        s.json = 'ana_all.json'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MiniTreeV18_Njets',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       run_half_mc = True,
                       )
    cs.submit_all(samples)
