from __future__ import absolute_import

import numpy as np

import helper_PyStorage_objects as sth
import nuisance_configs_and_functions as nsfc


# Nuisance tags
nuis_allsigs = set([
    "mc_stat", # MC Gamma-N
    "reco_effi", # Reconstruction efficiency
    "vtx_reco_TM", # TrackMover
    "pileup", # Pileup
    "int_lumi",])
nuis_lep = set([
    "lep_effi",])
nuis_bjet = set([
    "disp_kine", # Displacement trigger kinematic filters
    "bjet_filt", # B-Jet filters
    "disp_filt", # Displaced jet track filters
    "disp_tres", # Track Resolution, displaced filters
    "bjet_inef", # Inefficiencies in offline b jet selection
    "btag_scfa", # B-tag scale factors
    "JES", # Jet Energy Scale
    "JER", # Jet Energy Resolution
    "calo_inef",])

nuis_replacements = { # This replaces clusters of nuisances with overall uncertainties, e.g. B-jet SFs and JES/R are put together
    "all": {},
    # "bjet": {},
    "bjet": {
        frozenset(["trig_JESR_btag"]): set([
            "disp_kine", # Displacement trigger kinematic filters
            "bjet_filt", # B-Jet filters
            "disp_filt", # Displaced jet track filters
            "disp_tres", # Track Resolution, displaced filters
            "bjet_inef", # Inefficiencies in offline b jet selection # Note: this is the AN edit
            "btag_scfa", # B-tag scale factors
            "JES", # Jet Energy Scale
            "JER",]),
    },
    "lep": {},
}



nuis_bkg = set([
    "sum_dbvc", # The Constructed Sum-d_BV^C Distribution
    "pileup", #Pile-Up Effects
    "sig_cont", # Signal contamination
    "bkg_norm",
    "n2v_unc"])

nuis_bkg_replacements = { # not to be confused with nuis_replacements (about signal)
    frozenset(["bkg_jet_ang", "bkg_vtx_arbi", "bkg_vtx_refi"]): set(["sum_dbvc"])
}



"""
nominal_corr_sig = set([
    "reco_effi",])
"""



def replace_all_ones(new_nuis):
    """ Little function that removes a nuisance list, if they're all 1.0's """
    all_ones = True # Kill 1.0-nuis
    for nuis in new_nuis:
        if not np.prod(nuis.nuis_val == np.ones_like(nuis.nuis_val)):
            all_ones = False
            break
    if all_ones: return []
    else: return new_nuis






"""
def get_nominal_corr_sig_fromname(label, siginfo, debug_mode=False):
    """
    # -OUTPUT-
    # Numpy array of length #bins
"""
    factor = np.ones(siginfo.nbins)

    if label == "reco_effi": factor = nsfc.get_nominal_reco_effi_sig(siginfo, debug_mode=debug_mode)

    else: print "Error: signal multiplicative factor not implemented for", label

    return factor
"""






def get_nuis_fromname(nuis_name, siginfo, nuis_ls, debug_mode=False):
    """
    Not to be confused with get_bkg_nuis_fromname.

    -OUTPUTS-
    nuis_ls is appended to
    """
    new_nuis = []

    if nuis_name == "mc_stat": new_nuis = nsfc.get_mc_stat(nuis_name, siginfo, debug_mode=debug_mode)

    elif nuis_name == "reco_effi": new_nuis = nsfc.get_reco_effi("tk_reco_eff", siginfo, debug_mode=debug_mode)

    elif nuis_name == "vtx_reco_TM": new_nuis = nsfc.get_vtx_reco_TM(nuis_name, siginfo, debug_mode=debug_mode)

    elif nuis_name == "pileup": new_nuis = nsfc.get_pileup("CMS_pileup", siginfo, debug_mode=debug_mode)
    
    elif nuis_name == "int_lumi": new_nuis = nsfc.get_int_lumi("lumi", siginfo, debug_mode=debug_mode)

    elif nuis_name == "lep_effi": new_nuis = nsfc.get_lep_effi("CMS_eff_", siginfo, debug_mode=debug_mode)

    elif nuis_name == "trig_JESR_btag": new_nuis = nsfc.get_trig_JESR_btag("disp_trig_uncerts", siginfo, debug_mode=debug_mode)

    elif nuis_name == "calo_inef": new_nuis = nsfc.get_calo_inef("calo_ineff", siginfo, debug_mode=debug_mode)

    else: print "Error: nuisance name not implemented for", nuis_name

    new_nuis = replace_all_ones(new_nuis)

    nuis_ls += new_nuis
    return






