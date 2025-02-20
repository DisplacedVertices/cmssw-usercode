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

integral = 'entries' not in sys.argv
nvtx = 1 if 'one' in sys.argv else 2
ntk = ''
if 'ntk3' in sys.argv:
    ntk = 'Ntk3'
elif 'ntk4' in sys.argv:
    ntk = 'Ntk4'
elif 'ntk3or4' in sys.argv:
    ntk = 'Ntk3or4'
presel = 'presel' in sys.argv

if not integral:
    print 'using GetEntries(), but "pass vtx only" and all nm1s still use Integral()'

if '2018' in sys.argv:
    int_lumi = ac.int_lumi_2018 * ac.scale_factor_2018
else:
    int_lumi = ac.int_lumi_2017 * ac.scale_factor_2017

def effs(fn):
    global tot_sum, tot_var, tot_n2v3, tot_n1v3, tot_n2v4, tot_n1v4, tot_n2v5, tot_n1v5, err_tot_n2v3, err_tot_n1v3, err_tot_n2v4, err_tot_n1v4, err_tot_n2v5, err_tot_n1v5

    f = ROOT.TFile(fn)

    def get_n(dir_name, bin0,bin1):
        h = f.Get('%s/h_nsv' % dir_name)
        return h.Integral(bin0,bin1) if integral else h.GetEntries(), h.GetEntries()
    
    den = norm_from_file(fn)
    sname = os.path.basename(fn).replace('.root','')
    sample = getattr(Samples, sname, None)
    if sample:
        weight = sample.xsec * int_lumi / den
        weighted = True
    else:
        weight = 1.
        weighted = False
    
    if nvtx == 1:
        namenumall = 'mfvMiniTree'
        namenumvtx = 'mfvMiniTree/h_nsv'
    elif presel:
        namenumall = 'mfvMiniTreePreSelEvtFilt'
        namenumvtx = None
    else:
        namenumall = 'mfvMiniTree'
        namenumvtx = None
    
    namenumall = ntk + namenumall
   
    if namenumvtx:
        namenumvtx = ntk + namenumvtx

    numall, numall_unweighted = get_n(namenumall,1,999)
   
    ngen = f.Get('mfvWeight/h_sums').GetBinContent(1) 

    #weight = 137.1*1000*(0.063168 + 0.30885)/ngen #VH 
    weight = 137.1*(1.0)/ngen #RPV 
    #weight = 137.1*1000*(52.0)*0.1/ngen #ggH

    n1v3numall, n1v3numall_unweighted = get_n('mfvMiniTreeNtk3',2,2)
    n1v4numall, n1v4numall_unweighted = get_n('mfvMiniTreeNtk4',2,2)
    n1v5numall, n1v5numall_unweighted = get_n('mfvMiniTree',2,2)
    n2v3numall, n2v3numall_unweighted = get_n('mfvMiniTreeNtk3',3,999)
    n2v4numall, n2v4numall_unweighted = get_n('mfvMiniTreeNtk4',3,999)
    n2v5numall, n2v5numall_unweighted = get_n('mfvMiniTree',3,999)
    
    if namenumvtx is not None:
        h = f.Get(namenumvtx)
        numvtx = h.Integral(h.FindBin(nvtx), 1000000)
    else:
        numvtx = -1

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
    
    if csv:
        #print '%s & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$' % (sname, numall*weight, numall**0.5 * weight, n1v3numall*weight, n1v3numall**0.5 * weight, n2v3numall*weight, n2v3numall**0.5 * weight, n1v4numall*weight, n1v4numall**0.5 * weight, n2v4numall*weight, n2v4numall**0.5 * weight, n1v5numall*weight, n1v5numall**0.5 * weight, n2v5numall*weight, n2v5numall**0.5 * weight)
        print '%s & $%0.1f\pm%0.1f$ & $%0.2f\pm%0.2f$ & $%0.2f\pm%0.2f$ & $%0.2f\pm%0.2f$ & $%0.2f\pm%0.2f$ & $%0.2f\pm%0.2f$ & $%0.2f\pm%0.2f$' % (sname, numall*weight, numall**0.5 * weight, n1v3numall*weight, n1v3numall**0.5 * weight, n2v3numall*weight, n2v3numall**0.5 * weight, n1v4numall*weight, n1v4numall**0.5 * weight, n2v4numall*weight, n2v4numall**0.5 * weight, n1v5numall*weight, n1v5numall**0.5 * weight, n2v5numall*weight, n2v5numall**0.5 * weight)
        #print 'samples.push_back("%s");    weights.push_back(%0.2f);' % (sname, weight)
        #print '%s,%e,%f,%f,%f,%0.1f,%0.1f' % (sname, weight, den, numall, float(numall)/den, numall*weight, numall**0.5 * weight)
    else:
        print '%s (w = %.3e): # ev: %10.1f  pass evt+vtx: %5.1f -> %5.3e unweighted: %5.1f  pass vtx only: %5.1f -> %5.3e' % (sname.ljust(30), weight, den, numall, float(numall)/den, numall_unweighted, numvtx, float(numvtx)/den)
        if weighted:
            print '  weighted to %.1f/pb: %5.2f +/- %5.2f' % (int_lumi, numall*weight, numall**0.5 * weight)
        else:
            print '  number of events: %5.2f +/- %5.2f' % (numall*weight, numall**0.5 * weight)

