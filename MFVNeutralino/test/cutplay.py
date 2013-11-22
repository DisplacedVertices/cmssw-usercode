import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.CMSSWTools import glob_store

process.TFileService.fileName = 'cutplay.root'
process.source.fileNames = glob_store('/store/user/tucker/mfv_neutralino_tau0100um_M0400/mfvntuple_v10/5c05eb42bbf1b04cf0f00b96bae48439/*')

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
vtx_sel = process.mfvSelectedVerticesTight.clone(min_ntracks = 7,
                                                 min_maxtrackpt = 5)

process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
ana_sel = process.mfvAnalysisCuts.clone(min_ntracks01 = 0,
                                        min_maxtrackpt01 = 0)

def pize(f,sz):
    fmt = '%.' + str(sz) + 'f'
    return (fmt % f).replace('.','p').replace('-','n')

changes = []
changes.append(('nm1', '', ''))

for i in xrange(0,40):
    changes.append(('ntracksX%i'%i, 'min_ntracks = %i'%i, ''))

for i in xrange(0,10):
    changes.append(('njetssharetksX%i'%i, 'min_njetssharetks = %i'%i, ''))

for i in xrange(0,100):
    changes.append(('drminX%s'%pize(0.01*i,2), 'max_drmin = %f'%(0.01*i), ''))

for i in xrange(0,28):
    changes.append(('drmaxX%s'%pize(0.25*i,2), 'max_drmax = %f'%(0.25*i), ''))

for i in xrange(0,30):
    changes.append(('bs2dsigX%s'%pize(0.5*i,1), 'min_bs2dsig = %f'%(0.5*i), ''))

for i in xrange(0,30):
    changes.append(('maxtrackptX%i'%i, 'min_maxtrackpt = %i'%i, ''))

for i in xrange(0,80):
    changes.append(('ntracks01X%i'%i, '', 'min_ntracks01 = %i'%i))

for i in xrange(0,20):
    changes.append(('njetssharetks01X%i'%i, '', 'min_njetssharetks01 = %i'%i))

for i in xrange(0,60):
    changes.append(('maxtrackpt01X%i'%i, '', 'min_maxtrackpt01 = %i'%i))

for i in xrange(-50,50):
    changes.append(('costhmombsX%s'%pize(0.02*i,2), 'min_costhmombs = %f'%(0.02*i), ''))

for i in xrange(0,100,2):
    changes.append(('massX%i'%i, 'min_mass = %i'%i, ''))

for i in xrange(0,100,5):
    changes.append(('jetsmassntksX%i'%i, 'min_jetsmassntks = %i'%i, ''))

for i in xrange(0,200,4):
    changes.append(('mass01X%i'%i, '', 'min_mass01 = %i'%i))

for i in xrange(0,200,10):
    changes.append(('jetsmassntks01X%i'%i, '', 'min_jetsmassntks01 = %i'%i))

for i in xrange(0,100,2):
    changes.append(('ptX%i'%i, 'min_pt = %i'%i, ''))

for i in xrange(0,20):
    changes.append(('ntracksptgt3X%i'%i, 'min_ntracksptgt3 = %i'%i, ''))

for i in xrange(0,200,5):
    changes.append(('sumpt2X%i'%i, 'min_sumpt2 = %i'%i, ''))

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
    from JMTucker.Tools.Samples import mfv_neutralino_tau0100um_M0400, mfv_neutralino_tau1000um_M0400, ttbar_samples, qcd_samples
    for sample in ttbar_samples + qcd_samples:
        sample.total_events = {'ttbarhadronic': 5268722,
                               'ttbarsemilep':  12674909,
                               'ttbardilep':    6059506,
                               'qcdht0100':     25064759,
                               'qcdht0250':     13531039,
                               'qcdht0500':     15274646,
                               'qcdht1000':     6034431}[sample.name]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('CutPlay2',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    samples = [mfv_neutralino_tau0100um_M0400, mfv_neutralino_tau1000um_M0400] + ttbar_samples + qcd_samples
    cs.submit_all(samples)

