from collections import defaultdict
from JMTucker.Tools.LumiLines import *
from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('../../MFVNeutralino/test/plots/beamspot_per_fill', size=(1200,600), log=False)

lls = LumiLines('/uscms/home/tucker/mfvrecipe/lumi.gzpickle')

f = ROOT.TFile('crab/BeamSpotTree/MultiJetPk2012.root')
t = f.Get('BeamSpotTree/t')

nvtx = defaultdict(int)
bsx = defaultdict(float)
bsy = defaultdict(float)
bsz = defaultdict(float)
for jentry in ttree_iterator(t):
    if (len(lls.by_run[t.run]) > 0):
        nvtx[lls.by_run[t.run][0].fill] += 1
        bsx[lls.by_run[t.run][0].fill] = t.bsx
        bsy[lls.by_run[t.run][0].fill] = t.bsy
        bsz[lls.by_run[t.run][0].fill] = t.bsz

fills = sorted(nvtx.keys())
nfills = len(fills)

g_bsx = ROOT.TGraph(nfills)
g_bsy = ROOT.TGraph(nfills)
g_bsz = ROOT.TGraph(nfills)

for i, fill in enumerate(fills):
    g_bsx.SetPoint(i, i, bsx[fill])
    g_bsy.SetPoint(i, i, bsy[fill])
    g_bsz.SetPoint(i, i, bsz[fill])

g_bsx.SetTitle('# fills: %i;i_{fill};beamspot x (cm)' % nfills)
g_bsx.Draw('ALP')
ps.save('bsx')

g_bsy.SetTitle('# fills: %i;i_{fill};beamspot y (cm)' % nfills)
g_bsy.Draw('ALP')
ps.save('bsy')

g_bsx.SetTitle('# fills: %i;i_{fill};beamspot z (cm)' % nfills)
g_bsx.Draw('ALP')
ps.save('bsz')

