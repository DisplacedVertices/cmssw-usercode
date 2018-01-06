from base import *

mode, nice = 'avgpu', 'average PU'
mode, nice = 'avginst', 'average inst. luminosity (10^{34} cm^{-2} sec^{-1})'
mode, nice = 'maxinst', 'max inst. luminosity (10^{34} cm^{-2} sec^{-1})'
mode, nice = 'nls', '# LS'

year = 2016
mask_fn = '../jsons/ana_avail_%s.json' % year

ps = plot_saver(plot_dir('%s_%s' % (mode, year)), size=(2000,600), log=False, pdf=True)

plotter = ByRunPlotter(ps, mask_fn)
d = defaultdict(float)
for r in plotter.lls.runs(year):
    if mode == 'avgpu':
        d[r] = plotter.lls.avg_pu(r)
    elif mode == 'avginst':
        d[r] = plotter.lls.avg_inst(r) / 1e4
    elif mode == 'maxinst':
        d[r] = plotter.lls.max_inst(r) / 1e4
    elif mode == 'nls':
        d[r] = len(plotter.lls.by_run[r])

plotter.make(d, mode, str(year), nice, year, [], scale_by_lumi=False, verbose=True, do_fits=False)
