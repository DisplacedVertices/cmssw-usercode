from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
process.setName_('duh')

process.source.fileNames = ['file:ntuple.root']
process.TFileService.fileName = 'ntuple_histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.mfvSelectedVerticesTight.vertex_aux_src = 'mfvVerticesAux'

process.load('JMTucker.MFVNeutralino.Histos_cff')
process.mfvVertexHistos        .use_ref = False
process.mfvVertexHistosNoCuts  .use_ref = False
process.mfvVertexHistosWAnaCuts.use_ref = False

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvHistos)
