"""Central definition of all binning schemes and study signal points."""

SCHEMES = {
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
}

# (sig_id, channel)  — sig_id matches Datacard_<ch>_<sig_id>_<year>.txt filename stem
SIGNAL_POINTS = [
    # Lepton-triggered
    ("VH_tau1mm_M55",                        "lep"),
    ("VH_tau10mm_M55",                        "lep"),
    # Displacement-triggered
    ("ggHToSSTodddd_tau1mm_M55",              "bjet"),
    ("mfv_stopdbardbar_tau001000um_M0200",     "bjet"),
    ("mfv_stopdbardbar_tau000300um_M0400",     "bjet"),
    ("mfv_neu_tau001000um_M0400",              "bjet"),
]

YEARS = ["20161", "20162", "2017", "2018"]
