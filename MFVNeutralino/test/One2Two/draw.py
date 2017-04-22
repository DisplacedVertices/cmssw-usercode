#!/usr/bin/env python

from JMTucker.MFVNeutralino.MiniTreeBase import *
input_fn = [x for x in sys.argv if x.endswith('.root') and os.path.isfile(x)][0]
plot_path = os.path.join('plots/one2two', os.path.basename(input_fn).replace('.root', ''))
ps = plot_saver(plot_path, size=(600,600))

f = ROOT.TFile(input_fn)

def get_h(name):
    #print name
    return f.Get('mfvOne2Two/%s' % name)

####

'''
for ex in [''] + 'bkg sig sb sbbkg sbsig'.split():
    for name in 'h_1v_xy h_2v_xy'.split():
        if '1v' in name:
            ex = ex.replace('bkg','').replace('sig','')
        name = name.replace('v_', 'v%s_' % ex)
'''

for name in 'h_1v_xy h_2v_xy'.split():
    h = get_h(name)
    h.SetTitle(';vertex x (cm);vertex y (cm)')
    h.SetStats(0)
    if '1v' in name:
        h.Draw('colz')
    else:
        h.SetMarkerStyle(20)
        h.SetMarkerSize(1.3)
        h.Draw('scat same')
        ps.save(name, logz=True)

for name in 'h_2v_bs2ddist h_2v_bs2ddist_0 h_2v_bs2ddist_1 h_1v_bs2ddist'.split():
    h = get_h(name)
    h.Rebin(2)
    h.SetTitle(';vertex xy distance to beamspot (cm);vertices/20 #mum')
    h.Draw()
    ps.save(name)

for name in 'h_2v_bsdz h_2v_bsdz_0 h_2v_bsdz_1 h_1v_bsdz'.split():
    h = get_h(name)
    h.Rebin(2)
    h.SetTitle(';vertex #Delta z to beamspot (cm);vertices/0.4 cm')
    h.Draw()
    ps.save(name)

for name in 'h_2v_bs2ddist_v_bsdz h_2v_bs2ddist_v_bsdz_0 h_2v_bs2ddist_v_bsdz_1 h_1v_bs2ddist_v_bsdz'.split():
    h = get_h(name)
    h.SetTitle(';vertex #Delta z to beamspot (cm);vertex xy distance to beamspot (cm)')
    h.SetStats(0)
    h.Draw('colz')
    ps.save(name, logz=True)

h = get_h('h_2v_svdz')
h.Fit('gaus', 'ILQ')
ps.save('h_2v_svdz')

for name in 'h_1v_svdz h_1v_svdz_all'.split():
    h = get_h(name)
    h.SetTitle(';vertex #Delta z (cm);events/100 #mum')
    h.Draw()
    ps.save(name)

for name in 'h_2v_svdz_v_dphi h_1v_svdz_v_dphi'.split():
    h = get_h(name)
    h.SetTitle(';vertex #Delta #phi;vertex #Delta z (cm)')
    h.SetStats(0)
    h.Draw('colz')
    ps.save(name, logz=True)

for name in 'h_2v_ntracks h_1v_ntracks h_2v_ntracks01 h_1v_ntracks01'.split():
    h = get_h(name)
    if '01' in name:
        h.SetTitle(';sum of ntracks 0 and 1;events')
        h.Draw()
    else:
        h.SetTitle(';ntracks 0;ntracks 1')
        h.Draw('colz')
    ps.save(name)

####

h2v = get_h('h_2v_dphi')
h1v = get_h('h_1v_dphi')
hfn = get_h('h_fcn_dphi')

h1v.SetLineColor(ROOT.kRed)
hfn.SetLineColor(ROOT.kGreen+2)

h1v.Scale(h2v.Integral()/h1v.Integral())
hfn.Scale(h2v.Integral()/hfn.Integral())

