datacard = {
    "year": "2018",
    "year_key": ["20161", "20162", "2017", "2018"], # Any 4-element list is in this order
    "year_to_tag": {"20161": "2016preAPV", "20162": "2016postAPV", "2017": "2017", "2018": "2018"}, # Used when sig is called sig2017, or nuisance naming
    "bins": [0., 0.08, 0.16, 4.],
    "nbins": 3,
}


sig = {
    "type": "lep", # This MUST be either "lep" or "bjet"
    "folder": "/uscms/home/yuqingwu/nobackup/DV-testing/25-12_CombineTemplates/MiniTree_Ex/26-03-07_MiniTree_Table28Validation_CorrectedLepm/",
    "file_key": "*tau*", #"mfv_stopdbardbar_tau000300um*",
    
    "lep_sigs": ["WminusHToSSTodddd", "WplusHToSSTodddd", "ZHToSSTodddd", "mfv_neu"],
    # Leptonic things that aren't processed due to no TM: "ttHToLLPs_bbbb", "ttHToLLPs_dddd"
    "bjet_sigs": ["ggHToSSTodddd", "mfv_neu", "mfv_stopdbardbar", "mfv_stopbbarbbar"],

    "aliases": { # E.g. "VH" is an acceptable replacement for WH and ZH
        "WminusHToSSTodddd": {"VH"},
        "WplusHToSSTodddd": {"VH"},
        "ZHToSSTodddd": {"VH"},
    },
}

bkg = {
    "folder": "/uscms/home/yuqingwu/nobackup/DV-testing/25-12_CombineTemplates/Bkg_Example/26-03-11_Alec_Leptonic/",
    "fn": "2v_from_jets_{}_5track_default_ULV30Lepm.root", # Alec leptonic
}

output = {
    "out_folder": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/TESTING-OUT/lep_NEWEST/",
    "out_fn": "limitsinput", # code will append trigger, year, and .ROOT
}


datacard_out_loc = {
    "out_folder": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/TESTING-OUT/lep_NEWEST/",
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
    "scale_bkg_fake": False, # Set to False to not add fake scale factors
    "bkg_fake_sf": 100,
}



