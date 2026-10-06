from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import *
import pandas as pd
import numpy as np

from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

#presel_path = '/eos/user/p/pekotamn/MiniTree_LepIPCut_FixHT2016_OnnormdzULV30BvetoLHTm' #FIXME 
#presel_path = '/eos/user/p/pekotamn/MiniTree_LepIPCut_OnnormdzULV30Lepm'
#sel_path = '/eos/user/p/pekotamn/MiniTree_LepIPCut_FixHT2016_OnnormdzULV30BvetoLHTm'  #FIXME
#sel_path = '/eos/user/p/pekotamn/MiniTree_LepIPCut_OnnormdzULV30Lepm'
#presel_path = 'root://cmsxrootd.fnal.gov//store/group/lpclonglived/alecduqu/MiniTree_LepIPCut_Lepton_SF_2018correctionsLepm_noef'
#sel_path = 'root://cmsxrootd.fnal.gov//store/group/lpclonglived/alecduqu/MiniTree_LepIPCut_Lepton_SF_2018correctionsLepm_noef'
#presel_path = '~/crab_dirs/MiniTree_LepIPCut_eventweights_Lepton_SF_2018correctionsLepm_noef'
#sel_path = '~/crab_dirs/MiniTree_LepIPCut_eventweights_Lepton_SF_2018correctionsLepm_noef'
#presel_path = '/uscms/home/joeyr/crabdirs/MiniTree__tagTestFixTrigThresholdsBvetoLHTm'
#sel_path = '/uscms/home/joeyr/crabdirs/MiniTree__tagTestFixTrigThresholdsBvetoLHTm'

#lepton triggers
presel_path = '/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm'
sel_path = '/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm'

#btag triggers
#presel_path = '/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm'
#sel_path = '/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm'

#signal samples
#presel_path = '/uscms/home/alecduqu/crab_dirs'
#sel_path = '/uscms/home/alecduqu/crab_dirs'

data = bool_from_argv('data')
year = 'run2' if len(sys.argv) < 2 else sys.argv[1]
varname = 'nom' if len(sys.argv) < 3 else sys.argv[2] # use the BTV variations to compute syst shifts on pred2v
print("variation: %s" % varname)

if data:
    #fn, presel_scale = 'SingleLepton%s.root' % year, 1.
    fn, presel_scale = 'BTagDispl%s.root' % year, 1.
else:
    #fn, presel_scale = 'background_leptonpresel_%s.root' % year, 1.
    #fn, presel_scale = 'background_btagpresel_%s.root' % year, 1.
    #fn, presel_scale = 'dyjets_leptonpresel_%s.root' % year, 1.
    #fn, presel_scale = 'ttbar_btagpresel_%s.root' % year, 1.
    fn, presel_scale = 'ggHToSSTodddd_tau1mm_M55_%s.root' % year, 1.
def propagate_product(x, y, ex, ey):
    p = x * y
    e = p * ((ex / x)**2 + (ey / y)**2)**0.5
    return e

def fb(ft,efft,frt):
    return (ft-frt)/(efft-frt)

#presel_f = ROOT.TFile(os.path.join(presel_path, fn))
#sel_f = ROOT.TFile(os.path.join(sel_path, fn))
presel_f = ROOT.TFile.Open(os.path.join(presel_path, fn))
sel_f = ROOT.TFile.Open(os.path.join(sel_path, fn))

npresel, err_npresel = get_integral(presel_f.Get('mfvMiniTreePreSelEvtFilt/h_nsv'))

print 'year:', year
print 'presel events: %8.0f +- %4.0f' % (npresel, err_npresel)
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
    ntk_ls = [3,4]
    ntk2_ls = ['Ntk3or4']
else:
    ntk_ls = [3,4,5]
    ntk2_ls = ['Ntk3or4', 'Ntk3or5', 'Ntk4or5']

for ntk in ntk_ls:
    n1v, err_n1v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk)), 2, 2, x_are_bins=True)
    n2v, err_n2v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk)), 3, 999, x_are_bins=True)
    
    tot_n1v += n1v
    tot_n2v += n2v 
    var_n2v += (err_n2v**2)
    var_n1v += (err_n1v**2)

print 'n1 = %8.0f'%(tot_n1v)
print 'err_n1 = %f'%(math.sqrt(var_n1v)) 
for ntk in ntk2_ls:
    tracks = [int(i) for i in ntk if i.isdigit()]
    ntktot = sum(tracks)
    for i, n in enumerate(tracks):
        if n == 5:
            tracks[i] = ''
        else:
            tracks[i] = 'Ntk%s' % n
    
    n2v, err_n2v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('%sexact' % ntk)))

    tot_n2v += n2v
    var_n2v += (err_n2v**2) 

