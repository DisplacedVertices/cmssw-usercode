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

def arrit(l):
    return array('d', l)

def get_f_t(x, min_ntracks=None):
    if issubclass(type(x), Samples.Sample):
        sample = x
        input_fn = 'crab/One2Two/%s.root' % sample.name
    elif type(x) == str:
        input_fn = x
    f = ROOT.TFile.Open(input_fn)
    t = f.Get('mfvMiniTree/t')
    t.SetAlias('svdist', 'sqrt((x0-x1)**2 + (y0-y1)**2)')
    t.SetAlias('svdphi', 'TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))')
    t.SetAlias('svdz',   'z0 - z1')
    if min_ntracks is not None:
        t.SetAlias('min_ntracks_ok', 'ntk0 >= %i && ntk1 >= %i' % (min_ntracks, min_ntracks))
    return f, t

bkg_samples = Samples.ttbar_samples + Samples.qcd_samples
sig_samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau0300um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]

class FitResult:
    def __init__(self, *args):
        self.fcn, self.fit = args

binning = array('d', [0.02*i for i in xrange(5)] + [0.1, .15]) # JMTBAD keep in sync with Templates.cc
nbins = len(binning) - 1

def make_h(name, contents):
    assert contents is None or len(contents) == nbins
    h = ROOT.TH1F(name, '', nbins, binning)
    hs.append(h)
    if contents is not None:
        for i,c in enumerate(contents):
            h.SetBinContent(i+1, c)
    return h
