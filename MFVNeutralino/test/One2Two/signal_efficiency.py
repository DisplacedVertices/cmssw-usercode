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

    def __init__(self, simple=False):
        if simple:
            self.inputs = [Input(fn='limitsinput.root', int_lumi=38.529, sf=one, include_stat=True)]
        else:
            self.inputs = [
                Input(fn='limitsinput_nonhip.root', int_lumi= 2.62, sf=sf20156,  include_stat=False),
                Input(fn='limitsinput_hip.root',    int_lumi=19.70, sf=trigmult, include_stat=True),
                Input(fn='limitsinput_nonhip.root', int_lumi=16.23, sf=trigmult, include_stat=True),
                ]

        self.int_lumi = 0
        for inp in self.inputs:
            self.int_lumi += inp.int_lumi
            inp.f = ROOT.TFile(inp.fn)

    def check(self, nbins, int_lumi):
        assert self.nbins == nbins
        assert abs(self.int_lumi - int_lumi) < 0.25 # grr

    def combine(self, which):
        nice_name = None
        total_nsig = 0
        sig_rate = [0.] * self.nbins
        sig_uncert = None

        for inp in self.inputs:
            f = inp.f

            h_norm = f.Get('h_signal_%i_norm' % which)
            ngen = 1e-3 / h_norm.GetBinContent(2)
            nice_name = checkedset(nice_name, h_norm.GetTitle())
            mass = int(nice_name.split('_M')[-1])

            h_dvv = f.Get('h_signal_%i_dvv_rebin' % which)
            assert h_dvv.GetTitle() == nice_name
            assert h_dvv.GetNbinsX() == self.nbins
            nsig = self._get(h_dvv)

            if inp.include_stat:
                total_nsig += int(sum(nsig))

            for i in xrange(self.nbins):
                sig_rate[i] += nsig[i] / ngen * inp.int_lumi * inp.sf(mass)

            h_uncert = f.Get('h_signal_%i_uncert' % which)
            sig_uncert = checkedset(sig_uncert, self._get(h_uncert, offset=1))

        return Result(which = which,
                      nice_name = nice_name,
                      total_nsig = total_nsig,
                      sig_rate = sig_rate,
                      sig_uncert = sig_uncert)

if __name__ == '__main__':
    which = -1
    try:
        import sys
        which = int(sys.argv[1])
    except IndexError:
        pass
    except ValueError:
        from limitsinput import name2isample
        which = name2isample(ROOT.TFile('limitsinput.root'), sys.argv[1])
    r = SignalEfficiencyCombiner().combine(which)
    print r

