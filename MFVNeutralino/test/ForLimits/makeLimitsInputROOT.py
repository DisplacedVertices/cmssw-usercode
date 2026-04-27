from __future__ import division
from __future__ import absolute_import

import ROOT
import numpy as np
import os
from glob import glob

from JMTucker.Tools.ROOTTools import to_TH1D, move_overflow_into_last_bin

import script_configs as config # everything hard-coded goes into config
import sig_and_bkg_configs as sb_conf
import getNuisanceFromSig as getns
import makeDatacard as mkdat
import helper_PyStorage_objects as sth # Tracks signal and nuisance info. I called it sth to mean "storage helper", for no reason
import helper_ROOT_functions as ROOThelper
from makeDatacard import make_nuis_dcnm as mk_dcnm 



#Settings
debug = True # Will print a ton of statements to report progress
print_mapping = True # Print signal to int map, highly recommend

# Ad-hoc stuff
limitsinput_expr = "1==1" #historical



#Global variables
year = config.datacard["year"]
year_id = config.datacard["year_key"].index(year) # This is like the "int i" describing the location
nbins = config.datacard["nbins"]
bins = np.array(config.datacard["bins"])
sig_type = config.sig["type"]

year_to_tag = config.datacard["year_to_tag"]
year_tag = year_to_tag[year]






def check_config():
    """
    Sanity-check the config
    """
    if config.datacard["year"] not in config.datacard["year_key"]:
        raise Exception("year must be in the list year_key")
    
    if len(config.datacard["bins"])!=config.datacard["nbins"]+1:
        raise Exception("The entry nbins must match bins")
    
    if config.sig["type"]!="lep" and config.sig["type"]!="bjet":
        raise Exception("Signal type must be either lep or bjet")

    if len(config.obs[config.datacard["year"]])!=config.datacard["nbins"]:
        raise Exception("Length of observations must match nbins")

    if config.debug_settings["scale_bkg_fake"]: print "Will scale bkg by FAKE values"
    return






def make_bkg(f, **kwargs):
    """
    Write: lumi, observations, rebinned sum_dBV

    This section is NOT responsible for adding nuisance parameters to background
    
    -INPUTS-
    f: ROOT object to write into
    #year: string, like config.datacard["year"]
    #year_id: int, to index the year
    #year_tag: the bkg histogram will be called bkg+tag, e.g. bkg7
    #sig_type: string, either "lep" or "bjet"
    
    -OUTPUTS-
    f will store new histograms
    """
    
    bkg_fn = (config.bkg[sig_type]["folder"] + config.bkg[sig_type]["fn"]).format(year)
    if debug: print "Opening bkg file: ", bkg_fn, "\n"
    bkg_f = ROOT.TFile.Open(bkg_fn)

    new_bkg_hs = []
    
    
    h_int_lumi = ROOT.TH1D('h_int_lumi_%s' % year, '', 1, 0, 1) #historical
    h_int_lumi.SetBinContent(1, sb_conf.template_norms["lumi"][sig_type][year_id])
    if debug: print "Lumi: ", sb_conf.template_norms["lumi"][sig_type][year_id], "\n"
    new_bkg_hs.append(h_int_lumi)
    

    h_observed = ROOT.TH1D('h_observed_%s' % year, '', nbins, bins)
    for i,v in enumerate(config.obs[year]):
        h_observed.SetBinContent(i+1, v)
        if debug: print "Setting observed bin #", i, " to ", v
    if debug: print #newline
    new_bkg_hs.append(h_observed)
    

    # Not implemented: h_bkg_dbv
    
    h_bkg_sumdbv = to_TH1D(bkg_f.Get("h_c1v_sumdbv"), "h_bkg_sumdbv_%s" %year)
    scale_num, scale_den = sb_conf.template_norms["n2v"][sig_type][year_id], h_bkg_sumdbv.Integral()
    h_bkg_sumdbv.Scale(scale_num / scale_den) #FIXME: does Integral() add the over and under-flows?
    if debug: print "Old Sum_dBV integral %.3g" %scale_den, " was scaled to %.3g" %scale_num
    if config.debug_settings["scale_bkg_fake"]:
        h_bkg_sumdbv.Scale(config.debug_settings["bkg_fake_sf"])
        print "Warning: scaled background again by", config.debug_settings["bkg_fake_sf"], "to make FAKE bkg", "\n"
    
    h_bkg_sumdbv_rebin = h_bkg_sumdbv.Rebin(nbins, "bkg" + year_tag, bins)
    move_overflow_into_last_bin(h_bkg_sumdbv_rebin)
    new_bkg_hs.append(h_bkg_sumdbv_rebin)
    
    
    f.cd()
    for h in new_bkg_hs:
        h.SetTitle('')
        h.Write()
        if debug: print "Wrote to file: ", h.GetName()

    print "BACKGROUND processing complete"
    return






