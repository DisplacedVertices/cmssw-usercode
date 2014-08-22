import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Samples import *

set_style()
ROOT.gStyle.SetOptStat(0)
ps = plot_saver('plots/QuadJetTrigEff', size=(600,600), log=False)
ROOT.TH1.AddDirectory(0)

root_dir = 'crab/QuadJetTrigEff'

int_lumi = 17241.
data_fn = os.path.join(root_dir, 'SingleMu2012BCD.partial.root')
data_f = ROOT.TFile(data_fn)

kinds = 'Mu0pf Mu0cl Mu0cl3'.split()
ns = 'h_jet_pt_3 h_jet_pt_4 h_jet_pt_5 h_jet_eta_3 h_jet_eta_4 h_jet_eta_5'.split()

kinds = ['Mu0pf', 'Mu0cl3', 'Mu1pf', 'Mu1cl3']
ns = ['h_jet_pt_4', 'h_jet_pt_5'] #, 'h_jet_sumht']

#kinds = ['Mu1pf', 'Mu1cl3']
#ns = ['h_jet_pt_4', 'h_jet_pt_5']

#kinds = ['Mu1cl3']
#ns = ['h_genjet_pt_3', 'h_genjet_pt_4', 'h_genjet_pt_5', 'h_genjet_pt_6']

#kinds = ['Mu1pf']
#ns = ['h_jet_pt_4']

def make_fcn(name):
    fcn = ROOT.TF1(name, '[0] + [1]*(0.5 + 0.5 * TMath::Erf((x - [2])/[3]))', 20, 500)
    fcn.SetParNames('floor', 'ceil', 'turnmu', 'turnsig')
    fcn.SetParameters(0, 1, 48, 5)
    fcn.SetParLimits(1, 0, 1)
    fcn.SetLineWidth(1)
    return fcn

