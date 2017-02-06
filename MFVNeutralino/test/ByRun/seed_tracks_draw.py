from base import *

ROOT.gStyle.SetOptFit(0)

year, ntracks = 2016, 3

path = 'byrunseedtracks%i%i' % (ntracks, ntracks) if ntracks < 5 else None
plot_path = 'by_run_seed_tracks_%i_%itrk' % (year, ntracks)
title = '%i, %i-track events' % (year, ntracks)
if year == 2015:
    fns = ['/uscms_data/d2/tucker/crab_dirs/ByRunSeedTracks_2015/JetHT2015%s.root' % s for s in 'CD']
    mask_fn = 'fixme'
else:
    fns = ['/uscms_data/d2/tucker/crab_dirs/ByRunSeedTracks_2016partial/JetHT2016%s.root' % s for s in 'B3 C D E F G H2 H3'.split()]
    mask_fn = '/uscms_data/d2/tucker/crab_dirs/ByRunSeedTracks_2016partial/processedLumis.json'

def book():
    def b():
        return {'mean':{},'rms':{}}
    return [b(),b(),b(),b()]

dns = [
    'h_n_vertex_seed_tracks',
    'h_vertex_seed_track_chi2dof',
    'h_vertex_seed_track_pt',
    'h_vertex_seed_track_dxy',
    'h_vertex_seed_track_dz',
    'h_vertex_seed_track_npxhits',
    'h_vertex_seed_track_npxlayers',
    'h_vertex_seed_track_nsthits',
    'h_vertex_seed_track_nstlayers',
    ]
ds = dict((dn, book()) for dn in dns)

for fn in fns:
    f = ROOT.TFile(fn)
    for _, _, objects in tdirectory_walk(f.Get(path)):
        for h in objects:
            hname, nvtx, run = h.GetName().rsplit('_', 2)
            if not ds.has_key(hname):
                continue

            nvtx = int(nvtx)
            assert 0 <= nvtx <= 3
            run = int(run.replace('run', ''))

            ds[hname][nvtx]['mean'][run] = (h.GetMean(), h.GetMeanError())
            ds[hname][nvtx]['rms' ][run] = (h.GetRMS(),  h.GetRMSError())

ps = plot_saver(plot_dir(plot_path), size=(1000,400), log=False, pdf=True)
plotter = ByRunPlotter(ps, mask_fn)

excludes = [
    ('all', []),
    ]

for exclude_name, exclude in excludes:
    print 'excludes:', exclude_name
    for dn in dns:
        d = ds[dn]
        for nvtx in xrange(4):
            for q in ['mean', 'rms']:
                name = '%s_%s_%i_%s' % (exclude_name, dn, nvtx, q)
                plotter.make(d[nvtx][q], name, '', '', year, exclude, verbose=True)
    print '\n'
            
