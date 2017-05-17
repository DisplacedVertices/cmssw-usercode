#!/usr/bin/env python

import sys
from JMTucker.Tools.ROOTTools import *

ROOT.TH1.SetDefaultSumw2()

mc_fn = sys.argv[1]
data_fn = sys.argv[2]
path = sys.argv[3]
out_fn = sys.argv[4]
if len(sys.argv) > 5:
    out_path = sys.argv[5]
else:
    out_path = path

out_f = ROOT.TFile(out_fn, 'update')
if out_f.Get(out_path):
    raise ValueError('refusing to clobber %s in %s' % (path, out_fn))

mc_f, data_f = ROOT.TFile(mc_fn), ROOT.TFile(data_fn)
mc_h, data_h = mc_f.Get(path), data_f.Get(path)
if not mc_h or not data_h:
    raise ValueError('input hists not found: mc %r data %r' % (mc_h, data_h))

out_f.cd()
rat_h = data_h.Clone(out_path)
rat_h.Divide(mc_h)
rat_h.Write()
