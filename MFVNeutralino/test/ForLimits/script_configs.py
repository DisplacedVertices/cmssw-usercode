datacard = {
    "year": "2018",
    "year_key": ["20161", "20162", "2017", "2018"], # Any 4-element list is in this order
    "year_to_tag": {"20161": "2016preAPV", "20162": "2016postAPV", "2017": "2017", "2018": "2018"}, # Used when sig is called sig2017, or nuisance naming
    "bins": [0., 0.08, 0.16, 4.],
    "nbins": 3,
}


sig = {
    "type": "bjet", # This MUST be either "lep" or "bjet"

    "lep": {
        "folder": "/uscms/home/yuqingwu/nobackup/DV-testing/25-12_CombineTemplates/MiniTree_Ex/26-04-16_MiniTree_tag001Lepm/",
        "file_key": "*tau*",
    },
    "bjet": {
        "folder": "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm/",
        "file_key": "*tau*"+".root", #"mfv_stopdbardbar_tau000300um*",
    },
    
    "lep_sigs": ["WminusHToSSTodddd", "WplusHToSSTodddd", "ZHToSSTodddd", "ggZHToSSTobbbb", "ggZHToSSTodddd", "ttHToLLPs_bbbb", "ttHToLLPs_dddd", "mfv_neu"],
    "bjet_sigs": ["ggHToSSTodddd", "mfv_neu", "mfv_stopbbarbbar", "mfv_stopdbardbar", "ttHToLLPs_bbbb", "ttHToLLPs_dddd"],

    "sig_grps": { # If it hits e.g. "ZHToSSTodddd", it'll sum 3 files. It ignores the other 2.
        "VH": ["ZHToSSTodddd", "WminusHToSSTodddd", "WplusHToSSTodddd"],
    },
    "aliases": { # Designed for nuisances. E.g. "VH" is an acceptable replacement for WH and ZH
        "bjet": {
            "ttHToLLPs_bbbb": {"ggHToSSTodddd"},
            "ttHToLLPs_dddd": {"ggHToSSTodddd"},
        },
        "lep": {
            "ttHToLLPs_bbbb": {"VH"},
            "ttHToLLPs_dddd": {"VH"},
            "ggZHToSSTobbbb": {"VH"},
            "ggZHToSSTodddd": {"VH"},
            "WminusHToSSTodddd": {"VH"},
            "WplusHToSSTodddd": {"VH"},
            "ZHToSSTodddd": {"VH"},
        },
    },
}

bkg = {
    "lep": {
        "folder": "/uscms/home/yuqingwu/nobackup/DV-testing/25-12_CombineTemplates/Bkg_Example/26-03-11_Alec_Leptonic/",
        "fn": "2v_from_jets_{}_5track_default_ULV30Lepm.root", # Alec leptonic
    },
    "bjet": {
        "folder": "/uscms/home/yuqingwu/nobackup/DV-testing/25-12_CombineTemplates/Bkg_Example/25-12-18_Peace_LxPlus/",
        "fn": "2v_from_jets_{}_5track_default_ULV30BvetoLHTm.root",
    },
}

output = {
    "lep": {
        "out_folder": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/TESTING-OUT/lep_TEMP/",
    },
    "bjet": {
        "out_folder": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/TESTING-OUT/bjet_TEMP/",
    },
    "out_fn": "limitsinput", # code will append trigger, year, and .ROOT
}


datacard_out_loc = {
    "lep": {
        "out_folder": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/TESTING-OUT/lep_TEMP/",
    },
    "bjet": {
        "out_folder": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/TESTING-OUT/bjet_TEMP/",
    },
    "out_fn_prefix": "Datacard_", # code will append bjet/lep, process name
    "out_fn_suffix": ".txt",
}


obs = {
    "20161": [0,0,0],
    "20162": [0,0,0],
    "2017": [0,0,0],
    "2018": [0,0,0],
}


debug_settings = {
    "scale_sig_fake": True,
    "sig_fake_sf": { # write None for no correction. Leave as string, no underscores, no extra *.
        "lep": {
            "default": None,
            "overrides": {
                "VH": "1e-3",
            },
        },
        "bjet": {
            "default": None,
            "overrides": {
                "ggHToSSTodddd": "1e-3",
            },
        },
    },
    
    "scale_bkg_fake": False, # Set to False to not add fake scale factors
    "bkg_fake_sf": 100,
}



