from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import *
import pandas as pd

presel_path = '/uscms_data/d2/tucker/crab_dirs/PreselHistosV27m'
#sel_path = '/uscms_data/d3/dquach/crab3dirs/HistosV27m_moresidebands'
sel_path = '/uscms/home/pkotamni/nobackup/crabdirs/Histos2trkmergedV27m'
data = bool_from_argv('data')
year = '2017' if len(sys.argv) < 2 else sys.argv[1]
varname = 'nom' if len(sys.argv) < 3 else sys.argv[2] # use the BTV variations to compute syst shifts on pred2v
print("variation: %s" % varname)

# turn this on to get the proper pred2v stat err
# FIXME eventually just use this in place of epred
print_pred_n2v_propagated_stat_err = True

if data:
    fn, presel_scale = 'JetHT%s.root' % year, 1.
else:
    fn, presel_scale = 'background_%s.root' % year, 1.

def propagate_product(x, y, ex, ey):
    p = x * y
    e = p * ((ex / x)**2 + (ey / y)**2)**0.5
    return e

def fb(ft,efft,frt):
    return (ft-frt)/(efft-frt)

presel_f = ROOT.TFile(os.path.join(presel_path, fn))
sel_f = ROOT.TFile(os.path.join(sel_path, fn))
effs = pd.read_csv('MiniTree/efficiencies/all_effs.csv',index_col='variant')
cb_vals = pd.read_csv('One2Two/cb_vals/cb_vals.csv',index_col='variant')

fracdict = {}
cdict = {}
presel_var = 'presel_%s_%s' % (year, varname)
fracdict['presel'] = fb(effs.at[presel_var,'ft'], effs.at[presel_var,'efft'], effs.at[presel_var,'frt'])

for ntk in 3,4,5,7,8,9:
    fracdict[ntk] = {}
    cdict[ntk] = {}

    var = '%strk_1v_%s_%s' % (ntk, year, varname)
    try:
        fracdict[ntk]['1v'] = fb(effs.at[var,'ft'], effs.at[var,'efft'], effs.at[var,'frt'])
    except:
        print "Warning: did not find effs for",ntk
        fracdict[ntk]['1v'] = 0

    year_formatted = year if not data else "data_%s" % year
    cb_label = '%s_%strk' % (year_formatted, ntk)
    try:
        cdict[ntk]['cb'] = cb_vals.at[cb_label+'_cb','cb_val']
        cdict[ntk]['cbbar'] = cb_vals.at[cb_label+'_cbbar','cb_val']
    except:
        print "Warning: did not find cb/cbbar for",ntk
        cdict[ntk]['cb'] = 0
        cdict[ntk]['cbbar'] = 0

npresel, enpresel = get_integral(presel_f.Get('mfvEventHistosJetPreSel/h_npu'))
npresel  *= presel_scale
enpresel *= presel_scale
f0 = fracdict['presel']

print 'year:', year
print 'presel events: %8.0f +- %4.0f' % (npresel, enpresel)
print 'fraction of presel events with b-quarks: %.3f' % f0
print '%16s %8s %8s %8s %19s %15s %35s' % ('n1v', 'f1', 'cb', 'cbbar', 'pred n2v', 'n2v', 'ratio')

sum_n1v = 0
alpha_nn = {}
sum_rest = 0
sum2_erest = 0
sum_n2v = 0
sum2_en2v =0
sum2_en1v = 0
for ntk in 3,4,5:
   n1v, en1v = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % ('' if ntk == 5 else 'Ntk%s' % ntk)))
   n2v, en2v = get_integral(sel_f.Get('%smfvEventHistosFullSel/h_npu' % ('' if ntk == 5 else 'Ntk%s' % ntk)))
   sum_n1v += n1v
   f1 = fracdict[ntk]['1v']
   alpha = ((f0 - f1)*(f0 - f1)) - (f0*(f0-1)) #simplified alphas by assume Cb and Cbbar are about the same for all track multiplicities  
   alpha_nn[ntk] = alpha
   sum_rest += (n2v/alpha)
   sum2_erest += (en2v/alpha)**2 
   sum_n2v += n2v 
   sum2_en2v += (en2v**2)
   sum2_en1v += (en1v**2)
print 'n1 = %8.0f'%(sum_n1v)
print 'en1 = %f'%(math.sqrt(sum2_en1v)) 

