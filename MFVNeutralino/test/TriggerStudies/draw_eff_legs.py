import sys, os
from array import array
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.Tools.Samples import *

# FIXME
# also should be sure to look at the 2D efficiency plots (which will need to be computed here or somewhere)

version = '2017v0p6'
#version = '2017v0p6_require6jets'
#version = '2017v0p5'
#version = '2017v0p5_tighterbjetpt'
save_more = True
use_ttV = True
use_qcd = False # horrible statistics, as usual
use_WZ = False # also bad stats...
use_DYqq_WZlnuqq = False
use_singletop = True

which = typed_from_argv(int, 0)
data_period, int_lumi = [
    ('p8',101037.),
    ('',   41525.),
    ('B',   4794.),
    ('C',   9631.),
    ('D',   4248.),
    ('E',   9314.),
    ('F',  13538.),
    ('',   59512.),
    ('A',  14002.),
    ('B',   7091.),
    ('C',   6937.),
    ('D',  31482.),
    ][which]
year = 2017 if which < 7 else 2018
print year, data_period, int_lumi

########################################################################

root_dir = '/uscms/home/joeyr/crabdirs/TrigEff%s' % version
plot_path = 'TrigEff%s_%s_%s%s' % (version, "legs", year, data_period)
if use_ttV          : plot_path += '_use_ttH_ttZ'
if use_qcd          : plot_path += '_use_qcd'
if use_WZ           : plot_path += '_use_WZ'
if use_DYqq_WZlnuqq : plot_path += '_use_DYqq_WZlnuqq'
if use_singletop    : plot_path += '_use_singletop'

set_style()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ps = plot_saver(plot_dir(plot_path), size=(600,600), log=False, pdf=True)
ROOT.TH1.AddDirectory(0)

data_fn = os.path.join(root_dir, 'SingleMuon%s%s.root' % (year, data_period))
data_f = ROOT.TFile(data_fn)

if year == 2017 or year == 2018:
    bkg_samples = [ttbar_2017]
    if use_ttV : 
        bkg_samples += [ttHbb_2017, ttZsum_2017]
    if use_qcd :
        bkg_samples += [qcdmupt15_2017]
    if use_WZ :
        bkg_samples += [wjetstolnusum_2017, dyjetstollM50sum_2017, dyjetstollM10_2017]
    if use_DYqq_WZlnuqq :
        #bkg_samples += [dyjetstoqq_2017, wztolnuqq_2017]
        bkg_samples += [dyjetstoqq_2017]
    if use_singletop :
        bkg_samples += [singletop_tchan_top_2017, singletop_tchan_antitop_2017]

    sig_samples = [mfv_neu_tau001000um_M0400_2017] 

n_bkg_samples = len(bkg_samples)
for samples in bkg_samples, sig_samples:
    for sample in samples:
        sample.fn = os.path.join(root_dir, sample.name + '.root')
        sample.f = ROOT.TFile(sample.fn) if os.path.isfile(sample.fn) else None

########################################################################

lump_lower = 1200.
fitopt = 'RQS0' # 'RQS' for no drawn fit

def fit_limits(kind, n):
    if 'ht' in n:
        return 100, 5000
    elif 'njets' in n or 'nbjets' in n :
        return 0,20
    elif 'eta' in n :
        return -3,3
    else:
        if 'pf' in kind:
            if 'pt_4' in n:
                return 85, 250
            else:
                return 75, 250
        else:
            #return 60, 250
            return 0, 400

def draw_limits(kind, n):
    if 'ht' in n:
        return 0, 5000
    elif 'njets' in n or 'nbjets' in n :
        return 0,20
    elif 'eta' in n :
        return -3,3
    else:
        if 'pf' in kind:
            if 'pt_4' in n:
                return 85, 250
            else:
                return 75, 250
        else:
            #return 60, 250
            return 0, 500

