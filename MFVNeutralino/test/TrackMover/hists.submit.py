from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

version = 'ulv30lepmv2'
dataset = 'nr_trackmover' + version
#input_files(process, 'movedtree.root')
#samples = [getattr(Samples, 'qcdbctoept080_2017')]
#samples = [getattr(Samples, 'example_ttbar_2017')]
samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=False, met=False, diboson=False, Lepton_data=True)
#samples = pick_samples(dataset, both_years=True, all_signal=False)

for nl in 2,: # 3:
    for nb in 0,: # 1, 2:
        for tau in 100, 300, 1000, 10000, 30000, 100000,:
            batch = 'TrackMoverHists' + version.capitalize() + '_%i%i_tau%06ium' % (nl, nb, tau)
            args = '-t mfvMovedTree%i%i --tau %i' % (nl, nb, tau)
            NtupleReader_submit(batch, dataset, samples, exe_args=args)
