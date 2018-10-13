from JMTucker.Tools.ROOTTools import *

presel_fn = '/uscms_data/d2/tucker/crab_dirs/NtupleV20m_EventHistosOnlyV2/background_2017.root'
fn = '/uscms_data/d2/tucker/crab_dirs/HistosV20mp1/background_2017.root'

presel_f = ROOT.TFile(presel_fn)
f = ROOT.TFile(fn)

npresel, enpresel = get_integral(presel_f.Get('mfvEventHistosJetPreSel/h_npu'))
print 'presel events predicted: %8.0f +- %4.0f' % (npresel, enpresel)
print '%16s %24s %19s %19s %15s' % ('n1v', 'e1v', 'pred n2v', 'n2v', 'ratio')
for ntk in 'Ntk3', 'Ntk4', '':
    n1v, en1v = get_integral(f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % ntk))
    n2v, en2v = get_integral(f.Get('%smfvEventHistosFullSel/h_npu' % ntk))
    e1v, ee1v = effective_wilson_score_vpme(n1v, en1v, npresel, enpresel)
    pred = e1v**2 * npresel
    epred = (2 * e1v * npresel * ee1v**2 + e1v**2 * enpresel)**0.5
    rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
    print '%8.0f +- %4.0f %13.2e +- %7.2e %9.3f +- %6.3f %9.3f +- %6.3f %7.2f +- %4.2f' % (n1v, en1v, e1v, ee1v, pred, epred, n2v, en2v, rat, erat)
