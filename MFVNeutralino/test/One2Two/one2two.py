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


argv_ok = False
for arg in sys.argv:
    if os.path.isfile(arg):
        if arg.endswith('.vertices'):
            process.source = cms.Source('EmptySource')
            process.maxEvents.input = 0
            process.mfvOne2Two.filename = arg
            process.TFileService.fileName = arg.replace('.vertices', '_histos.root')

            for i in (6,7,8):
                o = process.mfvOne2Two.clone(min_ntracks_aft = i)
                setattr(process, 'mfvOne2TwoNtracks%i' % i, o)
                process.p *= o

            print 'running 2nd step with', arg
            argv_ok = True
            break
        elif arg.endswith('.root'):
            if not arg.startswith('/store'):
                arg = 'file:' + arg
            process.source.fileNames = [arg]
            print 'running 1st step with', arg
            argv_ok = True
            break

if not argv_ok:
    try:
        fn = {
            'qcdht0250': '/store/user/tucker/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/mfvminintuple_v18/ba03008a9ad7512ae49ff8fbd40bf0d3/merged.root',
            'qcdht0500': '/store/user/tucker/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/mfvminintuple_v18/ab2723f55b544e44b6f7c283e78a4fd3/merged.root',
            'qcdht1000': '/store/user/tucker/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/mfvminintuple_v18/59dbce4c4744ce2cb534302fb0e499de/merged.root',
            'ttbardilep': '/store/user/tucker/TTJets_FullLeptMGDecays_8TeV-madgraph/mfvminintuple_v18/79f73fd0971c6914ff132951d86b1e20/merged.root',
            'ttbarhadronic': '/store/user/tucker/TTJets_HadronicMGDecays_8TeV-madgraph/mfvminintuple_v18/d59b961e9ce571db158eb644bd3fcd7e/merged.root',
            'ttbarsemilep': '/store/user/tucker/TTJets_SemiLeptMGDecays_8TeV-madgraph/mfvminintuple_v18/3b2cc1ecca69c57de3286e3135a6660c/merged.root',
            }[sys.argv[-1]]
        process.source.fileNames = [fn]
        print 'running 1st step with', fn
    except KeyError:
        pass

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
