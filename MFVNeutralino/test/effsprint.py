#!/usr/bin/env python

# py $tmain/effsprint.py one . > effsprint.one.txt ; py $tmain/effsprint.py . > effsprint.txt ; py $tmain/effsprint.py . sigreg > effsprint.sigreg.txt ; py $tmain/effsprint.py mfv*root xx4*root sigreg > effsprint.sigreg.sigs.txt ;   py $tmain/effsprint.py mfv*root xx4*root  > effsprint.sigs.txt
# py $tmain/effsprint.py csv one . > effsprint.one.csv ; py $tmain/effsprint.py csv . > effsprint.csv ; py $tmain/effsprint.py csv . sigreg > effsprint.sigreg.csv ; py $tmain/effsprint.py csv mfv*root xx4*root sigreg > effsprint.sigreg.sigs.csv ;   py $tmain/effsprint.py csv mfv*root xx4*root  > effsprint.sigs.csv

import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import sumw_from_file
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

cuts = () if 'nonm1' in sys.argv else ('Bsbs2ddist', 'Bs2derr')
max_cut_name_len = max(len(x) for x in cuts) if cuts else -1
integral = True # FIXME currently set it to integral only 'entries' not in sys.argv
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

rpv = 'rpv' in sys.argv
ggh = 'ggh' in sys.argv
vh = 'vh' in sys.argv 
bkg = 'bkg' in sys.argv


if sum([sigreg, nvtx == 1, presel, nocuts]) > 1:
    raise ValueError("can only do one of onevtx, sigreg, presel, nocuts")
if any([sigreg,presel,nocuts]):
    cuts = ()

if not integral:
    print 'using GetEntries(), but "pass vtx only" and all nm1s still use Integral()'

year = '99'
if '2018' in sys.argv:
    year = '2018'
    int_lumi = ac.int_lumi_2018 * ac.scale_factor_2018
elif '2017' in sys.argv:
    year = '2017'
    int_lumi = ac.int_lumi_2017 * ac.scale_factor_2017
elif '20161' in sys.argv:
    year = '20161'
    int_lumi = ac.int_lumi_20161 * ac.scale_factor_20161
elif '20162' in sys.argv:
    year = '20162'
    int_lumi = ac.int_lumi_20162 * ac.scale_factor_20162
else:
    year = 'run2'
    int_lumi = ac.int_lumi_20161 + ac.int_lumi_20162 + ac.int_lumi_2017 + ac.int_lumi_2018 #ac.int_lumi_run2 * ac.scale_factor_run2