h2v.SetTitle(';#Delta#phi;events/0.63')
h2v.Draw()
h1v.Draw('sames')
hfn.Draw('sames')
ps.c.Update()
differentiate_stat_box(h2v, (1,0), new_size=(0.25, 0.25))
differentiate_stat_box(h1v, (1,1), new_size=(0.25, 0.25))
differentiate_stat_box(hfn, (1,2), new_size=(0.25, 0.25))
ps.save('deltaphi')

####

h2v = get_h('h_2v_abs_dphi')
h1v = get_h('h_1v_abs_dphi')
hfn = get_h('h_fcn_abs_dphi')

h1v.SetLineColor(ROOT.kRed)
hfn.SetLineColor(ROOT.kGreen+2)

h1v.Scale(h2v.Integral()/h1v.Integral())
hfn.Scale(h2v.Integral()/hfn.Integral())

h2v.SetTitle(';|#Delta#phi|;events/0.63')
h2v.Draw()
h1v.Draw('sames')
hfn.Draw('sames')
ps.c.Update()
differentiate_stat_box(h2v, (2,0), new_size=(0.25, 0.25))
differentiate_stat_box(h1v, (2,1), new_size=(0.25, 0.25))
differentiate_stat_box(hfn, (2,2), new_size=(0.25, 0.25))
ps.save('absdeltaphi')

####

h2v = get_h('h_2v_svdz')
h1v = get_h('h_1v_svdz')
hfn = get_h('h_fcn_dz')

h1v.SetLineColor(ROOT.kRed)
hfn.SetLineColor(ROOT.kGreen+2)

h1v.Scale(h2v.Integral()/h1v.Integral())
hfn.Scale(h2v.Integral()/hfn.Integral())

h2v.SetTitle(';#Delta z;events/0.02 cm')
h2v.Draw()
h1v.Draw('sames')
hfn.Draw('sames')
ps.c.Update()
differentiate_stat_box(h2v, (1,0), new_size=(0.25, 0.25))
differentiate_stat_box(h1v, (1,1), new_size=(0.25, 0.25))
differentiate_stat_box(hfn, (1,2), new_size=(0.25, 0.25))
ps.save('dz')

####

for name in 'h_2v_svdist2d h_2vbkg_svdist2d h_2vsig_svdist2d h_2vsb_svdist2d h_2vsbbkg_svdist2d h_2vsbsig_svdist2d h_1v_svdist2d h_1vsb_svdist2d'.split():
    h = get_h(name)
    h.SetTitle(';xy distance between vertex 0 and 1 (cm);events/10 #mum')
    h.Draw()
    ps.update_canvas()
    move_stat_box(h, (0.634, 0.591, 0.980, 0.997))
    ps.save(name)

####

