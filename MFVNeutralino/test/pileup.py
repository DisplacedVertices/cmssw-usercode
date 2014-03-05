import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.set(process, 'MFVNtupleV11', 'mfv_neutralino_tau0100um_M0400', 100000)
process.TFileService.fileName = 'pileup.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
vtx_sel = process.mfvSelectedVerticesTight

process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
ana_sel = process.mfvAnalysisCuts

def pize(f,sz):
    fmt = '%.' + str(sz) + 'f'
    return (fmt % f).replace('.','p').replace('-','n')

changes = []
changes.append(('nm1', '', ''))

changes.append(('tightX3', '', 'max_npv = 5'))
changes.append(('ABCDX3', 'min_ntracks = 5, min_maxtrackpt = 0', 'min_ntracks01 = 0, min_maxtrackpt01 = 0, max_npv = 5'))
changes.append(('triggerX3', '', 'apply_vertex_cuts = False, max_npv = 5'))
changes.append(('nocutsX3', '', 'trigger_bit = -1, min_4th_jet_pt = 0, min_njets = 0, apply_vertex_cuts = False, max_npv = 5'))

for i in xrange(6,30,3):
    changes.append(('tightX%i'%i, '', 'min_npv = %i, max_npv = %i+2'%(i,i)))
    changes.append(('ABCDX%i'%i, 'min_ntracks = 5, min_maxtrackpt = 0', 'min_ntracks01 = 0, min_maxtrackpt01 = 0, min_npv = %i, max_npv = %i+2'%(i,i)))
    changes.append(('triggerX%i'%i, '', 'apply_vertex_cuts = False, min_npv = %i, max_npv = %i+2'%(i,i)))
    changes.append(('nocutsX%i'%i, '', 'trigger_bit = -1, min_4th_jet_pt = 0, min_njets = 0, apply_vertex_cuts = False, min_npv = %i, max_npv = %i+2'%(i,i)))

changes.append(('tightX30', '', 'min_npv = 30'))
changes.append(('ABCDX30', 'min_ntracks = 5, min_maxtrackpt = 0', 'min_ntracks01 = 0, min_maxtrackpt01 = 0, min_npv = 30'))
changes.append(('triggerX30', '', 'apply_vertex_cuts = False, min_npv = 30'))
changes.append(('nocutsX30', '', 'trigger_bit = -1, min_4th_jet_pt = 0, min_njets = 0, apply_vertex_cuts = False, min_npv = 30'))

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


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import *
    samples = [mfv_neutralino_tau0100um_M0400, mfv_neutralino_tau1000um_M0400] + ttbar_samples + qcd_samples
    for sample in ttbar_samples + qcd_samples:
        sample.total_events = sample.nevents_orig/2

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles
    
    cs = CRABSubmitter('PileupV11',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles['MFVNtupleV11'],
                       )
    cs.submit_all(samples)

