import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.CMSSWTools import glob_store

#process.maxEvents.input = 1000
process.options.wantSummary = True
process.TFileService.fileName = 'cutplay.root'
process.source.fileNames = glob_store('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v8/99d7a676d206adfebd5d154091ebe5a6/*')

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

vtx_sel = process.mfvSelectedVerticesTight
ana_sel = process.mfvAnalysisCuts

process.All = cms.Path(vtx_sel * ana_sel)

changes = [
    ('NoMinNtracks',    'min_ntracks = 0', ''),
    ('RelaxMinNtracks', 'min_ntracks = 4', ''),
    ('NoMinMaxtrackpt',    'min_maxtrackpt = 0', ''),
    ('RelaxMinMaxtrackpt', 'min_maxtrackpt = 5', ''),
    ('NoMaxDrmin', 'max_drmin = 1e9', ''),
    ('NoMaxDrmax', 'max_drmin = 1e9', ''),
    ]

for name, vtx_change, ana_change in changes:
    vtx_name = 'Sel' + name
    ana_name = 'Ana' + name
    path_name = name

    vtx_obj = eval('vtx_sel.clone(%s)' % vtx_change)
    ana_obj = eval('ana_sel.clone(%s)' % ana_change)

    ana_obj.vertex_src = vtx_name

    setattr(process, vtx_name, vtx_obj)
    setattr(process, ana_name, ana_obj)

    setattr(process, path_name, cms.Path(vtx_obj * ana_obj))



process.effs = cms.EDAnalyzer('SimpleTriggerEfficiency',
                              trigger_results_src = cms.InputTag('TriggerResults', '', process.name_()),
                              )
process.p = cms.EndPath(process.effs)