nosort = 'nosort' in sys.argv
fns = [x for x in sys.argv[1:] if os.path.isfile(x) and x.endswith('.root')]
print_sum = 'sum' in sys.argv
if not fns:
    dir = os.path.abspath([x for x in sys.argv[1:] if os.path.isdir(x)][0])
    #fns = [os.path.join(dir, sn + '.root') for sn in 'qcdht0700_2017 qcdht1000_2017 qcdht1500_2017 qcdht2000_2017 ttbarht0600_2017 ttbarht0800_2017 ttbarht1200_2017 ttbarht2500_2017'.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' WminusHToSSTodddd_tau1mm_M55 WplusHToSSTodddd_tau1mm_M55 ZHToSSTodddd_tau1mm_M55'.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' VHToSSTodddd_tau1mm_M55_Run2 VHToSSTodddd_tau10mm_M55_Run2 '.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' ggHToSSTodddd_tau1mm_M55_Run2 '.split()]
    fns = [os.path.join(dir, sn + '.root') for sn in ' mfv_neu_tau001000um_M0400_Run2 mfv_stopdbardbar_tau000300um_M0400_Run2 mfv_stopdbardbar_tau001000um_M0200_Run2 '.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' wjetstolnu_2j_2017 '.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' dyjetstollM10_20161 dyjetstollM50_20161 qcdbctoept020_20161 qcdbctoept030_20161 qcdbctoept080_20161 qcdbctoept170_20161 qcdbctoept250_20161 qcdempt015_20161 qcdempt020_20161 qcdempt030_20161 qcdempt050_20161 qcdempt080_20161 qcdempt120_20161 qcdempt170_20161 qcdempt300_20161 qcdmupt15_20161 ttbar_20161 wjetstolnu_0j_20161 wjetstolnu_1j_20161 wjetstolnu_2j_20161 ww_20161 wz_20161 zz_20161'.split()]
    
    #fns = [os.path.join(dir, sn + '.root') for sn in ' dyjetstollM10_20162 dyjetstollM50_20162 qcdbctoept020_20162 qcdbctoept030_20162 qcdbctoept080_20162 qcdbctoept170_20162 qcdbctoept250_20162 qcdempt015_20162 qcdempt020_20162 qcdempt030_20162 qcdempt050_20162 qcdempt080_20162 qcdempt120_20162 qcdempt170_20162 qcdempt300_20162 qcdmupt15_20162 ttbar_20162 wjetstolnu_0j_20162 wjetstolnu_1j_20162 wjetstolnu_2j_20162 ww_20162 wz_20162 zz_20162'.split()]
    #fns = [os.path.join(dir, sn + '.root') for sn in ' ttbar_2017 dyjetstollM10_2017  qcdbctoept170_2017  qcdempt120_2017 qcdpt170mupt5_2017 qcdpt600mupt5_2017 ww_2017 dyjetstollM50_2017 qcdbctoept250_2017 qcdempt170_2017 qcdpt20mupt5_2017 qcdpt800mupt5_2017 wz_2017 qcdbctoept015_2017 qcdempt020_2017 qcdempt300_2017 qcdpt300mupt5_2017 qcdpt80mupt5_2017 zz_2017 qcdbctoept020_2017 qcdempt030_2017 qcdpt1000mupt5_2017 qcdpt30mupt5_2017 wjetstolnu_0j_2017 qcdbctoept030_2017 qcdempt050_2017 qcdpt120mupt5_2017 qcdpt470mupt5_2017  wjetstolnu_1j_2017 qcdbctoept080_2017 qcdempt080_2017 qcdpt15mupt5_2017 qcdpt50mupt5_2017 wjetstolnu_2j_2017 '.split()]
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
#print 'back_lep & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$' % (tot_n1v3, err_tot_n1v3**0.5, tot_n2v3, err_tot_n2v3**0.5, tot_n1v4, err_tot_n1v4**0.5, tot_n2v4, err_tot_n2v4**0.5, tot_n1v5, err_tot_n1v5**0.5, tot_n2v5, err_tot_n2v5**0.5)
if print_sum:
    if csv:
        print 'sum for %f/pb,,,,,%f,%f' % (int_lumi, tot_sum, tot_var**0.5)
    else:
        print 'sum for %.1f/pb: %5.2f +/- %5.2f' % (int_lumi, tot_sum, tot_var**0.5)
