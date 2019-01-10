# NB: this module should not depend on any local imports, except in __main__, unless you ship them with combine/submit.py

from math import hypot
import ROOT; ROOT.gROOT.SetBatch()

def trigmult(x):
    return 0.99
def sf20156(x, pars=(0.9784, -1128., 1444.)):
    return trigmult(x) * (2. - pars[0] * ROOT.TMath.Erf((x-pars[1])/pars[2]))
def one(x):
    return 1.

class _namedtuple:
    def __init__(self, **args):
        self._fields = args.keys()[:]
        for k,v in args.iteritems():
            setattr(self, k, v)
    def __repr__(self):
        return '<%s.%s(%s) at 0x%x>' % (self.__module__, self.__class__.__name__, ', '.join('%s=%s' % (f, repr(getattr(self, f))) for f in dir(self) if not f.startswith('_')), id(self))
        
class Input (_namedtuple): pass
class Result(_namedtuple): pass

def checkedset(x,y):
    if x is not None:
        assert x==y
    return y

class SignalEfficiencyCombiner:
    nbins = 3

    @classmethod
    def _get(cls, h, offset=0., mult=1.):
        return [offset + mult*h.GetBinContent(ibin) for ibin in xrange(1,cls.nbins+1)]
    @classmethod
    def _gete(cls, h):
        return [h.GetBinError(ibin) for ibin in xrange(1,cls.nbins+1)]

    def __init__(self, simple=False):
        if simple:
            fn = simple if type(simple) == str else 'limitsinput.root'
            self.inputs = [Input(fn=fn, int_lumi=38.529, sf=one, include_stat=True)]
        else:
            self.inputs = [
                Input(fn='limitsinput_nonhip.root', int_lumi= 2.62, sf=sf20156,  include_stat=False),
                Input(fn='limitsinput_hip.root',    int_lumi=19.70, sf=trigmult, include_stat=True),
                Input(fn='limitsinput_nonhip.root', int_lumi=16.23, sf=trigmult, include_stat=True),
                ]

        self.int_lumi = 0
        def check_names(f, last_names=[]):
            h = f.Get('name_list')
            names = [h.GetXaxis().GetBinLabel(ibin) for ibin in xrange(1,h.GetNbinsX()+1)]
            if last_names:
                if names != last_names:
                    raise ValueError('names are different between files')
            else:
                last_names.extend(names)

        for inp in self.inputs:
            self.int_lumi += inp.int_lumi
            inp.f = ROOT.TFile(inp.fn)
            check_names(inp.f)

    def check(self, nbins, int_lumi):
        assert self.nbins == nbins
        assert abs(self.int_lumi - int_lumi) < 0.25 # grr

    def __add_h(self, h, h2, c):
        if h is None:
            h = h2.Clone()
            h.Scale(c)
        else:
            h.Add(h2, c)
        return h

    def combine(self, which):
        nice_name = None
        ngens = []
        int_lumi_sum = 0.
        total_nsig = 0
        sig_rate = [0.] * self.nbins
        sig_stat_uncert = [0.] * self.nbins
        sig_uncert = None
        h_dbv_sum = None
        h_dvvs = []
        h_dvv_sum = None

        for inp in self.inputs:
            f = inp.f

            int_lumi_sum += inp.int_lumi

            h_norm = f.Get('h_signal_%i_norm' % which)
            ngen = 1e-3 / h_norm.GetBinContent(2)
            ngens.append(ngen)
            nice_name = checkedset(nice_name, h_norm.GetTitle())
            mass = int(nice_name.split('_M')[-1])

            scale = inp.int_lumi / ngen * inp.sf(mass)

            h_dbv = f.Get('h_signal_%i_dbv' % which)
            h_dvv = f.Get('h_signal_%i_dvv' % which)
            h_dvv_rebin = f.Get('h_signal_%i_dvv_rebin' % which)
            h_dvvs.append(h_dvv_rebin)
            assert h_dbv.GetTitle() == nice_name
            assert h_dvv.GetTitle() == nice_name
            assert h_dvv_rebin.GetTitle() == nice_name
            assert h_dvv_rebin.GetNbinsX() == self.nbins

            h_dbv_sum = self.__add_h(h_dbv_sum, h_dbv, scale)
            h_dvv_sum = self.__add_h(h_dvv_sum, h_dvv, scale)

            nsig  = self._get (h_dvv_rebin)
            nsige = self._gete(h_dvv_rebin)

            if inp.include_stat:
                total_nsig += int(sum(nsig))

            for i in xrange(self.nbins):
                sig_rate[i] += nsig[i] * scale
                if inp.include_stat:
                    sig_stat_uncert[i] = hypot(sig_stat_uncert[i], scale * nsige[i])

            h_uncert = f.Get('h_signal_%i_uncert' % which)
            sig_uncert = checkedset(sig_uncert, self._get(h_uncert, offset=1))

        total_sig_rate = sum(sig_rate)
        total_sig_1v = h_dbv_sum.Integral(0,h_dbv_sum.GetNbinsX()+2)

        # NB do not confuse the three entries of h_dvvs, ngens (which
        # are the three inputs listed above) with the three entries of
        # sig_* (which are the three dvv bins)
        return Result(which = which,
                      nice_name = nice_name,
                      ngens = ngens,
                      int_lumi_sum = int_lumi_sum,
                      total_nsig = total_nsig,
                      sig_rate = sig_rate,
                      total_sig_rate = total_sig_rate,
                      sig_rate_norm = [x / total_sig_rate if total_sig_rate > 0 else 0. for x in sig_rate],
                      total_efficiency = total_sig_rate / int_lumi_sum,
                      sig_stat_uncert = sig_stat_uncert,
                      sig_uncert = sig_uncert,
                      sig_uncert_rate = [x*(y-1) for x,y in zip(sig_rate, sig_uncert)],
                      total_sig_1v = total_sig_1v,
                      h_dbv = h_dbv_sum,
                      h_dvvs = h_dvvs,
                      h_dvv = h_dvv_sum)

if __name__ == '__main__':
    which = None
    combiner = SignalEfficiencyCombiner()
    try:
        import sys
        which = int(sys.argv[1])
    except ValueError:
        from limitsinput import name2isample
        which = name2isample(combiner.inputs[0].f, sys.argv[1])
    except IndexError:
        pass
    if which is not None:
        r = combiner.combine(which)
        print r

