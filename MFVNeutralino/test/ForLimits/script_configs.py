# Runtime paths and settings come from limits_config.yaml.
# Physics configuration (signal groupings, nuisance lists) lives here.
import os
import yaml

# --------------------------------------------------------------------------
# Load YAML config
# --------------------------------------------------------------------------
_here = os.path.dirname(os.path.abspath(__file__))
_yaml_path = os.path.join(_here, "limits_config.yaml")

with open(_yaml_path) as _f:
    _cfg = yaml.safe_load(_f)

def _abs(rel):
    """Resolve a path relative to the ForLimits directory."""
    return os.path.join(_here, rel)

# --------------------------------------------------------------------------
# Datacard settings
# --------------------------------------------------------------------------
_year_to_tag = {
    "20161": "2016preAPV",
    "20162": "2016postAPV",
    "2017":  "2017",
    "2018":  "2018",
}

datacard = {
    "year":        _cfg["year"],
    "year_key":    ["20161", "20162", "2017", "2018"],
    "year_to_tag": _year_to_tag,
    "bins":        _cfg["bins"],
    "nbins":       _cfg["nbins"],
}

# --------------------------------------------------------------------------
# Signal configuration
# --------------------------------------------------------------------------
# Signals that fire the lepton trigger.
# mfv_neu is NOT in the lepton channel -- it has no lepton in the hard scatter.
_lep_sigs = [
    "WminusHToSSTodddd", "WplusHToSSTodddd", "ZHToSSTodddd",
    "ggZHToSSTobbbb", "ggZHToSSTodddd",
    "ttHToLLPs_bbbb", "ttHToLLPs_dddd",
]

# Signals that fire the displaced (b-jet) trigger
_bjet_sigs = [
    "ggHToSSTodddd", "mfv_neu",
    "mfv_stopbbarbbar", "mfv_stopdbardbar",
    "ttHToLLPs_bbbb", "ttHToLLPs_dddd",
]

# Lepton-triggered signals that require a lepton reco efficiency nuisance.
# VH (ZH/WH/ggZH) and ttH have a lepton in the hard scatter; SUSY signals do not.
lep_reco_effi_sigs = frozenset([
    "WminusHToSSTodddd", "WplusHToSSTodddd", "ZHToSSTodddd",
    "ggZHToSSTobbbb", "ggZHToSSTodddd",
    "ttHToLLPs_bbbb", "ttHToLLPs_dddd",
])

sig = {
    "type":      _cfg["channel"],
    "lep":       _cfg["signal"]["lep"],
    "bjet":      _cfg["signal"]["bjet"],
    "lep_sigs":  _lep_sigs,
    "bjet_sigs": _bjet_sigs,
    # VH = ZH + WH+ + WH- summed (same lifetime/mass grid, different xsec)
    "sig_grps": {
        "VH": ["ZHToSSTodddd", "WminusHToSSTodddd", "WplusHToSSTodddd", "ggZHToSSTodddd"],
    },
    # Nuisance aliases: use when a dedicated table doesn't exist for a process
    "aliases": {
        "bjet": {
            "ttHToLLPs_bbbb": {"ggHToSSTodddd"},
            "ttHToLLPs_dddd": {"ggHToSSTodddd"},
        },
        "lep": {
            "ttHToLLPs_bbbb":    {"VH"},
            "ttHToLLPs_dddd":    {"VH"},
            "ggZHToSSTobbbb":    {"VH"},
            "ggZHToSSTodddd":    {"VH"},
            "WminusHToSSTodddd": {"VH"},
            "WplusHToSSTodddd":  {"VH"},
            "ZHToSSTodddd":      {"VH"},
        },
    },
}

# --------------------------------------------------------------------------
# Background configuration
# --------------------------------------------------------------------------
bkg = {
    "lep":  _cfg["background"]["lep"],
    "bjet": _cfg["background"]["bjet"],
}
# Rename YAML key "filename" -> "fn" to preserve the existing interface
bkg["lep"]["fn"]  = bkg["lep"].pop("filename", bkg["lep"].get("fn", ""))
bkg["bjet"]["fn"] = bkg["bjet"].pop("filename", bkg["bjet"].get("fn", ""))

# --------------------------------------------------------------------------
# Output paths
# root_output  : intermediate ROOT file with signal/bkg histograms
# datacard_out_loc : final combine .txt datacard files
# --------------------------------------------------------------------------
output = {
    "lep":    {"out_folder": _cfg["root_output"]["lep"]["folder"]},
    "bjet":   {"out_folder": _cfg["root_output"]["bjet"]["folder"]},
    "out_fn": _cfg["root_output"]["filename"],
}

datacard_out_loc = {
    "lep":           {"out_folder": _cfg["datacard_output"]["lep"]["folder"]},
    "bjet":          {"out_folder": _cfg["datacard_output"]["bjet"]["folder"]},
    "out_fn_prefix": _cfg["datacard_output"]["prefix"],
    "out_fn_suffix": _cfg["datacard_output"]["suffix"],
}

# --------------------------------------------------------------------------
# Observed events (kept at 0 for blind analysis)
# --------------------------------------------------------------------------
obs = {k: list(v) for k, v in _cfg["observations"].items()}

# --------------------------------------------------------------------------
# Nuisance table paths (absolute, resolved relative to ForLimits/)
# --------------------------------------------------------------------------
nuisance_table_paths = {
    "vtx_reco_TM":       _abs(_cfg["nuisance_tables"]["vtx_reco_TM"]),
    "disp_trig_uncerts": _abs(_cfg["nuisance_tables"]["disp_trig_uncerts"]),
    "tk_reco_eff": {
        "base":      _abs(_cfg["nuisance_tables"]["tk_reco_eff"]["base"]),
        "up_prefix": _cfg["nuisance_tables"]["tk_reco_eff"]["up_prefix"],
        "dn_prefix": _cfg["nuisance_tables"]["tk_reco_eff"]["dn_prefix"],
    },
}

# --------------------------------------------------------------------------
# Debug settings
# --------------------------------------------------------------------------
debug_settings = {
    "enabled":       _cfg.get("debug", True),
    "scale_bkg_fake": False,   # set True only for explicit testing; never in production
    "bkg_fake_sf":   100,
}
