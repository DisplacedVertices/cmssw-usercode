from base import *

ROOT.gStyle.SetOptFit(0)

year, ntracks, oneortwo = 2016, 3, 1

event_filter_fn = None #'/uscms_data/d2/tucker/eventids_temp/HT900_L1300.bin'
tree_path = 'tre%i%i/t' % (ntracks, ntracks) if ntracks < 5 else 'mfvMiniTree/t'
plot_path = 'vertex_xsec_%i_%itrk_%iV' % (year, ntracks, oneortwo)
if event_filter_fn:
    plot_path += '_' + os.path.basename(event_filter_fn).replace('.bin', '')
title = '%i, %i-track %i-vtx events' % (year, ntracks, oneortwo)
if year == 2015:
    fns = ['/uscms_data/d2/tucker/crab_dirs/MinitreeV12/JetHT2015%s.root' % s for s in 'CD']
    mask_fn = '/uscms_data/d2/tucker/crab_dirs/MinitreeV12/dataok_2015.json'
else:
    fns = ['/uscms_data/d2/tucker/crab_dirs/MinitreeV12/JetHT2016%s.root' % s for s in 'B3 C D E F H2 H3'.split()]
    mask_fn = '/uscms_data/d2/tucker/crab_dirs/MinitreeV12/dataok_2016_noG.json'

####

ps = plot_saver(plot_dir(plot_path), size=(2000,600), log=False, pdf=True)

event_filter = EventFilter(event_filter_fn) if event_filter_fn else None

nvtx = defaultdict(int)
for fn in fns:
    f = ROOT.TFile(fn)
    t = f.Get(tree_path)
    for rle in detree(t, 'run:lumi:event', 'nvtx==%i' % oneortwo):
        if event_filter is None or rle in event_filter:
            nvtx[rle[0]] += 1

excludes = [
    ('all', []),
    ]

plotter = ByRunPlotter(ps, mask_fn)

for exclude_name, exclude in excludes:
    print 'excludes:', exclude_name
    plotter.make(nvtx, exclude_name + '_xsec',           title, '#sigma (pb)',         year, exclude, scale_by_lumi=True, verbose=True)
    plotter.make(nvtx, exclude_name + '_xsec_per_avgpu', title, '#sigma (pb)/avg. PU', year, exclude, scale_by_lumi=True, scale_by_avgpu=True)
    print '\n'
