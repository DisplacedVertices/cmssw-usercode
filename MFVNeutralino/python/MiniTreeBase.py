import sys, os
from glob import glob
from array import array
from collections import namedtuple, Counter
from functools import partial
from itertools import combinations, permutations
from math import log, pi
from pprint import pprint
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.ROOTTools import *
import JMTucker.MFVNeutralino.AnalysisConstants as ac
import JMTucker.Tools.Samples as Samples
set_style()
ROOT.TH1.AddDirectory(0)

def t_path(ntk):
    if ntk in (3,4):
        return 'mfvMiniTreeNtk%i/t' % ntk
    elif ntk == 7:
        return 'mfvMiniTreeNtk3or4/t'
    elif ntk == 5:
        return 'mfvMiniTree/t'
    else:
        raise ValueError('ntk = %i' % ntk)

def get_f_t(x, min_ntracks=5, tree_path='trees'):
    if issubclass(type(x), Samples.Sample):
        sample = x
        input_fn = os.path.join(tree_path, '%s.root' % sample.name)
    elif type(x) == str:
        input_fn = x
    f = ROOT.TFile.Open(input_fn)
    if not f:
        raise IOError("couldn't open file %s" % input_fn)
    t = f.Get(t_path(min_ntracks))
    if not t:
        raise IOError("couldn't get tree from %s for ntks=%s" % (input_fn, min_ntracks))
    t.SetAlias('jetht', 'Sum$((jet_pt>40)*jet_pt)')
    t.SetAlias('svdist', 'sqrt((x0-x1)**2 + (y0-y1)**2)')
    t.SetAlias('sumdbv', 'sqrt((x0**2)+(y0**2)) + sqrt((x1**2)+(y1**2))')
    t.SetAlias('svdphi', 'TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))')
    t.SetAlias('svdz',   'z0 - z1')
    if min_ntracks >= 5:
        t.SetAlias('min_ntracks_ok', 'ntk0 >= %i && ntk1 >= %i' % (min_ntracks, min_ntracks))
    elif min_ntracks in (3,4):
        t.SetAlias('min_ntracks_ok', 'ntk0 == %i && ntk1 == %i' % (min_ntracks, min_ntracks))
    return f, t

def duplicate_check(fn):
    branches = 'nvtx:ntk0:ntk1:x0:y0:z0:x1:y1:z1'
    #branches = 'run:lumi:event:nvtx:ntk0:ntk1:x0:y0:z0:x1:y1:z1'
    #branches = 'run:lumi:event'
    def xform(x):
        assert len(x) == 9
        return tuple([int(y) for y in x[:3]] + [int(float(y)*1000) for y in x[3:]]) # vertex positions rounded to 10 um
        #return tuple([int(y) for y in x])
    for ntk in 3,4,7,5:
        try:
            f,t = get_f_t(fn, ntk)
        except IOError:
            print "skipping duplicate check for %s ntk=%s" % (fn, ntk)
            continue
        c = Counter(detree(t, branches, xform=xform))
        dups = [(k,v) for k,v in c.iteritems() if v > 1]
        dups_2vtx = [(k,v) for k,v in c.iteritems() if v > 1 and k[0] > 1]
        if dups_2vtx:
            print 'TWO-VERTEX DUPLICATES!', fn
        if dups:
            print 'DUPLICATES!', fn
            pprint(dups)

bkg_samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017
data_samples = Samples.data_samples_2017
#sig_samples = [] #Samples.mfv_neu_tau00100um_M0400, Samples.mfv_neu_tau00300um_M0400, Samples.mfv_neu_tau01000um_M0400, Samples.mfv_neu_tau10000um_M0400]

class FitResult:
    def __init__(self, *args):
        self.fcn, self.fit = args

binning = to_array(0, 0.04, 0.07, 4)
short_binning = binning[:]
short_binning[-1] = 0.15
nbins = len(binning) - 1

def make_raw_h(name, contents, use_short_binning=False):
    assert contents is None or len(contents) == nbins
    h = ROOT.TH1F(name, '', nbins, short_binning if use_short_binning else binning)
    if contents is not None:
        for i,c in enumerate(contents):
            h.SetBinContent(i+1, c)
    return h

def make_h(fn, name):
    f, t = get_f_t(fn, min_ntracks=5)
    h = make_raw_h(name, None)
    x = detree(t, 'svdist', 'nvtx >= 2 && min_ntracks_ok', lambda x: (float(x[0]),))
    for (d,) in x:
        if d > binning[-1]:
            d = binning[-1] - 1e-4
        h.Fill(d)
    return h

def dump_rle(fn, min_ntracks=5):
    f,t = get_f_t(fn, min_ntracks)
    for rle in sorted(detree(t)):
        print '%i %i %i' % rle

def dump(fn, min_ntracks=5):
    f,t = get_f_t(fn, min_ntracks)
    branches = 'run:lumi:event:nvtx:ntk0:ntk1'
    fmt = ' '.join(['%s'] * (branches.count(':')+1))
    for x in sorted(detree(t, branches)):
        print fmt % x

if __name__ == '__main__':
    cmd = sys.argv[1]
    ntk = 5 if len(sys.argv) == 3 else int(sys.argv[3])
    if cmd == 'dump_rle':
        dump_rle(sys.argv[2], ntk)
    elif cmd == 'dump':
        dump(sys.argv[2], ntk)
    elif cmd == 'dups':
        duplicate_check(sys.argv[2])
    else:
        sys.exit('no cmd %s' % cmd)
