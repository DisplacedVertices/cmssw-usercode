import sys
from JMTucker.Tools.ROOTTools import *

fn = sys.argv[1]
f = ROOT.TFile(fn)

h = f.Get('mfvOverlayHistos/h_dvv_true')

target = 4000
delta = 0.001
lo = 0.099
up = 0.100
bins = [up]

while lo > 0:
    while 1:
        i = get_integral(h, lo, up)[0]
        #print lo, up, i
        if i >= target:
            break
        lo -= delta
        if lo < 0:
            lo = 0.
            break
    #print 'new edge', lo
    bins.append(lo)
    up = lo
    lo = up - delta
bins.append(lo)
bins.reverse()
print '[',
for b in bins:
    print '%0.4f,' % b,
print ']'
