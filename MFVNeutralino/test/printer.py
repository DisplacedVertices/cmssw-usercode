import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.MFVNeutralino.Year import year

simple = False

process.source.fileNames = ['file:ntuple.root']
process.source.noEventSort = cms.untracked.bool(True)
file_event_from_argv(process)

geometry_etc(process, which_global_tag(True, year))
del process.TFileService
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

printer = cms.EDAnalyzer('MFVPrinter',
                         print_vertex = cms.bool(False),
                         print_event = cms.bool(False),
                         print_vertex_aux = cms.bool(False),
                         vertex_src = cms.InputTag('mfvVertices'),
                         event_src = cms.InputTag('mfvEvent'),
                         vertex_aux_src = cms.InputTag('mfvVerticesAux'),
                         )

if simple:
    process.justPrint = printer.clone(print_event = True, print_vertex_aux = True, vertex_aux_src = 'mfvSelectedVerticesTight')
    process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvAnalysisCuts * process.justPrint)
else:
    process.printRecoVertices = printer.clone(print_vertex = True)
    process.printRecoVerticesTight = printer.clone(print_vertex = True, vertex_src = 'mfvSelectedVerticesTight')
    process.printEventAll = printer.clone(print_event = True)
    process.printEventSel = printer.clone(print_event = True)
    process.printVertexAll = printer.clone(print_vertex_aux = True)
    process.printVertexSel = printer.clone(print_vertex_aux = True, vertex_aux_src = 'mfvSelectedVerticesTight')
    process.printVertexSelEvtSel = printer.clone(print_vertex_aux = True, vertex_aux_src = 'mfvSelectedVerticesTight')
    process.p = cms.Path(process.printEventAll * process.printVertexAll * process.mfvSelectedVerticesSeq * process.printVertexSel * process.mfvAnalysisCuts * process.printEventSel * process.printVertexSelEvtSel)

if __name__ == '__main__' and 'splitlog' in sys.argv:
    log_fn = sys.argv[sys.argv.index('splitlog')+1]
    buf = []
    rle = None
    dest = '/uscmst1b_scratch/lpc1/3DayLifetime/tucker/splitit_v15'

    def makefn():
        if rle is None:
            return
        d = os.path.join(dest, rle[0], rle[1])
        f = os.path.join(d, rle[2])
        return d,f

    def save():
        d,f = makefn()
        os.system('mkdir -p %s' % d)
        open(f, 'wt').writelines(buf)

    print 'splitting log', log_fn, 'into', dest

    for line in open(log_fn):
        if line.startswith(' printEventAll'):
            if rle is not None:
                save()

            buf = []
            rle = line.split('(')[1].split(')')[0].split(', ')
            print rle
            d,f = makefn()
            if os.path.isfile(f):
                buf = []
                rle = None

        if rle is not None:
            buf.append(line)

    if buf and rle is not None:
        save()

elif __name__ == '__main__' and 'validation' in sys.argv:
    x = {
        'v12': {
            'mfv_ddbar_tau00300um_M0400': (1, ['/store/user/tucker/mfv_ddbar_tau00300um_M0400/NtupleV12_validation_2016_mfv_ddbar_tau00300um_M0400/170412_192453/0000/ntuple_0.root']),
            'mfv_ddbar_tau00300um_M0800': (1, ['/store/user/tucker/mfv_ddbar_tau00300um_M0800/NtupleV12_validation_2016_mfv_ddbar_tau00300um_M0800/170412_192453/0000/ntuple_0.root']),
            'mfv_ddbar_tau01000um_M0400': (1, ['/store/user/tucker/mfv_ddbar_tau01000um_M0400/NtupleV12_validation_2016_mfv_ddbar_tau01000um_M0400/170412_192453/0000/ntuple_0.root']),
            'mfv_ddbar_tau01000um_M0800': (1, ['/store/user/tucker/mfv_ddbar_tau01000um_M0800/NtupleV12_validation_2016_mfv_ddbar_tau01000um_M0800/170412_192453/0000/ntuple_0.root']),
            'mfv_neu_tau00300um_M0800': (1, ['/store/user/tucker/mfv_neu_tau00300um_M0800/NtupleV12_validation_2016_mfv_neu_tau00300um_M0800/170412_192453/0000/ntuple_0.root']),
            'mfv_neu_tau01000um_M0600': (1, ['/store/user/tucker/mfv_neu_tau01000um_M0600/NtupleV12_validation_2016_mfv_neu_tau01000um_M0600/170412_192453/0000/ntuple_0.root']),
            'mfv_neu_tau30000um_M0800': (1, ['/store/user/tucker/mfv_neu_tau30000um_M0800/NtupleV12_validation_2016_mfv_neu_tau30000um_M0800/170412_192453/0000/ntuple_0.root']),
            'qcdht0700': (1, ['/store/user/tucker/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV12_validation_2016_qcdht0700/170412_192453/0000/ntuple_0.root']),
            'qcdht2000': (1, ['/store/user/tucker/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NtupleV12_validation_2016_qcdht2000/170412_192453/0000/ntuple_0.root']),
            'ttbar': (1, ['/store/user/tucker/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/NtupleV12_validation_2016_ttbar/170412_192453/0000/ntuple_0.root']),
            'JetHT2016B3': (1, ['/store/user/tucker/JetHT/NtupleV12_validation_2016_JetHT2016B3/170412_192453/0000/ntuple_0.root']),
            'JetHT2016C': (1, ['/store/user/tucker/JetHT/NtupleV12_validation_2016_JetHT2016C/170412_192453/0000/ntuple_0.root']),
            'JetHT2016D': (1, ['/store/user/tucker/JetHT/NtupleV12_validation_2016_JetHT2016D/170412_192453/0000/ntuple_0.root']),
            'JetHT2016E': (1, ['/store/user/tucker/JetHT/NtupleV12_validation_2016_JetHT2016E/170412_192453/0000/ntuple_0.root']),
            'JetHT2016F': (1, ['/store/user/tucker/JetHT/NtupleV12_validation_2016_JetHT2016F/170412_192453/0000/ntuple_0.root']),
            'JetHT2016G': (1, ['/store/user/tucker/JetHT/NtupleV12_validation_2016_JetHT2016G/170412_192453/0000/ntuple_0.root']),
            'JetHT2016H2': (1, ['/store/user/tucker/JetHT/NtupleV12_validation_2016_JetHT2016H2/170412_192453/0000/ntuple_0.root']),
            },
        'v13': {
            }
        }

    which = sys.argv[1]
    for s, (_, fns) in x[which].iteritems():
        print s
        out_fn = '/uscmst1b_scratch/lpc1/3DayLifetime/%s/%s.%s' % (os.environ['USER'], which, s)
        os.system('cmsRun printer.py %s > %s 2>&1' % (fns[0], out_fn))
        os.system('mlclean.py ' + out_fn)
        assert os.path.isfile(out_fn + '.mlclean')
        os.remove(out_fn)
        print
