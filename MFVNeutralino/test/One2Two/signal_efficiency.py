# NB: this module cannot depend on any non-stdlib imports, except in __main__, unless you ship them with combine/submit.py

from math import hypot
import ROOT; ROOT.gROOT.SetBatch()

class _reprable(object):
    def _reprs(self):
        return [(f, repr(getattr(self, f))) for f in sorted(dir(self)) if not f.startswith('_')]
    def __repr__(self):
        return '<%s.%s(%s) at 0x%x>' % (self.__module__, self.__class__.__name__, ', '.join('%s=%s' % (f,v) for f,v in self._reprs()), id(self))
    def _dump(self):
        maxl = max(len(f) for f,_ in self._reprs())
        for f,v in self._reprs():
            print f.ljust(maxl+3), v

class _namedtuple(_reprable):
    def __init__(self, **args):
        self._fields = args.keys()[:]
        for k,v in args.iteritems():
            setattr(self, k, v)
        
class SignalEfficiencyCombiner:
    class Input(_reprable):
        def __init__(self, fn, years, w=1., include_stat=True):
            self.fn = fn
            self.years = sorted(years)
            self.nyears = len(self.years)
            self.w = w
            self.include_stat = include_stat

            self.f = ROOT.TFile.Open(self.fn)

        def get(self, bn, isample):
            n = 'h_signal_%i_%s_' % (isample, bn)
            r = [None] * self.nyears
            for y,year in enumerate(self.years):
                year = str(year)
                h = self.f.Get(n + year)
                if not h:
                    raise ValueError('no %s in %s for year %s' % (n[:-1], self.fn, year))
                else:
                    h.Scale(self.w)
                    r[y] = h
            return r
                
    def __init__(self, years=['2016','2017','2018']):
        self.years = sorted(str(y) for y in years)
        self.nyears = len(self.years)

        self.inputs = [self.Input('limitsinput.root', self.years)]
        self.f = self.inputs[0].f # any of the f are equivalent for name_list and bkg stuff
        self.ninputs = len(self.inputs)

        get_int_lumis = lambda inp: [inp.f.Get('h_int_lumi_%s' % year).GetBinContent(1) for year in self.years]
        self.int_lumis = get_int_lumis(self.inputs[0])
        assert all(self.int_lumis == get_int_lumis(inp) for inp in self.inputs[1:])
        self.total_int_lumi = sum(self.int_lumis)

        sumw = sum(inp.w for inp in self.inputs)
        for inp in self.inputs:
            inp.w /= sumw

    def combine(self, isample):
        nice_name = None

        ngens = [0] * self.nyears
        hs_dbv = [None] * self.nyears
        hs_dphi = [None] * self.nyears
        hs_dvv = [None] * self.nyears
        hs_dvv_rebin = [None] * self.nyears
        hs_uncert = None # don't add these between inputs so we just set from the first input

        def _deyear(n):
            x = n.rsplit('_',1)
            assert x[1] in self.years
            return x[0]
        def _cset(x,y):
            if x is not None:
                assert x==y
            return y
        def _add_h(hs):
            h = hs[0].Clone(_deyear(hs[0].GetName()))
            for h2 in hs[1:]:
                h.Add(h2)
            return h
        def _add_hs(hs, hs2):
            r = []
            for h, h2 in zip(hs, hs2):
                if h is None:
                    h = h2.Clone()
                else:
                    h.Add(h2)
                r.append(h)
            return r

        for inp in self.inputs:
            hs_ngen = inp.get('ngen', isample)
            nice_name = _cset(nice_name, _deyear(hs_ngen[0].GetTitle()))
            if inp.include_stat:
                ngens = [n + int(h.GetBinContent(1)) for n, h in zip(ngens, hs_ngen)]

            hs_dbv       = _add_hs(hs_dbv,       inp.get('dbv',       isample))
            hs_dphi      = _add_hs(hs_dphi,      inp.get('dphi',      isample))
            hs_dvv       = _add_hs(hs_dvv,       inp.get('dvv',       isample))
            hs_dvv_rebin = _add_hs(hs_dvv_rebin, inp.get('dvv_rebin', isample))

            if hs_uncert is None:
                hs_uncert = inp.get('uncert', isample)

        rates = [tuple(h.GetBinContent(ib) for ib in xrange(1,h.GetNbinsX()+1)) for h in hs_dvv_rebin]
        rate = [sum(r) for r in zip(*rates)]
        tot_rate = sum(rate)

        uncerts = [tuple(h.GetBinContent(ib) for ib in xrange(1,h.GetNbinsX()+1)) for h in hs_uncert]

        class Result(_namedtuple): pass
        yearit = lambda x: dict(zip(self.years, x))
        return Result(isample = isample,
                      nice_name = nice_name,
                      ngens = yearit(ngens),
                      hs_dbv = yearit(hs_dbv),
                      hs_dphi = yearit(hs_dphi),
                      hs_dvv = yearit(hs_dvv),
                      hs_dvv_rebin = yearit(hs_dvv_rebin),
                      hs_uncert = yearit(hs_uncert),

                      rates = yearit(rates),
                      uncerts = yearit(uncerts),
                      rate = yearit(rate),

                      h_dbv = _add_h(hs_dbv),
                      h_dphi = _add_h(hs_dphi),
                      h_dvv = _add_h(hs_dvv),
                      h_dvv_rebin = _add_h(hs_dvv_rebin),

                      tot_rate = tot_rate,
                      )

if __name__ == '__main__':
    combiner = SignalEfficiencyCombiner()
    isample = None
    try:
        import sys
        isample = int(sys.argv[1])
    except ValueError:
        from limitsinput import name2isample
        isample = name2isample(combiner.f, sys.argv[1])
    except IndexError:
        pass
    if isample is not None:
        r = combiner.combine(isample)
        r._dump()

