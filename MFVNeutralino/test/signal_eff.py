#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
version = 'ULV1Lepm'
#ps = plot_saver(plot_dir('sigeff_%s' % version), size=(600,600), pdf=True, log=False)
#600 500 worked 
ps = plot_saver(plot_dir('nrequest_%s' % version), size=(600,500), pdf=True, log=False)

multijet = Samples.mfv_signal_samples_2017
dijet = Samples.mfv_stopdbardbar_samples_2017

semilep = Samples.mfv_stopld_samples_2018

#for sample in multijet + dijet:
  #  fn = os.path.join('/uscms_data/d2/tucker/crab_dirs/MiniTree%s' % version, sample.name + '.root')
for sample in semilep :
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/MiniTree%s' % version, sample.name + '.root')
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    if sample.name.startswith('mfv_stopld_tau001000um'):
        continue
    f = ROOT.TFile(fn)
    t = f.Get('mfvMiniTreeMinNtk4_loose/t')
    hr = draw_hist_register(t, True)
    cut = 'nvtx>=2' # && svdist > 0.04'
    h = hr.draw('weight', cut, binning='1,0,1', goff=True)
    num, _ = get_integral(h)
    den = Samples.norm_from_file(f)
    sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # ignore integral != entries, just get central value right
    if num != 0 :
        sample.y = 10000/sample.y
        sample.yl = 10000/sample.yl
        sample.yh = 10000/sample.yh
    #make it out of bounds 
    else :
        sample.y =  10000000
        sample.yl = 10000000
        sample.yh = 10000000
    
    #print '%26s: efficiency = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)
    print '%26s: nrequest = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

#per = PerSignal('efficiency', y_range=(0.,0.45))
per = PerSignal('N(to request)', y_range=(0.,1400000))

#per.add(multijet, title='#tilde{N} #rightarrow tbs')
#per.add(dijet, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)
per.add(semilep, title='#tilde{t} #rightarrow ld', color=ROOT.kBlue)
per.draw(canvas=ps.c)
#ps.save('sigeff_1loose')
ps.save('nrequest_loose')
