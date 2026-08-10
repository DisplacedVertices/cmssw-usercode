from base import *

ROOT.gStyle.SetOptFit(0)

year = '2017p8'
path = 'mfvByRunJetPreSel'
plot_path = 'ByRunPreSelV27m_%s' % year
title = '%s, presel events' % year
fn_path = '/uscms_data/d2/tucker/crab_dirs/PreselHistosV27m'
fn = os.path.join(fn_path, 'JetHT%s.root' % year)
mask_fn = os.path.join(fn_path, 'dataok_%s.json' % year)

def book():
    return dict((s,{}) for s in 'mean rms q50 iqr q10 q90'.split())

dns = [
    'h_trig',
    'h_njets',
    'h_jetpt0',
    'h_jetpt1',
    'h_jetpt2',
    'h_jetpt3',
    'h_jetpt4',
    'h_jetpt5',
    'h_ht40',
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

ds = dict((dn, book()) for dn in dns)

f = ROOT.TFile(fn)
for _, _, objects in tdirectory_walk(f.Get(path)):
    for h in objects:
        hname, nvtx, run = h.GetName().rsplit('_', 2)
        if not ds.has_key(hname):
            continue
        assert nvtx == '0'
        run = int(run.replace('run', ''))

        q10, q25, q50, q75, q90 = get_hist_quantiles(h, [0.1, 0.25, 0.5, 0.75, 0.9], 'error')

        ds[hname]['mean'][run] = int(h.GetEntries()) if hname.startswith('h_trig') else (h.GetMean(), h.GetMeanError())
        ds[hname]['rms' ][run] = (h.GetRMS(),  h.GetRMSError())
        ds[hname]['q50' ][run] = q50
        ds[hname]['iqr' ][run] = (q75[0] - q25[0], q75[1])
        ds[hname]['q10' ][run] = q10
        ds[hname]['q90' ][run] = q90

ps = plot_saver(plot_dir(plot_path), size=(1800,600), log=False, pdf=True)
plotter = ByRunPlotter(ps, mask_fn)

excludes = [
    ('all', []),
    ]

for exclude_name, exclude in excludes:
    for dn in dns:
        d = ds[dn]
        qs = ['mean', 'rms', 'q50', 'iqr', 'q10', 'q90']
        for q in qs:
            print path, exclude_name, dn, nvtx, q
            name = '%s_%s_%s' % (exclude_name, dn, q)
            plotter.make(d[q], name, '', '', year, exclude, verbose=True, scale_by_lumi=dn.startswith('h_trig'))
    print '\n'
            
