#!/usr/bin/env python

mc_scale_factor = 1.
use_effective = True

from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.TH1.AddDirectory(0)

variables = ['_movedist2_','_ht_','_njets_', '_nmuons_', '_muon_pT_', '_muon_abseta_', '_muon_iso_', '_muon_zoom_iso_', '_muon_absdxybs_', '_muon_nsigmadxybs_', '_neles_', '_ele_pT', '_ele_abseta_', '_ele_iso_', '_ele_zoom_iso_', '_ele_absdxybs_', '_ele_nsigmadxybs', '_met_pT_', '_w_pT_', '_w_mT_', '_z_pT_', '_z_m_', 'lnu_absphi', '_wjet_dphi_', '_zjet_dphi_', '_jet_asymm_','_vtx_unc_','_jet_dr_','_jet_deta_','_jet_dphi_','_jet_dind_','_pt0_','_pt1_','_ntks_j0_','_ntks_j1_','_nmovedtracks_','_dphi_sum_j_mv_'] 

def get_em(fn, scale=1., alpha=1-0.6827):
    f = ROOT.TFile.Open(fn)
    d = {}
    integ = None
    l = []
    ltmp = []

    def skip(name, obj):
        return not obj.Class().GetName().startswith('TH1') or obj.GetName() in ('h_norm', 'h_weight', 'h_npu') #or name in ('nlep')

    def rebin(name, obj):
        return obj
        if 'jetdravg' == name or \
           'jetdrmax' == name or \
           'npv' == name or \
           'ht' == name:
            obj.Rebin(2)
        elif 'jetsume' == name or \
             'movedist2' == name or \
             'movedist3' == name or \
             'nmovedtracks' == name or \
             'ntracks' == name or \
             'pvntracks' == name or \
             'pvrho' == name or \
             'pvscore' == name or \
             'pvx' == name or \
             'pvy' == name or \
             'pvz' == name:
            obj.Rebin(4)
        return obj

    hdummy = f.Get('h_weight')
    integ = hdummy.Integral(0,hdummy.GetNbinsX()+2)
    print 'integral:', integ

    for key in f.GetListOfKeys():
        name = key.GetName()
        if '_' not in name:
            continue
        obj = f.Get(name)
        sub = name.split('_')[1]

        if skip(sub, obj):
            continue

        obj.Scale(scale)
        obj = rebin(sub, obj)
        Isnametoplot = False
        for var in variables:
           if var in name:
             Isnametoplot = True
             break
        if not Isnametoplot:
           continue
        if name.startswith('h_'):
            l.append(name)
        else:
            ltmp.append(name)

        d[name] = obj

    ltmp.sort()

    cutsets = []

    for name in ltmp:
      if name.endswith('_num'):
          num = d[name]
          den = d[name.replace('_num', '_den')]
          g =  den #histogram_divide(num, den, confint_params=(alpha,), use_effective=use_effective)
          g.SetTitle('')
          g.GetXaxis().SetTitle(num.GetXaxis().GetTitle())
          g.GetYaxis().SetTitle('efficiency')
          rat_name = name.replace('_num', '_den')

          d[rat_name] = g
          l.append(rat_name)
          
          if '_ht_' in name: # nvtx is just a convenient one to take the integral of, can be any
              cutset = name.split('_ht_')[0]
              print name, cutset
              num_err, den_err = ROOT.Double(), ROOT.Double()
              num_int = num.IntegralAndError(0, 100, num_err)
              den_int = den.IntegralAndError(0, 100, den_err)
              cutsets.append((cutset, num_int, num_err, den_int, den_err))

    if not cutsets:
        raise ValueError('no cutsets?')
    cutsets.sort()
    c = []
    for cutset, num_int, num_err, den_int, den_err in cutsets:
        num = ROOT.TH1F(cutset + '_num', '', 1, 0, 1)
        den = ROOT.TH1F(cutset + '_den', '', 1, 0, 1)
        num.SetBinContent(1, num_int)
        num.SetBinError  (1, num_err)
        den.SetBinContent(1, den_int)
        den.SetBinError  (1, den_err)
        ef, lo, hi = clopper_pearson(num_int, den_int, alpha)
        ef, lo, hi = 100*ef, 100*lo, 100*hi
        print '%40s %5.2f [%5.2f, %5.2f] +%.2f -%.2f' % (cutset, ef, lo, hi, hi-ef, ef-lo)
        c.append((cutset, ef, (hi-lo)/2))
        g = den #histogram_divide(num, den, confint_params=(alpha,), use_effective=use_effective)
        rat_name = cutset + '_den'
        d[rat_name] = g
        l.append(rat_name)

    return f, l, d, c, integ

