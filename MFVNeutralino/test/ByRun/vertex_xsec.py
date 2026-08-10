from base import *

ROOT.gStyle.SetOptFit(0)

year = '2017p8'
excludes = [('all', [])]
event_filter_fn = None #'/uscms_data/d2/tucker/eventids_temp/HT900_L1300.bin'
file_path = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV27m/100pc'
plot_path = 'vertex_xsec_v27m_%s' % year

if event_filter_fn:
    plot_path += '_' + os.path.basename(event_filter_fn).replace('.bin', '')

fns = ['%s/JetHT%s.root' % (file_path, year)]
mask_fn = '%s/dataok_%s.json' % (file_path, year)

####

ps = plot_saver(plot_dir(plot_path), size=(1800,600), log=False, pdf=True)
plotter = ByRunPlotter(ps, mask_fn)

event_filter = EventFilter(event_filter_fn) if event_filter_fn else None

for min_dbv in 0, 0.035, 0.05:
    for ntracks, oneortwo in (3,1), (4,1), (3,2), (4,2):
        if oneortwo == 2 and min_dbv:
            continue

        tree_path = 'mfvMiniTreeNtk%i/t' % ntracks if ntracks < 5 else 'mfvMiniTree/t'
        min_dbv_s = 'd_{BV} > %.3f cm ' % min_dbv if min_dbv else ''
        title = '%s, %i-track %i-vtx %sevents' % (year, ntracks, oneortwo, min_dbv_s)
        print title

        nvtx = defaultdict(int)
        for fn in fns:
            f = ROOT.TFile(fn)
            t = f.Get(tree_path)
            cut = 'nvtx==%i' % oneortwo
            if min_dbv:
                cut += ' && dist0 > %f' % min_dbv
            for rle in detree(t, 'run:lumi:event', cut):
                if event_filter is None or rle in event_filter:
                    nvtx[rle[0]] += 1

        for exclude_name, exclude in excludes:
            print 'excludes:', exclude_name
            plotter.make(nvtx,
                         exclude_name + '_%itrk_%iV_mindbv%.3f_xsec' % (ntracks, oneortwo, min_dbv),
                         title,
                         '#sigma (pb)',
                         year,
                         exclude,
                         scale_by_lumi=True,
                         verbose=True,
                         #scale_by_avgpu = True,
                         do_fits=False,
                         #highlight=thirteen.l,
                         )
            print '\n'
