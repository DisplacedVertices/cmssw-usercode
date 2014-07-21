#!/usr/bin/env python

import sys, os, glob

batch_fn_lst = [x for x in sys.argv if x.endswith('.lst')][0]
batch_name = os.path.basename(batch_fn_lst).replace('.lst','')
batch_root = glob.glob('/store/user/tucker/mfvo2t_%s/mfvo2t_%s/*/' % (batch_name, batch_name))
assert len(batch_root) == 1
batch_root = batch_root[0]
#batch_fns = glob.glob(os.path.join(batch_root, '*.root'))
batch_fns = [x.strip() for x in open(batch_fn_lst).readlines() if x.strip()]
plot_dir = os.path.join('plots/o2t_fit', batch_name)

################################################################################

from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver(plot_dir, size=(600,600))

t = ROOT.TChain('Fitter/t_fit_info')
t.SetMarkerStyle(20)
t.SetMarkerSize(1.)

for fn in batch_fns:
    t.Add('root://cmseos.fnal.gov/' + fn)

vars = 'seed toy true_pars[0] true_pars[1] true_pars[2] true_pars[3]'
for y in 'h1 h0'.split():
    for x in 'istat maxtwolnL mu_sig err_mu_sig mu_bkg err_mu_bkg'.split():
        vars += ' t_obs_0__%s_%s' % (y,x)
vars += ' pval_signif pval_limit mu_sig_limit'

d = list(detree(t, vars.replace(' ', ':'), xform=lambda x: tuple(float(y) for y in x)))

h = ROOT.TH1D
h2 = ROOT.TH2D
h_seed = h('h_seed', '', 201, 0, 201)
h_toy = h('h_toy', '', 1, 0, 1)
h_mu_sig_true = h('h_mu_sig_true', '', 200, 0, 200)
h_mu_bkg_true = h('h_mu_bkg_true', '', 200, 0, 200)
h_istat = h2('h_istat', '', 5, 0, 5, 5, 0, 5)
h_h1_maxtwolnL = h('h_h1_maxtwolnL', '', 200, -300, 300)
h_h1_mu_sig = h('h_h1_mu_sig', '', 200, 0, 200)
h_h1_mu_sig_err = h('h_h1_mu_sig_err', '', 200, 0, 50)
h_h1_mu_sig_pull = h('h_h1_mu_sig_pull', '', 200, -10, 10)
h_h1_mu_bkg = h('h_h1_mu_bkg', '', 200, 0, 200)
h_h1_mu_bkg_err = h('h_h1_mu_bkg_err', '', 200, 0, 50)
h_h1_mu_bkg_pull = h('h_h1_mu_bkg_pull', '', 200, -10, 10)
h_h0_maxtwolnL = h('h_h0_maxtwolnL', '', 200, -300, 300)
h_h0_mu_bkg = h('h_h0_mu_bkg', '', 200, 0, 200)
h_h0_mu_bkg_err = h('h_h0_mu_bkg_err', '', 200, 0, 50)
h_h0_mu_bkg_pull = h('h_h0_mu_bkg_pull', '', 200, -10, 10)
h_pval_signif = h('h_pval_signif', '', 101, 0, 1.01)
h_zval_signif = h('h_zval_signif', '', 100, 0, 20)
h_zval_wilks = h('h_zval_wilks', '', 100, 0, 20)
h_zvals = h2('h_zvals', '', 100, 0, 20, 100, 0, 20)
h_pval_limit = h('h_pval_limit', '', 101, 0, 1.01)
h_mu_sig_limit = h('h_mu_sig_limit', '', 200, 0, 200)
h_pval_limit.GetXaxis().SetRangeUser(0, 0.2)
h_mu_sig_limit.GetXaxis().SetRangeUser(0,20)

mu_sig_true_mean = 0
mu_bkg_true_mean = 0
for seed,toy,true_pars_0,true_pars_1,true_pars_2,true_pars_3,h1_istat,h1_maxtwolnL,h1_mu_sig,h1_err_mu_sig,h1_mu_bkg,h1_err_mu_bkg,h0_istat,h0_maxtwolnL,h0_mu_sig,h0_err_mu_sig,h0_mu_bkg,h0_err_mu_bkg,pval_signif,pval_limit,mu_sig_limit in d:
    mu_sig_true_mean += true_pars_0
    mu_bkg_true_mean += true_pars_1
mu_sig_true_mean /= len(d)
mu_bkg_true_mean /= len(d)

