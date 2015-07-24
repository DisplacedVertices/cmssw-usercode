from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['file:gensimhlt.root']
process.TFileService.fileName = 'gencheck.root'

process.genCheck = cms.EDAnalyzer('MFVGenCheck',
                                  gen_src = cms.InputTag('genParticles'),
                                  lsp_id = cms.int32(1000021),
                                  allowed_dau_ids = cms.PSet(
                                      dummy = cms.vint32(1,-1),
                                      ),
                                  )

process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                   src = cms.InputTag('genParticles'),
                                   printVertex = cms.untracked.bool(True),
                                   )

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')

process.p = cms.Path(process.genCheck * process.printList)
process.p = cms.Path(process.genCheck)
