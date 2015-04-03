from JMTucker.Tools.Samples import MCSample

samples = [
    MCSample('mfv_hltrun2_M0900', '', '/mfv_hltrun2_M0900/tucker-mfv_hltrun2_M0900-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    ]

for sample in samples:
    sample.dbs_url_num = 3
