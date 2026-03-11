import JMTucker.MFVNeutralino.AnalysisConstants as ac


template_norms = {
    "n1v": {
        "lep": [52.19, 77.35, 442.23, 694.77],
        "bjet": [1004.1395, 434.13558, 187.79967, 276.98182],
    },
    "n2v": {
        "lep": [0.001, 0.012, 0.002, 0.034], # The 0.001 is fake
        "bjet": [0.258, 0.062, 0.078, 0.122],
    },
    "lumi": {
        "lep": [
            ac.scaled_int_lumi_20161,
            ac.scaled_int_lumi_20162,
            ac.scaled_int_lumi_2017,
            ac.scaled_int_lumi_2018],
        "bjet": [
            ac.scaled_int_lumi_20161,
            ac.scaled_int_lumi_20162,
            ac.scaled_int_lumi_2017,
            ac.scaled_int_lumi_2018],
    },
    "old_lumis": [19664., 16978., 40610., 59683.], # Derived from AnalysisConstants.h. I feel like if these != new lumis, we need corrections.
}

lumi_uncs = {
    "20161": 0.02,
    "20162": 0.02,
    "2017": 0.0082,
    "2018": 0.0084,
}


"""
sig_xsecs = {
    "index_start": { # In Samples.py, some xsecs depend on the process name start
        "WplusH": 3*(9.426e-02)*0.01,
        "WminusH": 3*(5.983e-02)*0.01,
        "ZH" : 3*(2.982e-02)*0.01,
    },
    "others": 1e-3,
}
"""


"""
sig_filtereffs = {
    "index_start": { # In Samples.py, some xsecs depend on the process name start
        "ggH": 0.10,
    },
    "others": 1.0,
}
"""


""" Instructions: if make_updn==True, add a list for what expression "weight" should be replaced with. Give in the order: up, down. """
updn_wt_dict = {
    "fake_fact_CMS_eff_lep": ["weight*fac_weight_up", "weight*fac_weight_dn"],
    "fake_fact_CMS_pileup_13TeV": ["weight*fac_weight_up", "weight*fac_weight_dn"],

}


