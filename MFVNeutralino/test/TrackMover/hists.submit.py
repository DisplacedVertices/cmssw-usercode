from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

version = 'ulv30lepelemv6'
dataset = 'trackmover' + version
samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=True)
#samples = [getattr(Samples, 'example_ttbar_2017')]
#samples = [getattr(Samples, 'qcdmupt15_2017')]
#samples = [getattr(Samples, 'wjetstolnu_2017')]
for nl in 2,: # 3:
    for nb in 0,: # 1, 2:
      for tau in 10000, : # 100, 300, 1000, 10000, 30000, 100000,
            batch = 'TrackMoverHists' + version.capitalize() + '_%i%i_tau%06ium' % (nl, nb, tau)
            args = '-t mfvMovedTree%i%i --tau %i' % (nl, nb, tau) #FIXME
            NtupleReader_submit(batch, dataset, samples, exe_args=args)
