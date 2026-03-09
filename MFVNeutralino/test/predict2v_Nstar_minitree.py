from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import *
import pandas as pd
import numpy as np

from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

presel_path = '/eos/user/p/pekotamn/MiniTree_LepIPCut_FixHT2016_OnnormdzULV30BvetoLHTm' #FIXME 
#presel_path = '/eos/user/p/pekotamn/MiniTree_LepIPCut_OnnormdzULV30Lepm'
sel_path = '/eos/user/p/pekotamn/MiniTree_LepIPCut_FixHT2016_OnnormdzULV30BvetoLHTm'  #FIXME
#sel_path = '/eos/user/p/pekotamn/MiniTree_LepIPCut_OnnormdzULV30Lepm'
data = bool_from_argv('data')
year = '2017' if len(sys.argv) < 2 else sys.argv[1]
varname = 'nom' if len(sys.argv) < 3 else sys.argv[2] # use the BTV variations to compute syst shifts on pred2v
print("variation: %s" % varname)

if data:
    #fn, presel_scale = 'SingleLepton%s.root' % year, 1.
    fn, presel_scale = 'BTagDispl%s.root' % year, 1.
else:
    #fn, presel_scale = 'background_leptonpresel_%s.root' % year, 1.
    fn, presel_scale = 'background_btagpresel_%s.root' % year, 1.
    #fn, presel_scale = 'background_%s.root' % year, 1.
def propagate_product(x, y, ex, ey):
    p = x * y
    e = p * ((ex / x)**2 + (ey / y)**2)**0.5
    return e

def fb(ft,efft,frt):
    return (ft-frt)/(efft-frt)

presel_f = ROOT.TFile(os.path.join(presel_path, fn))
sel_f = ROOT.TFile(os.path.join(sel_path, fn))

npresel, enpresel = get_integral(presel_f.Get('mfvMiniTreePreSelEvtFilt/h_nsv'))

print 'year:', year
print 'presel events: %8.0f +- %4.0f' % (npresel, enpresel)
print '%16s %19s %15s %35s' % ('n1v', 'pred n2v', 'n2v', 'ratio')

#See these evernotes(https://www.evernote.com/shard/s376/nl/66335180/7657f560-7151-4de9-b495-10ffb4cd3b74 and https://www.evernote.com/shard/s376/nl/66335180/aedb1579-5f71-4313-8730-bc43a2ef4579) for the details of this new-simplified calculation 
sum_n1v = 0 #total input(MC or observed) 1-vtx events
sum_n2v = 0 #total input(MC or observed) 2-vtx events
sum2_en2v =0 #the quadratic sum of errors due each 2-vtx input(MC or observed) 
sum2_en1v = 0 #the quadratic sum of errors due each 1-vtx input(MC or observed) 

for ntk in 3,4,5:
    n1v, en1v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk)), 2, 2, x_are_bins=True)
    n2v, en2v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk)), 3, 999, x_are_bins=True)
    
    sum_n1v += n1v
    sum_n2v += n2v 
    sum2_en2v += (en2v**2)
    sum2_en1v += (en1v**2)

print 'n1 = %8.0f'%(sum_n1v)
print 'en1 = %f'%(math.sqrt(sum2_en1v)) 
for ntk in 'Ntk3or4','Ntk3or5', 'Ntk4or5':
    tracks = [int(i) for i in ntk if i.isdigit()]
    ntktot = sum(tracks)
    for i, n in enumerate(tracks):
        if n == 5:
            tracks[i] = ''
        else:
            tracks[i] = 'Ntk%s' % n
    n1v0, en1v0 = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if tracks[0] == 5 else '%s' % tracks[0])), 2, 2, x_are_bins=True)
    n1v1, en1v1 = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if tracks[1] == 5 else '%s' % tracks[1])), 2, 2, x_are_bins=True)
    
    n2v, en2v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('%sexact' % ntk)))

    sum_n2v += n2v
    sum2_en2v += (en2v**2) 

print 'n2 = %8.0f'%(sum_n2v)
print 'en2 = %f'%(math.sqrt(sum2_en2v)) 

for ntk in 3,4,5:
    n1v, en1v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk)), 2, 2, x_are_bins=True)
    n2v, en2v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if ntk == 5 else 'Ntk%s' % ntk)), 3, 999, x_are_bins=True)
    n2v_poisson = poisson_interval(n2v)
    effn1v = n1v/sum_n1v
    eeffn1v = np.sqrt((effn1v*(1.0-effn1v))/sum_n1v)
    pred = (effn1v**2) * sum_n2v
    err_rat2 = 2*(effn1v**2)*(eeffn1v/effn1v)
    pred_n2v_propagated_stat_err = pred * (np.sqrt( ( np.sqrt(sum2_en2v)/sum_n2v)**2 + (err_rat2/(effn1v**2))**2)) 
    epred = pred_n2v_propagated_stat_err
    rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
    eratl, erath =  [n2v_temp / pred for n2v_temp in n2v_poisson] 
    print '%8.0f +- %4.0f %9.3f +- %6.3f %7.1f +- %4.1f  PI: [%5.1f, %5.1f] %7.2f +- %.2f PI: [%4.2f, %4.2f]' % (n1v, en1v, pred, epred, n2v, en2v, n2v_poisson[0], n2v_poisson[1], rat, erat, eratl, erath)
print
print '%16s %16s %19s %15s %35s' % ('n1v0', 'n1v1', 'pred n2v', 'n2v', 'ratio')

for ntk in 'Ntk3or4','Ntk3or5', 'Ntk4or5':
    tracks = [int(i) for i in ntk if i.isdigit()]
    ntktot = sum(tracks)
    for i, n in enumerate(tracks):
        if n == 5:
            tracks[i] = ''
        else:
            tracks[i] = 'Ntk%s' % n

    n1v0, en1v0 = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if tracks[0] == 5 else '%s' % tracks[0])), 2, 2, x_are_bins=True)
    n1v1, en1v1 = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('' if tracks[1] == 5 else '%s' % tracks[1])), 2, 2, x_are_bins=True)
    
    n2v, en2v = get_integral(sel_f.Get('mfvMiniTree%s/h_nsv' % ('%sexact' % ntk)))

    n2v_poisson = poisson_interval(n2v)
    effn1v0 = n1v0/sum_n1v
    eeffn1v0 = np.sqrt((effn1v0*(1.0-effn1v0))/sum_n1v)
    effn1v1 = n1v1/sum_n1v
    eeffn1v1 = np.sqrt((effn1v1*(1.0-effn1v1))/sum_n1v)
    pred = (2*(effn1v0)*(effn1v1))*sum_n2v
    err_ratv0v1 = effn1v0*effn1v0*np.sqrt( (eeffn1v0/effn1v0)**2 + (eeffn1v1/effn1v1)**2 )
    pred_n2v_propagated_stat_err =  pred * (np.sqrt( ( np.sqrt(sum2_en2v)/sum_n2v)**2 + (err_ratv0v1/(effn1v0*effn1v1))**2))
    epred = pred_n2v_propagated_stat_err    
    rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
    eratl, erath =  [n2v_temp / pred for n2v_temp in n2v_poisson] 

    print '%8.0f +- %4.0f %8.0f +- %4.0f %9.3f +- %6.3f %7.1f +- %4.1f  PI: [%5.1f, %5.1f] %7.2f +- %4.2f PI: [%4.2f, %4.2f]' % (n1v0, en1v0, n1v1, en1v1, pred, epred, n2v, en2v, n2v_poisson[0], n2v_poisson[1], rat, erat, eratl, erath)
