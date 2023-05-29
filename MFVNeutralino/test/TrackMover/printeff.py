from JMTucker.Tools.ROOTTools import *
from uncertainties import ufloat

fns = root_fns_from_argv()
print(fns)
width = max(len(fn) for fn in fns) + 2

cutsets = ['all', 'nocuts', 'ntracks']
print 'fn'.ljust(width), ' '.join('%19s' % x for x in cutsets)

z = []
for fn in fns:
    f = ROOT.TFile.Open(fn)
    print fn.ljust(width),
    zz = []
    for cutset in cutsets:
        num_name = '%s_npv_num' % cutset
        den_name = '%s_npv_den' % cutset

        num, num_unc = get_integral(f.Get(num_name))
        den, den_unc = get_integral(f.Get(den_name))
        num_w_unc = ufloat(num,num_unc)
        den_w_unc = ufloat(den,den_unc)
        eff = num_w_unc/den_w_unc
        r = eff.n
        e = eff.s

        #r,l,h = wilson_score(num, den)
        #e = (h-l)/2
        print '   %7.4f +- %7.4f' % (r, e),
        zz.append((r,e))
    z.append(zz)
    print

if len(z) == 2:
    print 'difference'.ljust(width),
    a,b = z
    for (aa,ea),(bb,eb) in zip(a,b):
        print '   %7.4f +- %7.4f' % (bb-aa, (ea**2 + eb**2)**0.5),
    print
    print 'ratio'.ljust(width),
    a,b = z
    for (aa,ea),(bb,eb) in zip(a,b):
        a_uf = ufloat(aa,ea)
        b_uf = ufloat(bb,eb)
        rab = a_uf/b_uf
        print '   %7.4f +- %7.4f' % (rab.n, rab.s),
