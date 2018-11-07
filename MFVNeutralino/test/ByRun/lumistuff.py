from base import *

year = '2017p8'
mask_fn = json_path('ana_avail_%s.json' % year)

ps = plot_saver(plot_dir('byrun_lumistuff_%s' % year), size=(1800,600), log=False, pdf=True)
plotter = ByRunPlotter(ps, mask_fn)

modes= [
    ('nls',     '# LS'),
    ('avgpu',   'average PU'),
    ('avginst', 'average inst. luminosity (10^{34} cm^{-2} sec^{-1})'),
    ('maxinst', 'max inst. luminosity (10^{34} cm^{-2} sec^{-1})'),
    ]

for mode, nice in modes:
    d = defaultdict(float)

    for r in plotter.lls.runs(year):
        if mode == 'avgpu':
            d[r] = plotter.lls.avg_pu(r)
        elif mode == 'avginst':
            d[r] = plotter.lls.avg_inst(r) / 1e4
        elif mode == 'maxinst':
            d[r] = plotter.lls.max_inst(r) / 1e4
        elif mode == 'nls':
            d[r] = (len(plotter.lls.by_run[r]), 0)

    plotter.make(d, mode, str(year), nice, year, [], scale_by_lumi=False, verbose=True, do_fits=False)
