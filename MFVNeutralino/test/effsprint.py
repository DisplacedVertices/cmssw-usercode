import sys, os
from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples

sum = 0.
var = 0.
int_lumi = 20000.
cuts = () if 'nonm1' in sys.argv else ('Ntracks', 'Drmin', 'Drmax', 'Mindrmax', 'Bs2derr', 'Njets', 'Bs2dsig', 'Ntracksptgt3', 'Sumnhitsbehind')
integral = 'entries' not in sys.argv
if not integral:
    print 'using GetEntries(), but "pass vtx only" and all nm1s still use Integral()'

def effs(fn):
    global sum, var
    f = ROOT.TFile(fn)
    if integral:
        den = f.Get('mfvEventHistosNoCuts/h_npv').Integral(0,1000000)
        numall = f.Get('mfvEventHistos/h_npv').Integral(0,1000000)
    else:
        den = f.Get('mfvEventHistosNoCuts/h_npv').GetEntries()
        numall = f.Get('mfvEventHistos/h_npv').GetEntries()
    h = f.Get('mfvVertexHistos/h_nsv')
    numvtx = h.Integral(h.FindBin(2), 1000000)
    sname = os.path.basename(fn).replace('.root','')
    try:
        s = getattr(Samples, sname)
        weight = s.cross_section*int_lumi/(den/s.ana_filter_eff)
    except AttributeError:
        weight = 1.
    sum += numall * weight
    var += numall * weight**2
    print '%s (w = %.3e): # ev: %5i  pass evt+vtx: %5i -> %5.3e  pass vtx only: %5i -> %5.3e' % (sname.ljust(30), weight, den, numall, float(numall)/den, numvtx, float(numvtx)/den)
    for cut in cuts:
        nm1 = f.Get('hstNo%s/h_nsv' % cut).Integral(h.FindBin(2), 1000000)
        print '    remove %s cut: %5i -> %5.3e (n-1: %5.3e)' % (cut.ljust(10), nm1, float(nm1)/den, float(numall)/nm1 if nm1 > 0 else -1)

fns = [x for x in sys.argv[1:] if os.path.isfile(x) and x.endswith('.root')]
if not fns:
    dir = [x for x in sys.argv[1:] if os.path.isdir(x)][0]
    fns = [os.path.join(dir, fn) for fn in 'qcdht0100.root qcdht0250.root qcdht0500.root qcdht1000.root ttbardilep.root ttbarhadronic.root ttbarsemilep.root'.split()]
fns.sort()
for fn in fns:
    effs(fn)
print 'sum for %.1f/fb: %5.2f +/- %5.2f' % (int_lumi, sum, var**0.5)
