from collections import defaultdict
from DVCode.Tools.LumiLines import *
from DVCode.Tools.ROOTTools import *
set_style()
ps = plot_saver('../../MFVNeutralino/test/plots/beamspot_per_fill', size=(1200,600), log=False)

lls = LumiLines('/uscms/home/tucker/mfvrecipe/lumi.gzpickle')

f = ROOT.TFile('crab/BeamSpotTree_0/MultiJetPk2012.root')
t = f.Get('BeamSpotTree/t')

run_nvtx = defaultdict(int)
run_bsx = defaultdict(list)
run_bsy = defaultdict(list)
run_bsz = defaultdict(list)
run_pvx = defaultdict(list)
run_pvy = defaultdict(list)
run_pvz = defaultdict(list)
fill_nvtx = defaultdict(int)
fill_bsx = defaultdict(list)
fill_bsy = defaultdict(list)
fill_bsz = defaultdict(list)
fill_pvx = defaultdict(list)
fill_pvy = defaultdict(list)
fill_pvz = defaultdict(list)
for jentry in ttree_iterator(t):
    run = t.run
    run_nvtx[run] += 1
    run_bsx[run].append(t.bsx)
    run_bsy[run].append(t.bsy)
    run_bsz[run].append(t.bsz)
    run_pvx[run].append(t.pvx)
    run_pvy[run].append(t.pvy)
    run_pvz[run].append(t.pvz)
    if (len(lls.by_run[t.run]) > 0):
        fill = lls.by_run[t.run][0].fill
        fill_nvtx[fill] += 1
        fill_bsx[fill].append(t.bsx)
        fill_bsy[fill].append(t.bsy)
        fill_bsz[fill].append(t.bsz)
        fill_pvx[fill].append(t.pvx)
        fill_pvy[fill].append(t.pvy)
        fill_pvz[fill].append(t.pvz)

runs = sorted(run_nvtx.keys())
nruns = len(runs)
fills = sorted(fill_nvtx.keys())
nfills = len(fills)

names = ['bsx', 'bsy', 'bsz', 'pvx', 'pvy', 'pvz']
run_dicts = [run_bsx, run_bsy, run_bsz, run_pvx, run_pvy, run_pvz]
fill_dicts = [fill_bsx, fill_bsy, fill_bsz, fill_pvx, fill_pvy, fill_pvz]
for i, name in enumerate(names):
    g_run = ROOT.TGraphErrors(nruns)
    for j, run in enumerate(runs):
        l = run_dicts[i][run]
        mean = sum(l)/len(l)
        stddev = (sum((x - mean)**2 for x in l)/((len(l)-1)*(len(l)-1)))**0.5 if len(l) > 1 else 0.0
        g_run.SetPoint(j, j, mean)
        g_run.SetPointError(j, 0.0, stddev)
    g_run.SetTitle('#runs: %i;i_{run};%s (cm)' % (nruns, name))
    g_run.Draw('AP')
    ps.save('%s_run' % name)

    g_fill = ROOT.TGraphErrors(nfills)
    for j, fill in enumerate(fills):
        l = fill_dicts[i][fill]
        mean = sum(l)/len(l)
        stddev = (sum((x - mean)**2 for x in l)/((len(l)-1)*(len(l)-1)))**0.5 if len(l) > 1 else 0.0
        g_fill.SetPoint(j, j, mean)
        g_fill.SetPointError(j, 0.0, stddev)
    g_fill.SetTitle('#fills: %i;i_{fill};%s (cm)' % (nfills, name))
    g_fill.Draw('AP')
    ps.save('%s_fill' % name)

