from base import *

ROOT.gStyle.SetOptFit(0)

year = 2016
excludes = [('all', [])]
event_filter_fn = None #'/uscms_data/d2/tucker/eventids_temp/HT900_L1300.bin'
file_path = '/uscms_data/d2/tucker/crab_dirs/!done/MiniTreeV14_forpick'
plot_path = 'vertex_xsec_v14_%i' % year

if event_filter_fn:
    plot_path += '_' + os.path.basename(event_filter_fn).replace('.bin', '')

if year == 2015:
    fns = ['%s/JetHT2015%s.root' % (file_path, s) for s in 'CD']
    mask_fn = '%s/dataok_2015.json' % file_path
else:
    fns = ['%s/JetHT2016%s.root' % (file_path, s) for s in 'B3 C D E F G H2 H3'.split()]
    mask_fn = '%s/dataok_2016.json' % file_path

####

ps = plot_saver(plot_dir(plot_path), size=(2000,600), log=False, pdf=True)
plotter = ByRunPlotter(ps, mask_fn)

event_filter = EventFilter(event_filter_fn) if event_filter_fn else None

for ntracks, oneortwo in (3, 1), (4, 1), (3, 2), (4, 2):
    tree_path = 'mfvMiniTreeNtk%i/t' % ntracks if ntracks < 5 else 'mfvMiniTree/t'
    title = '%i, %i-track %i-vtx events' % (year, ntracks, oneortwo)
    print title

    nvtx = defaultdict(int)
    for fn in fns:
        f = ROOT.TFile(fn)
        t = f.Get(tree_path)
        for rle in detree(t, 'run:lumi:event', 'nvtx==%i' % oneortwo):
            if event_filter is None or rle in event_filter:
                nvtx[rle[0]] += 1

    for exclude_name, exclude in excludes:
        print 'excludes:', exclude_name
        plotter.make(nvtx, exclude_name + '_%itrk_%iV_xsec' % (ntracks, oneortwo), title, '#sigma (pb)', year, exclude, scale_by_lumi=True, verbose=True) #, scale_by_avgpu = True)
        print '\n'
