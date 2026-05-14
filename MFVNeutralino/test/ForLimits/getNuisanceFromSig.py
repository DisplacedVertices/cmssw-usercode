import numpy as np

import script_configs as config
import helper_PyStorage_objects as sth
import nuisance_configs_and_functions as nsfc


# ---------------------------------------------------------------------------
# Nuisance tag sets
# ---------------------------------------------------------------------------
nuis_allsigs = set([
    "mc_stat",      # MC Gamma-N
    "reco_effi",    # Reconstruction efficiency
    "vtx_reco_TM",  # TrackMover
    "pileup",       # Pileup
    "int_lumi",
])

# lep_effi is NOT included here -- it is added conditionally per signal below.
nuis_lep = set()

nuis_bjet = set([
    "disp_kine",    # Displacement trigger kinematic filters
    "bjet_filt",    # B-Jet filters
    "disp_filt",    # Displaced jet track filters
    "disp_tres",    # Track resolution, displaced filters
    "bjet_inef",    # Inefficiencies in offline b jet selection
    "btag_scfa",    # B-tag scale factors
    "JES",          # Jet Energy Scale
    "JER",          # Jet Energy Resolution
    "calo_inef",
])

# Replacements merge groups of nuisances into a single combined uncertainty
nuis_replacements = {
    "all": {},
    "bjet": {
        frozenset(["trig_JESR_btag"]): set([
            "disp_kine",
            "bjet_filt",
            "disp_filt",
            "disp_tres",
            "bjet_inef",
            "btag_scfa",
            "JES",
            "JER",
        ]),
    },
    "lep": {},
}

# Background systematics are disabled until CRs are unblinded and real uncertainties measured.
nuis_bkg = set()
nuis_bkg_replacements = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def replace_all_ones(new_nuis):
    """Drop a nuisance list if every entry is all 1.0s (no effect on the limit)."""
    for nuis in new_nuis:
        if not np.prod(nuis.nuis_val == np.ones_like(nuis.nuis_val)):
            return new_nuis
    return []


def get_nuis_fromname(nuis_name, siginfo, nuis_ls, debug_mode=False):
    """Dispatch to the appropriate nuisance-building function and append to nuis_ls."""
    new_nuis = []

    if   nuis_name == "mc_stat":       new_nuis = nsfc.get_mc_stat("mc_stat", siginfo, debug_mode=debug_mode)
    elif nuis_name == "reco_effi":     new_nuis = nsfc.get_reco_effi("tk_reco_eff", siginfo, debug_mode=debug_mode)
    elif nuis_name == "vtx_reco_TM":   new_nuis = nsfc.get_vtx_reco_TM("vtx_reco_TM", siginfo, debug_mode=debug_mode)
    elif nuis_name == "pileup":        new_nuis = nsfc.get_pileup("CMS_pileup", siginfo, debug_mode=debug_mode)
    elif nuis_name == "int_lumi":      new_nuis = nsfc.get_int_lumi("lumi", siginfo, debug_mode=debug_mode)
    elif nuis_name == "lep_effi":      new_nuis = nsfc.get_lep_effi("CMS_eff_", siginfo, debug_mode=debug_mode)
    elif nuis_name == "trig_JESR_btag": new_nuis = nsfc.get_trig_JESR_btag("disp_trig_uncerts", siginfo, debug_mode=debug_mode)
    elif nuis_name == "calo_inef":     new_nuis = nsfc.get_calo_inef("calo_ineff", siginfo, debug_mode=debug_mode)
    else:
        print("Error: nuisance name not implemented for", nuis_name)

    new_nuis = replace_all_ones(new_nuis)
    nuis_ls += new_nuis


def get_bkg_nuis_fromname(nuis_name, nuis_bkg_ls, debug_mode=False):
    new_nuis = []

    if   nuis_name == "bkg_jet_ang":   new_nuis = nsfc.get_bkg_jet_ang("dphiVV", debug_mode=debug_mode)
    elif nuis_name == "bkg_vtx_arbi":  new_nuis = nsfc.get_bkg_vtx_arbi("vtx_pair_eff_NtkSeeds", debug_mode=debug_mode)
    elif nuis_name == "bkg_vtx_refi":  new_nuis = nsfc.get_bkg_vtx_refi("vtx_pair_eff_MC", debug_mode=debug_mode)
    elif nuis_name == "pileup":        new_nuis = nsfc.get_bkg_pileup("CMS_pileup", debug_mode=debug_mode)
    elif nuis_name == "sig_cont":      new_nuis = nsfc.get_bkg_sig_cont(nuis_name, debug_mode=debug_mode)
    elif nuis_name == "bkg_norm":      new_nuis = nsfc.get_bkg_bkg_norm("bkg_norm", debug_mode=debug_mode)
    elif nuis_name == "n2v_unc":       new_nuis = nsfc.get_bkg_n2v_unc("num_vtx_pair_unc", debug_mode=debug_mode)
    else:
        raise Exception("Error: background nuisance name not implemented for " + nuis_name)

    new_nuis = replace_all_ones(new_nuis)
    nuis_bkg_ls += new_nuis


# ---------------------------------------------------------------------------
# Main public interface
# ---------------------------------------------------------------------------

def get_nuis_fromsig(siginfo, nuis_ls, debug_mode=False):
    """Build the nuisance list for one signal hypothesis.

    lep_effi is only added for processes that have a lepton in the hard scatter
    (VH, ttH). Pure SUSY signals fired by the lepton trigger do not receive it.
    """
    trig_type = siginfo.trig_type

    nuis_set = nuis_allsigs.copy()
    if trig_type == "lep":
        nuis_set.update(nuis_lep)
        # Only VH and ttH carry a lepton reco efficiency uncertainty
        if siginfo.proc in config.lep_reco_effi_sigs:
            nuis_set.add("lep_effi")
    elif trig_type == "bjet":
        nuis_set.update(nuis_bjet)
    else:
        print("FAIL: please make sure the input SignalROOTInfo object has a trig_type identified")
        return

    for repl in nuis_replacements["all"]:
        nuis_set.update(repl)
        nuis_set = nuis_set.difference(nuis_replacements["all"][repl])
    for repl in nuis_replacements[trig_type]:
        nuis_set.update(repl)
        nuis_set = nuis_set.difference(nuis_replacements[trig_type][repl])

    if debug_mode:
        print("\n" + siginfo.return_nuis_key())
        print("Nuisances identified:", nuis_set, "\n")

    for nuis in sorted(nuis_set):
        get_nuis_fromname(nuis, siginfo, nuis_ls, debug_mode=debug_mode)

    if debug_mode:
        print("Nuisances that produced a SIG Nuisance object:")
        for nuis in nuis_ls:
            nuis.print_diagnostics()


def get_nuis_frombkg(nuis_bkg_ls, debug_mode=False):
    """Build the nuisance list for the background estimate."""
    nuis_set = nuis_bkg.copy()

    for repl in nuis_bkg_replacements:
        nuis_set.update(repl)
        nuis_set = nuis_set.difference(nuis_bkg_replacements[repl])

    if debug_mode:
        print("Nuisances identified:", nuis_set, "\n")

    for nuis in sorted(nuis_set):
        get_bkg_nuis_fromname(nuis, nuis_bkg_ls, debug_mode=debug_mode)

    if debug_mode:
        print("Nuisances that produced a BKG Nuisance object:")
        for nuis in nuis_bkg_ls:
            nuis.print_diagnostics()
