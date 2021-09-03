import sys
from DVCode.Tools.ROOTTools import *

fn = sys.argv[1]
f = ROOT.TFile(fn)

print fn

limit_t = f.Get('limit')
limit_by_toy = {}
for _ in ttree_iterator(limit_t):
    limit_by_toy[limit_t.iToy] = limit_t.limit

toys = f.Get('toys')
for ktoy in toys.GetListOfKeys():
    toy = ktoy.GetName()
    assert toy.startswith('toy_')
    itoy = int(toy.replace('toy_',''))

    a,b,c = x = [int(ktoy.ReadObj().get()['n_obs_binb%i'%i].getVal()) for i in 0,1,2]
    print sum(x), x, limit_by_toy[itoy]
