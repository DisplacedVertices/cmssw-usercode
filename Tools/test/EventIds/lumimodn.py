import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import colors
set_style()

ps = plot_saver(plot_dir('lumimodn'), size=(600,600), log=False)

fns = root_fns_from_argv()
ns = [os.path.basename(fn).replace('.root', '') for fn in fns]
fs = [ROOT.TFile.Open(fn) for fn in fns]
ts = [f.Get('EventIdRecorder/t') for f in fs]
drs = [draw_hist_register(t) for t in ts]
cs = [1,2,3,4,6,7,8,9] + range(40,50) + range(30,40)
while len(cs) < len(drs):
    cs *= 2

for j in [8]: #xrange(2,12):
    header = 'lumi%' + str(j) + ' remainders\n'
    header += '%25s %12s   ' % ('sample', 'n')
    header += ' '.join('%10i' % i for i in xrange(j))
    header += '     ratio 1st half/2nd half'
    print colors.bold(header)

    hs = []
    for i,(n,t,dr,c) in enumerate(zip(ns,ts,drs,cs)):
        h = dr.draw('lumi%'+str(j), binning='%i,0,%i' % (j,j), goff=True)
        hs.append(h)
        h.SetStats(0)
        h.SetLineWidth(2)
        h.SetLineColor(c)
        h.SetMarkerColor(c)

        bcs = [h.GetBinContent(ibin) for ibin in xrange(1,j+1)]
        print '%25s %12i  ' % (n, h.GetEntries()),
        print ' '.join(['%10i' % bc for bc in bcs]),

        a = sum(bcs[:j/2])
        b = sum(bcs[j/2:])
        n = a + b
        r, re = 9, 0
        if n > 0:
            r = a/n
            if a > 0:
                re = r*(1/a + 1/n)**0.5
        bad = abs(r - 0.5) > 0.005 # re
        print (colors.red if bad else colors.green)('    %.4f +- %.4f' % (r,re))

    draw_in_order((hs, 'hist text'))
    ps.save('lumimod%i' % j)
    print
