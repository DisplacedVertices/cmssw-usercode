from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import *
import pandas as pd
import numpy as np

from JMTucker.Tools import Samples
from JMTucker.Tools.Sample import MCSample
from JMTucker.MFVNeutralino.PerSignal import PerSignal
from JMTucker.MFVNeutralino.UtilitiesBase import *
import glob

lep = True
bjet = False

is_signal = False

#lepton triggers
#presel_path = '/uscms/home/yuqingwu/nobackup/crabdirs/26-10-19-MiniTree_tag004Lepm5_unblind_5trk_1vtx_inverted_mass_and_sumpt'
#sel_path = '/uscms/home/yuqingwu/nobackup/crabdirs/26-10-19-MiniTree_tag004Lepm5_unblind_5trk_1vtx_inverted_mass_and_sumpt'

#btag triggers
#presel_path = '/uscms/home/yuqingwu/nobackup/crabdirs/26-10-15-MiniTree_tag004BvetoLHTm4_unblind_5trk_1vtx-Joey-Data'
#sel_path = '/uscms/home/yuqingwu/nobackup/crabdirs/26-10-15-MiniTree_tag004BvetoLHTm4_unblind_5trk_1vtx-Joey-Data'

#signal samples
is_signal = True
presel_path = '/uscms/home/yuqingwu/nobackup/crabdirs/26-10-26-MiniTree_tag004Lepm-Signal/VHToSSTodddd_tau10mm_M55_run2'
sel_path = '/uscms/home/yuqingwu/nobackup/crabdirs/26-10-26-MiniTree_tag004Lepm-Signal/VHToSSTodddd_tau10mm_M55_run2'
#presel_path = '/uscms/home/yuqingwu/nobackup/crabdirs/26-10-26-MiniTree_tag004BvetoLHTm-Signal'
#sel_path = '/uscms/home/yuqingwu/nobackup/crabdirs/26-10-26-MiniTree_tag004BvetoLHTm-Signal'

data = False
year = 'run2' if len(sys.argv) < 2 else sys.argv[1]
varname = 'nom' if len(sys.argv) < 3 else sys.argv[2] # use the BTV variations to compute syst shifts on pred2v
print("variation: %s" % varname)

if data:
    #fn, presel_scale = 'Lepton_data_%s.root' % year, 1.
    fn, presel_scale = 'Bjet_data_%s.root' % year, 1.
elif not is_signal:
    #fn, presel_scale = 'background_leptonpresel_%s.root' % year, 1.
    fn, presel_scale = 'background_btagpresel_%s.root' % year, 1.
    #fn, presel_scale = 'dyjets_leptonpresel_%s.root' % year, 1.
    #fn, presel_scale = 'ttbar_btagpresel_%s.root' % year, 1.
else:
    fn, presel_scale = '*HToSSTodddd_tau10mm_M55_201*.root', 1.

signal_fns = sorted(glob.glob(os.path.join(presel_path, fn)))
if not signal_fns:
    raise ValueError('no signal files matched %s' % os.path.join(presel_path, fn))

signal_fs = []
signal_scales = []

def propagate_product(x, y, ex, ey):
    p = x * y
    e = p * ((ex / x)**2 + (ey / y)**2)**0.5
    return e

def fb(ft,efft,frt):
    return (ft-frt)/(efft-frt)

#presel_f = ROOT.TFile.Open(os.path.join(presel_path, fn))
#sel_f = ROOT.TFile.Open(os.path.join(sel_path, fn))

for fn in signal_fns:
    sample_index = os.path.basename(fn).replace('.root', '')
    mcsample = eval('Samples.' + sample_index)
    Samples._set_signal_stuff(mcsample)

    signal_f = ROOT.TFile.Open(fn)
    sumw = mcsample.sumw(signal_f)

    lumi = 0.0
    if "20161" in sample_index:
        lumi = AnalysisConstants.int_lumi_20161
    elif "20162" in sample_index:
        lumi = AnalysisConstants.int_lumi_20162
    elif "2017" in sample_index:
        if bjet:
            lumi = AnalysisConstants.int_lumi_bjet_trig_2017
        elif lep:
            lumi = AnalysisConstants.int_lumi_2017
    elif "2018" in sample_index:
        if bjet:
            lumi = AnalysisConstants.int_lumi_bjet_trig_2018
        elif lep:
            lumi = AnalysisConstants.int_lumi_2018
    else:
        raise NotImplementedError("Lumi not defined for sample %s" % sample_index)
    
    scale = mcsample.xsec * lumi / sumw
    signal_fs.append(signal_f)
    signal_scales.append(scale)

    print "Signal file:", fn
    print "   sumw, xsec, lumi:", sumw, mcsample.xsec, lumi
    print "   presel_scale:", scale
    print ""

