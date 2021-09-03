#!/usr/bin/env python

from DVCode.Tools.ROOTTools import *

if len(sys.argv) < 5:
    sys.exit('usage: renamefolder.py fn1 path1 fn2 path2\ncopies folder with path1 from file at fn1 to a new file at fn2 (overwriting any existing file) with path2')

fn1, path1, fn2, path2 = sys.argv[1:5]

f1 = ROOT.TFile(fn1)
fd1 = f1.Get(path1)

f2 = ROOT.TFile(fn2, 'recreate')
fd2 = f2.mkdir(path2)
fd2.cd()

for k in fd1.GetListOfKeys():
    k.ReadObj().Clone().Write()

f2.Write()
f2.Close()
