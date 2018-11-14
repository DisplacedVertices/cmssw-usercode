from base import *

ROOT.gStyle.SetOptFit(0)

year, ntracks = 2018, 3
do_ana_related = False

path = 'byrun%i%i' % (ntracks, ntracks) if ntracks < 5 else None
if do_ana_related:
    path += 'noana' # i.e. remove the njets/HT cuts
path = 'byrunInclusiveNoAna'
plot_path = 'by_run_stuff_%s_%itrk' % (year, ntracks)
title = '%s, %i-track events' % (year, ntracks)
fn_path = '/uscms_data/d2/tucker/crab_dirs/ByRunStuffV21m'
fn = os.path.join(fn_path, 'JetHT%s.root' % year)
mask_fn = os.path.join(fn_path, 'dataok_%s.json' % year)

def book():
    def b():
        return dict((s,{}) for s in 'mean rms q50 iqr q10 q90'.split())
    return [b(),b()]

if do_ana_related:
    dns = [
        'h_njets',
        'h_jetpt1',
        'h_jetpt4',
        'h_ht40',
        'h_ht',
        'h_trig',
        'h_ana',
        ]
    dns_1v_only = []
else:
    dns = [
        'h_n_vertex_seed_tracks',
        'h_vertex_seed_track_chi2dof',
        'h_vertex_seed_track_pt',
        'h_vertex_seed_track_dxy',
        'h_vertex_seed_track_dz',
        'h_vertex_seed_track_adxy',
        'h_vertex_seed_track_adz',
        'h_vertex_seed_track_npxhits',
        'h_vertex_seed_track_npxlayers',
        'h_vertex_seed_track_nsthits',
        'h_vertex_seed_track_nstlayers',
        ]
    dns_1v_only = [
        'h_vertex_x',
        'h_vertex_y',
        'h_vertex_dbv',
        'h_vertex_bs2derr',
        ]
    dns += dns_1v_only

ds = dict((dn, book()) for dn in dns)

f = ROOT.TFile(fn)
for _, _, objects in tdirectory_walk(f.Get(path)):
    for h in objects:
        hname, nvtx, run = h.GetName().rsplit('_', 2)
        if not ds.has_key(hname):
            continue
        nvtx = int(nvtx)
        assert 0 <= nvtx <= 1
        run = int(run.replace('run', ''))

        q10, q25, q50, q75, q90 = get_hist_quantiles(h, [0.1, 0.25, 0.5, 0.75, 0.9], 'error')

        if do_ana_related:
            if hname.startswith('h_trig'):
                ds[hname][nvtx]['mean'][run] = int(h.GetEntries())
            else:
                ds[hname][nvtx]['mean'][run] = (h.GetMean(), h.GetMeanError())
        else:
            ds[hname][nvtx]['mean'][run] = (h.GetMean(), h.GetMeanError())
            ds[hname][nvtx]['rms' ][run] = (h.GetRMS(),  h.GetRMSError())
            ds[hname][nvtx]['q50' ][run] = q50
            ds[hname][nvtx]['iqr' ][run] = (q75[0] - q25[0], q75[1])
            ds[hname][nvtx]['q10' ][run] = q10
            ds[hname][nvtx]['q90' ][run] = q90

ps = plot_saver(plot_dir(plot_path), size=(1800,600), log=False, pdf=True)
plotter = ByRunPlotter(ps, mask_fn)

excludes = [
    ('all', []),
    ]

for exclude_name, exclude in excludes:
    for dn in dns:
        d = ds[dn]
        for nvtx in 0,1:
            if nvtx == 0 and dn in dns_1v_only:
                continue
            qs = ['mean'] if do_ana_related else ['mean', 'rms', 'q50', 'iqr', 'q10', 'q90']
            for q in qs:
                print path, exclude_name, dn, nvtx, q
                name = '%s_%s_%i_%s' % (exclude_name, dn, nvtx, q)
                plotter.make(d[nvtx][q], name, '', '', year, exclude, verbose=True, scale_by_lumi=dn.startswith('h_trig'))
    print '\n'
            
