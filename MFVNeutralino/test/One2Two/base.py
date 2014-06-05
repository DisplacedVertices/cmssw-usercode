import sys, os
from array import array
from collections import namedtuple
from math import log, pi
from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
set_style()
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetOptStat(2222222)
ROOT.gStyle.SetOptFit(2222)

def arrit(l):
    return array('d', l)

def get_f_t(x, min_ntracks):
    if issubclass(type(x), Samples.Sample):
        sample = x
        input_fn = 'crab/One2Two/%s.root' % sample.name
    elif type(x) == str:
        input_fn = x
    f = ROOT.TFile(input_fn)
    t = f.Get('mfvOne2Two/t')
    t.SetAlias('svdist', 'sqrt((x0-x1)**2 + (y0-y1)**2)')
    t.SetAlias('svdphi', 'TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))')
    t.SetAlias('min_ntracks_ok', 'ntk0 >= %i && ntk1 >= %i' % (min_ntracks, min_ntracks))
    return f, t

bkg_samples = Samples.ttbar_samples + Samples.qcd_samples
sig_samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau0300um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]
