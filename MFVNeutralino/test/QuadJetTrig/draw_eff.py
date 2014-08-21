import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Samples import *

set_style()
ROOT.gStyle.SetOptStat(0)
ps = plot_saver('plots/QuadJetTrigEff')
ROOT.TH1.AddDirectory(0)

root_dir = 'crab/QuadJetTrigEff'

int_lumi = 17241.
data_fn = os.path.join(root_dir, 'SingleMu2012BCD.partial.root')
data_f = ROOT.TFile(data_fn)

kinds = 'Mu0pf Mu0cl Mu0cl3'.split()
ns = 'h_jet_pt_3 h_jet_pt_4 h_jet_pt_5 h_jet_eta_3 h_jet_eta_4 h_jet_eta_5'.split()

kinds = ['Mu0pf', 'Mu0cl3', 'Mu1pf', 'Mu1cl3']
ns = ['h_jet_pt_4', 'h_jet_pt_5', 'h_jet_sumht']

for kind in kinds:
    print kind
    for n in ns:
        print n
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

        data_num, data_den = get(data_f, n)

        bkg_samples = [wjetstolnu, dyjetstollM10, dyjetstollM50, ttbarsemilep, ttbardilep, ttbarhadronic, qcdmupt15]
        n_bkg_samples = len(bkg_samples)
        bkg_num, bkg_den = None, None
        reses = []
        for sample in bkg_samples:
            subsubname = subname + '_' + sample.name

            sample.fn = os.path.join(root_dir, sample.name + '.root')
            sample.f = ROOT.TFile(sample.fn)
            num, den = sample.num, sample.den = get(sample.f, n)
            rat = histogram_divide(num, den)
            rat.Draw('AP')
            if 'pt' in n:
                rat.GetXaxis().SetLimits(0, 600)
            elif 'sumht' in n:
                rat.GetXaxis().SetLimits(0, 3000)
            #fcn = ROOT.TF1('f_' subsubname, 'pol0', 60, 500)
            fcn = ROOT.TF1('f_' + subsubname, '[0] + [1]*(0.5 + 0.5 * TMath::Erf((x - [2])/[3]))', 20, 500)
            fcn.SetParameters(0, 1, 48, 5)
            fcn.SetParLimits(1, 0, 1)
            fcn.SetLineWidth(1)
            res = rat.Fit(fcn, 'RQS')
            reses.append(res)
            
            ps.save(subsubname)
            sample.total_events = -1
            scale = sample.partial_weight * int_lumi

            print sample.name, num.GetEntries(), den.GetEntries(), scale
            ll = 60 if 'pf' not in kind else 120
            ni = num.Integral(num.FindBin(ll), 1000)
            di = den.Integral(num.FindBin(ll), 1000)
            print '   ', ni, di, clopper_pearson(ni, di)
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
                hpar.SetBinContent(isam+1, reses[isam].Parameter(ipar))
                hpar.SetBinError  (isam+1, reses[isam].ParError (ipar))
                hpar.GetXaxis().SetBinLabel(isam+1, sample.name)
            hpar.Draw('hist e')
            hpar.SetLineWidth(2)
            fcnpar = ROOT.TF1('f_'  + subsubname, 'pol0')
            fcnpar.SetLineWidth(1)
            hpar.Fit(fcnpar, 'Q')
            ps.save(subsubname)

        print 'data', data_num.GetEntries(), data_den.GetEntries()
        ll = 60 if 'pf' not in kind else 120
        ni = data_num.Integral(num.FindBin(ll), 1000)
        di = data_den.Integral(num.FindBin(ll), 1000)
        print '   ', ni, di, clopper_pearson(ni, di)

        data_rat = histogram_divide(data_num, data_den)
        bkg_rat = histogram_divide(bkg_num, bkg_den)

        data_rat.Draw('AP')
        ROOT.gStyle.SetOptFit(1111)
        fcn = ROOT.TF1('f_data', '[0] + [1]*(0.5 + 0.5 * TMath::Erf((x - [2])/[3]))', 20, 300)
        fcn.SetParameters(0, 1, 48, 5)
        fcn.SetParLimits(1, 0, 1)
        fcn.SetLineWidth(1)
        res = data_rat.Fit(fcn, 'RQS')
        res.Print()

        bkg_rat.SetFillStyle(3002)
        bkg_rat.SetFillColor(2)
        bkg_rat.Draw('E2 same')

        ps.save(subname)
