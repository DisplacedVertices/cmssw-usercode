from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import *
import pandas as pd

presel_path = '/uscms_data/d2/tucker/crab_dirs/PreselHistosV27m'
sel_path = '/uscms_data/d2/tucker/crab_dirs/HistosV27m'
data = bool_from_argv('data')
year = '2017' if len(sys.argv) < 2 else sys.argv[1]
bquark_corrected = True

if data:
    fn, presel_scale = 'JetHT%s.root' % year, 1.
else:
    fn, presel_scale = 'background_%s.root' % year, 1.

def fb(ft,efft,frt):
    return (ft-frt)/(efft-frt)

presel_f = ROOT.TFile(os.path.join(presel_path, fn))
sel_f = ROOT.TFile(os.path.join(sel_path, fn))
effs = pd.read_csv('MiniTree/efficiencies/all_effs.csv',index_col='variant')

fracdict = {}
presel_var = 'presel_%s_nom' % year
fracdict['presel'] = fb(effs.at[presel_var,'ft'], effs.at[presel_var,'efft'], effs.at[presel_var,'frt'])

for ntk in 3,4,5,7:
    fracdict[ntk] = {}
    var = '%strk_1v_%s_nom' % (ntk, year)
    fracdict[ntk]['1v'] = fb(effs.at[var,'ft'], effs.at[var,'efft'], effs.at[var,'frt'])

npresel, enpresel = get_integral(presel_f.Get('mfvEventHistosJetPreSel/h_npu'))
npresel  *= presel_scale
enpresel *= presel_scale
f0 = fracdict['presel']

if bquark_corrected:
    print 'year:', year
    print 'presel events: %8.0f +- %4.0f' % (npresel, enpresel)
    print 'fraction of presel events with b-quarks: %.3f' % f0
    print '%16s %8s %19s %19s %15s' % ('n1v', 'f1', 'pred n2v', 'n2v', 'ratio')
    for ntk in 3,4,5:
        n1v, en1v = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % ('' if ntk == 5 else 'Ntk%s' % ntk)))
        n2v, en2v = get_integral(sel_f.Get('%smfvEventHistosFullSel/h_npu' % ('' if ntk == 5 else 'Ntk%s' % ntk)))
        f1 = fracdict[ntk]['1v']
        pred = n1v**2 / (npresel * (1-f0) * (f1 / (1-f1) + 1)**2) * ((f1 / (1 - f1))**2 * ((1 - f0) / f0) + 1)
        epred = 0 # FIXME
        rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
        print '%8.0f +- %4.0f %8.3f %9.3f +- %6.3f %9.3f +- %6.3f %7.2f +- %4.2f' % (n1v, en1v, f1, pred, epred, n2v, en2v, rat, erat)
else:
    print 'year:', year
    print 'presel events predicted: %8.0f +- %4.0f' % (npresel, enpresel)
    print '%16s %25s %19s %19s %15s' % ('n1v', 'e1v', 'pred n2v', 'n2v', 'ratio')
    for ntk in 'Ntk3', 'Ntk4', '':
        n1v, en1v = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % ntk))
        n2v, en2v = get_integral(sel_f.Get('%smfvEventHistosFullSel/h_npu' % ntk))
        e1v, ee1v = effective_wilson_score_vpme(n1v, en1v, npresel, enpresel)
        pred = e1v**2 * npresel
        epred = (2 * e1v * npresel * ee1v**2 + e1v**2 * enpresel)**0.5
        rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
        print '%8.0f +- %4.0f %13.2e +- %7.2e %9.3f +- %6.3f %9.3f +- %6.3f %7.2f +- %4.2f' % (n1v, en1v, e1v, ee1v, pred, epred, n2v, en2v, rat, erat)

    print
    print '%16s %25s %16s %25s %19s %19s %15s' % ('n1v0', 'e1v0','n1v1', 'e1v0', 'pred n2v', 'n2v', 'ratio')
    for ntk in 'Ntk3or4',:# 'Ntk3or5', 'Ntk4or5':
        tracks = [int(i) for i in ntk if i.isdigit()]
        for i, n in enumerate(tracks):
            if n == 5:
                tracks[i] = ''
            else:
                tracks[i] = 'Ntk%s' % n
        n1v0, en1v0 = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % tracks[0]))
        n1v1, en1v1 = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % tracks[1]))
        n2v, en2v = get_integral(sel_f.Get('%smfvEventHistosFullSel/h_npu' % ntk))
        e1v0, ee1v0 = effective_wilson_score_vpme(n1v0, en1v0, npresel, enpresel)
        e1v1, ee1v1 = effective_wilson_score_vpme(n1v1, en1v1, npresel, enpresel)
        pred = e1v0 * e1v1 * npresel
        epred = (ee1v0 * e1v1 * npresel + e1v0 * ee1v1 * npresel + e1v0 * e1v1 * enpresel)**0.5
        rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
        print '%8.0f +- %4.0f %13.2e +- %7.2e %8.0f +- %4.0f %13.2e +- %7.2e %9.3f +- %6.3f %9.3f +- %6.3f %7.2f +- %4.2f' % (n1v0, en1v0, e1v0, ee1v0, n1v1, en1v1, e1v1, ee1v1, pred, epred, n2v, en2v, rat, erat)
