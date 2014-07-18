#!/usr/bin/env python

import sys, os, glob

batch_name = 'Ntk5_SigTmpdef_SigSamno_Sam'
#batch_name = 'Ntk5_SigTmpdef_SigSamn-15x1_Sam'
batch_root = os.path.join('/home/uscms213/One2Two', batch_name)
batch_fns = glob.glob(os.path.join(batch_root, '*.root'))
plot_dir = os.path.join('plots/o2t_fit', batch_name)

################################################################################

from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver(plot_dir, size=(600,600))

t = ROOT.TChain('Fitter/t_fit_info')
t.SetMarkerStyle(20)
t.SetMarkerSize(1.5)

for fn in batch_fns:
    t.Add(fn)

for x in 'seed toy true_pars[0] true_pars[1] true_pars[2] true_pars[3]'.split():
    t.Draw(x)
    ps.save('fit_info_%s' % x)

for y in 'h1 h0'.split():
    for x in 'istat maxtwolnL mu_sig err_mu_sig mu_bkg err_mu_bkg'.split():
        n = 't_obs_0__%s_%s' % (y,x)
        t.Draw(n)
        ps.save(n)

t.Draw('pval_signif')
ps.save('pval_signif')

t.Draw('sqrt(2.)*TMath::ErfInverse(1-2*pval_signif)')
ps.save('Z_pval')

t.Draw('sqrt(2*(t_obs_0__h1_maxtwolnL - t_obs_0__h0_maxtwolnL))')
ps.save('Z_wilks')

t.Draw('sqrt(2*(t_obs_0__h1_maxtwolnL - t_obs_0__h0_maxtwolnL)):sqrt(2.)*TMath::ErfInverse(1-2*pval_signif)')
ps.save('Z_comp')

t.Draw('pval_limits:mu_sig_limits>>hlimscan')
ps.save('limitscan')

for x in 'pval_limit mu_sig_limit'.split():
    t.Draw(x)
    ps.save(x)
