#!/usr/bin/env python

# py $tmain/effsprint.py one . > effsprint.one.txt ; py $tmain/effsprint.py . > effsprint.txt ; py $tmain/effsprint.py . sigreg > effsprint.sigreg.txt ; py $tmain/effsprint.py mfv*root xx4*root sigreg > effsprint.sigreg.sigs.txt ;   py $tmain/effsprint.py mfv*root xx4*root  > effsprint.sigs.txt
# py $tmain/effsprint.py csv one . > effsprint.one.csv ; py $tmain/effsprint.py csv . > effsprint.csv ; py $tmain/effsprint.py csv . sigreg > effsprint.sigreg.csv ; py $tmain/effsprint.py csv mfv*root xx4*root sigreg > effsprint.sigreg.sigs.csv ;   py $tmain/effsprint.py csv mfv*root xx4*root  > effsprint.sigs.csv

import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

csv = 'csv' in sys.argv
plots = 'plots' in sys.argv
if plots:
    set_style()
    ROOT.gStyle.SetPaintTextFormat('.2g')
    ps = plot_saver('plots/nm1s', size=(500,500), log=False)

tot_ngen = 0.

tot_sum = 0.
tot_var = 0.

tot_n2v3 = 0.
tot_n1v3 = 0.
tot_n2v4 = 0.
tot_n1v4 = 0.
tot_n2v5 = 0.
tot_n1v5 = 0.

err_tot_n2v3 = 0.
err_tot_n1v3 = 0.
err_tot_n2v4 = 0.
err_tot_n1v4 = 0.
err_tot_n2v5 = 0.
err_tot_n1v5 = 0.

cuts = () if 'nonm1' in sys.argv else ('Bsbs2ddist', 'Bs2derr')
max_cut_name_len = max(len(x) for x in cuts) if cuts else -1
integral = 'entries' not in sys.argv
nvtx = 1 if 'one' in sys.argv else 2
ntk = ''
if 'ntk3' in sys.argv:
    ntk = 'Ntk3'
elif 'ntk4' in sys.argv:
    ntk = 'Ntk4'
elif 'ntk3or4' in sys.argv:
    ntk = 'Ntk3or4'
sigreg = 'sigreg' in sys.argv
presel = 'presel' in sys.argv
nocuts = 'nocuts' in sys.argv
if sum([sigreg, nvtx == 1, presel, nocuts]) > 1:
    raise ValueError("can only do one of onevtx, sigreg, presel, nocuts")
if any([sigreg,presel,nocuts]):
    cuts = ()

if not integral:
    print 'using GetEntries(), but "pass vtx only" and all nm1s still use Integral()'

if '2018' in sys.argv:
    int_lumi = ac.int_lumi_2018 * ac.scale_factor_2018
else:
    int_lumi = ac.int_lumi_2017 * ac.scale_factor_2017

