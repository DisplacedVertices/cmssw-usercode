import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

use_weights = True
do_nominal = True
do_distances = False

process.source.fileNames = ['/store/user/jchu/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ntuplev7/160209_224719/0000/ntuple_1.root']
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
    for i in xrange(0,10):
        changes.append(('njetsX%i'%i, '', 'min_njets = %i'%i))
    for i in xrange(250,1001,50):
        changes.append(('htX%i'%i, '', 'min_ht = %i'%i))
    for i in xrange(0,15):
        changes.append(('ntracksX%i'%i, 'min_ntracks = %i, min_njetsntks = 0'%i, ''))
    for i in xrange(0,10):
        changes.append(('ntracksptgt3X%i'%i, 'min_ntracksptgt3 = %i'%i, ''))
    for i in xrange(0,6):
        changes.append(('njetsntksX%i'%i, 'min_njetsntks = %i'%i, ''))
    for i in xrange(0,20):
        changes.append(('mintrackpairdphimaxX%s'%pize(0.1*i,1), 'min_trackpairdphimax = %f'%(0.1*i), ''))
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
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    samples = Samples.registry.from_argv(
        Samples.data_samples + \
        Samples.ttbar_samples + Samples.qcd_samples + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        Samples.xx4j_samples
        )

    for sample in samples:
        if sample.is_mc:
            sample.events_per = 250000
        else:
            sample.json = 'ana_10pc.json'
            sample.lumis_per = 200

    cs = CRABSubmitter('CutPlayV7',
                       dataset = 'ntuplev7',
                       job_control_from_sample = True,
                       aaa = True, # stored at FNAL, easy to run on T2_USes
                       )
    cs.submit_all(Samples.ttbar_samples + Samples.qcd_samples + [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + Samples.xx4j_samples)
