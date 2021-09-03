import sys, os

try:
    split = sys.argv.index('--')
except ValueError:
    sys.exit('usage: python diffdbv.py nice1 file1.root [file1_2.root ...] -- nice2 file2.root [file2_2.root ...]')

args1 = sys.argv[1:split]
args2 = sys.argv[split+1:]
sys.argv.remove('--') # confuses finding '-b' for root later

nices = args1.pop(0), args2.pop(0)
fnses = args1, args2
for x in args1 + args2:
    assert x.endswith('.root') and (x.startswith('root://') or os.path.isfile(x))

########################################################################

from DVCode.MFVNeutralino.MiniTreeBase import *

set_style()
ps = plot_saver(plot_dir('diffdbv'), size=(350,500), log=False)

binning, binwidth = '(2000,0,0.2)', '1 #mum'

hs = {}

for nice, fns in zip(nices, fnses):
    for ntk in 3,7,4,5:
        t = ROOT.TChain(t_path(ntk))
        for fn in fns:
            t.Add(fn)

        name = '%sdbvntk%i' % (nice, ntk)
        t.Draw('dist0>>%s%s' % (name, binning))
        h = hs[name] = getattr(ROOT, name)
        move_overflow_into_last_bin(h)
        h.SetStats(0)

a,b = nices
for ntk in 3,7,4,5:
    s = 'dbvntk%i' % ntk
    h = hs[b+s]
    h.Add(hs[a+s], -1)
    h.Draw('hist')
    h.SetTitle('ntk=%i, %s - %s;d_{BV} (cm);events/%s' % (ntk,b,a,binwidth))
    ps.save(s)