def make_sigs(f, sig_nums, sig_scales, sig_fake_corrs, **kwargs):
    """
    Writes: signal (rebinned sumdbv), ngen, ngen-per-bin

    -INPUTS-
    f: ROOT object to write into
    sig_nums: dictionary. Code will fill {SigGrp object : int}
    sig_scales: dictionary. Code will fill (SigGrp object: scalings from hist integral -> actual integral)
    
    -OUTPUTS-
    f will store new histograms
    sig_nums and sig_scales will be added to
    """

    sig_fn_syntax = config.sig[sig_type]["folder"] + config.sig[sig_type]["file_key"]
    candidate_files = sorted(glob(sig_fn_syntax)) # list of strings
    sig_id = int(0)

    if debug: print ""
    for cand in candidate_files:
        if os.path.basename(cand).find(year) != -1:
            generated_siggrp = False
            #if debug: print ""
            try:
                siginfo = sth.SignalROOTInfo(cand, root_exists=True, nbins=nbins) # If it prints 2 warnings, this line is why
                in_cluster = False
                for sc in config.sig["sig_grps"].keys(): # signal-cluster
                    if siginfo.proc in config.sig["sig_grps"][sc]:
                        in_cluster = True
                        if siginfo.proc==config.sig["sig_grps"][sc][0]: # if leading term, make the cluster
                            sig_str_ls = [cand.replace(siginfo.proc, p) for p in config.sig["sig_grps"][sc]]
                            print "Found cluster", sig_str_ls, "to be named", sc
                            siggrp = sth.SigRInf_Grp(sig_str_ls, root_exists=True, nbins=nbins, overwrite_proc=sc)
                            generated_siggrp=True
                            break
                if in_cluster == False: # ignore things that aren't the leading term of some sig-cluster
                    sig_str_ls = [cand]
                    siggrp = sth.SigRInf_Grp(sig_str_ls, root_exists=True, nbins=nbins, overwrite_proc=None)
                    generated_siggrp = True
                # siginfo = sth.SignalROOTInfo(cand, root_exists=True, nbins=nbins)
            except ValueError as e:
                if str(e)=="No Samples.py entry": print "Signal name not in Samples.py, skipping", os.path.basename(cand)
                else: raise Exception("Creating siginfo threw unknown error")
            if generated_siggrp==False: continue
            if siggrp.trig_type != sig_type: continue
            if debug: print "Queried file:", os.path.basename(cand), ". Type identified: ", siggrp.trig_type
            sig_nums.update({siggrp: str(sig_id)})
            if debug: print "This is signal #", sig_id
            sig_id += int(1)
            siggrp.print_diagnostics()
            if debug: print ""
    
    if print_mapping:
        print "\n\nMapping: "
        for k in sig_nums.keys():
            print k.fn, ":", sig_nums[k]
    print "\n"
    
    n = lambda sig_num, x: 'h_sig%s_%s_%s'  % (sig_num, x, year) # Inherited code
    
    
    for siggrp in sig_nums.keys():
        if debug: print "Reporting cluster", siggrp.fn
        
        sig_id = sig_nums[siggrp]

        sumw = 0.
        ngen = 0 # historical thing, not sure if useful

        r_f_corr = None # For "r fake correction"
        if config.debug_settings["scale_sig_fake"]:
            if siggrp.proc in config.debug_settings["sig_fake_sf"][sig_type]["overrides"]: r_f_corr = config.debug_settings["sig_fake_sf"][sig_type]["overrides"][siggrp.proc]
            else: r_f_corr = config.debug_settings["sig_fake_sf"][sig_type]["default"]
        if (r_f_corr is not None) and debug: print "Signal", siggrp.proc, "to be artificially scaled by", r_f_corr
        sig_fake_corrs.update({siggrp: r_f_corr})
        
        ROOT.TH1.AddDirectory(1)
        h_sumdbv_tot = ROOT.TH1D(n(sig_id, 'sumdbv'),  '', 800, 0, 8)
        h_sumdbv_nw_tot = ROOT.TH1D(n(sig_id, 'sumdbv')+"_nw",  '', 800, 0, 8) # No-weight version
        
        scales = []

        for sig in siggrp.sig_ls:
            if debug: print "Reporting sub-sig", sig.fn

            t = ROOT.TChain('mfvMiniTree/t')
            t.Add(sig.full_fn)
            t.SetAlias('limitsinput_pass', limitsinput_expr) # historical thing

            this_sumw = sig.get_sumw()
            this_ngen = sig.get_ngen()
            if debug: print "SumW obtained:", this_sumw, ", NGen obtained:", this_ngen

            # Rescale signal
            this_xsec = sig.get_xsec()
            if debug: print "X-Sec:", this_xsec
            this_sigyield = this_xsec * sb_conf.template_norms["lumi"][sig.trig_type][year_id]

            this_scale = this_sigyield / this_sumw
            scales.append(this_scale)
            if debug: print "Will scale sumw", this_sumw, "to", this_sigyield


            h_to_rescale = []

            ROOT.TH1.AddDirectory(1)
            h_child_sumdbv = ROOT.TH1D(n(sig_id, 'child_sumdbv'), '', 800, 0, 8)
            h_child_sumdbv_nw = ROOT.TH1D(n(sig_id, 'child_sumdbv')+"_nw",  '', 800, 0, 8) # No-weight version
            if debug: print "Made histogram", n(sig_id,'child_sumdbv'), ",", n(sig_id, 'child_sumdbv')+"_nw"
            t.Draw('sumdbv>>%s' % n(sig_id, 'child_sumdbv'),  'weight*(limitsinput_pass && nvtx>=2)')
            t.Draw('sumdbv>>%s' % n(sig_id, 'child_sumdbv')+"_nw",  '1.0*(limitsinput_pass && nvtx>=2)')
            h_to_rescale.append(h_child_sumdbv)

            ROOT.TH1.AddDirectory(0)
            for h in h_to_rescale:
                h.SetDirectory(0)
                h.Scale(this_scale)
            h_child_sumdbv_nw.SetDirectory(0) # historical, idk what this does

            h_sumdbv_tot.Add(h_child_sumdbv)
            h_sumdbv_nw_tot.Add(h_child_sumdbv_nw)

            sumw += this_sumw
            ngen += this_ngen
            
            t.Reset()
            h_child_sumdbv = ROOT.TH1D()
            h_child_sumdbv_nw = ROOT.TH1D()

        if debug: print "SumW obtained:", sumw, ", NGen obtained:", ngen 
        sig_scales.update({siggrp : scales})
        
        new_sig_hs = []
        
        h_sig = h_sumdbv_tot.Rebin(nbins, "sig"+year_tag+sig_id, bins)
        move_overflow_into_last_bin(h_sig)

        # nominal_corr_sig = getns.get_nominal_corr_fromsig(siggrp, debug_mode=debug) # Disabled code. This was when stuff was multiplied by central corrections.
        # ROOThelper.mult_hist_w_array(h_sig, nominal_corr_sig)

        if (r_f_corr is not None):
            h_sig.Scale(float(r_f_corr))
            if debug: print "Scaled signal by fake correction", r_f_corr
        if debug: print "Made signal: ", h_sig.GetName()
        new_sig_hs.append(h_sig)
 

        h_sig_nw = h_sumdbv_nw_tot.Rebin(nbins, n(sig_id, 'ngen_perbin'), bins)
        move_overflow_into_last_bin(h_sig_nw)
        new_sig_hs.append(h_sig_nw)

        h_sumw = ROOT.TH1D(n(sig_id, 'sumw'), '', 1,0,1)
        h_sumw.SetBinContent(1, sumw)
        new_sig_hs.append(h_sumw)

        f.cd()
        for h in new_sig_hs:
            h.SetTitle(siggrp.proc+"_"+year)
            h.Write()
            if debug: print "Wrote to file: ", h.GetName()
        if debug: print

    print "SIGNAL processing complete"
    return






