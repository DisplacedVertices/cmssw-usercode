#!/usr/bin/env python

import sys
from JMTucker.Tools.ROOTTools import *
set_style()

fn = sys.argv[1]
plot_dir = sys.argv[2]

f = ROOT.TFile(fn)
t = f.Get('Fitter/t_fit_info')

skip = ''
t.Draw('true_pars[0]>>htruesig(1000,0,1000)', skip, 'goff')
t.Draw('true_pars[1]>>htruebkg(1000,0,1000)', skip, 'goff')
t.Draw('true_pars[2]>>htruenuis0(1000,0,10)', skip, 'goff')
t.Draw('true_pars[3]>>htruenuis1(1000,0,10)', skip, 'goff')
mu_sig_true_mean = ROOT.htruesig.GetMean()
mu_bkg_true_mean = ROOT.htruebkg.GetMean()
nuis0_true_mean = ROOT.htruenuis0.GetMean()
nuis1_true_mean = ROOT.htruenuis1.GetMean()
print '<true sig> = %f, <true bkg> = %f' % (mu_sig_true_mean, mu_bkg_true_mean)

t.SetMarkerStyle(20)
t.SetMarkerSize(1.)

tree_vars = 'seed toy true_pars[0] true_pars[1] true_pars[2] true_pars[3]'
for y in 'h1 h0'.split():
    for x in 'istat maxtwolnL mu_sig err_mu_sig eplus_mu_sig eminus_mu_sig mu_bkg err_mu_bkg eplus_mu_bkg eminus_mu_bkg nuis0 err_nuis0 eplus_nuis0 eminus_nuis0 nuis1 err_nuis1 eplus_nuis1 eminus_nuis1 correlation_nuis'.split():
        tree_vars += ' t_obs_0__%s_%s' % (y,x)
tree_vars += ' fs_chi2 fs_ndof fs_prob pval_signif pval_cls sig_limit sig_limit_err sig_limit_fit_n sig_limit_fit_a sig_limit_fit_b sig_limit_fit_a_err sig_limit_fit_b_err sig_limit_fit_prob'
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

def skip(h0_istat, h1_istat, sig_limit_fit_n):
    return False #h0_istat <= 1

d = do_detree()

ps = plot_saver(plot_dir, size=(600,600))

