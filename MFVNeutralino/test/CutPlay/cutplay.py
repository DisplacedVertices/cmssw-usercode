import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

use_weights = True
do_nominal = True
do_distances = False

process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20/aaaa7d7d2dcfa08aa71c1469df6ebf05/ntuple_1_1_NQ9.root']
process.TFileService.fileName = 'cutplay.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
vtx_sel = process.mfvSelectedVerticesTight
ana_sel = process.mfvAnalysisCuts

def pize(f,sz):
    fmt = '%.' + str(sz) + 'f'
    return (fmt % f).replace('.','p').replace('-','n')

changes = []
changes.append(('nm1', '', ''))

if do_nominal:
    for i in xrange(40, 200, 5):
        changes.append(('calojetpt4X%i' % i, '', 'min_4th_calojet_pt = %i' % i))
    for i in xrange(250,1001,50):
        changes.append(('sumhtX%i'%i, '', 'min_sumht = %i'%i))
    for i in xrange(0,15):
        changes.append(('ntracksX%i'%i, 'min_ntracks = %i, min_njetsntks = 0'%i, ''))
    for i in xrange(0,10):
        changes.append(('ntracksptgt3X%i'%i, 'min_ntracksptgt3 = %i'%i, ''))
    for i in xrange(0,6):
        changes.append(('njetsntksX%i'%i, 'min_njetsntks = %i'%i, ''))
    for i in xrange(0,20):
        changes.append(('drminX%s'%pize(0.05*i,2), 'max_drmin = %f'%(0.05*i), ''))
    for i in xrange(0,20):
        changes.append(('mindrmaxX%s'%pize(0.1*i,1), 'min_drmax = %f'%(0.1*i),''))
    for i in xrange(4,28):
        changes.append(('maxdrmaxX%s'%pize(0.25*i,2), 'max_drmax = %f'%(0.25*i), ''))
    for i in xrange(15,41):
        changes.append(('geo2ddistX%s'%pize(0.1*i,1), 'max_geo2ddist = %f'%(0.1*i), ''))
    for i in xrange(0,50):
        changes.append(('bs2derrX%s'%pize(0.0005*i,4), 'max_bs2derr = %f'%(0.0005*i), ''))

if do_distances:
    for i in xrange(20):
        changes.append(('bs2ddist01X%s'%pize(0.005*i,3), '', 'min_bs2ddist01 = %f'%(0.005*i)))
    for i in xrange(20):
        changes.append(('pv2ddist01X%s'%pize(0.005*i,3), '', 'min_pv2ddist01 = %f'%(0.005*i)))
    for i in xrange(20):
        changes.append(('pv3ddist01X%s'%pize(0.005*i,3), '', 'min_pv3ddist01 = %f'%(0.005*i)))
    for i in xrange(20):
        changes.append(('svdist2dX%s'%pize(0.005*i,3), '', 'min_svdist2d = %f'%(0.005*i)))
    for i in xrange(20):
        changes.append(('svdist3dX%s'%pize(0.005*i,3), '', 'min_svdist3d = %f'%(0.005*i)))
    for i in xrange(20):
        changes.append(('bs2dsig01X%s'%pize(1.5*i,1), '', 'min_bs2dsig01 = %f'%(1.5*i)))
    for i in xrange(20):
        changes.append(('pv2dsig01X%s'%pize(1.5*i,1), '', 'min_pv2dsig01 = %f'%(1.5*i)))
    for i in xrange(20):
        changes.append(('pv3dsig01X%s'%pize(1.5*i,1), '', 'min_pv3dsig01 = %f'%(1.5*i)))

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


if use_weights:
    process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process, weight_src='mfvWeight' if use_weights else '')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
                                 Samples.mfv_neutralino_tau1000um_M0400,
                                 Samples.mfv_neutralino_tau0300um_M0400,
                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('CutPlayV20',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all(samples)
