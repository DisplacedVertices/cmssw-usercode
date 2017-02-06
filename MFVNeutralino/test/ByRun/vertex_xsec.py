from base import *

ROOT.gStyle.SetOptFit(0)

year, ntracks, oneortwo = 2015, 3, 1

plot_path = 'vertex_xsec_%i_%itrk_%iV' % (year, ntracks, oneortwo)
title = '%i, %i-track %i-vtx events' % (year, ntracks, oneortwo)
fns = ['/uscms_data/d2/tucker/crab_dirs/MinitreeV10_sidebanddata2015/JetHT2015D.root'] if year == 2015 else []
mask_fn = '/uscms_data/d2/tucker/crab_dirs/MinitreeV10_sidebanddata2015/condor_JetHT2015D/lumiSummary.json'
tree_path = 'tre%i%i/t' % (ntracks, ntracks) if ntracks < 5 else 'mfvMiniTree/t'

ps = plot_saver(plot_dir(plot_path), size=(1000,400), log=False, pdf=True)

nvtx = defaultdict(int)
for fn in fns:
    f = ROOT.TFile(fn)
    t = f.Get(tree_path)
    for (run,) in detree(t, 'run', 'nvtx==%i' % oneortwo):
        nvtx[run] += 1

excludes = [
    ('all', []),
    ]

plotter = ByRunPlotter(ps, mask_fn)

for exclude_name, exclude in excludes:
    print 'excludes:', exclude_name
    plotter.make(nvtx, exclude_name + '_xsec',           title, '#sigma (pb)',         year, exclude, scale_by_lumi=True, verbose=True)
    plotter.make(nvtx, exclude_name + '_xsec_per_avgpu', title, '#sigma (pb)/avg. PU', year, exclude, scale_by_lumi=True, scale_by_avgpu=True)
    print '\n'
