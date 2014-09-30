#!/usr/bin/env python

import sys, os, glob
import JMTucker.MFVNeutralino.AnalysisConstants as ac

batch_fn_lst = [x for x in sys.argv if x.endswith('.lst')][0]
batch_name = os.path.basename(batch_fn_lst).replace('.lst','')
fudge = 1. # 0.5 if 'fullhadded' not in batch_name else 1.
#batch_root = glob.glob('/store/user/tucker/mfvo2t_%s/mfvo2t_%s/*/' % (batch_name, batch_name))
#assert len(batch_root) == 1
#batch_root = batch_root[0]
#batch_fns = glob.glob(os.path.join(batch_root, '*.root'))
batch_fns = [x.strip() for x in open(batch_fn_lst).readlines() if x.strip()]
batch_fns = [x.replace('/store/user', '/mnt/xrootd/user') for x in batch_fns]
sig_tmpl_num = -int(batch_name.split('SigTmp')[1].split('_')[0])
try:
    sig_nfo = batch_name.split('SigSamn')[1].split('_')[0]
    sig_num, sig_scale = sig_nfo.split('x')
    sig_num = -int(sig_num)
    sig_scale = int(sig_scale)
except ValueError:
    sig_num = 0
    sig_scale = 0
plot_dir = os.path.join('plots/o2t_fit', batch_name)

################################################################################

from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver(plot_dir, size=(600,600))

t = ROOT.TChain('Fitter/t_fit_info')
t.SetMarkerStyle(20)
t.SetMarkerSize(1.)

for fn in batch_fns:
    t.Add(fn)

vars = 'seed toy true_pars[0] true_pars[1] true_pars[2] true_pars[3]'
for y in 'h1 h0'.split():
    for x in 'istat maxtwolnL mu_sig err_mu_sig mu_bkg err_mu_bkg nuis0 err_nuis0 nuis1 err_nuis1'.split():
        vars += ' t_obs_0__%s_%s' % (y,x)
vars += ' pval_signif sig_limit sig_limit_err sig_limit_fit_n sig_limit_fit_a sig_limit_fit_b sig_limit_fit_a_err sig_limit_fit_b_err sig_limit_fit_prob'

def xform(x):
    z = []
    for y in x:
        y = y.strip()
        if not y:
            z.append(0)
        else:
            z.append(float(y))
    return tuple(z)

d = list(detree(t, vars.replace(' ', ':'), xform=xform))

h = ROOT.TH1D
h2 = ROOT.TH2D
h_seed = h('h_seed', '', 201, 0, 201)
h_toy = h('h_toy', '', 1, 0, 1)
h_mu_sig_true = h('h_mu_sig_true', '', 200, 0, 200)
h_mu_bkg_true = h('h_mu_bkg_true', '', 200, 0, 200)
h_istat = h2('h_istat', '', 5, 0, 5, 5, 0, 5)
h_istatsum_v_seed = h2('h_istatsum_v_seed', '', 201, 0, 201, 5, 0, 5)
h_h1_maxtwolnL = h('h_h1_maxtwolnL', '', 100, -300, 1500)
h_h1_mu_sig = h('h_h1_mu_sig', '', 40, 0, 80)
h_h1_mu_sig_err = h('h_h1_mu_sig_err', '', 40, 0, 40)
h_h1_mu_sig_pull = h('h_h1_mu_sig_pull', '', 40, -10, 10)
h_h1_mu_bkg = h('h_h1_mu_bkg', '', 100, 0, 400)
h_h1_mu_bkg_err = h('h_h1_mu_bkg_err', '', 40, 0, 40)
h_h1_mu_bkg_pull = h('h_h1_mu_bkg_pull', '', 40, -10, 10)
h_h1_nuis0 = h('h_h1_nuis0', '', 40, 0, 0.2)
h_h1_nuis0_err = h('h_h1_nuis0_err', '', 40, 0, 0.1)
h_h1_nuis0_pull = h('h_h1_nuis0_pull', '', 40, -10, 10)
h_h1_nuis1 = h('h_h1_nuis1', '', 40, 0, 0.1)
h_h1_nuis1_err = h('h_h1_nuis1_err', '', 40, 0, 0.1)
h_h1_nuis1_pull = h('h_h1_nuis1_pull', '', 40, -10, 10)
h_h0_maxtwolnL = h('h_h0_maxtwolnL', '', 100, -300, 1500)
h_h0_mu_bkg = h('h_h0_mu_bkg', '', 100, 0, 400)
h_h0_mu_bkg_err = h('h_h0_mu_bkg_err', '', 40, 0, 40)
h_h0_mu_bkg_pull = h('h_h0_mu_bkg_pull', '', 40, -10, 10)
h_h0_nuis0 = h('h_h0_nuis0', '', 40, 0, 0.2)
h_h0_nuis0_err = h('h_h0_nuis0_err', '', 40, 0, 0.1)
h_h0_nuis0_pull = h('h_h0_nuis0_pull', '', 40, -10, 10)
h_h0_nuis1 = h('h_h0_nuis1', '', 40, 0, 0.1)
h_h0_nuis1_err = h('h_h0_nuis1_err', '', 40, 0, 0.1)
h_h0_nuis1_pull = h('h_h0_nuis1_pull', '', 40, -10, 10)
h_pval_signif = h('h_pval_signif', '', 51, 0, 1.02)
h_zval_signif = h('h_zval_signif', '', 50, 0, 20)
h_zval_wilks = h('h_zval_wilks', '', 50, 0, 20)
h_zvals = h2('h_zvals', '', 50, 0, 20, 50, 0, 20)
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