h = ROOT.TH1D
h2 = ROOT.TH2D
h_seed = h('h_seed', '', 201, 0, 201)
h_toy = h('h_toy', '', 1, 0, 1)
h_mu_sig_true = h('h_mu_sig_true', '', 200, 0, 200)
h_mu_bkg_true = h('h_mu_bkg_true', '', 200, 0, 200)
h_istat = h2('h_istat', '', 5, 0, 5, 5, 0, 5)
h_istatsum_v_seed = h2('h_istatsum_v_seed', '', 201, 0, 201, 5, 0, 5)
h_h1_maxtwolnL = h('h_h1_maxtwolnL', '', 100, -300, 2000)
h_h1_mu_sig = h('h_h1_mu_sig', '', 40, 0, 80)
h_h1_mu_sig_err = h('h_h1_mu_sig_err', '', 40, 0, 80)
h_h1_mu_sig_eplus = h('h_h1_mu_sig_eplus', '', 80, -80, 80)
h_h1_mu_sig_eminus = h('h_h1_mu_sig_eminus', '', 80, -80, 80)
h_h1_mu_sig_err_v_sig = h2('h_h1_mu_sig_err_v_sig', '', 40, 0, 80, 40, 0, 80)
h_h1_mu_sig_v_true = h2('h_h1_mu_sig_v_true', '', 40, 0, 80, 40, 0, 80)
h_h1_mu_sig_pull = h('h_h1_mu_sig_pull', '', 40, -10, 10)
h_h1_mu_bkg = h('h_h1_mu_bkg', '', 100, 0, 400)
h_h1_mu_bkg_err = h('h_h1_mu_bkg_err', '', 40, 0, 40)
h_h1_mu_bkg_eplus = h('h_h1_mu_bkg_eplus', '', 80, -40, 40)
h_h1_mu_bkg_eminus = h('h_h1_mu_bkg_eminus', '', 80, -40, 40)
h_h1_mu_bkg_err_v_bkg = h2('h_h1_mu_bkg_err_v_bkg', '', 100, 0, 400, 10, 0, 40)
h_h1_mu_bkg_v_true = h2('h_h1_mu_bkg_v_true', '', 100, 0, 400, 100, 0, 400)
h_h1_mu_bkg_pull = h('h_h1_mu_bkg_pull', '', 40, -10, 10)
h_h1_nuis0 = h('h_h1_nuis0', '', 40, 0, 0.2)
h_h1_nuis0_err = h('h_h1_nuis0_err', '', 40, 0, 0.1)
h_h1_nuis0_eplus = h('h_h1_nuis0_eplus', '', 80, -0.1, 0.1)
h_h1_nuis0_eminus = h('h_h1_nuis0_eminus', '', 80, -0.1, 0.1)
h_h1_nuis0_pull = h('h_h1_nuis0_pull', '', 40, -10, 10)
h_h1_nuis1 = h('h_h1_nuis1', '', 40, 0, 0.1)
h_h1_nuis1_err = h('h_h1_nuis1_err', '', 40, 0, 0.1)
h_h1_nuis1_eplus = h('h_h1_nuis1_eplus', '', 80, -0.1, 0.1)
h_h1_nuis1_eminus = h('h_h1_nuis1_eminus', '', 80, -0.1, 0.1)
h_h1_nuis1_pull = h('h_h1_nuis1_pull', '', 40, -10, 10)
h_h1_nuis1_nuis0 = h2('h_h1_nuis1_nuis0', '', 40, 0, 0.2, 40, 0, 0.1)
h_h1_nuis_correlation = h('h_h1_nuis_correlation', '', 40, -2, 2)
h_h0_maxtwolnL = h('h_h0_maxtwolnL', '', 100, -300, 2000)
h_h0_mu_bkg = h('h_h0_mu_bkg', '', 100, 0, 400)
h_h0_mu_bkg_err = h('h_h0_mu_bkg_err', '', 40, 0, 40)
h_h0_mu_bkg_eplus = h('h_h0_mu_bkg_eplus', '', 80, -40, 40)
h_h0_mu_bkg_eminus = h('h_h0_mu_bkg_eminus', '', 80, -40, 40)
h_h0_mu_bkg_pull = h('h_h0_mu_bkg_pull', '', 40, -10, 10)
h_h0_mu_bkg_err_v_bkg = h2('h_h0_mu_err_v_bkg', '', 100, 0, 400, 10, 0, 40)
h_h0_mu_bkg_v_true = h2('h_h0_mu_bkg_v_true', '', 100, 0, 400, 100, 0, 400)
h_h0_nuis0 = h('h_h0_nuis0', '', 40, 0, 0.2)
h_h0_nuis0_err = h('h_h0_nuis0_err', '', 40, 0, 0.1)
h_h0_nuis0_eplus = h('h_h0_nuis0_eplus', '', 80, -0.1, 0.1)
h_h0_nuis0_eminus = h('h_h0_nuis0_eminus', '', 80, -0.1, 0.1)
h_h0_nuis0_pull = h('h_h0_nuis0_pull', '', 40, -10, 10)
h_h0_nuis1 = h('h_h0_nuis1', '', 40, 0, 0.1)
h_h0_nuis1_err = h('h_h0_nuis1_err', '', 40, 0, 0.1)
h_h0_nuis1_eplus = h('h_h0_nuis1_eplus', '', 80, -0.1, 0.1)
h_h0_nuis1_eminus = h('h_h0_nuis1_eminus', '', 80, -0.1, 0.1)
h_h0_nuis1_pull = h('h_h0_nuis1_pull', '', 40, -10, 10)
h_h0_nuis1_nuis0 = h2('h_h0_nuis1_nuis0', '', 40, 0, 0.2, 40, 0, 0.1)
h_h0_nuis_correlation = h('h_h0_nuis_correlation', '', 40, -2, 2)
h_t = h('h_t', '', 40, -5, 100)
h_chi2 = h('h_chi2', '', 40, 0, 40)
h_ndof = h('h_ndof', '', 10, 0, 10)
h_chi2ndof = h('h_chi2ndof', '', 100, 0, 10)
h_prob = h('h_prob', '', 15, 0, 1.5)
h_pval_signif = h('h_pval_signif', '', 51, 0, 1.02)
h_zval_signif = h('h_zval_signif', '', 50, 0, 20)
h_zval2_wilks = h('h_zval2_wilks', '', 50, 0, 20)
h_zvals = h2('h_zvals', '', 50, 0, 20, 50, 0, 20)
h_pval_cls = h('h_pval_cls', '', 51, 0, 1.02)
h_sig_limit = h('h_sig_limit', '', 200, 0, 200)
h_sig_limit.GetXaxis().SetRangeUser(0,50)
h_sig_limit_scaled = h('h_sig_limit_scaled', '', 200, 0, 50)
h_sig_limit_err = h('h_sig_limit_err', '', 40, 0, 20)
h_sig_limit_fit_n = h('h_sig_limit_fit_n', '', 50, 0, 50)
h_sig_limit_fit_a = h('h_sig_limit_fit_a', '', 50, 0, 5)
h_sig_limit_fit_b = h('h_sig_limit_fit_b', '', 50, -0.1, 0.1)
h_sig_limit_fit_a_err = h('h_sig_limit_fit_a_err', '', 50, 0, 5)
h_sig_limit_fit_b_err = h('h_sig_limit_fit_b_err', '', 50, 0, 1)
h_sig_limit_fit_prob = h('h_sig_limit_fit_prob', '', 50, 0, 1)

