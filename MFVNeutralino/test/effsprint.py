#!/usr/bin/env python

# py $tmain/effsprint.py one . > effsprint.one.txt ; py $tmain/effsprint.py . > effsprint.txt ; py $tmain/effsprint.py . sigreg > effsprint.sigreg.txt ; py $tmain/effsprint.py mfv*root xx4*root sigreg > effsprint.sigreg.sigs.txt ;   py $tmain/effsprint.py mfv*root xx4*root  > effsprint.sigs.txt
# py $tmain/effsprint.py csv one . > effsprint.one.csv ; py $tmain/effsprint.py csv . > effsprint.csv ; py $tmain/effsprint.py csv . sigreg > effsprint.sigreg.csv ; py $tmain/effsprint.py csv mfv*root xx4*root sigreg > effsprint.sigreg.sigs.csv ;   py $tmain/effsprint.py csv mfv*root xx4*root  > effsprint.sigs.csv

import sys, os
from DVCode.Tools.ROOTTools import *
from DVCode.Tools.Sample import norm_from_file
import DVCode.Tools.Samples as Samples
import DVCode.MFVNeutralino.AnalysisConstants as ac

csv = 'csv' in sys.argv
plots = 'plots' in sys.argv
if plots:
    set_style()
    ROOT.gStyle.SetPaintTextFormat('.2g')
    ps = plot_saver('plots/nm1s', size=(500,500), log=False)

tot_sum = 0.
tot_var = 0.
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
    global tot_sum, tot_var

    f = ROOT.TFile(fn)

    def get_n(dir_name):
        h = f.Get('%s/h_npv' % dir_name)
        return h.Integral(0,1000000) if integral else h.GetEntries()

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

    numall = get_n(namenumall)
    if namenumvtx is not None:
        h = f.Get(namenumvtx)
        numvtx = h.Integral(h.FindBin(nvtx), 1000000)
    else:
        numvtx = -1

    tot_sum += numall * weight
    tot_var += numall * weight**2
    if csv:
        print '%s,%e,%f,%f,%f,%f,%f' % (sname, weight, den, numall, float(numall)/den, numall*weight, numall**0.5 * weight)
    else:
        print '%s (w = %.3e): # ev: %10.1f  pass evt+vtx: %5.1f -> %5.3e  pass vtx only: %5.1f -> %5.3e' % (sname.ljust(30), weight, den, numall, float(numall)/den, numvtx, float(numvtx)/den)
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
                nm1 = get_n('%sevtHst%sVNo%s' % (ntk, nvtx, cut))
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
    fns = [os.path.join(dir, sn + '.root') for sn in 'qcdht0700_2017 qcdht1000_2017 qcdht1500_2017 qcdht2000_2017 ttbarht0600_2017 ttbarht0800_2017 ttbarht1200_2017 ttbarht2500_2017'.split()]
    fns = [fn for fn in fns if os.path.isfile(fn)]
    nosort = True
    print_sum = True
if not nosort:
    fns.sort()
if csv:
    print 'sample,weight,den,num,eff,weighted,err_weighted'
for fn in fns:
    effs(fn)
if print_sum:
    if csv:
        print 'sum for %f/pb,,,,,%f,%f' % (int_lumi, tot_sum, tot_var**0.5)
    else:
        print 'sum for %.1f/pb: %5.2f +/- %5.2f' % (int_lumi, tot_sum, tot_var**0.5)