def make_fcn(name, kind, n):
    fcn = ROOT.TF1(name, '[0] + [1]*(0.5 + 0.5 * TMath::Erf((x - [2])/[3]))', *fit_limits(kind,n))
    fcn.SetParNames('floor', 'ceil', 'turnmu', 'turnsig')
    if 'ht' in n:
        fcn.SetParameters(0, 1, 900, 100)
    else:
        fcn.SetParameters(0, 1, 48, 5)
    fcn.SetParLimits(1, 0, 1)
    fcn.SetLineWidth(2)
    fcn.SetLineStyle(2)
    
    return fcn

def rebin_pt(h):
    #a = to_array(range(0, 100, 5) + range(100, 150, 10) + [150, 180, 220, 260, 370, 500])
    a = to_array(range(0, 500, 50))
    #a = to_array(range(0, 500, 10))
    return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)

def rebin_ht(h):
    #a = to_array(range(0, 500, 20) + range(500, 1000, 50) + range(1000, 1500, 100) + range(1500, 2000, 250) + [2000, 3000, 5000])
    #a = to_array(range(0, 1000, 20) + [2000, 3000, 5000])
    a = to_array(range(0, 1000, 100) + [2000, 3000, 5000])
    hnew = h.Rebin(len(a)-1, h.GetName() + '_rebin', a)
    move_overflow_into_last_bin(hnew)
    return hnew

def get(f, kind, n):
    def rebin(h):
        return h
    if 'pt' in n:
        rebin = rebin_pt
    elif 'ht' in n:
        rebin = rebin_ht
    num_hist = f.Get("%s_%s_nums" % (n,kind))
    den_hist = f.Get("%s_%s_dens" % (n,kind))
    if num_hist is None or den_hist is None :
        return None, None

    return rebin(num_hist), rebin(den_hist)

def num_den_draw(num, den):
    x = []
    for h in num, den:
        h2 = h.Clone(num.GetName() + '_drawscaled')
        #h2.Scale(1., 'width')
        x.append(h2)
    num, den = x
    num.SetFillColor(den.GetLineColor())
    num.SetFillStyle(3004)
    den.Draw('e')
    num.Draw('hist same')
    return num, den

########################################################################

kinds = ['dibjet', 'tribjet']
ns = ['h_bjet_leg_pt', 'h_bjet_leg_eta']

