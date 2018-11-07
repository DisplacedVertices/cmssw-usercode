from JMTucker.Tools.BasicAnalyzer_cfg import *

pc = 100 # 10 1

dataset = 'ntuplev21m'
sample_files(process, 'JetHT2017B', dataset, 1)
remove_tfileservice(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.data_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018

    batch_name = 'DummyV1'
    json = 'ana_2017p8.json'
    if pc in (1, 10):
        pc_s = '_%ipc' % pc
        json = json.replace('.json', pc_s + '.json')
        batch_name += pc_s

    set_splitting(samples, dataset, 'default', data_json=json_path(json))

    cs = CondorSubmitter(batch_name, ex = year, dataset = dataset)
    cs.submit_all(samples)
