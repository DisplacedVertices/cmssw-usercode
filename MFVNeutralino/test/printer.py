import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, geometry_etc
from JMTucker.Tools import SampleFiles

#SampleFiles.setup(process, 'MFVNtupleV13', 'mfv_neutralino_tau1000um_M0400', 10)
process.source.fileNames = ['file:ntuple.root']
#process.source.noEventSort = cms.untracked.bool(False)

geometry_etc(process, 'START53_V27::All')
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

process.printRecoVertices = printer.clone(print_vertex = True)
process.printRecoVerticesTight = printer.clone(print_vertex = True, vertex_src = 'mfvSelectedVerticesTight')
process.printEventAll = printer.clone(print_event = True)
process.printEventSel = printer.clone(print_event = True)
process.printVertexAll = printer.clone(print_vertex_aux = True)
process.printVertexSel = printer.clone(print_vertex_aux = True, vertex_aux_src = 'mfvSelectedVerticesTight')
process.printVertexSelEvtSel = printer.clone(print_vertex_aux = True, vertex_aux_src = 'mfvSelectedVerticesTight')

process.p = cms.Path(process.printRecoVerticesTight * process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.printEventSel * process.printVertexSelEvtSel)

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