def effs(fn):
    global tot_sum, tot_var, tot_n2v3, tot_n1v3, tot_n2v4, tot_n1v4, tot_n2v5, tot_n1v5, err_tot_n2v3, err_tot_n1v3, err_tot_n2v4, err_tot_n1v4, err_tot_n2v5, err_tot_n1v5

    f = ROOT.TFile(fn)
    def get_n(dir_name):
        h = f.Get('%s/h_nsv' % dir_name)
        return h.Integral(0,1000000) if integral else h.GetEntries(), h.GetEntries()
    
    den = sumw_from_file(fn)
    sname = os.path.basename(fn).replace('.root','')
    sample = getattr(Samples, sname, None)
    
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
    
    if rpv :
        weight = 137.1*(1.0)/den #RPV 
    elif ggh :
        weight = 137.1*1000*(52.0)*0.1/den #ggH
    elif vh :
        weight = 137.1*1000*(0.063168 + 0.30885)/den #VH 
    elif sample :
        weight = sample.xsec * int_lumi / den #for unscaled bkg inputs
        weighted = True
    else :
        weight = 1. #for scaled bkg inputs 
        weighted = False
    #print(" weight : ", weight)

    n1v3numall, n1v3numall_unweighted = get_n('Ntk3mfvVertexHistosOnlyOneVtx')
    n1v4numall, n1v4numall_unweighted = get_n('Ntk4mfvVertexHistosOnlyOneVtx')
    n1v5numall, n1v5numall_unweighted = get_n('mfvVertexHistosOnlyOneVtx')
    n2v3numall, n2v3numall_unweighted = get_n('Ntk3mfvVertexHistosFullSel')
    n2v4numall, n2v4numall_unweighted = get_n('Ntk4mfvVertexHistosFullSel')
    n2v5numall, n2v5numall_unweighted = get_n('mfvVertexHistosFullSel')

    if namenumvtx is not None:
        h = f.Get(namenumvtx)
        numvtx = h.Integral(h.FindBin(nvtx), 1000000)
    else:
        numvtx = -1


    tot_sum += numall * weight
    tot_var += numall * weight**2
   
    if n2v3numall*weight < 0.0:
        n2v3numall = 0.0
    if n2v4numall*weight < 0.0:
        n2v4numall = 0.0
    if n2v5numall*weight < 0.0:
        n2v5numall = 0.0
    if n1v3numall*weight < 0.0:
        n1v3numall = 0.0
    if n1v4numall*weight < 0.0:
        n1v4numall = 0.0
    if n1v5numall*weight < 0.0:
        n1v5numall = 0.0

 
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
        print '%s & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.2f\pm%.2f$ & $%.1f\pm%.1f$ & $%.2f\pm%.2f$ & $%.1f\pm%.1f$ & $%.2f\pm%.2f$ \\\\' % (sname, numall*weight, numall**0.5 * weight, n1v3numall*weight, n1v3numall**0.5 * weight, n2v3numall*weight, n2v3numall**0.5 * weight, n1v4numall*weight, n1v4numall**0.5 * weight, n2v4numall*weight, n2v4numall**0.5 * weight, n1v5numall*weight, n1v5numall**0.5 * weight, n2v5numall*weight, n2v5numall**0.5 * weight)
        #print '%s & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.2f\pm%.2f$ \\\\' % (sname, numall*weight, numall**0.5 * weight, n1v3numall*weight, n1v3numall**0.5 * weight, n2v3numall*weight, n2v3numall**0.5 * weight, n1v4numall*weight, n1v4numall**0.5 * weight, n2v4numall*weight, n2v4numall**0.5 * weight, n1v5numall*weight, n1v5numall**0.5 * weight, n2v5numall*weight, n2v5numall**0.5 * weight)
        #print sname+" & "+"{:.2e}".format(sample.xsec)+" & %d & %.3f  \\\\"%(den, weight) 
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
    if vh :
        fns = [os.path.join(dir, sn + '_run2.root') for sn in ' VHToSSTodddd_tau1mm_M55 VHToSSTodddd_tau10mm_M55 '.split()]
    elif rpv : 
        fns = [os.path.join(dir, sn + '_run2.root') for sn in ' mfv_neu_tau001000um_M0400 mfv_stopdbardbar_tau000300um_M0400 mfv_stopdbardbar_tau001000um_M0200 '.split()]
    elif ggh :
        fns = [os.path.join(dir, sn + '_run2.root') for sn in ' ggHToSSTodddd_tau1mm_M55 ggHToSSTodddd_tau10mm_M55 ggHToSSTodddd_tau10mm_M15 '.split()]
    else : 
        #fns = [os.path.join(dir, sn + '_leptonpresel_' + year + '.root') for sn in ' qcd ttbar wjetstolnu dyjets diboson '.split()]
        #fns = [os.path.join(dir, sn + '_btagpresel_' + year + '.root') for sn in 'qcd ttbar '.split()]
        #fns = [os.path.join(dir, sn + '_' + year + '.root') for sn in '  wjetstolnu_0j  wjetstolnu_1j  wjetstolnu_2j ww  zz  wz dyjetstollM10 dyjetstollM50  ttbar qcdmupt15  qcdempt015  qcdempt020  qcdempt030  qcdempt050  qcdempt080  qcdempt120  qcdempt170  qcdempt300  qcdbctoept015 qcdbctoept020  qcdbctoept030  qcdbctoept080  qcdbctoept170  qcdbctoept250 '.split()]
        
        #fns += [ os.path.join(dir, sn + '_' + year + '.root') for sn in 'qcdpt15mupt5 qcdpt20mupt5 qcdpt30mupt5 qcdpt50mupt5 qcdpt80mupt5 qcdpt120mupt5 qcdpt170mupt5 qcdpt300mupt5 qcdpt470mupt5 qcdpt600mupt5 qcdpt800mupt5 qcdpt1000mupt5'.split()]

        fns =  [os.path.join(dir, sn + '_' + year + '.root') for sn in ' qcdht0100 qcdht0200 qcdht0300 qcdht0500 qcdht0700 qcdht1000 qcdht1500 qcdht2000 ttbar'.split()]  
    
    fns = [fn for fn in fns if os.path.isfile(fn)]
    nosort = True
    print_sum = True
if not nosort:
    fns.sort()
if csv:
    print 'sample,weight,den,num,eff,weighted,err_weighted'

print(year, " int_lumi ", int_lumi)
for fn in fns:
    effs(fn)
print 'total & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%d\pm%d$ & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ & $%.2f\pm%.2f$' % ( tot_sum, tot_var**0.5,tot_n1v3, err_tot_n1v3**0.5, tot_n2v3, err_tot_n2v3**0.5, tot_n1v4, err_tot_n1v4**0.5, tot_n2v4, err_tot_n2v4**0.5, tot_n1v5, err_tot_n1v5**0.5, tot_n2v5, err_tot_n2v5**0.5)
if print_sum:
    if csv:
        print 'sum for %f/pb,,,,,%f,%f' % (int_lumi, tot_sum, tot_var**0.5)
    else:
        print 'sum for %.1f/pb: %5.2f +/- %5.2f' % (int_lumi, tot_sum, tot_var**0.5)
