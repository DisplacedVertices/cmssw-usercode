import os
from DVCode.Tools.ROOTTools import *
from DVCode.Tools.general import named_product

class Efficiencies:
    class EfficiencyFor:
        pathbase = '/uscms_data/d2/tucker/crab_dirs/TrackMoverHistsV21mV2'
        def __init__(self, cfg):
            self.cfg = cfg
            self.fn = os.path.join(self.pathbase,
                                   ('nsig%.1f' % cfg.nsigmadxy).replace('.', 'p'),
                                   'tau%06ium' % cfg.tau,
                                   '%i%i' % (cfg.njets, cfg.nbjets),
                                   'background_2017.root' if cfg.mc else 'JetHT2017.root'
                                   )
            f = ROOT.TFile(self.fn)
            self.num = get_integral(f.Get('%s_npv_num' % cfg.cutset))[0]
            self.den = get_integral(f.Get('%s_npv_den' % cfg.cutset))[0]
            r,l,h = wilson_score(self.num, self.den)
            self.eff = r,(h-l)/2

        def __repr__(self):
            return repr(self.cfg) + ': %.4f +- %.4f' % self.eff

    def __init__(self, **kwargs):
        self.cfgs = named_product(_name = 'TrackMoverCfg',
                                  cutset = ['nocuts', 'ntracks', 'all'],
                                  nsigmadxy = [4.0],
                                  tau = [100,300,1000,10000,30000],
                                  njets = [2,3],
                                  nbjets = [0,1,2],
                                  mc = [False,True])
        self.effs = [self.EfficiencyFor(cfg) for cfg in self.cfgs]

    def __call__(self, **c):
        for e in self.effs:
            if all(getattr(e.cfg, k) == v for k,v in c.iteritems()):
                return e
        raise ValueError('nothing matching %r' % c)

efficiencies = Efficiencies()

__all__ = ['efficiencies']
