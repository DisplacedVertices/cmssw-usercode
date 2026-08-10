import sys, ROOT
ROOT.gROOT.SetBatch()

fn = sys.argv[1]
f = ROOT.TFile(fn)
'f.ls:'
f.ls()
for x in 'nuisances_prefit_res', 'fit_b', 'fit_s':
    print x
    f.Get(x).Print()
for x in 'tree_fit_b', 'tree_fit_sb':
    print x
    f.Get(x).Show(0)