for kind in kinds:
    for n in ns:
        print
        print kind, n
        subname = '%s_%s' % (kind, n)

        def rebin_pt(h):
            a = array('d', range(0, 100, 5) + range(100, 150, 10) + [150, 180, 220, 260, 370, 500])
            return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)

        def rebin_sumht(h):
            a = array('d', range(0, 500, 20) + range(500, 1100, 60) + range(1100, 1500, 100) + range(1500, 2000, 250) + [2000, 2500, 3000])
            return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)


        def get(f,n):
            def rebin(h):
                return h
            if 'pt' in n:
                rebin = rebin_pt
            elif 'sumht' in n:
                rebin = rebin_sumht
            return rebin(f.Get(kind + 'num/%s' % n)), rebin(f.Get(kind + 'den/%s' % n))

        if 'gen' not in n:
            data_num, data_den = get(data_f, n)

        bkg_samples = [ttbarsemilep, ttbardilep, wjetstolnu, dyjetstollM50, dyjetstollM10, ttbarhadronic, qcdmupt15]
        n_bkg_samples = len(bkg_samples)
        bkg_num, bkg_den = None, None
        sum_scaled_nums, sum_scaled_dens = 0., 0.
        sum_scaled_nums_var, sum_scaled_dens_var = 0., 0.

        reses = []
        for sample in bkg_samples:
            subsubname = subname + '_' + sample.name

            sample.fn = os.path.join(root_dir, sample.name + '.root')
            sample.f = ROOT.TFile(sample.fn)
            num, den = sample.num, sample.den = get(sample.f, n)

            den.Draw()
            ps.save(subsubname + '_den')

            rat = histogram_divide(num, den)
            rat.Draw('AP')
            if 'pt' in n:
                rat.GetXaxis().SetLimits(0, 260)
            elif 'sumht' in n:
                rat.GetXaxis().SetLimits(0, 3000)
            
            fcn = make_fcn('f_' + subsubname)
            res = rat.Fit(fcn, 'RQS')
            reses.append(res)
            
            ps.save(subsubname)
            sample.total_events = -1
            scale = sample.partial_weight * int_lumi

            print '%s (%f)' % (sample.name, scale)
            if 'sumht' not in n:
                ll = 60 if 'pf' not in kind else (85 if 'pt_4' in n else 75)
                ib = num.FindBin(ll)
                ni = num.Integral(ib, 1000)
                di = den.Integral(ib, 1000)
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

        for ipar, parname in enumerate('floor ceil turnmu turnsig'.split()):
            subsubname = subname + '_' + parname
            hpar = ROOT.TH1F(parname, '', n_bkg_samples, 0, n_bkg_samples)
            for isam, sample in enumerate(bkg_samples):
                if sample.name == 'qcdmupt15' and 'Mu1' in kind:
                    continue
                hpar.SetBinContent(isam+1, reses[isam].Parameter(ipar))
                hpar.SetBinError  (isam+1, reses[isam].ParError (ipar))
                hpar.GetXaxis().SetBinLabel(isam+1, sample.name)
            hpar.Draw('hist e')
            hpar.SetLineWidth(2)
            fcnpar = ROOT.TF1('f_'  + subsubname, 'pol0')
            fcnpar.SetLineWidth(1)
            hpar.Fit(fcnpar, 'Q')
            ps.c.Update()
            move_stat_box(hpar, (0.507, 0.664, 0.864, 0.855))
            if parname == 'floor':
                hpar.GetYaxis().SetRangeUser(0, 0.3)
            elif parname == 'ceil':
                hpar.GetYaxis().SetRangeUser(0.2, 1)
                move_stat_box(hpar, (0.143, 0.147, 0.5, 0.339))
            elif parname == 'turnmu':
                hpar.GetYaxis().SetRangeUser(0, 100)
            elif parname == 'turnsig':
                hpar.GetYaxis().SetRangeUser(0, 30)
            ps.save(subsubname)

        print 'sum bkgs:'
        print '   %10.2f %10.2f %10s %10s  %.6f [%.6f, %.6f]' % ((sum_scaled_nums, sum_scaled_dens, '', '') + clopper_pearson(sum_scaled_nums, sum_scaled_dens))
        print '+- %10.2f %10.2f' % (sum_scaled_nums_var**0.5, sum_scaled_dens_var**0.5)

        if 'gen' in n:
            continue

        print 'data' #, data_num.GetEntries(), data_den.GetEntries()
        ll = 60 if 'pf' not in kind else (85 if 'pt_4' in n else 75)
        ib = num.FindBin(ll)
        ni = data_num.Integral(ib, 1000)
        di = data_den.Integral(ib, 1000)
        print '   %10i %10i %10s %10s  %.6f [%.6f, %.6f]' % ((ni, di, '', '') + clopper_pearson(ni, di))
        print '+- %10.2f %10.2f' % (ni**0.5, di**0.5)
        print 'data/mc:'
        print '   %10.4f %10.4f' % (ni/sum_scaled_nums, di/sum_scaled_dens)
        ivnum = clopper_pearson_poisson_means(ni, sum_scaled_nums)
        ivden = clopper_pearson_poisson_means(di, sum_scaled_dens)
        print '+- %10.4f %10.4f' % ((ivnum[2] - ivnum[1])/2, (ivden[2] - ivden[1])/2)

        data_rat = histogram_divide(data_num, data_den)
        bkg_rat = histogram_divide(bkg_num, bkg_den)

        for r in (data_rat, bkg_rat):
            i = int(n.split('_')[-1])
            k = 'PF' if 'pf' in kind else 'calo'
            r.SetTitle(';%ith %s jet p_{T} (GeV);efficiency' % (i, k))
            if 'pt' in n:
                r.GetXaxis().SetLimits(0, 260)
            elif 'sumht' in n:
                r.GetXaxis().SetLimits(0, 3000)
            r.GetHistogram().SetMinimum(0)
            r.GetHistogram().SetMaximum(1.1)

        data_rat.Draw('AP')
        ROOT.gStyle.SetOptFit(1111)
        data_fcn = make_fcn('f_data')
        data_res = data_rat.Fit(data_fcn, 'RQS')
        bkg_fcn = make_fcn('f_bkg')
        bkg_fcn.SetLineColor(2)
        bkg_res = bkg_rat.Fit(bkg_fcn, 'RQS')
        print 'bkg:'
        bkg_res.Print()
        print 'data:'
        data_res.Print()

        bkg_rat.SetFillStyle(3001)
        bkg_rat.SetFillColor(2)
        bkg_rat.Draw('E2 same')

        ps.c.Update()
        s = move_stat_box(bkg_rat,  (0.518, 0.350, 0.866, 0.560))
        s.SetLineColor(2)
        s.SetTextColor(2)
        move_stat_box(data_rat, (0.518, 0.133, 0.866, 0.343))

        ps.save(subname)