def comp(ex, fn1='data.root', fn2='ttbar.root', fn3='mergedqcd.root', fn4='dyjets.root', fn5 = 'wjets_amcatnlo.root', Isshort='dummy', whichlep='Muon'):
    assert ex
    ps = plot_saver(plot_dir('TrackMover_' + ex), size=(600,600), log=True)

    print ex
    print 'fn1:', fn1
    f_1, l_1, d_1, c_1, integ_1 = get_em(fn1)
    print 'fn2:', fn2
    f_2, l_2, d_2, c_2, integ_2 = get_em(fn2, scale=mc_scale_factor)
    assert l_1 == l_2
    assert len(d_1) == len(d_2)
    print 'fn3:', fn3
    f_3, l_3, d_3, c_3, integ_3 = get_em(fn3)
    f_4, l_4, d_4, c_4, integ_4 = get_em(fn4)
    f_5, l_5, d_5, c_5, integ_5 = get_em(fn5)
    #f_6, l_6, d_6, c_6, integ_6 = get_em(fn6)
    l = l_1

    scale = integ_1 / integ_2
    print 'scale is %f = %f * (mc_scale_factor=%f)' % (scale, scale/mc_scale_factor, mc_scale_factor)
    print 'diff (mc - data)'
    for i, (cutset, eff_1, eeff_1) in enumerate(c_1):
       cutset_2, eff_2, eeff_2 = c_2[i]
       assert cutset == cutset_2
       print '%40s %5.2f +- %5.2f' % (cutset, eff_2 - eff_1, (eeff_2**2 + eeff_1**2)**0.5)
    for name in l:
        data = d_1[name]
        mc   = d_2[name]
        mc2  = d_3[name]
        mc3  = d_4[name]
        mc4 = d_5[name]
        #signal = d_6[name]
        tot = (data, mc, mc2, mc3, mc4)
        if not name.startswith('nocuts_') or "ele" in name:
            continue
        if name.endswith('_den'): #or (not name.endswith('_num') and not name.endswith('_den')):
            
            ROOT.gStyle.SetOptStat(2211) #FIXME
          
            if (whichlep == "Muon"):
              data.SetName("SingleMuon 2017")
            else:
              data.SetName("SingleElectron 2017")
            data.ClearUnderflowAndOverflow()
            data.SetLineWidth(2)
            data.SetMarkerStyle(20)
            data.SetMarkerSize(0.8)
            data.SetLineColor(ROOT.kBlack)
           
            mc.SetName("MC other bkg. 2017")
            mc.ClearUnderflowAndOverflow()
            mc.SetFillStyle(3001)
            mc.SetMarkerStyle(24)
            mc.SetMarkerSize(0.8)
            mc.SetMarkerColor(8)
            mc.SetLineColor(8)
            mc.SetFillColor(8)

            mc2.SetName("MC combined QCD 2017")
            mc2.ClearUnderflowAndOverflow()
            mc2.SetFillStyle(3001)
            mc2.SetMarkerStyle(24)
            mc2.SetMarkerSize(0.8)
            mc2.SetMarkerColor(6)
            mc2.SetLineColor(6)
            mc2.SetFillColor(6)
            
            mc3.SetName("MC Drell-Yan 2017")
            mc3.ClearUnderflowAndOverflow()
            mc3.SetFillStyle(3001)
            mc3.SetMarkerStyle(24)
            mc3.SetMarkerSize(0.8)
            mc3.SetMarkerColor(2)
            mc3.SetLineColor(46)
            mc3.SetFillColor(46)

            mc4.SetName("MC NLO (W+->lnu)+jets 2017")
            mc4.ClearUnderflowAndOverflow()
            mc4.SetFillStyle(3001)
            mc4.SetMarkerStyle(24)
            mc4.SetMarkerSize(0.8)
            mc4.SetMarkerColor(2)
            mc4.SetLineColor(2)
            mc4.SetFillColor(2)
            
            """
            signal.SetName("MC (W+->lnu)H->4d 2017")
            signal.ClearUnderflowAndOverflow()
            signal.SetLineWidth(2)
            signal.SetMarkerStyle(24)
            signal.SetMarkerSize(0.8)
            signal.SetMarkerColor(4)
            signal.SetLineColor(4)
            """

            x_range = None
            y_range = None
            hist_objs = [data, mc4, mc3, mc2, mc]
            statbox_size = (0.2,0.2)
            if name.endswith('_den'):
                for g in tot:
                    g.GetYaxis().SetTitle('# of entries')
                #objs = [(mc3, 'PE2'), (data, 'P'), (mc2, 'P'), (mc, 'P'),(signal, 'P')]
                #objs = [(mc3, 'PE2'), (mc2, 'P'), (mc, 'P')]
                objs = [mc4, mc3, mc2, mc]
                #y_range = (0, 1.05)
                statbox_size = (0.2,0.1)
            if "bs2derr" in name:
                x_range = (0, 0.01)
            if "_vtx_unc_" in name:
                x_range = (0,0.03)
            if Isshort == "short" and '_movedist2_' in name:
                x_range = (0,0.5)

            """ 
            ratios_plot(name,
                        hist_objs,
                        plot_saver=ps,
                        x_range=x_range,
                        y_range=y_range,
                        res_y_range=0.10,
                        res_y_title='ratio to MC',
                        res_fit=False,
                        res_divide_opt={'confint': propagate_ratio, 'force_le_1': False, 'allow_subset': True}, #name in ('all_jetsumntracks_rat', )},
                        res_lines=1.,
                        statbox_size=statbox_size,
                        )
            
            """ 
            #wjetstolnu_amcatnlo_2017 : 0.00250943282198
            #dyjetstollM10_2017 : 0.000224017744928
            #dyjetstollM50_2017 : 5.23357647837e-05
            #ttbar_2017 : 3.37956553194e-06
            #ww_2017 : 4.77239816156e-06
            #zz_2017 : 4.48301329394e-06
            #wz_2017 :3.55258076973e-06
            data_mc_comparison(name,
                        hist_objs,
                        background_samples = objs,
                        #signal_samples = [signal],
                        data_samples = [data],
                
                        bkg_partial_weights = [0.00250943282198, 1.0/(40163.29), 1.0/(40163.29), 1.0/(40163.29)],
                        #wjetstolnu_amcatnlo_2017, dyjetstollM10+50_2017, combined qcd, other bkg.
                        #sig_partial_weights = [5.65661819127e-08],
                        plot_saver=ps,
                        int_lumi = 40163.29*0.1, #for 2017 only
                        normalize_to_data = False,
                        canvas_size = (600, 600),
                        x_title = mc.GetXaxis().GetTitle(), 
                        x_range=x_range,
                        #legend_pos = (0.5,0.7,0.88,0.9),
                        #y_range_max=y_range,
                        statbox_size=statbox_size,
                        )
             
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 9:
        sys.exit('usage: python draw.py tag_for_plots fn1 fn2 f3 f4 f5 f6[fn2 scale factor] tag_for_300um tag_which_lep')

    ex = sys.argv[1]
    fn1 = sys.argv[2]
    fn2 = sys.argv[3]
    fn3 = sys.argv[4]
    fn4 = sys.argv[5]
    fn5 = sys.argv[6]
    #fn6 = sys.argv[7]
    Isshort = sys.argv[7]
    whichlep = sys.argv[8]
    if len(sys.argv) > 9:
        mc_scale_factor = float(sys.argv[9])
    comp(ex, fn1, fn2, fn3, fn4, fn5, Isshort, whichlep)
