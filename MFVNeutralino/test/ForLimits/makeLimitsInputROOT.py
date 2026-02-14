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

year_to_tag = {"20161": "5", "20162": "6", "2017": "7", "2018": "8"} # used when we e.g. call background bkg5 to bkg8
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
    
    bkg_fn = (config.bkg["folder"] + config.bkg["fn"]).format(year)
    if debug: print "Opening bkg file: ", bkg_fn, "\n"
    bkg_f = ROOT.TFile.Open(bkg_fn)

    new_bkg_hs = []
    
    
    h_int_lumi = ROOT.TH1D('h_int_lumi_%s' % year, '', 1, 0, 1) #historical
    h_int_lumi.SetBinContent(1, sb_conf.template_norms["lumi"][year_id])
    if debug: print "Lumi: ", sb_conf.template_norms["lumi"][year_id], "\n"
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
    if debug: print "Old Sum_dBV integral %.3g" %scale_den, " was scaled to %.3g" %scale_num, "\n"
    
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






def make_sigs(f, sig_nums, sig_scales, **kwargs):
    """
    Writes: signal (rebinned sumdbv), ngen, ngen-per-bin

    -INPUTS-
    f: ROOT object to write into
    sig_nums: dictionary. Code will fill {SigInfo object : int}
    sig_scales: dictionary. Code will fill (SigInfo object: scaling from hist integral -> actual integral)
    #year: string, like config.datacard["year"]
    #year_id: int, to index the year
    #year_tag: the sig histogram will be called sig+tag+N, e.g. sig89 for sig 2018, 9th
    #sig_type: string, either "lep" or "bjet"
    
    -OUTPUTS-
    f will store new histograms
    sig_nums and sig_scales will be added to
    """

    sig_fn_syntax = config.sig["folder"] + config.sig["file_key"]
    candidate_files = sorted(glob(sig_fn_syntax)) # list of strings
    sig_id = int(0)

    for cand in candidate_files:
        if os.path.basename(cand).find(year) != -1:
            siginfo = sth.SignalROOTInfo(cand, root_exists=True, nbins=nbins)
            if debug: print "Queried file:", os.path.basename(cand), ". Type identified: ", siginfo.trig_type
            if siginfo.trig_type != sig_type: continue
            sig_nums.update({siginfo: str(sig_id)})
            if debug: print "This is signal #", sig_id
            sig_id += int(1)
            siginfo.print_diagnostics()
    
    if print_mapping:
        print "\n\nMapping: "
        for k in sig_nums.keys():
            print k.fn, ":", sig_nums[k]
    print "\n"
    
    n = lambda sig_num, x: 'h_sig%s_%s_%s'  % (sig_num, x, year) # Inherited code
    
    
    for sigfn in sig_nums.keys():
        if debug: print "Reporting sig", sigfn.fn
        
        sig_id = sig_nums[sigfn]

        sumw = 0.
        ngen = 0 # historical thing, not sure if useful
        t = ROOT.TChain('mfvMiniTree/t')
        t.Add(sigfn.full_fn)
        t.SetAlias('limitsinput_pass', limitsinput_expr) # historical thing

        sumw = sigfn.get_sumw()
        ngen = sigfn.get_ngen()
        if debug: print "SumW obtained:", sumw, ", NGen obtained:", ngen


        # Rescale signal
        xsec = sigfn.get_xsec()
        if debug: print "X-Sec:", xsec
        sigyield = xsec * sb_conf.template_norms["lumi"][year_id]

        scale = sigyield / sumw
        sig_scales.update({sigfn : scale})
        if debug: print "Will scale sumw", sumw, "to", sigyield
        

        new_sig_hs = []
        h_to_rescale = []
        
        ROOT.TH1.AddDirectory(1)
        h_sumdbv = ROOT.TH1D(n(sig_id, 'sumdbv'),  '', 800, 0, 8)
        h_sumdbv_nw = ROOT.TH1D(n(sig_id, 'sumdbv')+"_nw",  '', 800, 0, 8) # No-weight version
        if debug: print "Made histogram", n(sig_id,'sumdbv'), ",", n(sig_id, 'sumdbv')+"_nw"
        t.Draw('sumdbv>>%s' % n(sig_id, 'sumdbv'),  'weight*(limitsinput_pass && nvtx>=2)')
        t.Draw('sumdbv>>%s' % n(sig_id, 'sumdbv')+"_nw",  '1.0*(limitsinput_pass && nvtx>=2)')
        h_to_rescale.append(h_sumdbv)
        
        ROOT.TH1.AddDirectory(0)
        for h in h_to_rescale:
            h.SetDirectory(0)
            h.Scale(scale)
        h_sumdbv_nw.SetDirectory(0) # historical, idk what this does
            
        h_sig = h_sumdbv.Rebin(nbins, "sig"+year_tag+sig_id, bins)
        move_overflow_into_last_bin(h_sig)
        if debug: print "Made signal: ", h_sig.GetName()
        new_sig_hs.append(h_sig)

        h_sig_nw = h_sumdbv_nw.Rebin(nbins, n(sig_id, 'ngen_perbin'), bins)
        move_overflow_into_last_bin(h_sig_nw)
        new_sig_hs.append(h_sig_nw)

        h_sumw = ROOT.TH1D(n(sig_id, 'sumw'), '', 1,0,1)
        h_sumw.SetBinContent(1, sumw)
        new_sig_hs.append(h_sumw)


        f.cd()

        for h in new_sig_hs:
            h.SetTitle(sigfn.proc+"_"+year)
            h.Write()
            if debug: print "Wrote to file: ", h.GetName()
        if debug: print
        t.Reset()
        
    print "SIGNAL processing complete"
    return






