from JMTucker.Tools.ROOTTools import *

presel_path = '/uscms_data/d2/tucker/crab_dirs/PreselHistosV25m'
sel_path = '/uscms_data/d2/tucker/crab_dirs/HistosV25mv3'

if 'data' in sys.argv:
    fn, presel_scale = 'JetHT2017p8.root', 0.1
else:
    fn, presel_scale = 'background_2017.root', 1.

presel_f = ROOT.TFile(os.path.join(presel_path, fn))
sel_f = ROOT.TFile(os.path.join(sel_path, fn))

npresel, enpresel = get_integral(presel_f.Get('mfvEventHistosJetPreSel/h_npu'))
npresel  *= presel_scale
enpresel *= presel_scale
print 'presel events predicted: %8.0f +- %4.0f' % (npresel, enpresel)
print '%16s %24s %19s %19s %15s' % ('n1v', 'e1v', 'pred n2v', 'n2v', 'ratio')
for ntk in 'Ntk3', 'Ntk4', '':
    n1v, en1v = get_integral(sel_f.Get('%smfvEventHistosOnlyOneVtx/h_npu' % ntk))
    n2v, en2v = get_integral(sel_f.Get('%smfvEventHistosFullSel/h_npu' % ntk))
    e1v, ee1v = effective_wilson_score_vpme(n1v, en1v, npresel, enpresel)
    pred = e1v**2 * npresel
    epred = (2 * e1v * npresel * ee1v**2 + e1v**2 * enpresel)**0.5
    rat, erat = interval_to_vpme(*propagate_ratio(n2v, pred, en2v, epred))
    print '%8.0f +- %4.0f %13.2e +- %7.2e %9.3f +- %6.3f %9.3f +- %6.3f %7.2f +- %4.2f' % (n1v, en1v, e1v, ee1v, pred, epred, n2v, en2v, rat, erat)