def get_bkg_nuis_fromname(nuis_name, nuis_bkg_ls, debug_mode=False):
    new_nuis = []

    #if nuis_name == "sum_dbvc": new_nuis = nsfc.get_bkg_sum_dbvc(nuis_name, debug_mode=debug_mode)

    if nuis_name == "bkg_jet_ang": new_nuis = nsfc.get_bkg_jet_ang("dphiVV", debug_mode=debug_mode)

    elif nuis_name == "bkg_vtx_arbi": new_nuis = nsfc.get_bkg_vtx_arbi("vtx_pair_eff_NtkSeeds", debug_mode=debug_mode)

    elif nuis_name == "bkg_vtx_refi": new_nuis = nsfc.get_bkg_vtx_refi("vtx_pair_eff_MC", debug_mode=debug_mode)

    elif nuis_name == "pileup": new_nuis = nsfc.get_bkg_pileup("CMS_pileup", debug_mode=debug_mode)

    elif nuis_name == "sig_cont": new_nuis = nsfc.get_bkg_sig_cont(nuis_name, debug_mode=debug_mode)

    elif nuis_name == "bkg_norm": new_nuis = nsfc.get_bkg_bkg_norm("bkg_norm", debug_mode=debug_mode) # Note naming. Chosen to prevent mix-ups

    elif nuis_name == "n2v_unc": new_nuis = nsfc.get_bkg_n2v_unc("num_vtx_pair_unc", debug_mode=debug_mode)

    else: raise Exception("Error: background nuisance name not implemented for", nuis_name)

    new_nuis = replace_all_ones(new_nuis)

    nuis_bkg_ls += new_nuis
    return






""" # Removed code, was for central corrections
def get_nominal_corr_fromsig(siginfo, debug_mode=False):
    """
    # Given a siginfo object, give corrections to nominal values.

    # -OUTPUT-
    # Array-like of float, size #bins: multiplicative correction
"""
    corr_ls = []

    for label in sorted(nominal_corr_sig):
        corr_ls.append(get_nominal_corr_sig_fromname(label, siginfo, debug_mode=debug_mode))

    total_factor = np.ones(siginfo.nbins)
    for cor in corr_ls:
        total_factor *= cor


    if debug_mode:
        print "Queried multiplicative corrections to Signal, multiplying by:", total_factor

    return total_factor
"""






def get_nuis_fromsig(siginfo, nuis_ls, debug_mode=False):
    """
    Given a siginfo object, produce a list of nuisance parameters.

    -INPUTS-
    siginfo: a SignalROOTInfo object
    nuis_ls: empty list (though it should work if not empty)
    """

    trig_type = siginfo.trig_type

    nuis_set = nuis_allsigs.copy()
    if trig_type == "lep":
        nuis_set.update(nuis_lep)
    elif trig_type == "bjet":
        nuis_set.update(nuis_bjet)
    else:
        print "FAIL: please make sure the input SignalROOTInfo object has a trig_type identified"
        return

    for repl in nuis_replacements["all"].keys():
        nuis_set.update(repl)
        nuis_set = nuis_set.difference(nuis_replacements["all"][repl])
    for repl in nuis_replacements[trig_type].keys():
        nuis_set.update(repl)
        nuis_set = nuis_set.difference(nuis_replacements[trig_type][repl])
    if debug_mode: print "\n"+siginfo.return_nuis_key()
    if debug_mode: print "Nuisances identified: ", nuis_set, "\n"
    
    
    for nuis in sorted(nuis_set):
        get_nuis_fromname(nuis, siginfo, nuis_ls, debug_mode=debug_mode)
    if debug_mode:
        print "Nuisances that produced a SIG Nuisance object:"
        for nuis in nuis_ls: nuis.print_diagnostics()
        
    return






def get_nuis_frombkg(nuis_bkg_ls, debug_mode=False):
    """
    Given the background information, produce a list of nuisance parameters.

    -INPUTS-
    nuis_bkg_ls: empty list (though it should work if not empty)
    """

    nuis_set = nuis_bkg.copy()

    for repl in nuis_bkg_replacements.keys():
        nuis_set.update(repl)
        nuis_set = nuis_set.difference(nuis_bkg_replacements[repl])
    if debug_mode: print "Nuisances identified: ", nuis_set, "\n"


    for nuis in sorted(nuis_set):
        get_bkg_nuis_fromname(nuis, nuis_bkg_ls, debug_mode=debug_mode)
    if debug_mode:
        print "Nuisances that produced a BKG Nuisance object:"
        for nuis in nuis_bkg_ls: nuis.print_diagnostics()
        print "Warning: most nuisances haven't been implemented. I will write them after the rest of the pipeline is set up."
    
    return