for kind in kinds :
    print kind
    for n in ns :

        print n

        subname = '%s_%s' % (kind, n) if kind else n
        bkg_num, bkg_den = None, None
        sum_scaled_nums, sum_scaled_dens = 0., 0.
        sum_scaled_nums_var, sum_scaled_dens_var = 0., 0.
        
        reses = []

        for sample in bkg_samples :
            subsubname = subname + '_' + sample.name

            num, den = sample.num, sample.den = get(sample.f, kind, n)

            if save_more:
                x = num_den_draw(num, den)
                ps.save(subsubname + '_num_den',log=True)


            if den.Integral():
                rat = histogram_divide(num, den)
                rat.Draw('AP')
                if 'pt' in n or 'ht' in n:
                    rat.GetXaxis().SetLimits(0, draw_limits(kind,n)[1])

                fcn = make_fcn('f_' + subsubname, kind, n)
                res = rat.Fit(fcn, fitopt)
                reses.append(res)
                if save_more:
                    rat.SetTitle('')
                    ps.c.Update()
                    ps.save(subsubname)
            else:
                reses.append(None)

            sample.total_events = -1
            scale = sample.partial_weight(sample.f) * int_lumi

            print '%s (%f)' % (sample.name, scale)
            #ib = num.FindBin(lump_lower)
            ib = 1
            ni = num.Integral(ib, 10000)
            di = den.Integral(ib, 10000)
            sum_scaled_nums += ni*scale
            sum_scaled_dens += di*scale
            sum_scaled_nums_var += scale**2 * ni
            sum_scaled_dens_var += scale**2 * di
            print '   %10i %10i %10.2f %10.2f  %.6f [%.6f, %.6f]' % ((ni, di, ni*scale, di*scale) + clopper_pearson(ni, di))
            #res.Print()

            num.Scale(scale)
            den.Scale(scale)
            if bkg_num is None and bkg_den is None:
                bkg_num = num.Clone('bkg_num')
                bkg_den = den.Clone('bkg_den')
            else:
                bkg_num.Add(num)
                bkg_den.Add(den)

        if sum_scaled_dens_var > 0 and sum_scaled_dens > 0 and sum_scaled_nums_var > 0:
            bkg_effective_den = sum_scaled_dens**2 / sum_scaled_dens_var
            bkg_effective_num = sum_scaled_nums / sum_scaled_dens * bkg_effective_den
            print 'sum bkgs with effective n =', bkg_effective_den
            print '   %10.2f %10.2f %10s %10s  %.6f [%.6f, %.6f]' % ((sum_scaled_nums, sum_scaled_dens, '', '') + clopper_pearson(bkg_effective_num, bkg_effective_den))
            print '+- %10.2f %10.2f' % (sum_scaled_nums_var**0.5, sum_scaled_dens_var**0.5)

        if 'gen' in n:
            continue

        if save_more:
            x = num_den_draw(bkg_num, bkg_den)
            ps.save(subname + '_bkg_num_den', log=True)

        print 'data' #, data_num.GetEntries(), data_den.GetEntries()
        data_num, data_den = get(data_f, kind, n)
        if save_more:
            x = num_den_draw(data_num, data_den)
            ps.save(subname + '_data_num_den', log=True)

        #ib = data_num.FindBin(lump_lower)
        ib = 1
        ni = data_num.Integral(ib, 10000)
        di = data_den.Integral(ib, 10000)
        print '   %10i %10i %10s %10s  %.6f [%.6f, %.6f]' % ((ni, di, '', '') + clopper_pearson(ni, di))
        print '+- %10.2f %10.2f' % (ni**0.5, di**0.5)
        if sum_scaled_nums and sum_scaled_dens:
            print 'data/mc:'
            print '   %10.4f %10.4f' % (ni/sum_scaled_nums, di/sum_scaled_dens)
            ivnum = clopper_pearson_poisson_means(ni, sum_scaled_nums)
            ivden = clopper_pearson_poisson_means(di, sum_scaled_dens)
            # FIXME weird edge case, probably empty hist that I should protect against a better way
            if not (ivnum[1] is None or ivnum[2] is None or ivden[1] is None or ivden[2] is None) :
                print '+- %10.4f %10.4f' % ((ivnum[2] - ivnum[1])/2, (ivden[2] - ivden[1])/2)

        if True :
            print 'signal'
            sig_num, sig_den = get(sig_samples[0].f, kind, n)
            if save_more:
                x = num_den_draw(sig_num, sig_den)
                ps.save(subname + '_sig_num_den', log=True)
            sig_rat = histogram_divide(sig_num, sig_den, use_effective=True) if sig_num and sig_den else None

        data_rat = histogram_divide(data_num, data_den)
        bkg_rat = histogram_divide(bkg_num, bkg_den, use_effective=True) if bkg_num and bkg_den else None

        #for r in (data_rat, bkg_rat):
        for r in (data_rat, bkg_rat, sig_rat):
        #for r in (bkg_rat, ):
            if not r:
                continue
            if 'pt' in n and not 'leg' in n:
                i = int(n.split('_')[-1])
                k = 'b' if 'bjet' in n else ''
                r.SetTitle(';%i%s %sjet p_{T} (GeV);efficiency' % (i, "st" if i == 1 else "nd" if i == 2 else "rd" if i == 3 else "th", k))
            elif 'pt' in n and 'leg' in n:
                k = 'b' if 'bjet' in n else ''
                r.SetTitle(';%sjet leg p_{T} (GeV);efficiency' % (k))
            elif 'ht' in n:
                r.GetXaxis().SetLimits(draw_limits(kind, n)[0],draw_limits(kind, n)[1])
                k = ''
                r.SetTitle(';%s H_{T} (GeV);efficiency' % k)
            elif 'njets' in n:
                r.GetXaxis().SetLimits(draw_limits(kind, n)[0],draw_limits(kind, n)[1])
                k = ''
                r.SetTitle(';%s # selected jets;efficiency' % k)
            elif 'nbjets' in n:
                r.GetXaxis().SetLimits(draw_limits(kind, n)[0],draw_limits(kind, n)[1])
                k = ''
                r.SetTitle(';%s # selected bjets;efficiency' % k)
            elif 'eta' in n and not 'leg' in n:
                i = int(n.split('_')[-1])
                r.GetXaxis().SetLimits(draw_limits(kind, n)[0],draw_limits(kind, n)[1])
                k = 'b' if 'bjet' in n else ''
                r.SetTitle(';%i%s %sjet #eta;efficiency' % (i, "st" if i == 1 else "nd" if i == 2 else "rd" if i == 3 else "th", k))
            elif 'eta' in n and 'leg' in n:
                r.GetXaxis().SetLimits(draw_limits(kind, n)[0],draw_limits(kind, n)[1])
                k = 'b' if 'bjet' in n else ''
                r.SetTitle(';%sjet #eta;efficiency' % (k))
            r.GetHistogram().SetMinimum(0)
            r.GetHistogram().SetMaximum(1.05)
            r.SetLineWidth(2)

        data_rat.SetMarkerStyle(20)
        data_rat.Draw('AP')
        
        #ROOT.gStyle.SetOptFit(1111)
        ROOT.gStyle.SetOptFit(0)
        data_fcn = make_fcn('f_data', kind, n)
        data_fcn.SetLineColor(ROOT.kBlack)
        data_res = data_rat.Fit(data_fcn, fitopt)
        print '\ndata:'
        data_res.Print()
        if bkg_rat:
            bkg_fcn = make_fcn('f_bkg', kind, n)
            bkg_fcn.SetLineColor(2)
            bkg_res = bkg_rat.Fit(bkg_fcn, fitopt)
            print '\nbkg:'
            bkg_res.Print()

            bkg_rat.SetFillStyle(3004)
            bkg_rat.SetFillColor(2)
            bkg_rat.SetLineColor(2)
            bkg_rat.SetMarkerColor(2)
            bkg_rat.SetMarkerStyle(24)
            bkg_rat.Draw('pE2 same')

        if sig_rat:
            sig_fcn = make_fcn('f_sig', kind, n)
            sig_fcn.SetLineColor(4)
            sig_res = sig_rat.Fit(sig_fcn, fitopt)
            print '\nsig:'
            sig_res.Print()

            sig_rat.SetFillStyle(3005)
            sig_rat.SetFillColor(4)
            sig_rat.SetLineColor(4)
            sig_rat.SetMarkerColor(4)
            sig_rat.SetMarkerStyle(24)
            sig_rat.Draw('pE2 same')

        ps.c.Update()
        ps.save(subname)

        ratios_plot("ratio_"+subname, [bkg_rat, data_rat], ps, res_fit=False, res_divide_opt={'confint': propagate_ratio, 'force_le_1': False}, res_y_range=(0.5,1.5), y_range=(0,1))
        #ratios_plot("ratio_"+subname+"_with_signal", [bkg_rat, data_rat, sig_rat], ps, res_fit=False, res_divide_opt={'confint': propagate_ratio, 'force_le_1': False}, res_y_range=(0.5,1.5))

        print '\nsignals'
        for sample in sig_samples:
            if sample.f:
                sig_num, sig_den = get(sample.f, kind, n)
                #ib = sig_num.FindBin(lump_lower)
                ib = 1
                ni = sig_num.Integral(ib, 10000)
                di = sig_den.Integral(ib, 10000)
                print '   %10i %10i %10s %10s  %.6f [%.6f, %.6f]' % ((ni, di, '', '') + clopper_pearson(ni, di))
                print '+- %10.2f %10.2f' % (ni**0.5, di**0.5)