pval_signifs = []
sig_limits = []
sig_limits_scaled = []
for seed,toy,true_pars_0,true_pars_1,true_pars_2,true_pars_3,h1_istat,h1_maxtwolnL,h1_mu_sig,h1_err_mu_sig,h1_eplus_mu_sig,h1_eminus_mu_sig,h1_mu_bkg,h1_err_mu_bkg,h1_eplus_mu_bkg,h1_eminus_mu_bkg,h1_nuis0,h1_err_nuis0,h1_eplus_nuis0,h1_eminus_nuis0,h1_nuis1,h1_err_nuis1,h1_eplus_nuis1,h1_eminus_nuis1,h1_correlation_nuis,h0_istat,h0_maxtwolnL,h0_mu_sig,h0_err_mu_sig,h0_eplus_mu_sig,h0_eminus_mu_sig,h0_mu_bkg,h0_err_mu_bkg,h0_eplus_mu_bkg,h0_eminus_mu_bkg,h0_nuis0,h0_err_nuis0,h0_eplus_nuis0,h0_eminus_nuis0,h0_nuis1,h0_err_nuis1,h0_eplus_nuis1,h0_eminus_nuis1,h0_correlation_nuis,chi2,ndof,prob,pval_signif,pval_cls,sig_limit,sig_limit_err,sig_limit_fit_n,sig_limit_fit_a,sig_limit_fit_b,sig_limit_fit_a_err,sig_limit_fit_b_err,sig_limit_fit_prob in d:
    if skip(h0_istat, h1_istat, sig_limit_fit_n):
        continue
    h_seed.Fill(seed)
    h_toy.Fill(toy)
    h_mu_sig_true.Fill(true_pars_0)
    h_mu_bkg_true.Fill(true_pars_1)
    h_istat.Fill(h0_istat, h1_istat)
    h_istatsum_v_seed.Fill(seed, h0_istat + h1_istat)
    h_h1_maxtwolnL.Fill(h1_maxtwolnL)
    h_h1_mu_sig.Fill(h1_mu_sig)
    h_h1_mu_sig_err.Fill(h1_err_mu_sig)
    if h1_eplus_mu_sig != 0:
        h_h1_mu_sig_eplus.Fill(h1_eplus_mu_sig)
    if h1_eminus_mu_sig != 0:
        h_h1_mu_sig_eminus.Fill(h1_eminus_mu_sig)
    h_h1_mu_sig_err_v_sig.Fill(h1_mu_sig, h1_err_mu_sig)
    h_h1_mu_sig_v_true.Fill(true_pars_0, h1_mu_sig)
    h_h1_mu_sig_pull.Fill((h1_mu_sig - mu_sig_true_mean)/h1_err_mu_sig)
    h_h1_mu_bkg.Fill(h1_mu_bkg)
    h_h1_mu_bkg_err.Fill(h1_err_mu_bkg)
    if h1_eplus_mu_bkg != 0:
        h_h1_mu_bkg_eplus.Fill(h1_eplus_mu_bkg)
    if h1_eminus_mu_bkg != 0:
        h_h1_mu_bkg_eminus.Fill(h1_eminus_mu_bkg)
    h_h1_mu_bkg_err_v_bkg.Fill(h1_mu_bkg, h1_err_mu_bkg)
    h_h1_mu_bkg_v_true.Fill(true_pars_1, h1_mu_bkg)
    h_h1_mu_bkg_pull.Fill((h1_mu_bkg - mu_bkg_true_mean)/h1_err_mu_bkg)
    #h_h1_nuis0.Fill(h1_nuis0)
    #h_h1_nuis0_err.Fill(h1_err_nuis0)
    #if h1_eplus_nuis0 != 0:
    #    h_h1_nuis0_eplus.Fill(h1_eplus_nuis0)
    #if h1_eminus_nuis0 != 0:
    #    h_h1_nuis0_eminus.Fill(h1_eminus_nuis0)
    #h_h1_nuis0_pull.Fill((h1_nuis0 - nuis0_true_mean)/h1_err_nuis0)
    #h_h1_nuis_correlation.Fill(h1_correlation_nuis)
    #h_h1_nuis1.Fill(h1_nuis1)
    #h_h1_nuis1_err.Fill(h1_err_nuis1)
    #if h1_eplus_nuis1 != 0:
    #    h_h1_nuis1_eplus.Fill(h1_eplus_nuis1)
    #if h1_eminus_nuis1 != 0:
    #    h_h1_nuis1_eminus.Fill(h1_eminus_nuis1)
    #h_h1_nuis1_pull.Fill((h1_nuis1 - nuis1_true_mean)/h1_err_nuis1)
    #h_h1_nuis1_nuis0.Fill(h1_nuis0, h1_nuis1)
    h_h0_maxtwolnL.Fill(h0_maxtwolnL)
    h_h0_mu_bkg.Fill(h0_mu_bkg)
    h_h0_mu_bkg_err.Fill(h0_err_mu_bkg)
    if h0_eplus_mu_bkg != 0:
        h_h0_mu_bkg_eplus.Fill(h0_eplus_mu_bkg)
    if h0_eminus_mu_bkg != 0:
        h_h0_mu_bkg_eminus.Fill(h0_eminus_mu_bkg)
    h_h0_mu_bkg_err_v_bkg.Fill(h0_mu_bkg, h0_err_mu_bkg)
    h_h0_mu_bkg_v_true.Fill(true_pars_1, h0_mu_bkg)
    h_h0_mu_bkg_pull.Fill((h0_mu_bkg - mu_bkg_true_mean)/h0_err_mu_bkg)
    #h_h0_nuis0.Fill(h0_nuis0)
    #h_h0_nuis0_err.Fill(h0_err_nuis0)
    #if h0_eplus_nuis0 != 0:
    #    h_h0_nuis0_eplus.Fill(h0_eplus_nuis0)
    #if h0_eminus_nuis0 != 0:
    #    h_h0_nuis0_eminus.Fill(h0_eminus_nuis0)
    #h_h0_nuis0_pull.Fill((h0_nuis0 - nuis0_true_mean)/h0_err_nuis0)
    #h_h0_nuis1.Fill(h0_nuis1)
    #h_h0_nuis1_err.Fill(h0_err_nuis1)
    #if h0_eplus_nuis1 != 0:
    #    h_h0_nuis1_eplus.Fill(h0_eplus_nuis1)
    #if h0_eminus_nuis1 != 0:
    #    h_h0_nuis1_eminus.Fill(h0_eminus_nuis1)
    #h_h0_nuis1_pull.Fill((h0_nuis1 - nuis1_true_mean)/h0_err_nuis1)
    #h_h0_nuis1_nuis0.Fill(h0_nuis0, h0_nuis1)
    #h_h0_nuis_correlation.Fill(h0_correlation_nuis)
    h_t.Fill(h1_maxtwolnL - h0_maxtwolnL)
    h_chi2.Fill(chi2)
    h_ndof.Fill(ndof)
    h_chi2ndof.Fill(chi2/ndof)
    h_prob.Fill(prob)
    pval_signifs.append(pval_signif)
    h_pval_signif.Fill(pval_signif)
    zval_signif = 2**0.5*ROOT.TMath.ErfInverse(1.-2.*pval_signif)
    h_zval_signif.Fill(zval_signif)
    zval2_wilks = h1_maxtwolnL - h0_maxtwolnL
    h_zval2_wilks.Fill(zval2_wilks)
    h_zvals.Fill(zval_signif, zval2_wilks)
    h_pval_cls.Fill(pval_cls)
    sig_limits.append(sig_limit)
    h_sig_limit.Fill(sig_limit)
    #sig_limit_scaled = sig_limit / (sig_eff * xsec2nevt)
    #h_sig_limit_scaled.Fill(sig_limit_scaled)
    #sig_limits_scaled.append(sig_limit_scaled)
    h_sig_limit_err.Fill(sig_limit_err)
    h_sig_limit_fit_n.Fill(sig_limit_fit_n)
    h_sig_limit_fit_a.Fill(sig_limit_fit_a)
    h_sig_limit_fit_b.Fill(sig_limit_fit_b)
    h_sig_limit_fit_a_err.Fill(sig_limit_fit_a_err)
    h_sig_limit_fit_b_err.Fill(sig_limit_fit_b_err)
    h_sig_limit_fit_prob.Fill(sig_limit_fit_prob)