def write_sig_updown(f, nuis_ls, siggrp, sig_scales, sig_fake_corrs, sig_id, **kwargs):
    """
    Given a list of nuisances and signal tag, write corresponding histograms for every shape nuisance (ignores non-shape nuisances).

    -INPUTS-
    f: ROOT file
    nuis_ls: list of Nuisance objects
    siggrp: SigGrp object
    sig_scales: mapping of SigInfo objects to scales (scale := MiniTree to signal model)
    sig_id: integer describing the signal
    
    -OUTPUTS-
    f: will be written to
    """

    scales = sig_scales[siggrp]
    if debug: print "\nAll hists of", siggrp.fn, "to be scaled by", scales

    r_f_corr = sig_fake_corrs[siggrp]
    if (r_f_corr is not None) and debug: print "All hists artificially scaled by", r_f_corr
    

    for nuis in nuis_ls:
        if nuis.make_updn == False: continue

        nname = mk_dcnm(nuis, siggrp)
        nname_dict = mk_dcnm(nuis, siggrp, force_no_CADItag=True) # for searching config
        #if nuis.sep_yrs==True: nn_yrtg = year_tag # In the datacard-writing phase, nuis_name will have year_tag appended to it if year-dependent
        #else: nn_yrtg = ""

        hname_up = "sig"+year_tag+sig_id + "_"+nname+"Up"
        hname_dn = "sig"+year_tag+sig_id + "_"+nname+"Down"

        ROOT.TH1.AddDirectory(1)
        h_sumdbv_up_tot = ROOT.TH1D(hname_up+"_orig", '', 800, 0, 8)
        h_sumdbv_dn_tot = ROOT.TH1D(hname_dn+"_orig", '', 800, 0, 8)


        for i, sig in enumerate(siggrp.sig_ls):
            t = ROOT.TChain('mfvMiniTree/t')
            t.Add(sig.full_fn)
            t.SetAlias('limitsinput_pass', limitsinput_expr)

            ROOT.TH1.AddDirectory(1)
            h_sumdbv_up = ROOT.TH1D(hname_up+"_child_orig", '', 800, 0, 8)
            h_sumdbv_dn = ROOT.TH1D(hname_dn+"_child_orig", '', 800, 0, 8)
            
            t.Draw('sumdbv>>%s' % hname_up+"_child_orig", 'weight*(limitsinput_pass && nvtx>=2)'.replace('weight', sb_conf.updn_wt_dict[nname_dict][0]))
            t.Draw('sumdbv>>%s' % hname_dn+"_child_orig", 'weight*(limitsinput_pass && nvtx>=2)'.replace('weight', sb_conf.updn_wt_dict[nname_dict][1]))

            h_sumdbv_up.Scale(scales[i])
            h_sumdbv_dn.Scale(scales[i])

            h_sumdbv_up_tot.Add(h_sumdbv_up)
            h_sumdbv_dn_tot.Add(h_sumdbv_dn)

            t.Reset()
            h_sumdbv_up = ROOT.TH1D()
            h_sumdbv_dn = ROOT.TH1D()


        ROOT.TH1.AddDirectory(0)
        h_sig_up = h_sumdbv_up_tot.Rebin(nbins, hname_up, bins)
        h_sig_dn = h_sumdbv_dn_tot.Rebin(nbins, hname_dn, bins)
        hs_updn = [h_sig_up, h_sig_dn]

        # nominal_corr_sig = getns.get_nominal_corr_fromsig(siggrp, debug_mode=False)

        for h in hs_updn:
            move_overflow_into_last_bin(h)
            # ROOThelper.mult_hist_w_array(h, nominal_corr_sig)
            if (r_f_corr is not None):
                h.Scale(float(r_f_corr))
            h.SetDirectory(0)


        f.cd()
        for h in hs_updn:
            h.SetTitle(siggrp.proc+"_"+year)
            h.Write()
            if debug: print "Wrote to file: ", h.GetName()

        h_sumdbv_up_tot = ROOT.TH1D() # wipe info
        h_sumdbv_dn_tot = ROOT.TH1D()
        h_sig_up = ROOT.TH1D()
        h_sig_dn = ROOT.TH1D()

    return