def effs(fn):
    global tot_ngen, tot_sum, tot_var, tot_n2v3, tot_n1v3, tot_n2v4, tot_n1v4, tot_n2v5, tot_n1v5, err_tot_n2v3, err_tot_n1v3, err_tot_n2v4, err_tot_n1v4, err_tot_n2v5, err_tot_n1v5

    f = ROOT.TFile(fn)

    def get_n(dir_name):
        h = f.Get('%s/h_npv' % dir_name)
        return h.Integral(0,1000000) if integral else h.GetEntries(), h.GetEntries()

    den = norm_from_file(fn)
    sname = os.path.basename(fn).replace('.root','')
    sample = getattr(Samples, sname, None)
    if sample:
        weight = sample.xsec * int_lumi / den
        weighted = True
    else:
        weight = 1.
        weighted = False
    if sigreg:
        namenumall = 'mfvEventHistosSigReg'
        namenumvtx = 'mfvVertexHistosSigReg/h_nsv'
    elif nvtx == 1:
        namenumall = 'mfvEventHistosOnlyOneVtx'
        namenumvtx = 'mfvVertexHistosOnlyOneVtx/h_nsv'
    elif presel:
        namenumall = 'mfvEventHistosPreSel'
        namenumvtx = None
    elif nocuts:
        namenumall = 'mfvEventHistosNoCuts'
        namenumvtx = None
    else:
        namenumall = 'mfvEventHistosFullSel'
        namenumvtx = None
    
    namenumall = ntk + namenumall
   
    if namenumvtx:
        namenumvtx = ntk + namenumvtx

    numall, numall_unweighted = get_n(namenumall)
   
    n1v3numall, n1v3numall_unweighted = get_n('Ntk3mfvEventHistosOnlyOneVtx')
    n1v4numall, n1v4numall_unweighted = get_n('Ntk4mfvEventHistosOnlyOneVtx')
    n1v5numall, n1v5numall_unweighted = get_n('mfvEventHistosOnlyOneVtx')
    n2v3numall, n2v3numall_unweighted = get_n('Ntk3mfvEventHistosFullSel')
    n2v4numall, n2v4numall_unweighted = get_n('Ntk4mfvEventHistosFullSel')
    n2v5numall, n2v5numall_unweighted = get_n('mfvEventHistosFullSel')
    
    if namenumvtx is not None:
        h = f.Get(namenumvtx)
        numvtx = h.Integral(h.FindBin(nvtx), 1000000)
    else:
        numvtx = -1
    ngen = f.Get('mfvWeight/h_sums').GetBinContent(1) 
    #weight = 40.6*1000*(0.063168 + 0.30885)/ngen
    #weight = 137.1*(1.0)/ngen

    tot_ngen += ngen
    tot_sum += numall * weight
    tot_var += numall * weight**2
    
    tot_n2v3 += n2v3numall*weight
    tot_n2v4 += n2v4numall*weight
    tot_n2v5 += n2v5numall*weight
    tot_n1v3 += n1v3numall*weight
    tot_n1v4 += n1v4numall*weight
    tot_n1v5 += n1v5numall*weight
    err_tot_n2v3 += n2v3numall * (weight**2)
    err_tot_n2v4 += n2v4numall * (weight**2)
    err_tot_n2v5 += n2v5numall * (weight**2)
    err_tot_n1v3 += n1v3numall * (weight**2)
    err_tot_n1v4 += n1v4numall * (weight**2)
    err_tot_n1v5 += n1v5numall * (weight**2)
    
    if n1v3numall < 0.0:
      n1v3numall = 0.0
    if n1v4numall < 0.0:
      n1v4numall = 0.0
    if n1v5numall < 0.0:
      n1v5numall = 0.0
    if n2v3numall < 0.0:
      n2v3numall = 0.0
    if n2v4numall < 0.0:
      n2v4numall = 0.0
    if n2v5numall < 0.0:
      n2v5numall = 0.0
    
    if csv:
        print '%s (numgen $%.d$ of weight $%.1f$) & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ \\\\ ' % (sname, ngen, weight, numall*weight, numall**0.5 * weight, n1v3numall*weight, n1v3numall**0.5 * weight, n2v3numall*weight, n2v3numall**0.5 * weight, n1v4numall*weight, n1v4numall**0.5 * weight, n2v4numall*weight, n2v4numall**0.5 * weight, n1v5numall*weight, n1v5numall**0.5 * weight, n2v5numall*weight, n2v5numall**0.5 * weight)
        #print '%s & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ \\' % (sname, numall*weight, numall**0.5 * weight, n1v3numall*weight, n1v3numall**0.5 * weight, n2v3numall*weight, n2v3numall**0.5 * weight, n1v4numall*weight, n1v4numall**0.5 * weight, n2v4numall*weight, n2v4numall**0.5 * weight, n1v5numall*weight, n1v5numall**0.5 * weight, n2v5numall*weight, n2v5numall**0.5 * weight)
        #print 'samples.push_back("%s");    weights.push_back(%0.2f);' % (sname, weight)
        #print '%s,%e,%f,%f,%f,%0.1f,%0.1f' % (sname, weight, den, numall, float(numall)/den, numall*weight, numall**0.5 * weight)
    else:
        print '%s (w = %.3e): # ev: %10.1f  pass evt+vtx: %5.1f -> %5.3e unweighted: %5.1f  pass vtx only: %5.1f -> %5.3e' % (sname.ljust(30), weight, den, numall, float(numall)/den, numall_unweighted, numvtx, float(numvtx)/den)
        if weighted:
            print '  weighted to %.1f/pb: %5.2f +/- %5.2f' % (int_lumi, numall*weight, numall**0.5 * weight)
        else:
            print '  number of events: %5.2f +/- %5.2f' % (numall*weight, numall**0.5 * weight)
        if cuts:
            nm1s_name = 'h_nm1_%s' % sname
            h_nm1_abs = ROOT.TH1F(nm1s_name + '_abs', ';cut;abs. eff. w/o cut', len(cuts)+1, 0, len(cuts)+1)
            h_nm1_rel = ROOT.TH1F(nm1s_name + '_rel', ';cut;n-1 eff.', len(cuts), 0, len(cuts))
            for icut, cut in enumerate(cuts):
                h_nm1_abs.GetXaxis().SetBinLabel(icut+1, cut)
                h_nm1_rel.GetXaxis().SetBinLabel(icut+1, cut)
                nm1, nm1_unweighted = get_n('%sevtHst%sVNo%s' % (ntk, nvtx, cut))
                nm1_abs = float(nm1)/den
                nm1_rel = float(numall)/nm1 if nm1 > 0 else -1
                h_nm1_abs.SetBinContent(icut+1, nm1_abs)
                h_nm1_rel.SetBinContent(icut+1, nm1_rel)
                print '    remove %s cut: %5i -> %5.3e (n-1: %5.3e)' % (cut.ljust(max_cut_name_len), nm1, nm1_abs, nm1_rel)
                print '    weighted to %.1f/pb: %5.2f +/- %5.2f' % (int_lumi, nm1*weight, abs(nm1)**0.5 * weight)
            h_nm1_abs.GetXaxis().SetBinLabel(len(cuts)+1, 'all')
            h_nm1_abs.SetBinContent(len(cuts)+1, float(numall)/den)
            def draw(h):
                if not plots:
                    return
                h.SetStats(0)
                h.GetYaxis().SetRangeUser(0,1.05)
                h.SetMarkerSize(2)
                h.Draw('hist text')
                ps.save(h.GetName())
            draw(h_nm1_abs)
            draw(h_nm1_rel)