def svdist2d_comp(norm_below, rebin=None, shift=None, save=None):
    name = ('norm%.3f' % norm_below).replace('.','p')
    if shift is not None:
        name += '_shift%i' % shift

    h2v = get_h('h_2v_svdist2d').Clone('h2v')
    h1v = get_h('h_1v_svdist2d').Clone('h1v')
    if rebin:
        h2v.Rebin(rebin)
        h1v.Rebin(rebin)

    h1v.Scale(1/h1v.Integral())
    nbins = h1v.GetNbinsX()

    if shift is not None:
        h1v_shift = ROOT.TH1F('h1v_shift%i' % shift, '', nbins, h1v.GetXaxis().GetXmin(), h1v.GetXaxis().GetXmax())
        for ibin in xrange(1, nbins+2):
            ifrom = ibin - shift
            val, err = 0., 0.
            if ifrom >= 0:
                val = h1v.GetBinContent(ifrom)
                err = h1v.GetBinError  (ifrom)
            if ibin == nbins+1:
                var = err**2
                for irest in xrange(ifrom+1, nbins+2):
                    val += h1v.GetBinContent(ifrom)
                    var += h1v.GetBinError  (ifrom)**2
                err = var**0.5
            h1v_shift.SetBinContent(ibin, val)
            h1v_shift.SetBinError  (ibin, err)
        h1v = h1v_shift

    ksdist = h1v.KolmogorovTest(h2v, 'M')
    ksprob = h1v.KolmogorovTest(h2v)
    ks = (ksdist, ksprob)

    h2v.SetLineWidth(2)
    h1v.SetLineColor(ROOT.kRed)

    lb = h2v.FindBin(norm_below)
    h1v.Scale(h2v.Integral(1, lb)/h1v.Integral(1, lb))

    h2v.SetTitle('norm_below %f shift %i;xy distance between vertex 0 and 1 (cm);events/10 #mum' % (norm_below, shift))

    h2v.Draw('e')
    h1v.Draw('sames')
    ps.c.Update()
    differentiate_stat_box(h2v, 0, new_size=(0.3, 0.3))
    differentiate_stat_box(h1v,    new_size=(0.3, 0.3))

    chi2 = h2v.Clone(h2v.GetName() + '_chi2')
    chi2.Add(h1v, -1)
    for ibin in xrange(1, chi2.GetNbinsX()+1):
        dif = chi2.GetBinContent(ibin)
        err = chi2.GetBinError  (ibin)
        if h2v.GetBinContent(ibin):
            if err < 1e-9:
                err = 1e-9
            chi2.SetBinContent(ibin, dif**2/err)
    chi2_rescale = h2v.GetYaxis().GetXmax()/chi2.GetMaximum()
    chi2.Scale(chi2_rescale)
    tpl = ROOT.TPaveLabel(0.214, 0.898, 0.875, 0.998, '#chi^{2} rescale = %f' % chi2_rescale, 'brNDC')
    tpl.SetTextSize(0.25)
    tpl.SetBorderSize(0)
    tpl.SetFillColor(0)
    tpl.SetFillStyle(0)
    tpl.Draw()
    chi2.SetMarkerStyle(20)
    chi2.SetMarkerSize(0.8)
    chi2.SetMarkerColor(ROOT.kBlack)
    chi2.Draw("same")
    chi2.SetStats(0)
    if save is not None:
        if save != '':
            save = '_' + save
        ps.save('svdist2d_%s%s' % (name, save))

    for opt in ('ge', 'le'):
        ch2v = cumulative_histogram(h2v, opt)
        ch1v = cumulative_histogram(h1v, opt)

        ch2v.SetTitle(';x = svdist2d (cm);# events w/ svdist2d #%sq x' % opt)
        ch2v.SetStats(0)
        ch1v.SetStats(0)
        ch2v.SetLineWidth(2)
        ch1v.SetLineColor(ROOT.kRed)
        ch2v.Draw()
        ch1v.Draw('hist same')
        if save is not None:
            ps.save('svdist2d_%s%s_cumul%s' % (name, save, opt))

    return ks

svdist2d_cut = 0.05

for shift in xrange(20):
    svdist2d_comp(svdist2d_cut, None, shift, 'shift%i' % shift)

h2v = get_h('h_2vsb_svdist2d').Clone('h2v')
h1v = get_h('h_1vsb_svdist2d').Clone('h1v')
bin_size = h2v.GetBinWidth(1)
shift_by_means = int(round((h2v.GetMean() - h1v.GetMean())/bin_size))
svdist2d_comp(svdist2d_cut, None, shift_by_means, 'bymeans')

def shifted(h, shift, last_bin):
    B = [(h.GetBinContent(i), h.GetBinError(i)) for i in xrange(0, h.GetNbinsX()+1)]
    if shift:
        B = [(0.,0.)]*shift + B[:-shift]
    return B[:last_bin+2]

def get_F(h, last_bin, shift):
    B = shifted(h, shift, last_bin)
    I = sum(b for b,e in B)
    B = [(b/I, e/I) for b,e in B]
    F = [B[0]]
    for b,e in B[1:]:
        bl, el = F[-1]
        F.append((b + bl, (e + el)**0.5))
    return F

