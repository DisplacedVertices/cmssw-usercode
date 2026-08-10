import os
from uncertainties import ufloat
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import named_product

class Efficiencies:
    class EfficiencyFor:
        pathbase = '/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverJetByJetHistsUlv30lepmumv4_20_tau001000um_2Djetdrjet1sumpCorrection'
        def __init__(self, cfg):
            self.cfg = cfg
            self.fn = os.path.join(self.pathbase,'background_leptonpresel_2017.root' if cfg.mc else 'SingleMuon2017.root')
            f = ROOT.TFile.Open(self.fn)
            self.num,self.num_unc = get_integral(f.Get('%s_npv_num' % cfg.cutset))
            self.den,self.den_unc = get_integral(f.Get('%s_npv_den' % cfg.cutset))
            self.num_w_unc = ufloat(self.num,self.num_unc)
            self.den_w_unc = ufloat(self.den,self.den_unc)
            e = self.num_w_unc/self.den_w_unc
            self.eff = e.n, e.s

            #r,l,h = wilson_score(self.num, self.den)
            #self.eff = r,(h-l)/2
        def __repr__(self):
            return repr(self.cfg) + ': %.4f +- %.4f' % self.eff

    def __init__(self, **kwargs):
        self.cfgs = named_product(_name = 'TrackMoverCfg',
                                  cutset = ['nocuts', 'ntracks', 'all'],
                                  nsigmadxy = [4.0],
                                  tau = [100,300,1000,10000,30000],
                                  njets = [2],
                                  nbjets = [0],
                                  year = [2017], #FIXME 
                                  mc = [False,True])
        self.effs = [self.EfficiencyFor(cfg) for cfg in self.cfgs]

    def __call__(self, **c):
        for e in self.effs:
            if all(getattr(e.cfg, k) == v for k,v in c.iteritems()):
                return e
        raise ValueError('nothing matching %r' % c)

efficiencies = Efficiencies()

__all__ = ['efficiencies']
