import sys, os
from collections import defaultdict
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.gStyle.SetOptStat(110)
ps = plot_saver(plot_dir('vtoy'), size=(400,300), log=False)

path = sys.argv[1]
if os.path.isdir(path):
    path = os.path.join(path, 'expected.root')
f = ROOT.TFile(path)

limit_t = f.Get('limit')
limit_by_toy = {}
for _ in ttree_iterator(limit_t):
    limit_by_toy[limit_t.iToy] = limit_t.limit

limit_by_dist = defaultdict(list)
toys = f.Get('toys')
for ktoy in toys.GetListOfKeys():
    toy = ktoy.GetName()
    assert toy.startswith('toy_')
    itoy = int(toy.replace('toy_',''))

    a,b,c = x = [int(ktoy.ReadObj().get()['n_obs_binb%i'%i].getVal()) for i in 0,1,2]
    k = (sum(x), a,b,c)
    limit_by_dist[k].append(limit_by_toy[itoy])

dists = sorted(limit_by_dist.keys())
mv = max(max(x) for x in limit_by_dist.values())
mv2 = 0.8
assert mv < mv2
mv = mv2
for dist in dists:
    name = '%i_%i_%i_%i' % dist
    h = ROOT.TH1D(name, 'sum=%i, [%i,%i,%i]' % dist, 1000, 0, mv)
    for v in limit_by_dist[dist]:
        h.Fill(v)
    h.Draw()
    ps.c.Update()
    resize_stat_box(h, (0.2, 0.1))
    ps.save(name)

