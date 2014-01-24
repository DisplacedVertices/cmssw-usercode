import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV13', 'mfv_neutralino_tau0100um_M0400', 500)
process.TFileService.fileName = 'cutplay.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
vtx_sel = process.mfvSelectedVerticesTight.clone(min_ntracks = 5,
                                                 min_maxtrackpt = 0,
                                                 min_njetsntks = 1,
                                                 max_bs2derr = 1e9)

process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
ana_sel = process.mfvAnalysisCuts.clone(min_ntracks01 = 0,
                                        min_maxtrackpt01 = 0,
                                        min_sumht = 500)

def pize(f,sz):
    fmt = '%.' + str(sz) + 'f'
    return (fmt % f).replace('.','p').replace('-','n')

changes = []
changes.append(('nm1', '', ''))

#A region: max_ntracks01 = 12, max_maxtrackpt01 = 30
for i in xrange(0,2):
    for j in xrange(5,11):
        for k in xrange(0,9):
            changes.append(('A%intracks%ibs2ddistX%s'%(i,j,pize(0.005*k,3)), 'min_ntracks = %i, min_bs2ddist = %f'%(j,(0.005*k)), 'max_ntracks01 = 12, max_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

    for j in xrange(5,11):
        for k in xrange(0,10):
            changes.append(('A%intracks%ibs2derrX%s'%(i,j,pize(0.005*k,3)), 'min_ntracks = %i, max_bs2derr = %f'%(j,(0.005*k)), 'max_ntracks01 = 12, max_maxtrackpt01 = 30, min_nsemileptons = %i'%i))
        changes.append(('A%intracksX%i'%(i,j), 'min_ntracks = %i'%j, 'max_ntracks01 = 12, max_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

    for j in xrange(5,11):
        for k in xrange(0,11):
            changes.append(('A%intracks%ibs2dsigX%i'%(i,j,k), 'min_ntracks = %i, min_bs2dsig = %f'%(j,k), 'max_ntracks01 = 12, max_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

#B region: min_ntracks01 = 13, max_maxtrackpt01 = 30
for i in xrange(0,2):
    for j in xrange(5,11):
        for k in xrange(0,9):
            changes.append(('B%intracks%ibs2ddistX%s'%(i,j,pize(0.005*k,3)), 'min_ntracks = %i, min_bs2ddist = %f'%(j,(0.005*k)), 'min_ntracks01 = 13, max_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

    for j in xrange(5,11):
        for k in xrange(0,10):
            changes.append(('B%intracks%ibs2derrX%s'%(i,j,pize(0.005*k,3)), 'min_ntracks = %i, max_bs2derr = %f'%(j,(0.005*k)), 'min_ntracks01 = 13, max_maxtrackpt01 = 30, min_nsemileptons = %i'%i))
        changes.append(('B%intracksX%i'%(i,j), 'min_ntracks = %i'%j, 'min_ntracks01 = 13, max_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

    for j in xrange(5,11):
        for k in xrange(0,11):
            changes.append(('B%intracks%ibs2dsigX%i'%(i,j,k), 'min_ntracks = %i, min_bs2dsig = %f'%(j,k), 'min_ntracks01 = 13, max_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

#C region: max_ntracks01 = 12, min_maxtrackpt01 = 30
for i in xrange(0,2):
    for j in xrange(5,11):
        for k in xrange(0,9):
            changes.append(('C%intracks%ibs2ddistX%s'%(i,j,pize(0.005*k,3)), 'min_ntracks = %i, min_bs2ddist = %f'%(j,(0.005*k)), 'max_ntracks01 = 12, min_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

    for j in xrange(5,11):
        for k in xrange(0,10):
            changes.append(('C%intracks%ibs2derrX%s'%(i,j,pize(0.005*k,3)), 'min_ntracks = %i, max_bs2derr = %f'%(j,(0.005*k)), 'max_ntracks01 = 12, min_maxtrackpt01 = 30, min_nsemileptons = %i'%i))
        changes.append(('C%intracksX%i'%(i,j), 'min_ntracks = %i'%j, 'max_ntracks01 = 12, min_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

    for j in xrange(5,11):
        for k in xrange(0,11):
            changes.append(('C%intracks%ibs2dsigX%i'%(i,j,k), 'min_ntracks = %i, min_bs2dsig = %f'%(j,k), 'max_ntracks01 = 12, min_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

#D region: min_ntracks01 = 13, min_maxtrackpt01 = 30
for i in xrange(0,2):
    for j in xrange(5,11):
        for k in xrange(0,9):
            changes.append(('D%intracks%ibs2ddistX%s'%(i,j,pize(0.005*k,3)), 'min_ntracks = %i, min_bs2ddist = %f'%(j,(0.005*k)), 'min_ntracks01 = 13, min_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

    for j in xrange(5,11):
        for k in xrange(0,10):
            changes.append(('D%intracks%ibs2derrX%s'%(i,j,pize(0.005*k,3)), 'min_ntracks = %i, max_bs2derr = %f'%(j,(0.005*k)), 'min_ntracks01 = 13, min_maxtrackpt01 = 30, min_nsemileptons = %i'%i))
        changes.append(('D%intracksX%i'%(i,j), 'min_ntracks = %i'%j, 'min_ntracks01 = 13, min_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

    for j in xrange(5,11):
        for k in xrange(0,11):
            changes.append(('D%intracks%ibs2dsigX%i'%(i,j,k), 'min_ntracks = %i, min_bs2dsig = %f'%(j,k), 'min_ntracks01 = 13, min_maxtrackpt01 = 30, min_nsemileptons = %i'%i))

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
    bkg_samples = ttbar_samples + qcd_samples
    samples = [mfv_neutralino_tau0100um_M0200, mfv_neutralino_tau0100um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400] + bkg_samples
    for sample in bkg_samples:
        sample.total_events = sample.nevents_orig/2

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles
    
    cs = CRABSubmitter('CutPlay2dV13',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles['MFVNtupleV13'],
                       )
    cs.submit_all(samples)