def write_sig_updown(f, nuis_ls, siginfo, sig_scales, sig_id, **kwargs):
    """
    Given a list of nuisances and signal tag, write corresponding histograms for every shape nuisance (ignores non-shape nuisances).

    -INPUTS-
    f: ROOT file
    nuis_ls: list of Nuisance objects
    siginfo: SigInfo object
    sig_scales: mapping of SigInfo objects to scales (scale := MiniTree to signal model)
    sig_id: integer describing the signal
    #year: string, describing year number
    #year_tag: string/char, one digit describing the year (5 for 20161, etc)
    
    -OUTPUTS-
    f: will be written to
    """

    scale = sig_scales[siginfo]
    if debug: print "\nAll hists of", siginfo.fn, "to be scaled by", scale

    t = ROOT.TChain('mfvMiniTree/t')
    t.Add(siginfo.full_fn)
    t.SetAlias('limitsinput_pass', limitsinput_expr)
    if debug: print "Re-opened", siginfo.full_fn, "for Up/Down uncertainty generation\n"
    
    
    for nuis in nuis_ls:
        if nuis.make_updn == False: continue

        nname = nuis.nuis_name
        if nuis.sep_yrs==True: nn_yrtg = year_tag # In the datacard-writing phase, nuis_name will have year_tag appended to it if year-dependent
        else: nn_yrtg = ""

        hname_up = "sig"+year_tag+sig_id + "_"+nname+nn_yrtg+"Up"
        hname_dn = "sig"+year_tag+sig_id + "_"+nname+nn_yrtg+"Down"

        ROOT.TH1.AddDirectory(1)
        h_sumdbv_up = ROOT.TH1D(hname_up+"_orig", '', 800, 0, 8)
        h_sumdbv_dn = ROOT.TH1D(hname_dn+"_orig", '', 800, 0, 8)

        t.Draw('sumdbv>>%s' % hname_up+"_orig",  'weight*(limitsinput_pass && nvtx>=2)'.replace('weight', sb_conf.updn_wt_dict[nname][0]))
        t.Draw('sumdbv>>%s' % hname_dn+"_orig",  'weight*(limitsinput_pass && nvtx>=2)'.replace('weight', sb_conf.updn_wt_dict[nname][1]))
        

        ROOT.TH1.AddDirectory(0)
        h_sig_up = h_sumdbv_up.Rebin(nbins, hname_up, bins)
        h_sig_dn = h_sumdbv_dn.Rebin(nbins, hname_dn, bins)
        hs_updn = [h_sig_up, h_sig_dn]

        for h in hs_updn:
            h.Scale(scale)
            move_overflow_into_last_bin(h)
            h.SetDirectory(0)


        f.cd()
        for h in hs_updn:
            h.SetTitle(siginfo.proc+"_"+year)
            h.Write()
            if debug: print "Wrote to file: ", h.GetName()

        h_sumdbv_up = ROOT.TH1D() # wipe info
        h_sumdbv_dn = ROOT.TH1D()
        h_sig_up = ROOT.TH1D()
        h_sig_dn = ROOT.TH1D()

    t.Reset()
    return






def make():
    """
    The main executable.
    """
    if debug: print "Year is ", year, ", type ", sig_type
    
    out_loc = config.output["out_folder"] + config.output["out_fn"] +"_"+sig_type +"_"+year + ".ROOT"
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
    
    if debug: print "\nStarted writing SIGNAL"
    make_sigs(f=f, sig_nums=sig_nums, sig_scales=sig_scales)


    # Get bkg nuisances FIXME
    if debug: print "\nAdding BACKGROUND nuisances"
    nuis_bkg_ls = []
    getns.get_nuis_frombkg(nuis_bkg_ls, debug_mode=debug)
    if debug: print "Warning: up-down functionality for BKG not yet implemented"


    # Get Signal nuisances
    if debug: print "\nAdding SIGNAL nuisances"
    nuis_ls = []
    
    for siginfo in sig_nums.keys():
        nuis_ls = []
        getns.get_nuis_fromsig(siginfo, nuis_ls, debug_mode=debug)

        if debug: print "Writing Up and Down"
        write_sig_updown(f=f, nuis_ls=nuis_ls, siginfo=siginfo, sig_scales=sig_scales, sig_id=sig_nums[siginfo])

        if debug: print "Writing DATACARD"
        mkdat.make_datacard(f=f, nuis_ls=nuis_ls, nuis_bkg_ls=nuis_bkg_ls, siginfo=siginfo, sig_id=sig_nums[siginfo], debug_mode=debug)
    nuis_ls = []
    
    return




if __name__ == '__main__':
    check_config()
    make()
    
