import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.fileNames = ['/store/user/tucker/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/mfvntuple_v18/c761ddfa7f093d8f86a338439e06a1d4/ntuple_1_1_URD.root']
process.source.noEventSort = cms.untracked.bool(True)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
process.TFileService.fileName = 'one2two.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCuts.min_nvertex = 1

process.mfvOne2Two = cms.EDAnalyzer('MFVOne2Two',
                                    filename = cms.string(''),
                                    tree_path = cms.string('mfvOne2Two/t'),
                                    event_src = cms.InputTag('mfvEvent'),
                                    vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                    wrep = cms.bool(True),
                                    npairs = cms.int32(-1),
                                    min_ntracks = cms.int32(5),
                                    min_ntracks_aft = cms.int32(5),
                                    use_f_dz = cms.bool(False),
                                    max_1v_dz = cms.double(0.025),
                                    max_1v_ntracks = cms.int32(1000000)
                                    )

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.mfvOne2Two)


for arg in sys.argv:
    if os.path.isfile(arg) and arg.endswith('.root'):
        process.source = cms.Source('EmptySource')
        process.maxEvents.input = 0
        process.mfvOne2Two.filename = arg
        process.TFileService.fileName = os.path.basename(arg).replace('.root', '_histos.root')

        for i in (6,7,8):
            o = process.mfvOne2Two.clone(min_ntracks_aft = i)
            setattr(process, 'mfvOne2TwoNtracks%i' % i, o)
            process.p *= o

        print 'running 2nd step with', arg
        break
        
if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
                                 Samples.mfv_neutralino_tau1000um_M0400,
                                 Samples.mfv_neutralino_tau0300um_M0400,
                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('One2Two',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       run_half_mc = True,
                       )
    cs.submit_all(samples)
