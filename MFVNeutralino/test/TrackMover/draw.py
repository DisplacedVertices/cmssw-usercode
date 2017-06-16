#!/usr/bin/env python

extra_factor = 1. #17600/3629.809
use_effective = True

from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.TH1.AddDirectory(0)

def get_em(fn, alpha=1-0.6827):
    f = ROOT.TFile(fn)
    d = {}
    integ = None
    l = []
    ltmp = []

    def skip(name, obj):
        return obj.GetName() in ('h_norm', 'h_weight', 'h_npu') #or name in ('nlep')

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
             'nseltracks' == name or \
             'ntracks' == name or \
             'pvntracks' == name or \
             'pvrho' == name or \
             'pvsumpt2' == name or \
             'pvx' == name or \
             'pvy' == name or \
             'pvz' == name:
            obj.Rebin(4)
        return obj

    integ = f.Get('h_weight').Integral(0,100000)
    print 'integral:', integ

    for key in f.GetListOfKeys():
        name = key.GetName()
        if '_' not in name:
            continue
        obj = f.Get(name)
        sub = name.split('_')[1]

        if skip(sub, obj):
            continue

        obj = rebin(sub, obj)

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
            g = histogram_divide(num, den, confint_params=(alpha,), use_effective=use_effective)
            g.SetTitle('')
            g.GetXaxis().SetTitle(num.GetXaxis().GetTitle())
            g.GetYaxis().SetTitle('efficiency')
            rat_name = name.replace('_num', '_rat')

            d[rat_name] = g
            l.append(rat_name)

            if 'nlep' in name: # nlep is just a convenient one to take the integral of, can be any
                cutset = name.split('nlep')[0]
                num_err, den_err = ROOT.Double(), ROOT.Double()
                num_int = num.IntegralAndError(0, 100, num_err)
                den_int = den.IntegralAndError(0, 100, den_err)
                cutsets.append((cutset, num_int, num_err, den_int, den_err))


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
        print '%40s %.2f [%.2f, %.2f] +%.2f -%.2f' % (cutset, ef, lo, hi, hi-ef, ef-lo)
        c.append((cutset, ef, (hi-lo)/2))
        g = histogram_divide(num, den, confint_params=(alpha,), use_effective=use_effective)
        rat_name = cutset + '_rat'
        d[rat_name] = g
        l.append(rat_name)

    return f, l, d, c, integ

def comp(ex, fn1='data.root', fn2='mc.root', is_data_mc=True):
    print ex
    if ex:
        ex = '_' + ex
    ps = plot_saver(plot_dir('trackmover_tmp' + ex), size=(600,600), log=False)

    print 'is_data_mc:', is_data_mc
    print 'fn1:', fn1
    f_1, l_1, d_1, c_1, integ_1 = get_em(fn1)
    print 'fn2:', fn2
    f_2, l_2, d_2, c_2, integ_2 = get_em(fn2)
    assert l_1 == l_2
    assert len(d_1) == len(d_2)
    l = l_1

    scale = integ_1 / integ_2
    print 'scale is %f = %f * (extra_factor=%f)' % (scale, scale/extra_factor, extra_factor)
    print 'diff (mc - data)'
    for i, (cutset, eff_1, eeff_1) in enumerate(c_1):
       cutset_2, eff_2, eeff_2 = c_2[i]
       assert cutset == cutset_2
       print '%40s %.2f +- %.2f' % (cutset, eff_2 - eff_1, (eeff_2**2 + eeff_1**2)**0.5)

    for name in l:
        data = d_1[name]
        mc   = d_2[name]
        both = (data, mc)

        if name.endswith('_rat') or (not name.endswith('_num') and not name.endswith('_den')):
            data.SetLineWidth(2)
            data.SetMarkerStyle(20)
            data.SetMarkerSize(0.8)
            data.SetLineColor(ROOT.kBlack)

            mc.SetFillStyle(3001)
            mc.SetMarkerStyle(24)
            mc.SetMarkerSize(0.8)
            mc.SetMarkerColor(2)
            mc.SetLineColor(2)
            mc.SetFillColor(2)

            if name.endswith('_rat'):
                for g in both:
                    g.GetYaxis().SetTitle('efficiency')
                objs = [(mc, 'PE2'), (data, 'P')]
                y_range = (0, 1.05)
                statbox_size = None
            else:
                objs = [mc, data]
                y_range = None
                statbox_size = (0.2,0.2)

            ratios_plot(name, 
                        objs,
                        plot_saver=ps,
                        y_range=y_range,
                        res_y_range=0.05,
                        res_y_title='data/MC',
                        res_fit=False,
                        res_divide_opt={'confint': propagate_ratio, 'force_le_1': False, 'allow_subset': True}, #name in ('all_jetsumntracks_rat', )},
                        statbox_size=statbox_size,
                        )

import sys
x = sys.argv[1]
comp(x, '%s/JetHT2016.root'%x, '%s/background.root'%x)
#comp('mctruth', 'mfv_neu_tau01000um_M0800.root', 'mfv_neu_tau01000um_M0800.root')