def skip(h0_istat, h1_istat, sig_limit_fit_n):
    return h0_istat <= 1 or h1_istat <= 1 or sig_limit_fit_n < 4

sig_true = [0., 0.0245, 0.1102, 0.2085, 0.3064, 0.3293, 0.3279, 0.1531, 0.7707, 1.4223, 2.0397, 2.1889, 2.1456, 0.3920, 2.2956, 4.2842, 5.8373, 6.1553, 6.0429, 0.7841, 4.5308, 8.5589, 11.0880, 11.4206, 11.3452]
sig_effs = [x / (ac.int_lumi / 1000 * ac.scale_factor) for x in sig_true]
sig_eff = sig_effs[sig_tmpl_num]
mu_sig_true_mean = sig_true[sig_num] * sig_scale
print 'sig_num', sig_num, 'mu_sig_true_mean', mu_sig_true_mean
mu_bkg_true_mean = 39.47 * fudge
nuis0_true_mean = 0
nuis1_true_mean = 0
for seed,toy,true_pars_0,true_pars_1,true_pars_2,true_pars_3,h1_istat,h1_maxtwolnL,h1_mu_sig,h1_err_mu_sig,h1_mu_bkg,h1_err_mu_bkg,h1_nuis0,h1_err_nuis0,h1_nuis1,h1_err_nuis1,h0_istat,h0_maxtwolnL,h0_mu_sig,h0_err_mu_sig,h0_mu_bkg,h0_err_mu_bkg,h0_nuis0,h0_err_nuis0,h0_nuis1,h0_err_nuis1,pval_signif,sig_limit,sig_limit_err,sig_limit_fit_n,sig_limit_fit_a,sig_limit_fit_b,sig_limit_fit_a_err,sig_limit_fit_b_err,sig_limit_fit_prob in d:
    if skip(h0_istat, h1_istat, sig_limit_fit_n):
        continue
    nuis0_true_mean += true_pars_2
    nuis1_true_mean += true_pars_2
n = len(d)
nuis0_true_mean /= n
nuis1_true_mean /= n

pval_signifs = []
sig_limits = []
sig_limits_scaled = []
for seed,toy,true_pars_0,true_pars_1,true_pars_2,true_pars_3,h1_istat,h1_maxtwolnL,h1_mu_sig,h1_err_mu_sig,h1_mu_bkg,h1_err_mu_bkg,h1_nuis0,h1_err_nuis0,h1_nuis1,h1_err_nuis1,h0_istat,h0_maxtwolnL,h0_mu_sig,h0_err_mu_sig,h0_mu_bkg,h0_err_mu_bkg,h0_nuis0,h0_err_nuis0,h0_nuis1,h0_err_nuis1,pval_signif,sig_limit,sig_limit_err,sig_limit_fit_n,sig_limit_fit_a,sig_limit_fit_b,sig_limit_fit_a_err,sig_limit_fit_b_err,sig_limit_fit_prob in d:
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
    h_h1_mu_sig_pull.Fill((h1_mu_sig - mu_sig_true_mean)/h1_err_mu_sig)
    h_h1_mu_bkg.Fill(h1_mu_bkg)
    h_h1_mu_bkg_err.Fill(h1_err_mu_bkg)
    h_h1_mu_bkg_pull.Fill((h1_mu_bkg - mu_bkg_true_mean)/h1_err_mu_bkg)
    h_h1_nuis0.Fill(h1_nuis0)
    h_h1_nuis0_err.Fill(h1_err_nuis0)
    h_h1_nuis0_pull.Fill((h1_nuis0 - nuis0_true_mean)/h1_err_nuis0)
    h_h1_nuis1.Fill(h1_nuis1)
    h_h1_nuis1_err.Fill(h1_err_nuis1)
    h_h1_nuis1_pull.Fill((h1_nuis1 - nuis1_true_mean)/h1_err_nuis1)
    h_h0_maxtwolnL.Fill(h0_maxtwolnL)
    h_h0_mu_bkg.Fill(h0_mu_bkg)
    h_h0_mu_bkg_err.Fill(h0_err_mu_bkg)
    h_h0_mu_bkg_pull.Fill((h0_mu_bkg - mu_bkg_true_mean)/h0_err_mu_bkg)
    h_h0_nuis0.Fill(h0_nuis0)
    h_h0_nuis0_err.Fill(h0_err_nuis0)
    h_h0_nuis0_pull.Fill((h0_nuis0 - nuis0_true_mean)/h0_err_nuis0)
    h_h0_nuis1.Fill(h0_nuis1)
    h_h0_nuis1_err.Fill(h0_err_nuis1)
    h_h0_nuis1_pull.Fill((h0_nuis1 - nuis1_true_mean)/h0_err_nuis1)
    pval_signifs.append(pval_signif)
    h_pval_signif.Fill(pval_signif)
    zval_signif = 2**0.5*ROOT.TMath.ErfInverse(1.-2.*pval_signif)
    h_zval_signif.Fill(zval_signif)
    zval_wilks = h1_maxtwolnL - h0_maxtwolnL
    h_zval_wilks.Fill(zval_wilks)
    h_zvals.Fill(zval_signif, zval_wilks)
    sig_limits.append(sig_limit)
    h_sig_limit.Fill(sig_limit)
    sig_limit_scaled = sig_limit / (sig_eff * ac.int_lumi / 1000. * ac.scale_factor)
    h_sig_limit_scaled.Fill(sig_limit_scaled)
    sig_limits_scaled.append(sig_limit_scaled)
    h_sig_limit_err.Fill(sig_limit_err)
    h_sig_limit_fit_n.Fill(sig_limit_fit_n)
    h_sig_limit_fit_a.Fill(sig_limit_fit_a)
    h_sig_limit_fit_b.Fill(sig_limit_fit_b)
    h_sig_limit_fit_a_err.Fill(sig_limit_fit_a_err)
    h_sig_limit_fit_b_err.Fill(sig_limit_fit_b_err)
    h_sig_limit_fit_prob.Fill(sig_limit_fit_prob)

