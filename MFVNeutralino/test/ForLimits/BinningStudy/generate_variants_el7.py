#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Run inside el7 apptainer + CMSSW_10_6_48 cmsenv.
# For each binning scheme: backs up limits_config.yaml, writes a modified
# version redirecting outputs to BinningStudy/, runs makeLimitsInputROOT.py,
# then restores the original yaml (even on error).
from __future__ import print_function
import os, sys, shutil, subprocess

try:
    import yaml
except ImportError:
    print("ERROR: yaml not available - run inside CMSSW cmsenv.")
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import SCHEMES

HERE     = os.path.dirname(os.path.abspath(__file__))
FORLIM   = os.path.dirname(HERE)
YAML     = os.path.join(FORLIM, "limits_config.yaml")
YAML_BAK = YAML + ".study_backup"

YEARS    = ["20161", "20162", "2017", "2018"]
CHANNELS = ["lep", "bjet"]


def is_split(scheme_info):
    return "lep_bins" in scheme_info


def _write_yaml(scheme_name, bins, nbins, channels):
    """Write limits_config.yaml for given bins/nbins, for specified channels only."""
    with open(YAML_BAK) as f:
        cfg = yaml.safe_load(f)
    cfg["bins"]  = bins
    cfg["nbins"] = nbins
    cfg["observations"] = {yr: [0]*nbins for yr in YEARS}
    root_base = os.path.join(HERE, "root_output", scheme_name)
    dc_base   = os.path.join(HERE, "datacards",   scheme_name)
    for ch in channels:
        for d in [os.path.join(root_base, ch), os.path.join(dc_base, ch)]:
            if not os.path.exists(d):
                os.makedirs(d)
        cfg["root_output"][ch]["folder"]    = os.path.join(root_base, ch) + "/"
        cfg["datacard_output"][ch]["folder"] = os.path.join(dc_base,  ch) + "/"
    with open(YAML, "w") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False)


def write_study_yaml(scheme_name, scheme_info):
    _write_yaml(scheme_name, scheme_info["bins"], scheme_info["nbins"], CHANNELS)


def restore_yaml():
    if os.path.exists(YAML_BAK):
        shutil.copy2(YAML_BAK, YAML)
        os.remove(YAML_BAK)


def run_pipeline(scheme_name, channels=None):
    script = os.path.join(FORLIM, "makeLimitsInputROOT.py")
    for ch in (channels or CHANNELS):
        cmd = [sys.executable, script, "--year", "all", "--channel", ch]
        print("\n>>> %s" % " ".join(cmd))
        ret = subprocess.call(cmd, cwd=FORLIM)
        if ret != 0:
            print("WARNING: exit %d for %s %s" % (ret, scheme_name, ch))


def main():
    schemes_to_run = sys.argv[1:] if len(sys.argv) > 1 else sorted(SCHEMES.keys())

    for name in schemes_to_run:
        if name not in SCHEMES:
            print("Unknown scheme:", name); continue

        info = SCHEMES[name]
        print("\n" + "="*60)
        print("SCHEME:", name)
        print("="*60)

        shutil.copy2(YAML, YAML_BAK)
        try:
            if is_split(info):
                # Run each channel separately with its own boundaries
                _write_yaml(name, info["lep_bins"], info["lep_nbins"], ["lep"])
                run_pipeline(name, ["lep"])
                _write_yaml(name, info["bjet_bins"], info["bjet_nbins"], ["bjet"])
                run_pipeline(name, ["bjet"])
            else:
                write_study_yaml(name, info)
                run_pipeline(name)
        finally:
            restore_yaml()
            print("Restored limits_config.yaml for scheme: %s" % name)

    print("\nAll schemes done. Nominal limits_config.yaml and Datacards/ untouched.")


if __name__ == "__main__":
    main()
