"""
A place to store the messy dictionaries required to make nuisance_configs_and_functions.py work.

nuis_names: nuisance naming

pickle_prefixes: where to find nuisance table storage
year_remaps: some filenames are provided with a different convention to our 20161-2018 conventions
"""
import script_configs as config

_ntpaths = config.nuisance_table_paths

nuis_names = {
    "CMS-CADI-tag": "CMS_EXO24035_",
    "Run2-key":     "13TeV",
}

pickle_prefixes = {
    "vtx_reco_TM":       _ntpaths["vtx_reco_TM"],
    "disp_trig_uncerts": _ntpaths["disp_trig_uncerts"],
}

pickle_triple_prefixes = {
    "example": {
        "base":    "location of pickle files",
        "up":      "filename of up pickle",
        "dn":      "filename of down pickle",
    },
}

year_remaps = {
    "vtx_reco_TM":       {"20161": "20161-2", "20162": "20161-2", "2017": "2017-8", "2018": "2017-8"},
    "disp_trig_uncerts": {"20161": "2016",    "20162": "2016APV",  "2017": "2017",   "2018": "2018"},
}

fac_scale_VH_csv_path = _ntpaths["fac_scale_VH_csv"]
