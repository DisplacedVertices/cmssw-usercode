import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

#SampleFiles.setup(process, 'MFVNtupleV13', 'mfv_neutralino_tau1000um_M0400', 10)
process.source.fileNames = ['file:selected_v13.root']
process.source.noEventSort = cms.untracked.bool(False)

del process.TFileService
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

printer = cms.EDAnalyzer('MFVPrinter',
                         event_src = cms.InputTag(''),
                         vertex_src = cms.InputTag(''),
                         )

process.printEventAll = printer.clone(event_src = 'mfvEvent')
process.printEventSel = printer.clone(event_src = 'mfvEvent')
process.printVertexAll = printer.clone(vertex_src = 'mfvVerticesAux')
process.printVertexSel = printer.clone(vertex_src = 'mfvSelectedVerticesTight')
process.printVertexSelEvtSel = printer.clone(vertex_src = 'mfvSelectedVerticesTight')

process.p = cms.Path(process.mfvSelectedVerticesTight * process.printEventAll * process.printVertexAll * process.printVertexSel * process.mfvAnalysisCuts * process.printEventSel * process.printVertexSelEvtSel)

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
