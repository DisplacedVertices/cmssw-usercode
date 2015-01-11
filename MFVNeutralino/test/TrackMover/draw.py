#!/usr/bin/env python

'''
hadd.py data.root MultiJetPk2012*root
py ~/cmswork/Tools/python/Samples.py merge qcdht0500.root qcdht1000.root ttbar*root -3629.809 ; mv merge.root mc.root
'''

extra_factor = 17600/3629.809

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
    integ = None
    l = []
    ltmp = []

    def skip(name, obj):
        if 'jetsumntracks' == name:
            return True
        return False

    def rebin(name, obj):
        #print name
        if 'jetdravg' == name or \
           'jetdrmax' == name or \
           'npv' == name or \
           'sumht' == name:
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

    for key in f.GetListOfKeys():
        name = key.GetName()
        obj = f.Get(name)
        sub = name.split('_')[1]

        if skip(sub, obj):
            continue

        obj = rebin(sub, obj)

        if name.startswith('h_'):
            if name == 'h_weight':
                integ = obj.Integral(0,100000)
                print 'integral:', integ
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
        g = histogram_divide(num, den, confint_params=(alpha,))
        rat_name = cutset + '_rat'
        d[rat_name] = g
        l.append(rat_name)

    return f, l, d, c, integ

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
        
def data_mc_comp(ex, mc_fn='mc.root'):
    print ex
    if ex:
        ex = '_' + ex
    ps = plot_saver('plots/trackmover' + ex, size=(600,600), log=False)

    print 'data'
    f_data, l_data, d_data, c_data, integ_data = get_em('data.root')
    print 'mc'
    f_mc,   l_mc,   d_mc,   c_mc,   integ_mc   = get_em(mc_fn)
    assert l_data == l_mc
    assert len(d_data) == len(d_mc)
    l = l_data

    scale = integ_data / integ_mc
    print 'scale is %f = %f * (extra_factor=%f)' % (scale, scale/extra_factor, extra_factor)
    print 'diff (mc - data)'
    for i, (cutset, eff_data, eeff_data) in enumerate(c_data):
       cutset_mc, eff_mc, eeff_mc = c_mc[i]
       assert cutset == cutset_mc
       print '%40s %.2f +- %.2f' % (cutset, eff_mc - eff_data, (eeff_mc**2 + eeff_data**2)**0.5)
        
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
            mc.SetLineColor(ROOT.kRed)
            mc.Scale(scale)

            if data.GetMaximum() > mc.GetMaximum():
                data.Draw()
                mc.Draw('sames')
            else:
                mc.Draw()
                data.Draw('sames')

            ps.c.Update()
            for i,h in enumerate((data, mc)):
                h.SetLineWidth(2)
                differentiate_stat_box(h, i, new_size=(0.2,0.2))

            ps.save(name)

            ratio = data.Clone(data.GetName() + '_ratio')
            ratio.Divide(mc)
            ratio.SetLineColor(ROOT.kGreen+2)
            ratio.SetLineWidth(2)
            #ratio.Scale(max(data.GetMaximum(), mc.GetMaximum())/2.)
            ratio.Draw()
            ratio.GetYaxis().SetRangeUser(0, 3)
            #ratio.Fit('pol1', 'Q')
            ps.save(name + '_ratio')

#data_mc_comp('32_all', 'merge_all.root')
#data_mc_comp('32_gt500', 'merge_gt500.root')
#data_mc_comp('21_gt250_leadweight1', 'merge_gt250_leadweight1.root')
#data_mc_comp('21_gt500_leadweight1_ttbup20pc', 'merge_gt500_leadweight1_ttbup20pc.root')
#data_mc_comp('21_gt500_leadweight1_ttbup100pc', 'merge_gt500_leadweight1_ttbup100pc.root')

data_mc_comp('')
