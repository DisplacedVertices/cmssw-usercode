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

g_bsx = ROOT.TGraphErrors(nfills)
for i, fill in enumerate(fills):
    l = bsx[fill]
    mean = sum(l)/len(l)
    stddev = (sum((x - mean)**2 for x in l)/((len(l)-1)*(len(l)-1)))**0.5 if len(l) > 1 else 0.0
    g_bsx.SetPoint(i, i, mean)
    g_bsx.SetPointError(i, 0.0, stddev)
g_bsx.SetTitle('# fills: %i;i_{fill};beamspot x (cm)' % nfills)
g_bsx.Draw('AP')
ps.save('bsx')

g_bsy = ROOT.TGraphErrors(nfills)
for i, fill in enumerate(fills):
    l = bsy[fill]
    mean = sum(l)/len(l)
    stddev = (sum((x - mean)**2 for x in l)/(((len(l)-1)*len(l)-1)))**0.5 if len(l) > 1 else 0.0
    g_bsy.SetPoint(i, i, mean)
    g_bsy.SetPointError(i, 0.0, stddev)
g_bsy.SetTitle('# fills: %i;i_{fill};beamspot y (cm)' % nfills)
g_bsy.Draw('AP')
ps.save('bsy')

g_bsz = ROOT.TGraphErrors(nfills)
for i, fill in enumerate(fills):
    l = bsz[fill]
    mean = sum(l)/len(l)
    stddev = (sum((x - mean)**2 for x in l)/((len(l)-1)*(len(l)-1)))**0.5 if len(l) > 1 else 0.0
    g_bsz.SetPoint(i, i, mean)
    g_bsz.SetPointError(i, 0.0, stddev)
g_bsz.SetTitle('# fills: %i;i_{fill};beamspot z (cm)' % nfills)
g_bsz.Draw('AP')
ps.save('bsz')

g_pvx = ROOT.TGraphErrors(nfills)
for i, fill in enumerate(fills):
    l = pvx[fill]
    mean = sum(l)/len(l)
    stddev = (sum((x - mean)**2 for x in l)/((len(l)-1)*(len(l)-1)))**0.5 if len(l) > 1 else 0.0
    g_pvx.SetPoint(i, i, mean)
    g_pvx.SetPointError(i, 0.0, stddev)
g_pvx.SetTitle('# fills: %i;i_{fill};primary vertex x (cm)' % nfills)
g_pvx.Draw('AP')
ps.save('pvx')

g_pvy = ROOT.TGraphErrors(nfills)
for i, fill in enumerate(fills):
    l = pvy[fill]
    mean = sum(l)/len(l)
    stddev = (sum((x - mean)**2 for x in l)/((len(l)-1)*(len(l)-1)))**0.5 if len(l) > 1 else 0.0
    g_pvy.SetPoint(i, i, mean)
    g_pvy.SetPointError(i, 0.0, stddev)
g_pvy.SetTitle('# fills: %i;i_{fill};primary vertex y (cm)' % nfills)
g_pvy.Draw('AP')
ps.save('pvy')

g_pvz = ROOT.TGraphErrors(nfills)
for i, fill in enumerate(fills):
    l = pvz[fill]
    mean = sum(l)/len(l)
    stddev = (sum((x - mean)**2 for x in l)/((len(l)-1)*(len(l)-1)))**0.5 if len(l) > 1 else 0.0
    g_pvz.SetPoint(i, i, mean)
    g_pvz.SetPointError(i, 0.0, stddev)
g_pvz.SetTitle('# fills: %i;i_{fill};primary vertex z (cm)' % nfills)
g_pvz.Draw('AP')
ps.save('pvz')