for x in 'h_seed h_toy h_mu_sig_true h_mu_bkg_true h_istat h_istatsum_v_seed h_h1_maxtwolnL h_h1_mu_sig h_h1_mu_sig_err h_h1_mu_sig_eplus h_h1_mu_sig_eminus h_h1_mu_sig_err_v_sig h_h1_mu_sig_v_true h_h1_mu_sig_pull h_h1_mu_bkg h_h1_mu_bkg_err h_h1_mu_bkg_eplus h_h1_mu_bkg_eminus h_h1_mu_bkg_err_v_bkg h_h1_mu_bkg_v_true h_h1_mu_bkg_pull h_h1_nuis0 h_h1_nuis0_err h_h1_nuis0_eplus h_h1_nuis0_eminus h_h1_nuis0_pull h_h1_nuis1 h_h1_nuis1_err h_h1_nuis1_eplus h_h1_nuis1_eminus h_h1_nuis1_pull h_h1_nuis1_nuis0 h_h1_nuis_correlation h_h0_maxtwolnL h_h0_mu_bkg h_h0_mu_bkg_err h_h0_mu_bkg_eplus h_h0_mu_bkg_eminus h_h0_mu_bkg_err_v_bkg h_h0_mu_bkg_v_true h_h0_mu_bkg_pull h_h0_nuis0 h_h0_nuis0_err h_h0_nuis0_eplus h_h0_nuis0_eminus h_h0_nuis0_pull h_h0_nuis1 h_h0_nuis1_err h_h0_nuis1_eplus h_h0_nuis1_eminus h_h0_nuis1_pull h_h0_nuis1_nuis0 h_h0_nuis_correlation h_t h_chi2 h_ndof h_chi2ndof h_prob h_pval_signif h_zval_signif h_zval2_wilks h_zvals h_pval_cls h_sig_limit h_sig_limit_scaled h_sig_limit_err h_sig_limit_fit_n h_sig_limit_fit_a h_sig_limit_fit_b h_sig_limit_fit_a_err h_sig_limit_fit_b_err h_sig_limit_fit_prob'.split():
    if 'nuis' in x:
        continue
    #print x
    h = eval(x)
    log = False
    if type(h) == ROOT.TH1D:
        log = True
        if 'pull' in x:
            h.Fit('gaus', 'q')
        else:
            h.Draw()
        ps.c.Update()
        differentiate_stat_box(h, 0, new_size=(0.3,0.4))
    elif x == 'h_istat':
        h.SetStats(0)
        h.SetMarkerSize(2)
        h.SetMarkerColor(ROOT.kWhite)
        h.Draw('colz text')
    else:
        h.Draw('colz')
        #h.SetStats(0)
    ps.save(x, log=log)

