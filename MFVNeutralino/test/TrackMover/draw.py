#!/usr/bin/env python

# py ~/cmswork/Tools/python/Samples.py merge qcdht0500.root qcdht1000.root  ttbar*root -3629.809

from array import array
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.TH1.AddDirectory(0)

def arr(*l):
    return array('d', l)

def rebin(obj, binning):
    b = arr(binning)
    return obj.Rebin(len(b)-1, obj.GetName(), b)

def get_em(fn, alpha=1-0.6827):
    f = ROOT.TFile(fn)
    d = {}

    l = []
    ltmp = []

    def skip(name, obj):
        if 'jetsumntracks' in name:
            return True
        return False

    def rebin(name, obj):
        #print name
        if 'jetdravg_' in name or \
           'jetdrmax_' in name or \
           'npv_' in name or \
           'sumht_' in name:
            obj.Rebin(2)
        elif 'jetsume_' in name or \
             'movedist2_' in name or \
             'movedist3_' in name or \
             'nseltracks_' in name or \
             'ntracks_' in name or \
             'pvntracks_' in name or \
             'pvrho_' in name or \
             'pvsumpt2_' in name or \
             'pvx_' in name or \
             'pvy_' in name or \
             'pvz_' in name:
            obj.Rebin(4)
        return obj

    for key in f.GetListOfKeys():
        name = key.GetName()
        obj = f.Get(name)

        if skip(name, obj):
            continue

        obj = rebin(name, obj)

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
            g = histogram_divide(num, den, confint_params=(alpha,))
            g.SetTitle('')
            g.GetXaxis().SetTitle(num.GetXaxis().GetTitle())
            g.GetYaxis().SetTitle('efficiency')
            rat_name = name.replace('_num', '_rat')

            d[rat_name] = g
            l.append(rat_name)

            if 'nlep' in name:
                cutset = name.split('nlep')[0]
                num_err, den_err = ROOT.Double(), ROOT.Double()
                num_int = num.IntegralAndError(0, 100, num_err)
                den_int = den.IntegralAndError(0, 100, den_err)
                cutsets.append((cutset, num_int, num_err, den_int, den_err))

    cutsets.sort()
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
        g = histogram_divide(num, den, confint_params=(alpha,))
        rat_name = cutset + '_rat'
        d[rat_name] = g
        l.append(rat_name)

    return f, l, d

def test():
    ps = plot_saver('plots/trackmover_tmp', log=False)

    f,l,d = get_em('qcdht0250.root')
    for name in l:
        if name.endswith('_rat'):
            g = d[name]
            g.SetLineWidth(2)
            g.SetMarkerStyle(20)
            g.SetMarkerSize(0.8)
            g.Draw('AP')
            g.GetYaxis().SetRangeUser(0., 1.05)
            ps.save(name)
        
def data_mc_comp(ex, mc_fn):
    print ex
    ps = plot_saver('plots/trackmover_' + ex, size=(600,600), log=False)

    print 'data'
    f_data, l_data, d_data = get_em('data.root')
    print 'mc'
    f_mc,   l_mc,   d_mc   = get_em(mc_fn)
    assert l_data == l_mc
    assert len(d_data) == len(d_mc)
    l = l_data

    for name in l:
        data = d_data[name]
        mc   = d_mc  [name]
        both = (data, mc)

        if name.endswith('_rat'):
            data.SetLineWidth(2)
            data.SetMarkerStyle(20)
            data.SetMarkerSize(0.8)
            data.Draw('AP')

            mc.SetFillStyle(3001)
            mc.SetFillColor(2)
            mc.Draw('E2 same')

            for g in both:
                g.GetYaxis().SetRangeUser(0., 1.05)

            ps.save(name)

        elif not name.endswith('_num') and not name.endswith('_den'):
            data.Draw()
            mc.SetLineColor(ROOT.kRed)
            mc.Draw('sames')

            ps.c.Update()
            for i,h in enumerate((data, mc)):
                h.SetLineWidth(2)
                differentiate_stat_box(h, i, new_size=(0.2,0.2))

            ps.save(name)

#data_mc_comp('32_all', 'merge_all.root')
#data_mc_comp('32_gt500', 'merge_gt500.root')
data_mc_comp('21_gt250_leadweight1', 'merge_gt250_leadweight1.root')
data_mc_comp('21_gt500_leadweight1', 'merge_gt500_leadweight1.root')
data_mc_comp('21_gt500_leadweight1_ttbup20pc', 'merge_gt500_leadweight1_ttbup20pc.root')
data_mc_comp('21_gt500_leadweight1_ttbup100pc', 'merge_gt500_leadweight1_ttbup100pc.root')