for x in 'h_seed h_toy h_mu_sig_true h_mu_bkg_true h_istat h_istatsum_v_seed h_h1_maxtwolnL h_h1_mu_sig h_h1_mu_sig_err h_h1_mu_sig_pull h_h1_mu_bkg h_h1_mu_bkg_err h_h1_mu_bkg_pull h_h1_nuis0 h_h1_nuis0_err h_h1_nuis0_pull h_h1_nuis1 h_h1_nuis1_err h_h1_nuis1_pull h_h0_maxtwolnL h_h0_mu_bkg h_h0_mu_bkg_err h_h0_mu_bkg_pull h_h0_nuis0 h_h0_nuis0_err h_h0_nuis0_pull h_h0_nuis1 h_h0_nuis1_err h_h0_nuis1_pull h_pval_signif h_zval_signif h_zval_wilks h_zvals h_sig_limit h_sig_limit_scaled h_sig_limit_err h_sig_limit_fit_n h_sig_limit_fit_a h_sig_limit_fit_b h_sig_limit_fit_a_err h_sig_limit_fit_b_err h_sig_limit_fit_prob'.split():
    print x
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
ns = [0,1] + [int(i*len(d)/3.) for i in xrange(1,3)] + [-2,-1]
for n in ns:
    x = d[n]
    seed, toy = int(x[0]), int(x[1])
    assert toy == 0 or toy == -1
    snip = '/mfvo2t_%i_' % seed
    fn = [fn for fn in batch_fns if snip in fn][0]
    f = ROOT.TFile(fn)
    dr = f.Get('Fitter/seed%02i_toy%02i/fit_results' % (seed, toy))
    for t in 'sb b'.split():
        leg = ROOT.TLegend(0.502, 0.620, 0.848, 0.861)
        s = dr.Get('h_sig_%s_fit_nodiv' % t)
        b = dr.Get('h_bkg_%s_fit_nodiv' % t)
        sb = dr.Get('h_sum_%s_fit_nodiv' % t)
        dt = dr.Get('h_data_%s_fit_nodiv' % t)
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
        dt.Draw('same e')

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

    g = dr.Get('g_limit_bracket_fit')
    g.Draw('ALP')
    ps.save('limit_bracket_fit_seed%i_toy%i_pval%s' % (seed, toy, str(x[-3]).replace('.','p')))

def stats(l, prints=False):
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
    if prints:
        print 'Expected  2.5%: r <', lo95
        print 'Expected 16.0%: r <', lo68
        print 'Expected 50.0%: r <', median
        print 'Expected 84.0%: r <', hi68
        print 'Expected 97.5%: r <', hi95
        if n <= 20:
            print 'Observed Limit: r <', median
    return median, lo68, hi68, lo95, hi95

#print 'limit on mu_sig:'
#limit_stats(sig_limits)
#print
print 'median pval_signif:', stats(pval_signifs)[0]
print 'scaled limits:'
stats(sig_limits_scaled, True)

'''
foreach x ( crab/One2Two/crab_* )
  crtools -outputFromFJR $x | grep root > `echo $x | sed -e 's/.*crab_//'`.lst
end
'''