alpha_nm = {}
for ntk in 'Ntk3or4','Ntk3or5', 'Ntk4or5':
   tracks = [int(i) for i in ntk if i.isdigit()]
   ntktot = sum(tracks)
   f1 = []
   for i, n in enumerate(tracks):
        if n == 5:
	    tracks[i] = ''
	    f1.append(fracdict[5]['1v'])
	else:
	    tracks[i] = 'Ntk%s' % n
	    f1.append(fracdict[n]['1v'])
   n1v0, en1v0 = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % tracks[0]))
   n1v1, en1v1 = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % tracks[1]))
   n2v, en2v = get_integral(sel_f.Get('%smfvEventHistosFullSel/h_npu' % ntk))
   alpha = ((f0 - f1[0])*(f0 - f1[1])) - (f0*(f0-1)) #simplified alphas by assume Cb and Cbbar are about the same for all track multiplicities     
   alpha_nm[ntk] = alpha
   sum_rest += (n2v/alpha)
   sum2_erest += (en2v/alpha)**2
   sum_n2v += n2v
   sum2_en2v += (en2v**2) 

for ntk in 3,4,5:
    n1v, en1v = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % ('' if ntk == 5 else 'Ntk%s' % ntk)))
    n2v, en2v = get_integral(sel_f.Get('%smfvEventHistosFullSel/h_npu' % ('' if ntk == 5 else 'Ntk%s' % ntk)))
    n2v_poisson = poisson_interval(n2v)
    f1 = fracdict[ntk]['1v']
    cb = cdict[ntk]['cb']
    cbbar = cdict[ntk]['cbbar']
    print 'start printing out beta + e_beta'
    effn1v = n1v/sum_n1v
    eeffn1v = effn1v * math.sqrt( (en1v/n1v)**2 + ((sum2_en1v)/(sum_n1v**2)))
    #pred = n1v**2 / (npresel * (1-f0) * (f1 / (1-f1) + 1)**2) * ((f1 / (1 - f1))**2 * ((1 - f0) / f0) * cb + cbbar)
    pred = (n1v**2 /(sum_n1v)**2) * (alpha_nn[ntk]) * sum_rest  
    epred = interval_to_vpme(*propagate_ratio(n1v**2, npresel, 2 * n1v * en1v, enpresel))[1] # ignores f0, f1 uncert
    rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
    eratl, erath = n2v_poisson / pred
    #print '%8.0f +- %4.0f %8.3f %8.3f %8.3f %9.3f +- %6.3f %7.1f +- %4.1f  PI: [%5.1f, %5.1f] %7.2f +- %.2f PI: [%4.2f, %4.2f]' % (n1v, en1v, f1, cb, cbbar, pred, epred, n2v, en2v, n2v_poisson[0], n2v_poisson[1], rat, erat, eratl, erath)
    if print_pred_n2v_propagated_stat_err :
        # see https://www.evernote.com/shard/s376/nl/201739427/5a38bab1-3b56-442e-82e2-13d9ac597fb8/ ("Stat error on 2-vertex prediction and uncertainty on prediction due to BTV SFs")
        #pred_n2v_propagated_stat_err = 2 * (n1v * n1v / npresel) * (f1 * f1 / f0) * cb * math.sqrt( 1./(n1v*f1) ) + 2 * (n1v * n1v / npresel) * ( (1-f1) * (1-f1) / (1-f0) ) * cbbar * math.sqrt( 1./(n1v * (1-f1)) )
        pred_n2v_propagated_stat_err = pred * math.sqrt((eeffn1v/effn1v)**2 + (eeffn1v/effn1v)**2 + (sum2_erest/(sum_rest**2)))
        epred = pred_n2v_propagated_stat_err
        print "pred_n2v_propagated_stat_err %8.3f (%8.3f percent)" % (pred_n2v_propagated_stat_err, (100*pred_n2v_propagated_stat_err/pred))
    print '%8.0f +- %4.0f %8.3f %8.3f %8.3f %9.3f +- %6.3f %7.1f +- %4.1f  PI: [%5.1f, %5.1f] %7.2f +- %.2f PI: [%4.2f, %4.2f]' % (n1v, en1v, f1, cb, cbbar, pred, epred, n2v, en2v, n2v_poisson[0], n2v_poisson[1], rat, erat, eratl, erath)
