from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV15', 'mfv_neutralino_tau1000um_M0400', 10)
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
