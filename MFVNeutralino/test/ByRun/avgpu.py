from base import *

ps = plot_saver(plot_dir('avgpu'), size=(2000,600), log=False, pdf=True)
mask_fn = '/uscms_data/d2/tucker/crab_dirs/MinitreeV10_2016_data_partial_notrigbit/processedLumis.json'

plotter = ByRunPlotter(ps, mask_fn)
avgpu = defaultdict(float)
for r in plotter.lls.runs(2016):
    avgpu[r] = plotter.lls.avg_pu(r)

plotter.make(avgpu, 'avgpu',      '2016', 'avg pu', 2016, [], scale_by_lumi=False, verbose=True)
plotter.make(avgpu, 'avgpu_xsec', '2016', 'avg pu #sigma (pb)', 2016, [], scale_by_lumi=True, verbose=False)
