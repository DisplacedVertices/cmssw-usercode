import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.fileNames = ['file:ttbarhadronic.root']
process.source.noEventSort = cms.untracked.bool(True)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
process.TFileService.fileName = 'one2two.root'
report_every(100)

add_analyzer('MFVOne2Two',
             filename = cms.string(''),
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

argv_ok = False
for arg in sys.argv:
    if os.path.isfile(arg):
        if arg.endswith('.vertices'):
            process.source = cms.Source('EmptySource')
            process.maxEvents.input = 0
            process.MFVOne2Two.filename = arg
            process.TFileService.fileName = arg.replace('.vertices', '_histos.root')
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
    fn = {
        'qcdht0250': '/store/user/tucker/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/mfvminintuple_v18/59dbce4c4744ce2cb534302fb0e499de/merged.root',
        'qcdht0500': '/store/user/tucker/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/mfvminintuple_v18/ba03008a9ad7512ae49ff8fbd40bf0d3/merged.root',
        'qcdht1000': '/store/user/tucker/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/mfvminintuple_v18/ab2723f55b544e44b6f7c283e78a4fd3/merged.root',
        'ttbardilep': '/store/user/tucker/TTJets_FullLeptMGDecays_8TeV-madgraph/mfvminintuple_v18/79f73fd0971c6914ff132951d86b1e20/merged.root',
        'ttbarhadronic': '/store/user/tucker/TTJets_HadronicMGDecays_8TeV-madgraph/mfvminintuple_v18/d59b961e9ce571db158eb644bd3fcd7e/merged.root',
        'ttbarsemilep': '/store/user/tucker/TTJets_SemiLeptMGDecays_8TeV-madgraph/mfvminintuple_v18/3b2cc1ecca69c57de3286e3135a6660c/merged.root',
        }[sys.argv[-1]]
    process.source.fileNames = [fn]
    print 'running 1st step with', fn
