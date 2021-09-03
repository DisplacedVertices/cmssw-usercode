import sys, os
from DVCode.Tools.ROOTTools import ROOT
import DVCode.Tools.Samples as Samples

for i, fn in enumerate(sys.argv[1:]):
    if not fn.endswith('.root') or not os.path.isfile(fn):
        continue
    f = ROOT.TFile(fn)
    h = f.Get('mfvWeight/h_sums')
    if not h:
        h = f.Get('mcStat/h_sums')

    nevents_orig = -1
    try:
        sn = os.path.basename(fn).replace('.root', '')
        s = getattr(Samples, sn)
        print 'sample %s nevents_orig: %s' % (sn, s.nevents_orig)
        nevents_orig = s.nevents_orig
    except AttributeError:
        pass
    for i in xrange(1, h.GetNbinsX()+1):
        print '%2i %30s %20.1f' % (i, h.GetXaxis().GetBinLabel(i), h.GetBinContent(i)),
        if i == 1:
            print '  %.3f' % (h.GetBinContent(i) / nevents_orig)
        else:
            print
    print
