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


# n2v_uncs: excluded from datacards until real uncertainties are measured.
# Replace the placeholder values below and uncomment to re-enable;
# also add "n2v_unc" back to nuis_bkg in getNuisanceFromSig.py.
#
# n2v_uncs = {
#     "lep":  [0.0001, 0.0001, 0.0001, 0.0001],
#     "bjet": [0.0001, 0.0001, 0.0001, 0.0001],
# }
n2v_uncs = None  # sentinel; code must not use this until real values are filled


lumi_lit_corrs = {
    "lumi_13TeV_1516_l": {"2016": 1.0118, "2017": None, "2018": None},
    "lumi_13TeV_151617_l": {"2016": 1.0004, "2017": 1.0055, "2018": None},
    "lumi_13TeV_15161718_l": {"2016": 1.0035, "2017": 1.0061, "2018": 1.0084},
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


