import sys, os, glob
from array import array
from collections import namedtuple
from math import log, pi
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.ROOTTools import *
import JMTucker.MFVNeutralino.AnalysisConstants as ac
import JMTucker.Tools.Samples as Samples
set_style()
ROOT.TH1.AddDirectory(0)
ROOT.TH1.SetDefaultSumw2()

def get_f_t(x, min_ntracks=None, tree_path='trees'):
    if issubclass(type(x), Samples.Sample):
        sample = x
        input_fn = os.path.join(tree_path, '%s.root' % sample.name)
    elif type(x) == str:
        input_fn = x
    f = ROOT.TFile.Open(input_fn)
    if min_ntracks:
        t = f.Get('mfvMiniTreeNtk%i/t' % min_ntracks)
    else:
        t = f.Get('mfvMiniTree/t')
    t.SetAlias('jetht', 'Sum$((jet_pt>40)*jet_pt)')
    t.SetAlias('svdist', 'sqrt((x0-x1)**2 + (y0-y1)**2)')
    t.SetAlias('svdphi', 'TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))')
    t.SetAlias('svdz',   'z0 - z1')
    if min_ntracks >= 5:
        t.SetAlias('min_ntracks_ok', 'ntk0 >= %i && ntk1 >= %i' % (min_ntracks, min_ntracks))
    elif min_ntracks in (3,4):
        t.SetAlias('min_ntracks_ok', 'ntk0 == %i && ntk1 == %i' % (min_ntracks, min_ntracks))
    return f, t

bkg_samples = Samples.ttbar_samples + Samples.qcd_samples_sum
data_samples = Samples.data_samples
#sig_samples = [] #Samples.mfv_neu_tau00100um_M0400, Samples.mfv_neu_tau00300um_M0400, Samples.mfv_neu_tau01000um_M0400, Samples.mfv_neu_tau10000um_M0400]

class FitResult:
    def __init__(self, *args):
        self.fcn, self.fit = args

binning = to_array([0.02*i for i in xrange(5)] + [0.1, 5]) # JMTBAD keep in sync with Templates.cc
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

