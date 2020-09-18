import sys, os
from array import array
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.Tools.Samples import *

version = '2017v0p4'
zoom = False #(0.98,1.005)
save_more = True
data_only = False
use_qcd = False
#trig_path = "DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV"
trig_path = "PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV"
#postfix = "_inc_tight"
postfix = "_inc_tight_meas_leg"

#postfix = "_ttbar_tight"
#postfix = "_inc"
#postfix = "_ttbar"

num_dir, den_dir = "num"+trig_path+postfix, "den"+trig_path+postfix
#num_dir, den_dir = "num", "den"

#num_dir, den_dir = 'numDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc', 'denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc'
#num_dir, den_dir = 'numDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_ttbar', 'denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_ttbar'
#num_dir, den_dir = 'numDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight', 'denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight'
#num_dir, den_dir = 'numDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_ttbar_tight', 'denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_ttbar_tight'
#num_dir, den_dir = 'numjet6pt75', 'denjet6pt75'

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
plot_path = 'TrigEff%s_%s_%s%s' % (version, num_dir, year, data_period)
if zoom:
    plot_path += '_zoom'

set_style()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ps = plot_saver(plot_dir(plot_path), size=(600,600), log=False, pdf=True)
ROOT.TH1.AddDirectory(0)

data_fn = os.path.join(root_dir, 'SingleMuon%s%s.root' % (year, data_period))
data_f = ROOT.TFile(data_fn)

if data_only:
    bkg_samples, sig_samples = [], []
else:
    if year == 2017 or year == 2018:
        #bkg_samples = [ttbar_2017]
        bkg_samples = [ttbar_2017, wjetstolnusum_2017, dyjetstollM50sum_2017, dyjetstollM10_2017, qcdmupt15_2017]
        #bkg_samples = [wjetstolnu_2017, dyjetstollM50_2017]
        #bkg_samples = [mfv_neu_tau001000um_M0400_2017]
        if use_qcd:
            bkg_samples.append(qcdmupt15_2017)
        #sig_samples = [getattr(Samples, 'mfv_neu_tau001000um_M%04i_2017' % m) for m in (400, 800, 1200, 1600)] + [Samples.mfv_neu_tau010000um_M0800_2017]
        sig_samples = [mfv_neu_tau001000um_M0400_2017] 

n_bkg_samples = len(bkg_samples)
for samples in bkg_samples, sig_samples:
    for sample in samples:
        sample.fn = os.path.join(root_dir, sample.name + '.root')
        sample.f = ROOT.TFile(sample.fn) if os.path.isfile(sample.fn) else None

########################################################################

kinds = ['']
ns = ['h_jet_ht30', 'h_jet_ht', 'h_njets', 'h_nbjets', 'h_jet_pt_1', 'h_jet_pt_2', 'h_jet_pt_3', 'h_jet_pt_4', 'h_bjet_pt_1', 'h_bjet_pt_2', 'h_bjet_pt_3', 'h_jet_eta_1', 'h_jet_eta_2', 'h_jet_eta_3', 'h_bjet_eta_1', 'h_bjet_eta_2', 'h_bjet_eta_3']

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
            return 0, 400

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
    #print kind + '%s/%s' % (num_dir, n)
    #print kind + '%s/%s' % (den_dir, n)
    num_hist = f.Get(kind + '%s/%s' % (num_dir, n))
    den_hist = f.Get(kind + '%s/%s' % (den_dir, n))
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

