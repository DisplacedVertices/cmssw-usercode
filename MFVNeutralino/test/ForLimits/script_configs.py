datacard = {
    "year": "2017",
    "year_key": ["20161", "20162", "2017", "2018"], # Any 4-element list is in this order
    "bins": [0., 0.08, 0.16, 4.],
    "nbins": 3,
}


sig = {
    "type": "bjet", # This MUST be either "lep" or "bjet"
    "folder": "/uscms/home/yuqingwu/nobackup/DV-testing/25-12_CombineTemplates/MiniTree_Ex/25-12-29_MiniTree_LepIPCut_FixHT2016_OnnormdzULV30BvetoLHTm/",
    "file_key": "*tau*", #"mfv_stopdbardbar_tau000300um*",
    
    "lep_sigs": [], #FIXME
    "bjet_sigs": ["ggHToSSTodddd", "mfv_neu", "mfv_stopdbardbar", "mfv_stopbbarbbar"],
}

bkg = {
    "folder": "/uscms/home/yuqingwu/nobackup/DV-testing/25-12_CombineTemplates/Bkg_Example/",
    "fn": "2v_from_jets_{}_5track_default_ULV30BvetoLHTm.root",
}

output = {
    "out_folder": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/TESTING-OUT/",
    "out_fn": "limitsinputTEMP", # code will append trigger, year, and .ROOT
}


datacard_out_loc = {
    "out_folder": "/uscms/home/yuqingwu/work/mfv_10647/src/JMTucker/MFVNeutralino/test/ForLimits/TESTING-OUT/",
    "out_fn_prefix": "Datacard_", # code will append process name
    "out_fn_suffix": ".txt",
}


obs = {
    "20161": [0,0,0],
    "20162": [0,0,0],
    "2017": [0,0,0],
    "2018": [0,0,0],
}