for seed,toy,true_pars_0,true_pars_1,true_pars_2,true_pars_3,h1_istat,h1_maxtwolnL,h1_mu_sig,h1_err_mu_sig,h1_mu_bkg,h1_err_mu_bkg,h0_istat,h0_maxtwolnL,h0_mu_sig,h0_err_mu_sig,h0_mu_bkg,h0_err_mu_bkg,pval_signif,pval_limit,mu_sig_limit in d:
    h_seed.Fill(seed)
    h_toy.Fill(toy)
    h_mu_sig_true.Fill(true_pars_0)
    h_mu_bkg_true.Fill(true_pars_1)
    h_istat.Fill(h0_istat, h1_istat)
    h_h1_maxtwolnL.Fill(h1_maxtwolnL)
    h_h1_mu_sig.Fill(h1_mu_sig)
    h_h1_mu_sig_err.Fill(h1_err_mu_sig)
    h_h1_mu_sig_pull.Fill((h1_mu_sig - mu_sig_true_mean)/h1_err_mu_sig)
    h_h1_mu_bkg.Fill(h1_mu_bkg)
    h_h1_mu_bkg_err.Fill(h1_err_mu_bkg)
    h_h1_mu_bkg_pull.Fill((h1_mu_bkg - mu_bkg_true_mean)/h1_err_mu_bkg)
    h_h0_maxtwolnL.Fill(h0_maxtwolnL)
    h_h0_mu_bkg.Fill(h0_mu_bkg)
    h_h0_mu_bkg_err.Fill(h0_err_mu_bkg)
    h_h0_mu_bkg_pull.Fill((h0_mu_bkg - mu_bkg_true_mean)/h0_err_mu_bkg)
    h_pval_signif.Fill(pval_signif)
    zval_signif = 2**0.5*ROOT.TMath.ErfInverse(1.-2.*pval_signif)
    h_zval_signif.Fill(zval_signif)
    zval_wilks = h1_maxtwolnL - h0_maxtwolnL
    h_zval_wilks.Fill(zval_wilks)
    h_zvals.Fill(zval_signif, zval_wilks)
    h_pval_limit.Fill(pval_limit)
    h_mu_sig_limit.Fill(mu_sig_limit)

for x in 'h_seed h_toy h_mu_sig_true h_mu_bkg_true h_istat h_h1_maxtwolnL h_h1_mu_sig h_h1_mu_sig_err h_h1_mu_sig_pull h_h1_mu_bkg h_h1_mu_bkg_err h_h1_mu_bkg_pull h_h0_maxtwolnL h_h0_mu_bkg h_h0_mu_bkg_err h_h0_mu_bkg_pull h_pval_signif h_zval_signif h_zval_wilks h_zvals h_pval_limit h_mu_sig_limit'.split():
    h = eval(x)
    if type(h) == ROOT.TH1D:
        if 'pull' in x:
            h.Fit('gaus')
        else:
            h.Draw()
    else:
        h.Draw('colz')
        h.SetStats(0)
    ps.save(x)

d.sort(key=lambda x: x[-3])
ns = [int(i*len(d)/3.) for i in xrange(3)] + [-1]
for n in ns:
    x = d[n]
    seed, toy = int(x[0]), int(x[1])
    assert toy == 0
    snip = '/mfvo2t_%i_' % seed
    fn = [fn for fn in batch_fns if snip in fn][0]
    f = ROOT.TFile(fn)
    dr = f.Get('Fitter/seed%02i_toy%02i/fit_results' % (seed, toy))
    for t in 'sb b'.split():
        leg = ROOT.TLegend(0.502, 0.620, 0.848, 0.861)
        s = dr.Get('h_sig_%s_fit' % t)
        b = dr.Get('h_bkg_%s_fit' % t)
        sb = dr.Get('h_sum_%s_fit' % t)
        dt = dr.Get('h_data_%s_fit' % t)
        for h in (s,b,sb,dt):
            h.SetStats(0)
            h.SetTitle(';d_{VV} (cm)')
            h.GetXaxis().SetRangeUser(0, 0.2)
        if dt.GetMaximum() > sb.GetMaximum():
            dt.Draw('e')
            sb.Draw('hist same')
        else:
            sb.Draw('hist')
            dt.Draw('same e')
        s.Draw('same hist')
        b.Draw('same hist')

        leg.AddEntry(s, 'sig shape', 'F')
        leg.AddEntry(b, 'bkg shape', 'F')
        leg.AddEntry(sb, 'sig + bkg', 'F')
        leg.AddEntry(dt, '"data"', 'LE')
        leg.Draw()

        nm = '%s_fit_seed%i_toy%i_pval%s' % (t, seed, toy, str(x[-3]).replace('.','p'))
        ps.save(nm)

        h = dr.Get('h_likelihood_%s_scannuis' % t)
        h.Draw('colz')
        h.SetStats(0)
        h.GetXaxis().SetLabelSize(0.02)
        h.GetYaxis().SetLabelSize(0.02)
        h.SetTitle(';#mu_{clear} (cm);#sigma_{clear} (cm)')
        ps.save(nm + '_scannuis')

        h.SetMinimum(h.GetMaximum() - 4)
        h.Draw('colz')
        ps.save(nm + '_scannuis_2sg')

        h = dr.Get('h_likelihood_%s_scanmus' % t)
        h.Draw('colz')
        h.SetStats(0)
        h.SetTitle(';s;b')
        h.GetYaxis().SetTitleOffset(1.25)
        ps.save(nm + '_scanmus')

        h.SetMinimum(h.GetMaximum() - 4)
        h.Draw('colz')
        ps.save(nm + '_scanmus_2sg')


'''

foreach x ( crab/One2Two/crab_* )
  py ~/cmswork/Tools/python/CRABTools.py -outputFromFJR $x | grep root > `echo $x | sed -e 's/.*crab_//'`.lst
  end

  '''