d.sort(key=lambda x: x[i_pval_signif])
ns = [0,1] + [int(i*len(d)/3.) for i in xrange(1,3)] + [-2,-1]
for n in ns:
    x = d[n]
    seed, toy = int(x[0]), int(x[1])
    assert toy == 0 or toy == -1
    snip = '/mfvo2t_%i_' % seed
    f = ROOT.TFile(fn)
    dr = f.Get('Fitter/seed%02i_toy%02i/fit_results' % (seed, toy))
    for t in 'sb b'.split():
        leg = ROOT.TLegend(0.502, 0.620, 0.848, 0.861)
        s = dr.Get('h_sig_%s_fit_bb_nodiv' % t)
        b = dr.Get('h_bkg_%s_fit_bb_nodiv' % t)
        dt = dr.Get('h_data_%s_fit_bb_nodiv' % t)
        sb = b.Clone('sb')
        sb.Add(s)
        for h in (s,b,sb,dt):
            h.SetTitle(';d_{VV} (cm)')
            h.GetYaxis().SetRangeUser(1e-2, 50)
        if dt.GetMaximum() > sb.GetMaximum():
            dt.Draw('e')
            sb.Draw('hist same')
        else:
            sb.Draw('hist')
            dt.Draw('same e')
        s.Draw('same hist')
        b.Draw('same hist')
        dt.Draw('same e')

        leg.AddEntry(s, 'sig shape', 'F')
        leg.AddEntry(b, 'bkg shape', 'F')
        leg.AddEntry(sb, 'sig + bkg', 'F')
        leg.AddEntry(dt, '"data"', 'LE')
        leg.Draw()

        nm = '%s_fit_seed%i_toy%i_pval%s' % (t, seed, toy, str(x[i_pval_signif]).replace('.','p'))
        ps.save(nm)

        h = dr.Get('h_likelihood_%s_scannuis' % t)
        if h:
            h.Draw('colz')
            h.SetStats(0)
            h.GetXaxis().SetLabelSize(0.02)
            h.GetYaxis().SetLabelSize(0.02)
            ti = h.GetTitle().split(';')[0]
            nums = []
            for v in ti.replace(',', ' ').split():
                try:
                    nums.append(float(v))
                except ValueError:
                    pass
            assert len(nums) == 8
            best_mu_sig = nums[0]
            best_mu_bkg = nums[2]
            best_nuis0 = nums[4]
            best_nuis1 = nums[6]
            h.SetTitle('%s;#mu_{clear} (cm);#sigma_{clear} (cm)' % ti)
            m = ROOT.TMarker(best_nuis0, best_nuis1, 5)
            m.SetMarkerColor(ROOT.kWhite)
            m.SetMarkerSize(1)
            m.Draw()
            ps.save(nm + '_scannuis')
            h.SetMinimum(h.GetMaximum() - 4)
            h.Draw('colz')
            m.Draw()
            ps.save(nm + '_scannuis_2sg')

        if t == 'sb':
            h = dr.Get('h_likelihood_%s_scanmus' % t)
            if h:
                h.Draw('colz')
                h.SetStats(0)
                assert ti == h.GetTitle().split(';')[0]
                h.SetTitle('%s;s;b' % ti)
                m = ROOT.TMarker(best_mu_sig, best_mu_bkg, 5)
                m.SetMarkerColor(ROOT.kWhite)
                m.SetMarkerSize(1)
                m.Draw()
                h.GetYaxis().SetTitleOffset(1.25)
                ps.save(nm + '_scanmus')
                h.SetMinimum(h.GetMaximum() - 4)
                h.Draw('colz')
                m.Draw()
                ps.save(nm + '_scanmus_2sg')

        #for par in ['mubkg_nuis0', 'mubkg_nuis1', 'musig_nuis0', 'musig_nuis1', 'mubkg', 'musig', 'nuis0', 'nuis1']:
        for par in 'mubkg', 'musig':
            h = dr.Get('h_likelihood_%s_scan_%s' % (t,par))
            if h:
                h.Draw('colz')
                h.SetStats(0)
                ps.save(nm + '_scan_%s'%par)
                h.SetMinimum(h.GetMaximum() - 4)
                h.Draw('colz')
                ps.save(nm + '_scan_%s_2sg'%par)

    g = dr.Get('g_limit_bracket_fit')
    if g:
        g.Draw('ALP')
        ps.save('limit_bracket_fit_seed%i_toy%i_pval%s' % (seed, toy, str(x[i_pval_signif]).replace('.','p')))

def stats(l, header=''):
    l.sort()
    n = len(l)
    if n % 2 == 0:
        median = (l[n/2] + l[n/2-1])/2.
    else:
        median = l[n/2]
    lo68 = l[int(n/2 - 0.34*n)]
    hi68 = l[int(n/2 + 0.34*n)]
    lo95 = l[int(n/2 - 0.475*n)]
    hi95 = l[int(n/2 + 0.475*n)]
    print '\n'
    print header
    print header + ':Expected  2.5%: r <', lo95
    print header + ':Expected 16.0%: r <', lo68
    print header + ':Expected 50.0%: r <', median
    print header + ':Expected 84.0%: r <', hi68
    print header + ':Expected 97.5%: r <', hi95
    print header + ':Observed Limit: r <', median
    return median, lo68, hi68, lo95, hi95

stats(pval_signifs, 'pval_signif')
stats(sig_limits, 'mu_sig_limit')
stats(sig_limits_scaled, 'sigma_sig_limit')

'''
foreach x (lsts/*lst)
  echo $x; py draw_fit.py $x >& `echo $x | sed -e s/.lst/.out/`
end
'''
