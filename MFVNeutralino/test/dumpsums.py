import sys, os
from JMTucker.Tools.ROOTTools import ROOT
import JMTucker.Tools.Samples as Samples

for i, fn in enumerate(sys.argv[1:]):
    if not fn.endswith('.root') or not os.path.isfile(fn):
        continue
    f = ROOT.TFile(fn)
    h = f.Get('mfvWeight/h_sums')

    sn = os.path.basename(fn).replace('.root', '')
    print sn
    s = getattr(Samples, sn)
    print 'sample nevents_orig:', s.nevents_orig
    for i in xrange(1, h.GetNbinsX()+1):
        print '%2i %30s %20.1f' % (i, h.GetXaxis().GetBinLabel(i), h.GetBinContent(i)),
        if i == 1:
            print '  %.3f' % (h.GetBinContent(i) / s.nevents_orig)
        else:
            print
    print