for kind in kinds:
    for n in ns:
        print
        print '============================================================================='
        print kind, n
        print '-----------------------'
        subname = '%s_%s' % (kind, n) if kind else n

        bkg_num, bkg_den = None, None
        sum_scaled_nums, sum_scaled_dens = 0., 0.
        sum_scaled_nums_var, sum_scaled_dens_var = 0., 0.

        reses = []
        for sample in bkg_samples:
            subsubname = subname + '_' + sample.name

            print sample.name
            print sample.f
            num, den = sample.num, sample.den = get(sample.f, kind, n)

            if save_more:
                x = num_den_draw(num, den)
                ps.save(subsubname + '_num_den',log=True)

            if den.Integral():
                rat = histogram_divide(num, den)
                rat.Draw('AP')
                if 'pt' in n:
                    rat.GetXaxis().SetLimits(0, 260)
                elif 'ht' in n:
                    rat.GetXaxis().SetLimits(0, draw_limits(kind,n)[1])

                fcn = make_fcn('f_' + subsubname, kind, n)
                res = rat.Fit(fcn, fitopt)
                reses.append(res)
                if save_more:
                    rat.SetTitle('')
                    ps.c.Update()
                    # if the fit data is empty, we don't have a stat box to move
                    if res.Get() :
                        pass
                        #move_stat_box(rat, 'inf' if zoom else (0.518, 0.133, 0.866, 0.343))
                    ps.save(subsubname)
            else:
                reses.append(None)

            sample.total_events = -1
            scale = sample.partial_weight(sample.f) * int_lumi

            print '%s (%f)' % (sample.name, scale)
            ib = num.FindBin(lump_lower)
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

        # FIXME
        if reses and False:
            pars = [reses[0].GetParameterName(i) for i in xrange(reses[0].NPar())]
            for ipar, parname in enumerate(pars):
                subsubname = subname + '_' + parname
                hpar = ROOT.TH1F(parname, '', n_bkg_samples, 0, n_bkg_samples)
                for isam, sample in enumerate(bkg_samples):
                    if not reses[isam] or not reses[isam].Get() : continue
                    #print reses[isam], reses[isam].Get()
                    #print hpar

                    #if sample.name == 'qcdmupt15' and 'Mu1' in kind:
                    #    continue
                    #print isam, reses[isam].Parameter(ipar), reses[isam].ParError(ipar)
                    hpar.SetBinContent(isam+1, reses[isam].Parameter(ipar))
                    hpar.SetBinError  (isam+1, reses[isam].ParError (ipar))
                    hpar.GetXaxis().SetBinLabel(isam+1, sample.name)
                hpar.Draw('hist e')
                hpar.SetLineWidth(2)
                fcnpar = ROOT.TF1('f_'  + subsubname, 'pol0')
                fcnpar.SetLineWidth(1)
                hpar.Fit(fcnpar, 'QS0')
                ps.c.Update()
                #move_stat_box(hpar, (0.507, 0.664, 0.864, 0.855))
                if parname == 'floor':
                    hpar.GetYaxis().SetRangeUser(0, 0.3)
                elif parname == 'ceil':
                    hpar.GetYaxis().SetRangeUser(0.2, 1)
                    #move_stat_box(hpar, (0.143, 0.147, 0.5, 0.339))
                elif parname == 'turnmu':
                    hpar.GetYaxis().SetRangeUser(0, 1500)
                elif parname == 'turnsig':
                    hpar.GetYaxis().SetRangeUser(0, 300)
                ps.save(subsubname)

        if sum_scaled_dens_var > 0 and sum_scaled_dens > 0 and sum_scaled_nums_var > 0:
            bkg_effective_den = sum_scaled_dens**2 / sum_scaled_dens_var
            bkg_effective_num = sum_scaled_nums / sum_scaled_dens * bkg_effective_den
            print 'sum bkgs with effective n =', bkg_effective_den
            print '   %10.2f %10.2f %10s %10s  %.6f [%.6f, %.6f]' % ((sum_scaled_nums, sum_scaled_dens, '', '') + clopper_pearson(bkg_effective_num, bkg_effective_den))
            print '+- %10.2f %10.2f' % (sum_scaled_nums_var**0.5, sum_scaled_dens_var**0.5)

        if 'gen' in n:
            continue

        print 'data' #, data_num.GetEntries(), data_den.GetEntries()
        data_num, data_den = get(data_f, kind, n)
        if save_more:
            x = num_den_draw(data_num, data_den)
            ps.save(subname + '_data_num_den', log=True)

        ib = data_num.FindBin(lump_lower)
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
            if 'pt' in n:
                #r.GetXaxis().SetLimits(0, 260)
                i = int(n.split('_')[-1])
                #k = 'PF' if 'pf' in kind else 'calo'
                k = 'b' if 'bjet' in n else ''
                r.SetTitle(';%i%s %sjet p_{T} (GeV);efficiency' % (i, "st" if i == 1 else "nd" if i == 2 else "rd" if i == 3 else "th", k))
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
            elif 'eta' in n:
                i = int(n.split('_')[-1])
                r.GetXaxis().SetLimits(draw_limits(kind, n)[0],draw_limits(kind, n)[1])
                k = 'b' if 'bjet' in n else ''
                r.SetTitle(';%i%s %sjet #eta;efficiency' % (i, "st" if i == 1 else "nd" if i == 2 else "rd" if i == 3 else "th", k))
            r.GetHistogram().SetMinimum(0)
            r.GetHistogram().SetMaximum(1.05)
            r.SetLineWidth(2)

        data_rat.SetMarkerStyle(20)
        data_rat.Draw('AP')
        if zoom:
            data_rat.GetYaxis().SetRangeUser(*zoom)
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
        #move_stat_box(data_rat, 'inf' if zoom else (0.518, 0.133, 0.866, 0.343))
        if bkg_rat:
            pass
            #s = move_stat_box(bkg_rat, 'inf' if zoom else (0.518, 0.350, 0.866, 0.560))
            #s.SetLineColor(2)
            #s.SetTextColor(2)

        ps.save(subname)

        print '\nsignals'
        for sample in sig_samples:
            if sample.f:
                sig_num, sig_den = get(sample.f, kind, n)
                ib = sig_num.FindBin(lump_lower)
                ni = sig_num.Integral(ib, 10000)
                di = sig_den.Integral(ib, 10000)
                print '   %10i %10i %10s %10s  %.6f [%.6f, %.6f]' % ((ni, di, '', '') + clopper_pearson(ni, di))
                print '+- %10.2f %10.2f' % (ni**0.5, di**0.5)
