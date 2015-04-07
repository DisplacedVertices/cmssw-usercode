from JMTucker.Tools.Samples import MCSample

samples = [
    MCSample('mfv_hltrun2_3j_M0200', '', '/mfv_hltrun2_3j_M0200/tucker-mfv_hltrun2_3j_M0200-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_3j_M0300', '', '/mfv_hltrun2_3j_M0300/tucker-mfv_hltrun2_3j_M0300-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_3j_M0400', '', '/mfv_hltrun2_3j_M0400/tucker-mfv_hltrun2_3j_M0400-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_3j_M0500', '', '/mfv_hltrun2_3j_M0500/tucker-mfv_hltrun2_3j_M0500-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_3j_M0600', '', '/mfv_hltrun2_3j_M0600/tucker-mfv_hltrun2_3j_M0600-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_3j_M0700', '', '/mfv_hltrun2_3j_M0700/tucker-mfv_hltrun2_3j_M0700-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_3j_M0800', '', '/mfv_hltrun2_3j_M0800/tucker-mfv_hltrun2_3j_M0800-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_3j_M0900', '', '/mfv_hltrun2_3j_M0900/tucker-mfv_hltrun2_3j_M0900-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_3j_M1000', '', '/mfv_hltrun2_3j_M1000/tucker-mfv_hltrun2_3j_M1000-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M0200', '', '/mfv_hltrun2_M0200/tucker-mfv_hltrun2_M0200-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M0300', '', '/mfv_hltrun2_M0300/tucker-mfv_hltrun2_M0300-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M0400', '', '/mfv_hltrun2_M0400/tucker-mfv_hltrun2_M0400-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M0500', '', '/mfv_hltrun2_M0500/tucker-mfv_hltrun2_M0500-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M0600', '', '/mfv_hltrun2_M0600/tucker-mfv_hltrun2_M0600-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M0700', '', '/mfv_hltrun2_M0700/tucker-mfv_hltrun2_M0700-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M0800', '', '/mfv_hltrun2_M0800/tucker-mfv_hltrun2_M0800-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M0900', '', '/mfv_hltrun2_M0900/tucker-mfv_hltrun2_M0900-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    MCSample('mfv_hltrun2_M1000', '', '/mfv_hltrun2_M1000/tucker-mfv_hltrun2_M1000-b0221db6bdc577a56c275739395c3940/USER', 100000, 1, 1, 1),
    ]

for sample in samples:
    exec '%s = sample' % sample.name
    sample.dbs_url_num = 3

    sample.gen_done = True
    sample.gen_dataset = sample.dataset

    sample.sim_done = False
    sample.rawpu40_done = False
    sample.hltpu40_done = False
    sample.recopu40_done = False

mfv_hltrun2_M0400.sim_dataset = '/mfv_hltrun2_M0400/tucker-sim-6f2bea2f4650fd314ffd47e16b4b2771/USER'
mfv_hltrun2_M0400.sim_done = True

mfv_hltrun2_M0400.rawpu40_dataset = '/mfv_hltrun2_M0400/tucker-rawpu40-5a59286feabf00f03677a86d7e0dd538/USER'
mfv_hltrun2_M0400.rawpu40_done = True

mfv_hltrun2_M0400.hltpu40_dataset = '/mfv_hltrun2_M0400/tucker-hltpu40-17e0ae5ebda92df9604093b8c31d7d4c/USER'
mfv_hltrun2_M0400.hltpu40_done = True

mfv_hltrun2_M0400.recopu40_dataset = '/mfv_hltrun2_M0400/tucker-recopu40-49797b714f9dfc7d08ee5c9f0726e700/USER'
mfv_hltrun2_M0400.recopu40_done = True
