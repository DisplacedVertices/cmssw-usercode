# Input and output paths come from the required CLI arguments via set_paths().
# limits_config.yaml holds the runtime settings (bins, observations, filename patterns).
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
# Lepton trigger signals (mfv_neu excluded -- no hard-scatter lepton).
_lep_sigs = [
    "WminusHToSSTodddd", "WplusHToSSTodddd", "ZHToSSTodddd",
    "ggZHToSSTobbbb", "ggZHToSSTodddd",
    "ttHToLLPs_bbbb", "ttHToLLPs_dddd",
    "VHToSSTodddd", "VH",  # Signal clusters are treated similarly to signals
]

# Signals that fire the displaced (b-jet) trigger
_bjet_sigs = [
    "ggHToSSTodddd", "mfv_neu",
    "mfv_stopbbarbbar", "mfv_stopdbardbar",
    "ttHToLLPs_bbbb", "ttHToLLPs_dddd",
]

sig = {
    "type":      _cfg["channel"],
    "lep":       _cfg["signal"]["lep"],
    "bjet":      _cfg["signal"]["bjet"],
    "lep_sigs":  _lep_sigs,
    "bjet_sigs": _bjet_sigs,
    # VH = ZH + WH+ + WH- + ggZH summed. All four must be present at a given lifetime/mass
    # for the cluster to be built.
    "sig_grps": {
        "VHToSSTodddd": ["ZHToSSTodddd", "WminusHToSSTodddd", "WplusHToSSTodddd", "ggZHToSSTodddd"],
    },
    # Cluster members that are also generated on a wider lifetime grid than the rest of the
    # cluster. WplusH and WminusH only exist at 6 lifetimes, ggZH at 12, so a point where
    # only ggZH exists is not a broken cluster, it is simply not a VH point and gets skipped.
    # Any other member sitting alone IS a broken cluster and raises.
    "sig_grp_wide_members": frozenset(["ggZHToSSTodddd"]),
    # Nuisance aliases: use when a dedicated table doesn't exist for a process
    "aliases": {
        "bjet": {
            "ttHToLLPs_bbbb": {"ggHToSSTodddd"},
            "ttHToLLPs_dddd": {"ggHToSSTodddd"},
        },
        "lep": {
            "VHToSSTodddd":      {"VH"},
            "ttHToLLPs_bbbb":    {"VH"},
            "ttHToLLPs_dddd":    {"VH"},
            "ggZHToSSTobbbb":    {"VH"},
            "ggZHToSSTodddd":    {"VH"},
            "WminusHToSSTodddd": {"VH"},
            "WplusHToSSTodddd":  {"VH"},
            "ZHToSSTodddd":      {"VH"},
        },
    },
    # Nuisances that only apply to specific processes.
    # procs: process names that receive the nuisance
    # channels: trigger channels it applies in, None means any channel
    "spec_nuis": {
        # Processes with a hard-scatter lepton -- get lep_effi nuisance (VH, ttH; not SUSY).
        # "VH" is the combined signal group (ZH+WH++WH-+ggZH); individual sub-process names
        # are also listed for any cards generated outside the combined group path.
        # AN Sec 6.2.3: the electron SF uncertainty applies to the lepton-triggered channel only.
        "lep_effi": {
            "procs": frozenset([
                "VHToSSTodddd",
                "WminusHToSSTodddd", "WplusHToSSTodddd", "ZHToSSTodddd",
                "ggZHToSSTobbbb", "ggZHToSSTodddd",
                "ttHToLLPs_bbbb", "ttHToLLPs_dddd",
            ]),
            "channels": frozenset(["lep"]),
        },
        # Process-specific theory systematics (year- and bin-correlated, no CMS_EXO24035_ prefix)
        "qcd_scale_ren_ggH": {"procs": frozenset(["ggHToSSTodddd"]), "channels": None},
        "qcd_scale_fac_VH":  {"procs": frozenset(["VHToSSTodddd"]),            "channels": None},
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
# Folders stay None until set_paths() fills them from the required CLI arguments.
# --------------------------------------------------------------------------
output = {
    "lep":    {"out_folder": None},
    "bjet":   {"out_folder": None},
    "out_fn": _cfg["root_output"]["filename"],
}

datacard_out_loc = {
    "lep":           {"out_folder": None},
    "bjet":          {"out_folder": None},
    "out_fn_prefix": _cfg["datacard_output"]["prefix"],
    "out_fn_suffix": _cfg["datacard_output"]["suffix"],
}


def set_paths(minitree_dir, bkg_template_dir, out_dir):
    """
    Fill in the runtime paths from the required CLI arguments. Nothing in the committed
    yaml points at a personal area, so these must be supplied on every run.

    -INPUTS-
    minitree_dir: folder holding the signal MiniTrees for the channel being run
    bkg_template_dir: folder holding the background templates for the channel being run
    out_dir: base output folder; the LimitsInput and Datacard subfolders are made underneath
    """
    for ch in ("lep", "bjet"):
        sig[ch]["folder"] = os.path.join(minitree_dir, "")
        bkg[ch]["folder"] = os.path.join(bkg_template_dir, "")
        output[ch]["out_folder"] = os.path.join(
            out_dir, _cfg["root_output"]["subdir"], ch, "")
        datacard_out_loc[ch]["out_folder"] = os.path.join(
            out_dir, _cfg["datacard_output"]["subdir"], ch, "")


def make_out_dirs(channel):
    """Create the output folders for one channel if they don't already exist."""
    for folder in (output[channel]["out_folder"], datacard_out_loc[channel]["out_folder"]):
        if folder is None:
            raise Exception("Output paths not set. set_paths() must be called first.")
        if not os.path.isdir(folder):
            os.makedirs(folder)

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
    "fac_scale_VH_csv": _abs(_cfg["nuisance_tables"]["fac_scale_VH_csv"]),
}

# --------------------------------------------------------------------------
# Debug settings
# Both fake-scaling switches are off by default and must never be True in production.
# Datacards are assumed to already carry the intended scaling, since the MiniTree/Histos
# maker uses the correct branching fractions in the cross-section file.
# --------------------------------------------------------------------------
debug_settings = {
    "enabled":       _cfg.get("debug", True),
    "scale_bkg_fake": False,   # set True only for explicit testing; never in production
    "bkg_fake_sf":   100,
    "scale_sig_fake": False,   # set True only for explicit testing; never in production
    "sig_fake_sf": {           # write None for no correction. Store corrections as string
        "lep": {
            "default": None,
            "overrides": {},
        },
        "bjet": {
            "default": None,
            "overrides": {},
        },
    },
}
