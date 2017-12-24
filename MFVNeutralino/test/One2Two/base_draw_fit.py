#!/usr/bin/env python

import sys, os, glob
import JMTucker.MFVNeutralino.AnalysisConstants as ac

batch_fn_lst = [x for x in sys.argv if x.endswith('.lst')][0]
batch_name = os.path.basename(batch_fn_lst).replace('.lst','')
print 'batch name', batch_name
fudge = 1. # 0.5 if 'fullhadded' not in batch_name else 1.
#batch_root = glob('/store/user/tucker/mfvo2t_%s/mfvo2t_%s/*/' % (batch_name, batch_name))
#assert len(batch_root) == 1
#batch_root = batch_root[0]
#batch_fns = glob(os.path.join(batch_root, '*.root'))
batch_fns = [x.strip() for x in open(batch_fn_lst).readlines() if x.strip()]
#batch_fns = [x.replace('/store/user', '/mnt/xrootd/user') for x in batch_fns]
batch_fns = [('root://cmsxrootd.fnal.gov/' + x if x.startswith('/store') else x) for x in batch_fns]
sig_tmpl_num = -int(batch_name.split('SigTmp')[1].split('_')[0])
try:
    sig_nfo = batch_name.split('SigSamn')[1].split('_')[0]
    sig_num, sig_scale = sig_nfo.split('x')
    sig_num = -int(sig_num)
    sig_scale = int(sig_scale)
except ValueError:
    sig_num = 0
    sig_scale = 0

################################################################################

from JMTucker.Tools.ROOTTools import *
set_style()

t = ROOT.TChain('Fitter/t_fit_info')
t.SetMarkerStyle(20)
t.SetMarkerSize(1.)

for fn in batch_fns:
    t.Add(fn)

tree_vars = 'seed toy true_pars[0] true_pars[1] true_pars[2] true_pars[3]'
for y in 'h1 h0'.split():
    for x in 'istat maxtwolnL mu_sig err_mu_sig mu_bkg err_mu_bkg nuis0 err_nuis0 nuis1 err_nuis1'.split():
        tree_vars += ' t_obs_0__%s_%s' % (y,x)
tree_vars += ' pval_signif pval_cls sig_limit sig_limit_err sig_limit_fit_n sig_limit_fit_a sig_limit_fit_b sig_limit_fit_a_err sig_limit_fit_b_err sig_limit_fit_prob'
i_pval_signif = -9

def tree_xform(x):
    z = []
    for y in x:
        y = y.strip()
        if not y:
            z.append(0)
        else:
            z.append(float(y))
    return tuple(z)

def do_detree():
    return list(detree(t, tree_vars.replace(' ', ':'), xform=tree_xform))

################################################################################

#               1       2       3       4       5       6       7       8       9       10      11      12      13      14      15      16      17      18      19      20      21      22       23       24
xsec2nevt = ac.int_lumi / 1000 * ac.scale_factor
if sig_tmpl_num > 100:
    import bigsigscan
    sig_eff = bigsigscan.num2eff(-sig_tmpl_num)
    mu_sig_true_mean = sig_eff * xsec2nevt * sig_scale
else:
    sig_trues = [0., 0.0245, 0.1102, 0.2085, 0.3064, 0.3293, 0.3279, 0.1531, 0.7707, 1.4223, 2.0397, 2.1889, 2.1456, 0.3920, 2.2956, 4.2842, 5.8373, 6.1553, 6.0429, 0.7841, 4.5308, 8.5589, 11.0880, 11.4206, 11.3452]
    sig_effs = [x / xsec2nevt for x in sig_trues]
    sig_eff = sig_effs[sig_tmpl_num]
    mu_sig_true_mean = sig_trues[sig_num] * sig_scale
print 'sig_num', sig_num, 'mu_sig_true_mean', mu_sig_true_mean
if sig_scale < 0:
    print '( this is data )'
mu_bkg_true_mean = 39.47 * fudge

def skip(h0_istat, h1_istat, sig_limit_fit_n):
    return h1_istat == 0 or (sig_scale < 0 and sig_limit_fit_n <= 3) #h0_istat <= 1 or h1_istat <= 1 or sig_limit_fit_n < 4

#for seed,toy,true_pars_0,true_pars_1,true_pars_2,true_pars_3,h1_istat,h1_maxtwolnL,h1_mu_sig,h1_err_mu_sig,h1_mu_bkg,h1_err_mu_bkg,h1_nuis0,h1_err_nuis0,h1_nuis1,h1_err_nuis1,h0_istat,h0_maxtwolnL,h0_mu_sig,h0_err_mu_sig,h0_mu_bkg,h0_err_mu_bkg,h0_nuis0,h0_err_nuis0,h0_nuis1,h0_err_nuis1,pval_signif,sig_limit,sig_limit_err,sig_limit_fit_n,sig_limit_fit_a,sig_limit_fit_b,sig_limit_fit_a_err,sig_limit_fit_b_err,sig_limit_fit_prob in d:
#    if skip(h0_istat, h1_istat, sig_limit_fit_n):
#        continue
#    ...