nosort = 'nosort' in sys.argv
fns = [x for x in sys.argv[1:] if os.path.isfile(x) and x.endswith('.root')]
print_sum = 'sum' in sys.argv
if not fns:
    dir = os.path.abspath([x for x in sys.argv[1:] if os.path.isdir(x)][0])
    #fns = [os.path.join(dir, sn + '.root') for sn in 'qcdht0700_2017 qcdht1000_2017 qcdht1500_2017 qcdht2000_2017 ttbarht0600_2017 ttbarht0800_2017 ttbarht1200_2017 ttbarht2500_2017'.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' WminusHToSSTodddd_tau1mm_M55 WplusHToSSTodddd_tau1mm_M55 ZHToSSTodddd_tau1mm_M55'.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' wjetstolnu_2j_2017 '.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' VHToSSTodddd_tau1mm_M55_2017 VHToSSTodddd_tau10mm_M55_2017 '.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' mfv_neu_tau001000um_M0400_2017 '.split()]
    fns = [os.path.join(dir, sn + '_2017.root') for sn in ' ttbar qcdpt15mupt5 qcdpt20mupt5 qcdpt30mupt5 qcdpt50mupt5 qcdpt80mupt5 qcdpt120mupt5 qcdpt170mupt5 qcdpt300mupt5 qcdpt470mupt5 qcdpt470mupt5 qcdpt1000mupt5 qcdpt600mupt5 qcdpt800mupt5 qcdempt020 qcdempt030 qcdempt050 qcdempt080 qcdempt120 qcdempt170 qcdempt300 qcdbctoept015 qcdbctoept020 qcdbctoept030 qcdbctoept170 qcdbctoept250 ww wz zz dyjetstollM10 dyjetstollM50 wjetstolnu_0j wjetstolnu_1j wjetstolnu_2j '.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' ttbar_2018 qcdmupt15_2018 qcdempt015_2018 qcdempt020_2018 qcdempt030_2018 qcdempt050_2018 qcdempt080_2018 qcdempt120_2018 qcdempt170_2018 qcdbctoept015_2018 qcdbctoept020_2018 qcdbctoept030_2018 qcdbctoept080_2018 qcdbctoept170_2018 qcdbctoept250_2018 qcdempt300_2018 wjetstolnu_0j_2018 wjetstolnu_1j_2018 wjetstolnu_2j_2018 dyjetstollM10_2018 dyjetstollM50_2018 ww_2018 wz_2018 zz_2018 SingleMuon2018A SingleMuon2018B SingleMuon2018C SingleMuon2018D EGamma2018A EGamma2018B EGamma2018C EGamma2018D '.split()] 
    fns = [fn for fn in fns if os.path.isfile(fn)]
    nosort = True
    print_sum = True
if not nosort:
    fns.sort()
if csv:
    print 'sample,weight,den,num,eff,weighted,err_weighted'

for fn in fns:
    effs(fn)
print 'tot (numgen $%.d$) & $%d\pm%d$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$' % (tot_ngen, tot_sum, tot_var**0.5,tot_n1v3, err_tot_n1v3**0.5, tot_n2v3, err_tot_n2v3**0.5, tot_n1v4, err_tot_n1v4**0.5, tot_n2v4, err_tot_n2v4**0.5, tot_n1v5, err_tot_n1v5**0.5, tot_n2v5, err_tot_n2v5**0.5)
if print_sum:
    if csv:
        print 'sum for %f/pb,,,,,%f,%f' % (int_lumi, tot_sum, tot_var**0.5)
    else:
        print 'sum for %.1f/pb: %5.2f +/- %5.2f' % (int_lumi, tot_sum, tot_var**0.5)