def get_scaled_integral(signal_fs, signal_scales, hist_path, **kwargs):
    """
    Wrapper for get_integral()
    -Forces integral_only=False while calling get_integral

    -INPUTS-
    signal_fs: list of ROOT.TFile objects
    signal_scales: list of floats, to scale the integrals and uncertainties
    hist_path: path to the histogram in the ROOT files (ex. 'mfvMiniTreePreSelEvtFilt/h_nsv')
    """

    tot_int = 0.0
    tot_var = 0.0

    for signal_f, scale in zip(signal_fs, signal_scales):
        hist = signal_f.Get(hist_path)
        temp_val, temp_err = get_integral(hist, integral_only=False, **kwargs)
        tot_int += temp_val * scale
        tot_var += (temp_err * scale)**2
    
    if 'integral_only' in kwargs and kwargs['integral_only']:
        return tot_int
    else:
        return tot_int, np.sqrt(tot_var)


npresel, err_npresel = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTreePreSelEvtFilt/h_nsv')

print 'year:', year
print 'presel events: %8.2f +- %4.2f' % (npresel, err_npresel)
#print '%16s %19s %15s %35s' % ('n1v', 'pred n2v', 'n2v', 'ratio')

#See these evernotes for an explanation of the calculations:
#Error of efficiencies (replacement of the Binomial error): https://www.evernote.com/client/web#/notes/b4b263d9-3aef-4116-4c27-0cb66c582ca3
#Errors relating to N+M-trk events, and ratios: https://share.evernote.com/note/4a8218f4-569c-391d-3f91-9ed9b44ab02a
#Descriptions of the variables used by the previous code version: https://share.evernote.com/note/a3ac74f7-7416-dda2-1015-59791328824e
#Evernotes written by previous authors of this code: https://www.evernote.com/shard/s376/nl/66335180/7657f560-7151-4de9-b495-10ffb4cd3b74 and https://www.evernote.com/shard/s376/nl/66335180/aedb1579-5f71-4313-8730-bc43a2ef4579
tot_n1v = 0 #total input(MC or observed) 1-vtx events
tot_n2v = 0 #total input(MC or observed) 2-vtx events
var_n1v = 0 #the quadratic sum of errors due each 1-vtx input(MC or observed)
var_n2v = 0 #the quadratic sum of errors due each 2-vtx input(MC or observed)

if data:
    ntk_ls = [3,4,5]
    ntk_ls_2v = [3,4]
    ntk2_ls = ['Ntk3or4', 'Ntk3or5', 'Ntk4or5']
else:
    ntk_ls = [3,4,5]
    ntk_ls_2v = [3,4,5]
    ntk2_ls = ['Ntk3or4', 'Ntk3or5', 'Ntk4or5']

for ntk in ntk_ls:
    n1v, err_n1v = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk), xlo=2, xhi=2, x_are_bins=True)
    if ntk in ntk_ls_2v:
        n2v, err_n2v = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk), xlo=3, xhi=999, x_are_bins=True)
    else:
        n2v, err_n2v = 0.0, 0.0
    
    tot_n1v += n1v
    tot_n2v += n2v 
    var_n2v += (err_n2v**2)
    var_n1v += (err_n1v**2)

print 'n1 = %8.2f'%(tot_n1v)
print 'err_n1 = %f'%(math.sqrt(var_n1v)) 
for ntk in ntk2_ls:
    tracks = [int(i) for i in ntk if i.isdigit()]
    ntktot = sum(tracks)
    for i, n in enumerate(tracks):
        if n == 5:
            tracks[i] = ''
        else:
            tracks[i] = 'Ntk%s' % n
    
    n2v, err_n2v = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTree%s/h_nsv' % ('%sexact' % ntk))

    tot_n2v += n2v
    var_n2v += (err_n2v**2) 

print 'n2 = %8.2f'%(tot_n2v)
print 'err_n2 = %f'%(math.sqrt(var_n2v)) 
print '%8s %16s %19s %15s %35s' % ('ntracks', 'n1v', 'pred n2v', 'n2v', 'ratio')