def make():
    """
    The main executable.
    """
    if debug: print "Year is ", year, ", type ", sig_type
    
    out_loc = config.output[sig_type]["out_folder"] + config.output["out_fn"] +"_"+sig_type +"_"+year
    if config.debug_settings["scale_bkg_fake"]: out_loc += "_fakebkg"
    out_loc += ".ROOT"
    if debug: print "Making and writing ", out_loc, "\n"
    #assert not os.path.exists(out_loc)
    ROOT.TH1.AddDirectory(0)
    f = ROOT.TFile(out_loc, 'recreate')


    # Background Processing
    if debug: print "\nStarted writing BACKGROUND"
    make_bkg(f=f)


    # Draw Signal
    sig_nums = {} # signal obj to number dictionary
    sig_scales = {} # Apparently this is a nightmare to calculate unless I store them
    sig_fake_corrs = {} # signal object to forced SFs (e.g. force multiply sig by 1e-3)
    
    if debug: print "\nStarted writing SIGNAL"
    make_sigs(f=f, sig_nums=sig_nums, sig_scales=sig_scales, sig_fake_corrs=sig_fake_corrs)


    # Get bkg nuisances FIXME
    if debug: print "\nAdding BACKGROUND nuisances"
    nuis_bkg_ls = []
    getns.get_nuis_frombkg(nuis_bkg_ls, debug_mode=debug)
    if debug: print "Warning: up-down functionality for BKG not yet implemented"


    # Get Signal nuisances
    if debug: print "\nAdding SIGNAL nuisances"
    nuis_ls = []
    
    for siggrp in sig_nums.keys():
        nuis_ls = []
        getns.get_nuis_fromsig(siggrp, nuis_ls, debug_mode=debug)

        if debug: print "Writing Up and Down"
        write_sig_updown(f=f, nuis_ls=nuis_ls, siggrp=siggrp, sig_scales=sig_scales, sig_fake_corrs=sig_fake_corrs, sig_id=sig_nums[siggrp])

        if debug: print "Writing DATACARD"
        mkdat.make_datacard(f=f, nuis_ls=nuis_ls, nuis_bkg_ls=nuis_bkg_ls, siggrp=siggrp, sig_fake_corrs=sig_fake_corrs, sig_id=sig_nums[siggrp], debug_mode=debug)
    nuis_ls = []
    
    return




if __name__ == '__main__':
    check_config()
    make()
    
