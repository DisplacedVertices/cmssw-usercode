from base import *

ROOT.gStyle.SetOptFit(0)

year, eras = 2017, 'BCDEF'
year, eras = 2018, ('A1','A2','A3','B1','B2','C1','C2','C3','D2')
excludes = [('all', [])]
event_filter_fn = None #'/uscms_data/d2/tucker/eventids_temp/HT900_L1300.bin'
file_path = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV21m'
plot_path = 'vertex_xsec_v21m_%i' % year

if event_filter_fn:
    plot_path += '_' + os.path.basename(event_filter_fn).replace('.bin', '')

fns = ['%s/JetHT%s%s.root' % (file_path, year, era) for era in eras]
mask_fn = '%s/dataok_%s.json' % (file_path, year)

####

ps = plot_saver(plot_dir(plot_path), size=(1800,600), log=False, pdf=True)
plotter = ByRunPlotter(ps, mask_fn)

event_filter = EventFilter(event_filter_fn) if event_filter_fn else None

for ntracks, oneortwo in (3,1),: #, (4,1), (3,2), (4,2):
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