for ntk in ntk_ls:
    n1v, err_n1v = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk), xlo=2, xhi=2, x_are_bins=True)
    if ntk in ntk_ls_2v:
        n2v, err_n2v = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk), xlo=3, xhi=999, x_are_bins=True)
    else:
        n2v, err_n2v = 0.0, 0.0
    n2v_poiss = poisson_interval(n2v) # FIXME - Do NOT use for MC
    effn1v = n1v/tot_n1v
    err_effn1v = np.sqrt(((1.0-2*effn1v)*err_n1v**2+effn1v**2*var_n1v) / tot_n1v**2)
    pred = (effn1v**2) * tot_n2v
    var_fracvNN = (2*(effn1v**2)*(err_effn1v/effn1v))**2
    if tot_n2v == 0:
        err_pred = pred * (np.sqrt( ( np.sqrt(var_n2v)/1)**2 + (np.sqrt(var_fracvNN)/(effn1v**2))**2)) # set #2-vtx events to 1
    else:
        err_pred = pred * (np.sqrt( ( np.sqrt(var_n2v)/tot_n2v)**2 + (np.sqrt(var_fracvNN)/(effn1v**2))**2))
    if ntk not in ntk_ls_2v:
        print "Printing predicted and error for %s-trk 2-vtx events: %9.7f +- %6.7f" % (ntk, pred, err_pred)
        continue
    effn2v = n2v/tot_n2v
    if err_n2v == 0: err_n2v = 1.0
    if effn2v!=1:
        err_effn2v = np.sqrt(((1.0-2*effn2v)*err_n2v**2+effn2v**2*var_n2v) / tot_n2v**2)
    elif effn2v==1:
        err_effn2v = np.sqrt(((1.0-2*effn2v)*err_n2v**2+effn2v**2*(var_n2v+1)) / tot_n2v**2)
    else:
        raise Exception
    rat = n2v/pred
    if effn2v!=0:
        err_rat = rat * np.sqrt( (err_effn2v/effn2v)**2 + 4*(err_effn1v/effn1v)**2 )
    else:
        err_rat = np.sqrt((1/pred)**2 + (n2v/pred**2)**2 * err_pred**2)
    if pred == 0:
        err_ratl_poiss, err_rath_poiss =  [n2v_temp / 1 for n2v_temp in n2v_poiss] # FIXME - Do NOT use for MC
    else:
        err_ratl_poiss, err_rath_poiss =  [n2v_temp / pred for n2v_temp in n2v_poiss] # FIXME - Do NOT use for MC
    print '%5d %11.3f +- %4.3f %9.6f +- %6.6f %7.3f +- %4.3f  PI: [%5.1f, %5.1f] %7.4f +- %.4f PI: [%4.2f, %4.2f]' % (ntk, n1v, err_n1v, pred, err_pred, n2v, err_n2v, n2v_poiss[0], n2v_poiss[1], rat, err_rat, err_ratl_poiss, err_rath_poiss)
print
print '%8s %16s %16s %19s %15s %35s' % ('ntracks', 'n1vN', 'n1vM', 'pred n2v', 'n2v', 'ratio')

for ntk in ntk2_ls:
    ntkspervtx = [int(i) for i in ntk if i.isdigit()]
    tracks = [int(i) for i in ntk if i.isdigit()]
    ntktot = sum(tracks)
    for i, n in enumerate(tracks):
        if n == 5:
            tracks[i] = ''
        else:
            tracks[i] = 'Ntk%s' % n

    n1vN, err_n1vN = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTree%s/h_nsv' % ('' if tracks[0] == 5 else '%s' % tracks[0]), xlo=2, xhi=2, x_are_bins=True)
    n1vM, err_n1vM = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTree%s/h_nsv' % ('' if tracks[1] == 5 else '%s' % tracks[1]), xlo=2, xhi=2, x_are_bins=True)
    n1v_oth = tot_n1v - n1vN - n1vM
    err_n1v_oth = np.sqrt(var_n1v - err_n1vN**2 - err_n1vM**2)
    
    n2v, err_n2v = get_scaled_integral(signal_fs, signal_scales, 'mfvMiniTree%s/h_nsv' % ('%sexact' % ntk))

    n2v_poiss = poisson_interval(n2v) # FIXME - Do NOT use for MC
    effn1vN = n1vN/tot_n1v
    effn1vM = n1vM/tot_n1v
    effn2v = n2v/tot_n2v
    if err_n2v == 0: err_n2v = 1.0
    err_effn2v = np.sqrt(((1.0-2*effn2v)*err_n2v**2+effn2v**2*var_n2v) / tot_n2v**2)
    pred = (2*(effn1vN)*(effn1vM))*tot_n2v
    var_fracvNM = (1.0-2*effn1vN)**2*(err_n1vN/n1vN)**2 + (1.0-2*effn1vM)**2*(err_n1vM/n1vM)**2 + 4*(err_n1v_oth/tot_n1v)**2
    if tot_n2v == 0:
        err_pred = pred * np.sqrt(var_n2v + var_fracvNM) # set #2-vtx events to 1
    else:
        err_pred = pred * np.sqrt(var_n2v/(tot_n2v)**2 + var_fracvNM)
    rat = n2v/pred
    if effn2v!=0:
        err_rat = rat * np.sqrt((err_effn2v/effn2v)**2 + var_fracvNM)
    else:
        err_rat = np.sqrt((1/pred)**2 + (n2v/pred**2)**2 * err_pred**2)
    err_ratl_poiss, err_rath_poiss =  [n2v_temp / pred for n2v_temp in n2v_poiss] # FIXME - Do NOT use for MC

    print '%3d %s %d %11.3f +- %4.3f %8.3f +- %4.3f %9.6f +- %6.6f %7.3f +- %4.3f  PI: [%5.1f, %5.1f] %7.4f +- %.4f PI: [%4.2f, %4.2f]'% (ntkspervtx[0], 'x', ntkspervtx[1], n1vN, err_n1vN, n1vM, err_n1vM, pred, err_pred, n2v, err_n2v, n2v_poiss[0], n2v_poiss[1], rat, err_rat, err_ratl_poiss, err_rath_poiss)
