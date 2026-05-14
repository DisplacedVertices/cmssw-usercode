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


def write_study_yaml(scheme_name, scheme_info):
    with open(YAML_BAK) as f:
        cfg = yaml.safe_load(f)

    nbins = scheme_info["nbins"]
    bins  = scheme_info["bins"]
    cfg["bins"]  = bins
    cfg["nbins"] = nbins
    cfg["observations"] = {yr: [0]*nbins for yr in YEARS}

    # Redirect outputs -- never touch nominal Datacards/ or LimitsInput/
    root_base = os.path.join(HERE, "root_output", scheme_name)
    dc_base   = os.path.join(HERE, "datacards",   scheme_name)
    for ch in CHANNELS:
        for d in [os.path.join(root_base, ch), os.path.join(dc_base, ch)]:
            if not os.path.exists(d):
                os.makedirs(d)
        cfg["root_output"][ch]["folder"]    = os.path.join(root_base, ch) + "/"
        cfg["datacard_output"][ch]["folder"] = os.path.join(dc_base,  ch) + "/"

    with open(YAML, "w") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False)


def restore_yaml():
    if os.path.exists(YAML_BAK):
        shutil.copy2(YAML_BAK, YAML)
        os.remove(YAML_BAK)


def run_pipeline(scheme_name):
    script = os.path.join(FORLIM, "makeLimitsInputROOT.py")
    for ch in CHANNELS:
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

        print("\n" + "="*60)
        print("SCHEME: %s   bins=%s" % (name, SCHEMES[name]["bins"]))
        print("="*60)

        # Always work from a clean backup
        shutil.copy2(YAML, YAML_BAK)
        try:
            write_study_yaml(name, SCHEMES[name])
            run_pipeline(name)
        finally:
            restore_yaml()
            print("Restored limits_config.yaml for scheme: %s" % name)

    print("\nAll schemes done. Nominal limits_config.yaml and Datacards/ untouched.")


if __name__ == "__main__":
    main()