def get_hF(h, last_bin, shift):
    F = get_F(h, last_bin, shift)
    h = h.Clone(h.GetName() + 'F')
    for ibin in xrange(h.GetNbinsX()+2):
        if ibin <= last_bin:
            h.SetBinContent(ibin, F[ibin][0])
            h.SetBinError  (ibin, 0)
        else:
            h.SetBinContent(ibin, 0)
            h.SetBinError  (ibin, 0)
    return h

def svdist2d_sideband_fitstat(h2v, h1v, shift, last_bin, stat):
    if stat in ('ad', 'cvm', 'ks'):
        F2v = get_F(h2v, last_bin)
        F1v = get_F(h1v, last_bin, shift)
        s = 0.
        for (F,Fe),(Fn,Fne) in zip(F1v, F2v):
            if stat == 'ad':
                if F > 0 and F < 1:
                    w = F*(1-F)
                else:
                    w = 1e-6
            else:
                w = 1.
            if stat == 'ks':
                s = max(s, abs(Fn - F))
            else:
                s += abs(Fn - F)**2 / w
        return s
    elif stat == 'chi2':
        h2v = shifted(h1v,     0, last_bin)
        h1v = shifted(h1v, shift, last_bin)
        s2v = sum(b for b,e in h2v)
        s1v = sum(b for b,e in h1v)
        scale = s2v/s1v
        h1v = [(b*scale, e*scale) for b,e in h1v]
        print sum(b for b,e in h2v), sum(b for b,e in h1v)
        chi2 = 0.
        #print '  shift: %i' % shift
        for (v,ve), (vn,vne) in zip(h1v, h2v):
            if vn:
                dif2 = (vn - v)**2
                err = (ve**2 + vne**2)**0.5
                if err < 1e-9:
                    err = 1e-9
                chi2 += dif2/err
            #print '    dif2:', dif2, 'err:', err, 'd/e:', dif2/err, 'cchi2:', chi2
        return chi2
        
for stat_name in ('chi2',): #, 'ks', 'ad', 'cvm'):
    h2v = get_h('h_2v_svdist2d').Clone('h2v')
    h1v = get_h('h_1v_svdist2d').Clone('h1v')
    rebin = 1
    h2v.Rebin(rebin)
    h1v.Rebin(rebin)
    last_bin = h1v.FindBin(svdist2d_cut) - 1

    nshifts = 20
    shifts = range(nshifts)
    stats = [svdist2d_sideband_fitstat(h2v, h1v, shift, last_bin, stat_name) for shift in shifts]
    print 'stat:', stat_name
    for shift, stat in zip(shifts, stats):
        print '%2i' % shift, stat
    best_shift, best_stat = min(zip(shifts, stats), key=lambda x:x[1])
    print 'best:', best_shift

    Fh2v = get_hF(h2v, last_bin, best_shift)
    Fh1v = get_hF(h1v, last_bin, best_shift)
    Fh1v.Draw()
    Fh2v.Draw('same')
    ps.save('%s_Fs' % stat_name)

    g = ROOT.TGraph(nshifts, to_array(shifts), to_array(stats))
    g.SetTitle('%s;shift;stat' % stat_name)
    g.SetMarkerStyle(20)
    g.SetMarkerSize(1)
    g.Draw('ALP')
    ps.save('%s_v_shift' % stat_name)

    svdist2d_comp(svdist2d_cut, rebin, best_shift, '%sfit' % stat_name)

####
'''
verbose = 'Q'
h = get_h('h_2v_dphi')

for i in xrange(2, 17, 2):
    if verbose == 'V':
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%i' % i
    fcn = ROOT.TF1('fcn', '[0]*x**%i' % i, pi, pi)
    res = h.Fit(fcn, 'IRS' + verbose)
    ps.save('power_%i' % i)
    #res.Print()

h = get_h('h_2v_abs_dphi')

for i in xrange(2, 17, 2):
    if verbose == 'V':
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%i' % i
    fcn = ROOT.TF1('fcn', '[0]*x**%i' % i, pi, pi)
    res = h.Fit(fcn, 'IRS' + verbose)
    ps.save('abs_power_%i' % i)
    #res.Print()
'''

