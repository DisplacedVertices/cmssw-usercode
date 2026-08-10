#!/usr/bin/env python

import os
import numpy as np
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('sigeff_trig'), size=(600,600), log=False, pdf=True)

# where "new" triggers = bjet and displaced dijet triggers
study_new_triggers = True

if study_new_triggers :
    num_file_dir = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_PTV_BjetAgnostic_ToyPunish_Aug1_On'
    den_file_dir = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_PTV_BjetAgnostic_ToyPunish_Aug1_Off'
    trigs = ['Logical OR']
    nice = ['Logical OR']
    colors = [ROOT.kOrange+2]

def sample_ok(s):
    return True #s.mass not in (500,3000)

multijet = [s for s in Samples.mfv_signal_samples_2017 if sample_ok(s)]
dijet_d  = [s for s in Samples.mfv_stopdbardbar_samples_2017 if sample_ok(s)]
dijet_b  = [s for s in Samples.mfv_stopbbarbbar_samples_2017 if sample_ok(s)]
higgs    = [s for s in Samples.HToSSTodddd_samples_2017 if sample_ok(s)]

def getit(fnum, fden, pmpt_var, pt_shift):
    h_nom_num = fnum.Get('evtHstPrompt1p00Pt0p0/h_npu')
    h_nom_den = fden.Get('evtHstPrompt1p00Pt0p0/h_npu')
    n_nom_num = h_nom_num.Integral()
    n_nom_den = h_nom_den.Integral()

    hnum = fnum.Get('evtHstPrompt{}Pt{}/h_npu'.format(pmpt_var, pt_shift))
    hden = fden.Get('evtHstPrompt{}Pt{}/h_npu'.format(pmpt_var, pt_shift))
    nnum = hnum.Integral()
    nden = hden.Integral()

    if nden < 0.1 or n_nom_den < 0.1 or n_nom_num < 0.1:
        return 0.0, 0.0, 0.0, 0.0

    eff     = nnum/nden
    nom_eff = n_nom_num/n_nom_den

    eff_rat = eff/nom_eff
    yld_rat = nnum/n_nom_num
    err = np.sqrt(eff*(1-eff)/nden)
    #return eff, eff-err, min(eff+err, 1.0)

    return eff, err, nnum, nden

for sample in multijet + higgs:
#for sample in multijet + dijet_d + dijet_b + higgs:
    print '\nSample: {} \n------------------------------------------'.format(sample.name)
    fnnum = os.path.join(num_file_dir, sample.name + '.root')
    fnden = os.path.join(den_file_dir, sample.name + '.root')
    if not os.path.exists(fnnum) or not os.path.exists(fnden):
        print fnnum
        print "uhh, problem!"
        continue
    fnum = ROOT.TFile(fnnum)
    fden = ROOT.TFile(fnden)
    for pmpt_var in ['1p00', '0p75', '0p50', '0p25', '0p00']:
        #for pt_shift in ['0p0']:
        for pt_shift in ['0p0', '2p5', '5p0', '7p5', '10p0']:
            eff, err, yld, den = getit(fnum, fden, pmpt_var, pt_shift)

            print 'PromptVar: {}   PtShift: {}   eff: {} +- {}    num: {}    den: {}'.format(pmpt_var, pt_shift, round(eff, 3), round(err, 3), round(yld), round(den))
        print '--------------------------------------------------------------------------------------------------'
