from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

dataset = 'k0ntuplev25mv1'
#input_files(process, './k0tree.root')
#samples = pick_samples(dataset, ttbar=True, all_signal=False)
samples = [getattr(Samples, 'ttbar_2017')]
NtupleReader_submit('K0HistsV25mv1_nsigdxy0p0_rhomin0p268_ctaumin0p0268_costh2min0p99975', dataset, samples,
                    split = {'qcdht1000_2017': 2,
                             'qcdht1000_2018': 2,
                             'qcdht1500_2017': 5,
                             'qcdht1500_2018': 5,
                             'qcdht2000_2017': 3,
                             'qcdht2000_2018': 3,
                             'JetHT2017C': 2,
                             'JetHT2017E': 2,
                             'JetHT2017F': 3,
                             'JetHT2018A': 4,
                             'JetHT2018B': 2,
                             'JetHT2018C': 2,
                             'JetHT2018D': 5
                             })
