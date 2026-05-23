"""Central definition of all binning schemes and study signal points."""

SCHEMES = {
    "old_binning": {"bins": [0., 0.08, 0.16, 4.0],    "nbins": 3,
                    "label": "3-bin old [0, 0.08, 0.16, 4.0]"},
    "2bin":     {"bins": [0., 1.6, 4.0],              "nbins": 2,
                 "label": "2-bin [0, 1.6, 4.0]"},
    "3bin_nom": {"bins": [0., 0.8, 1.6, 4.0],         "nbins": 3,
                 "label": "3-bin nominal [0, 0.8, 1.6, 4.0]"},
    "3bin_v1":  {"bins": [0., 0.4, 1.6, 4.0],         "nbins": 3,
                 "label": "3-bin v1 [0, 0.4, 1.6, 4.0]"},
    "3bin_v2":  {"bins": [0., 0.8, 2.5, 4.0],         "nbins": 3,
                 "label": "3-bin v2 [0, 0.8, 2.5, 4.0]"},
    "3bin_v3":  {"bins": [0., 1.0, 2.0, 4.0],         "nbins": 3,
                 "label": "3-bin v3 [0, 1.0, 2.0, 4.0]"},
    "3bin_v4":  {"bins": [0., 0.5, 1.0, 4.0],         "nbins": 3,
                 "label": "3-bin v4 [0, 0.5, 1.0, 4.0]"},
    "4bin_v1":  {"bins": [0., 0.4, 0.8, 1.6, 4.0],    "nbins": 4,
                 "label": "4-bin v1 [0, 0.4, 0.8, 1.6, 4.0]"},
    "4bin_v2":  {"bins": [0., 0.8, 1.2, 1.6, 4.0],    "nbins": 4,
                 "label": "4-bin v2 [0, 0.8, 1.2, 1.6, 4.0]"},
    # --- Per-channel split schemes (bjet and lep get different boundaries) ---
    # Motivated by background shape plots: bjet bkg falls steeply by ~0.4 cm;
    # lep bkg has a secondary bump to ~0.7 cm and long-lifetime signals extend flat.
    "3bin_split": {
        "bjet_bins": [0., 0.4, 1.2, 4.0], "bjet_nbins": 3,
        "lep_bins":  [0., 0.5, 1.6, 4.0], "lep_nbins":  3,
        "label": "split: bjet[0,0.4,1.2,4] lep[0,0.5,1.6,4]",
    },
    "3bin_split_v2": {
        "bjet_bins": [0., 0.3, 1.0, 4.0], "bjet_nbins": 3,
        "lep_bins":  [0., 0.5, 1.6, 4.0], "lep_nbins":  3,
        "label": "split v2: bjet[0,0.3,1.0,4] lep[0,0.5,1.6,4]",
    },
    "3bin_412": {
        "bins": [0., 0.4, 1.2, 4.0], "nbins": 3,
        "label": "3-bin [0, 0.4, 1.2, 4.0]",
    },
    "2bin_split": {
        "bjet_bins": [0., 0.4, 4.0], "bjet_nbins": 2,
        "lep_bins":  [0., 0.5, 4.0], "lep_nbins":  2,
        "label": "2-bin split: bjet[0,0.4,4] lep[0,0.5,4]",
    },
    "4bin_split": {
        "bjet_bins": [0., 0.3, 0.8, 1.6, 4.0], "bjet_nbins": 4,
        "lep_bins":  [0., 0.4, 0.8, 1.6, 4.0], "lep_nbins":  4,
        "label": "4-bin split: bjet[0,0.3,0.8,1.6,4] lep[0,0.4,0.8,1.6,4]",
    },
    # --- Round 2: high-displacement boundaries ---
    # bjet: ggH tau=1mm M=55 extends to 3+ cm; add boundary at 2.5 cm
    # lep:  VH tau=10mm is flat to 4 cm with ~0 bkg past 2 cm; boundary at 3 cm
    "4bin_412_25": {"bins": [0., 0.4, 1.2, 2.5, 4.0], "nbins": 4,
                    "label": "4-bin [0, 0.4, 1.2, 2.5, 4.0]"},
    "3bin_420":    {"bins": [0., 0.4, 2.0, 4.0],       "nbins": 3,
                    "label": "3-bin [0, 0.4, 2.0, 4.0]"},
    "4bin_nom_30": {"bins": [0., 0.8, 1.6, 3.0, 4.0],  "nbins": 4,
                    "label": "4-bin [0, 0.8, 1.6, 3.0, 4.0]"},
    "4bin_516_30": {"bins": [0., 0.5, 1.6, 3.0, 4.0],  "nbins": 4,
                    "label": "4-bin [0, 0.5, 1.6, 3.0, 4.0]"},
    "3bin_520":    {"bins": [0., 0.5, 2.0, 4.0],        "nbins": 3,
                    "label": "3-bin [0, 0.5, 2.0, 4.0]"},
    "3bin_104":    {"bins": [0., 0.1, 0.4, 4.0],        "nbins": 3,
                    "label": "3-bin [0, 0.1, 0.4, 4.0]"},
    "4bin_104_200": {"bins": [0., 0.1, 0.4, 2.0, 4.0], "nbins": 4,
                     "label": "4-bin [0, 0.1, 0.4, 2.0, 4.0]"},
    "4bin_104_250": {"bins": [0., 0.1, 0.4, 2.5, 4.0], "nbins": 4,
                     "label": "4-bin [0, 0.1, 0.4, 2.5, 4.0]"},
}

# (sig_id, channel)  — sig_id matches Datacard_<ch>_<sig_id>_<year>.txt filename stem
SIGNAL_POINTS = [
    # Lepton-triggered
    ("VH_tau1mm_M55",                        "lep"),
    ("VH_tau10mm_M55",                       "lep"),
    ("VH_tau1mm_M40",                        "lep"),
    ("VH_tau1mm_M15",                        "lep"),
    # Displacement-triggered
    ("ggHToSSTodddd_tau1mm_M55",             "bjet"),
    ("ggHToSSTodddd_tau1mm_M40",             "bjet"),
    ("mfv_stopdbardbar_tau001000um_M0200",    "bjet"),
    ("mfv_stopdbardbar_tau000300um_M0400",    "bjet"),
    ("mfv_neu_tau001000um_M0400",             "bjet"),
]

YEARS = ["20161", "20162", "2017", "2018"]
