import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV13', 'mfv_neutralino_tau1000um_M0400', 500)
process.TFileService.fileName = 'cutplay.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
vtx_sel = process.mfvSelectedVerticesTight.clone(min_ntracks = 5,
                                                 min_maxtrackpt = 0)

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

for i in xrange(0,20):
    changes.append(('ntracksptgt3X%i'%i, 'min_ntracksptgt3 = %i'%i, ''))

for i in xrange(0,10):
    changes.append(('njetsntksX%i'%i, 'min_njetsntks = %i'%i, ''))

for i in xrange(0,100,2):
    changes.append(('tkonlyptX%i'%i, 'min_tkonlypt = %i'%i, ''))

for i in xrange(0,100,2):
    changes.append(('tkonlymassX%i'%i, 'min_tkonlymass = %i'%i, ''))

for i in xrange(0,100,5):
    changes.append(('jetsntkptX%i'%i, 'min_jetsntkpt = %i'%i, ''))

for i in xrange(0,100,5):
    changes.append(('jetsntkmassX%i'%i, 'min_jetsntkmass = %i'%i, ''))

for i in xrange(0,100,5):
    changes.append(('tksjetsntkptX%i'%i, 'min_tksjetsntkpt = %i'%i, ''))

for i in xrange(0,100,5):
    changes.append(('tksjetsntkmassX%i'%i, 'min_tksjetsntkmass = %i'%i, ''))

for i in xrange(-50,50):
    changes.append(('costhtkonlymombsX%s'%pize(0.02*i,2), 'min_costhtkonlymombs = %f'%(0.02*i), ''))

for i in xrange(-50,50):
    changes.append(('costhjetsntkmombsX%s'%pize(0.02*i,2), 'min_costhjetsntkmombs = %f'%(0.02*i), ''))

for i in xrange(-50,50):
    changes.append(('costhtksjetsntkmombsX%s'%pize(0.02*i,2), 'min_costhtksjetsntkmombs = %f'%(0.02*i), ''))

for i in xrange(0,30):
    changes.append(('missdisttksjetsntkpvsigX%i'%i, 'min_missdisttksjetsntkpvsig = %i'%i, ''))

for i in xrange(0,200,5):
    changes.append(('sumpt2X%i'%i, 'min_sumpt2 = %i'%i, ''))

for i in xrange(0,30):
    changes.append(('maxtrackptX%i'%i, 'min_maxtrackpt = %i'%i, ''))

for i in xrange(0,100):
    changes.append(('drminX%s'%pize(0.01*i,2), 'max_drmin = %f'%(0.01*i), ''))

for i in xrange(0,28):
    changes.append(('drmaxX%s'%pize(0.25*i,2), 'max_drmax = %f'%(0.25*i), ''))

for i in xrange(0,50):
    changes.append(('bs2derrX%s'%pize(0.0005*i,4), 'max_bs2derr = %f'%(0.0005*i), ''))

for i in xrange(0,30):
    changes.append(('bs2dsigX%s'%pize(0.5*i,1), 'min_bs2dsig = %f'%(0.5*i), ''))

for i in xrange(0,1000,50):
    changes.append(('sumhtX%i'%i, '', 'min_sumht = %i'%i))

for i in xrange(0,3):
    changes.append(('nsemilepmuonsX%i'%i, '', 'min_nsemilepmuons = %i'%i))

for i in xrange(0,3):
    changes.append(('nleptonsX%i'%i, '', 'min_nleptons = %i'%i))

for i in xrange(0,3):
    changes.append(('nsemileptonsX%i'%i, '', 'min_nsemileptons = %i'%i))

for i in xrange(0,80):
    changes.append(('ntracks01X%i'%i, '', 'min_ntracks01 = %i'%i))

for i in xrange(0,60):
    changes.append(('maxtrackpt01X%i'%i, '', 'min_maxtrackpt01 = %i'%i))

for i in xrange(0,20):
    changes.append(('njetsntks01X%i'%i, '', 'min_njetsntks01 = %i'%i))

for i in xrange(0,200,4):
    changes.append(('tkonlymass01X%i'%i, '', 'min_tkonlymass01 = %i'%i))

for i in xrange(0,200,10):
    changes.append(('jetsntkmass01X%i'%i, '', 'min_jetsntkmass01 = %i'%i))

for i in xrange(0,200,10):
    changes.append(('tksjetsntkmass01X%i'%i, '', 'min_tksjetsntkmass01 = %i'%i))

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
    bkg_samples = ttbar_samples + qcd_samples + leptonic_background_samples
    samples = [mfv_neutralino_tau0100um_M0200, mfv_neutralino_tau0100um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400] + bkg_samples
    for sample in bkg_samples:
        sample.total_events = sample.nevents_orig/2

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles
    
    cs = CRABSubmitter('CutPlayV13',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles['MFVNtupleV13'],
                       )
    cs.submit_all(samples)