print
print '%16s %16s %8s %8s %8s %8s %19s %15s %35s' % ('n1v0', 'n1v1', 'f1_0', 'f1_1', 'cb', 'cbbar', 'pred n2v', 'n2v', 'ratio')

for ntk in 'Ntk3or4','Ntk3or5', 'Ntk4or5':
    tracks = [int(i) for i in ntk if i.isdigit()]
    ntktot = sum(tracks)
    f1 = []
    for i, n in enumerate(tracks):
        if n == 5:
            tracks[i] = ''
            f1.append(fracdict[5]['1v'])
        else:
            tracks[i] = 'Ntk%s' % n
            f1.append(fracdict[n]['1v'])
    n1v0, en1v0 = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % tracks[0]))
    n1v1, en1v1 = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % tracks[1]))
    n2v, en2v = get_integral(sel_f.Get('%smfvEventHistosFullSel/h_npu' % ntk))
    cb = cdict[ntktot]['cb']
    cbbar = cdict[ntktot]['cbbar']
    n2v_poisson = poisson_interval(n2v)
    effn1v0 = n1v0/sum_n1v
    eeffn1v0 = effn1v0 * math.sqrt( (en1v0/n1v0)**2 + ((sum2_en1v)/(sum_n1v**2)))
    effn1v1 = n1v1/sum_n1v
    eeffn1v1 = effn1v1 * math.sqrt( (en1v1/n1v1)**2 + ((sum2_en1v)/(sum_n1v**2))) 
    #pred = 2 * n1v0*n1v1 / (npresel * (1-f0) * (f1[0] / (1-f1[0]) + 1) * (f1[1] / (1-f1[1]) + 1)) * ((f1[0] / (1 - f1[0])) * (f1[1] / (1 - f1[1])) * ((1 - f0) / f0) * cb + cbbar)
    pred = (2*(n1v0*n1v1)/(sum_n1v**2)) * (alpha_nm[ntk]) * sum_rest
    epred = interval_to_vpme(*propagate_ratio(n1v0 * n1v1, npresel, propagate_product(n1v0, n1v1, en1v0, en1v1), enpresel))[1]
    rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
    eratl, erath = n2v_poisson / pred
    #print '%8.0f +- %4.0f %8.0f +- %4.0f %8.3f %8.3f %8.3f %8.3f %9.3f +- %6.3f %7.1f +- %4.1f  PI: [%5.1f, %5.1f] %7.2f +- %4.2f PI: [%4.2f, %4.2f]' % (n1v0, en1v0, n1v1, en1v1, f1[0], f1[1], cb, cbbar, pred, epred, n2v, en2v, n2v_poisson[0], n2v_poisson[1], rat, erat, eratl, erath)

    if print_pred_n2v_propagated_stat_err :
        #pred_n2v_propagated_stat_err = (n1v0 * n1v1 / npresel) * (f1[0] * f1[1] / f0) * cb * math.sqrt( 1./(n1v0*f1[0]) + 1./(n1v1*f1[1]) ) + (n1v0 * n1v1 / npresel) * ( (1-f1[0]) * (1-f1[1]) / (1-f0) ) * cbbar * math.sqrt( 1./(n1v0 * (1-f1[0])) + 1./(n1v1 * (1-f1[1]))  )
        pred_n2v_propagated_stat_err = pred * math.sqrt((eeffn1v0/effn1v0)**2 + (eeffn1v1/effn1v1)**2 + (sum2_erest/(sum_rest**2)))
        epred = pred_n2v_propagated_stat_err    
        print "pred_n2v_propagated_stat_err %8.3f (%8.3f percent)" % (pred_n2v_propagated_stat_err, (100*pred_n2v_propagated_stat_err/pred))
    print '%8.0f +- %4.0f %8.0f +- %4.0f %8.3f %8.3f %8.3f %8.3f %9.3f +- %6.3f %7.1f +- %4.1f  PI: [%5.1f, %5.1f] %7.2f +- %4.2f PI: [%4.2f, %4.2f]' % (n1v0, en1v0, n1v1, en1v1, f1[0], f1[1], cb, cbbar, pred, epred, n2v, en2v, n2v_poisson[0], n2v_poisson[1], rat, erat, eratl, erath)

