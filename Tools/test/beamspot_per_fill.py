from collections import defaultdict
from JMTucker.Tools.LumiLines import *
from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('../../MFVNeutralino/test/plots/beamspot_per_fill', size=(1200,600), log=False)

lls = LumiLines('/uscms/home/tucker/mfvrecipe/lumi.gzpickle')

f = ROOT.TFile('crab/BeamSpotTree_0/MultiJetPk2012.root')
t = f.Get('BeamSpotTree/t')

nvtx = defaultdict(int)
bsx = defaultdict(list)
bsy = defaultdict(list)
bsz = defaultdict(list)
pvx = defaultdict(list)
pvy = defaultdict(list)
pvz = defaultdict(list)
for jentry in ttree_iterator(t):
    if (len(lls.by_run[t.run]) > 0):
        fill = lls.by_run[t.run][0].fill
        nvtx[fill] += 1
        bsx[fill].append(t.bsx)
        bsy[fill].append(t.bsy)
        bsz[fill].append(t.bsz)
        pvx[fill].append(t.pvx)
        pvy[fill].append(t.pvy)
        pvz[fill].append(t.pvz)

fills = sorted(nvtx.keys())
nfills = len(fills)

names = ['bsx', 'bsy', 'bsz', 'pvx', 'pvy', 'pvz']
dicts = [bsx, bsy, bsz, pvx, pvy, pvz]
for i, pos in enumerate(dicts):
    g = ROOT.TGraphErrors(nfills)
    for j, fill in enumerate(fills):
        l = pos[fill]
        mean = sum(l)/len(l)
        stddev = (sum((x - mean)**2 for x in l)/((len(l)-1)*(len(l)-1)))**0.5 if len(l) > 1 else 0.0
        g.SetPoint(j, j, mean)
        g.SetPointError(j, 0.0, stddev)
    g.SetTitle('#fills: %i;i_{fill};%s (cm)' % (nfills, names[i]))
    g.Draw('AP')
    ps.save(names[i])