print 'n2 = %8.0f'%(tot_n2v)
print 'err_n2 = %f'%(math.sqrt(var_n2v)) 
print '%8s %16s %19s %15s %35s' % ('ntracks', 'n1v', 'pred n2v', 'n2v', 'ratio')

for ntk in ntk_ls:
    n1v, err_n1v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk)), 2, 2, x_are_bins=True)
    n2v, err_n2v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk)), 3, 999, x_are_bins=True)
    n2v_poiss = poisson_interval(n2v) # FIXME - Do NOT use for MC
    effn1v = n1v/tot_n1v
    err_effn1v = np.sqrt(((1.0-2*effn1v)*err_n1v**2+effn1v**2*var_n1v) / tot_n1v**2)
    pred = (effn1v**2) * tot_n2v
    var_fracvNN = (2*(effn1v**2)*(err_effn1v/effn1v))**2
    if tot_n2v == 0:
        err_pred = pred * (np.sqrt( ( np.sqrt(var_n2v)/1)**2 + (np.sqrt(var_fracvNN)/(effn1v**2))**2)) # set #2-vtx events to 1
    else:
        err_pred = pred * (np.sqrt( ( np.sqrt(var_n2v)/tot_n2v)**2 + (np.sqrt(var_fracvNN)/(effn1v**2))**2))
    effn2v = n2v/tot_n2v
    err_effn2v = np.sqrt(((1.0-2*effn2v)*err_n2v**2+effn2v**2*var_n2v) / tot_n2v**2)
    rat = n2v/pred
    err_rat = rat * np.sqrt( (err_effn2v/effn2v)**2 + 4*(err_effn1v/effn1v)**2 )
    if pred == 0:
        err_ratl_poiss, err_rath_poiss =  [n2v_temp / 1 for n2v_temp in n2v_poiss] # FIXME - Do NOT use for MC
    else:
        err_ratl_poiss, err_rath_poiss =  [n2v_temp / pred for n2v_temp in n2v_poiss] # FIXME - Do NOT use for MC
    print '%5d %11.0f +- %4.0f %9.3f +- %6.3f %7.1f +- %4.1f  PI: [%5.1f, %5.1f] %7.4f +- %.4f PI: [%4.2f, %4.2f]' % (ntk, n1v, err_n1v, pred, err_pred, n2v, err_n2v, n2v_poiss[0], n2v_poiss[1], rat, err_rat, err_ratl_poiss, err_rath_poiss)
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

    n1vN, err_n1vN = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if tracks[0] == 5 else '%s' % tracks[0])), 2, 2, x_are_bins=True)
    n1vM, err_n1vM = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if tracks[1] == 5 else '%s' % tracks[1])), 2, 2, x_are_bins=True)
    n1v_oth = tot_n1v - n1vN - n1vM
    err_n1v_oth = np.sqrt(var_n1v - err_n1vN**2 - err_n1vM**2)
    
    n2v, err_n2v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('%sexact' % ntk)))

    n2v_poiss = poisson_interval(n2v) # FIXME - Do NOT use for MC
    effn1vN = n1vN/tot_n1v
    effn1vM = n1vM/tot_n1v
    effn2v = n2v/tot_n2v
    err_effn2v = np.sqrt(((1.0-2*effn2v)*err_n2v**2+effn2v**2*var_n2v) / tot_n2v**2)
    pred = (2*(effn1vN)*(effn1vM))*tot_n2v
    var_fracvNM = (1.0-2*effn1vN)**2*(err_n1vN/n1vN)**2 + (1.0-2*effn1vM)**2*(err_n1vM/n1vM)**2 + 4*(err_n1v_oth/tot_n1v)**2
    if tot_n2v == 0:
        err_pred = pred * np.sqrt(var_n2v + var_fracvNM) # set #2-vtx events to 1
    else:
        err_pred = pred * np.sqrt(var_n2v/(tot_n2v)**2 + var_fracvNM)
    rat = n2v/pred
    err_rat = rat * np.sqrt((err_effn2v/effn2v)**2 + var_fracvNM)
    err_ratl_poiss, err_rath_poiss =  [n2v_temp / pred for n2v_temp in n2v_poiss] # FIXME - Do NOT use for MC

    print '%3d %s %d %11.0f +- %4.0f %8.0f +- %4.0f %9.3f +- %6.3f %7.1f +- %4.1f  PI: [%5.1f, %5.1f] %7.4f +- %.4f PI: [%4.2f, %4.2f]'% (ntkspervtx[0], 'x', ntkspervtx[1], n1vN, err_n1vN, n1vM, err_n1vM, pred, err_pred, n2v, err_n2v, n2v_poiss[0], n2v_poiss[1], rat, err_rat, err_ratl_poiss, err_rath_poiss)
