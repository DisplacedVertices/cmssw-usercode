from JMTucker.Tools.MetaSubmitter import *

version = 'v27mv1'
dataset = 'nr_trackmover' + version
samples = pick_samples(dataset, both_years=True, all_signal=False)

for nl in 2,: # 3:
    for nb in 0,: # 1, 2:
        for tau in 100, 300, 1000, 10000, 30000, 100000,:
            batch = 'TrackMoverHists' + version.capitalize() + '_%i%i_tau%06ium' % (nl, nb, tau)
            args = '-t mfvMovedTree%i%i --tau %i' % (nl, nb, tau)
            NtupleReader_submit(batch, dataset, samples, exe_args=args)
