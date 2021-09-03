from DVCode.Tools.MetaSubmitter import *

dataset = 'nr_k0ntuplev25mv1'
samples = pick_samples(dataset, both_years=True, ttbar=False, all_signal=False)
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
