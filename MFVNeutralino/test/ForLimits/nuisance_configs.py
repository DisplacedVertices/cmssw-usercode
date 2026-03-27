"""
A place to store the messy dictionaries required to make nuisance_configs_and_functions.py work.

nuis_names: nuisance naming

pickle_prefixes: where to find nuisance table storage
year_remaps: some filenames are provided with a different convention to our 20161-2018 conventions
"""

nuis_names = {
    "CMS-CADI-tag" : "CMS_EXO24035_",
    "Run2-key": "13TeV",
}

pickle_prefixes = {
    "vtx_reco_TM" : "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/NuisTabStore_TrkMvr/pickle",
    "disp_trig_uncerts": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/NuisTabStore_7p4p1/pickle",
}

pickle_triple_prefixes = { # Actually I don't use central anymore, so pair not triple
    "tk_reco_eff": {
        "base": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/NuisTabStore_TrkRec/",
        #"central": "ct_pickle",
        "up": "up_pickle",
        "dn": "dn_pickle",
    },
}

year_remaps = {
    "vtx_reco_TM" : {"20161": "20161-2", "20162": "20161-2", "2017": "2017-8", "2018": "2017-8"},
    "disp_trig_uncerts": {"20161": "2016", "20162": "2016APV", "2017": "2017", "2018": "2018"},
}

