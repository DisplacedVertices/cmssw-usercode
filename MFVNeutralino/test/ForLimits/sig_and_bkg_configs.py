import JMTucker.MFVNeutralino.AnalysisConstants as ac


template_norms = {
    "n1v": {
        "lep": [52.19, 77.35, 442.23, 694.77],
        "bjet": [1004.1395, 434.13558, 187.79967, 276.98182],
    },
    "n2v": {
        "lep": [0.001, 0.012, 0.002, 0.034],  # 0.001 (20161) is a placeholder -- update when lepton bkg estimate for 20161 is available
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


# n2v_uncs disabled until real uncertainties measured after unblinding.
# To re-enable: fill values below, uncomment, add "n2v_unc" to nuis_bkg.
#
# n2v_uncs = {
#     "lep":  [0.0001, 0.0001, 0.0001, 0.0001],
#     "bjet": [0.0001, 0.0001, 0.0001, 0.0001],
# }
n2v_uncs = None  # sentinel; code must not use this until real values are filled


# CMS Run 2 luminosity uncertainty decomposition (CMS-LUM-17-003/4, CMS-LUM-18-002).
# Totals: 2016 1.2%, 2017 2.3%, 2018 2.5%.
lumi_lit_corrs = {
    "lumi_13TeV_correlated": {"2016": 1.006,  "2017": 1.009,  "2018": 1.020 },
    "lumi_13TeV_1718":       {"2016": None,   "2017": 1.006,  "2018": 1.002 },
    "lumi_2016":             {"2016": 1.010,  "2017": None,   "2018": None  },
    "lumi_2017":             {"2016": None,   "2017": 1.020,  "2018": None  },
    "lumi_2018":             {"2016": None,   "2017": None,   "2018": 1.015 },
}


updn_wt_dict = {
    "fake_fact_CMS_eff_lep": ["weight*fac_weight_up", "weight*fac_weight_dn"],
    "fake_fact_CMS_pileup": ["weight*fac_weight_up", "weight*fac_weight_dn"],
}


printout_flags = { # Convention: True for printing statements, False for silence
    "PyStorage": {
        "sig_type_conflict": False,
    },
}


