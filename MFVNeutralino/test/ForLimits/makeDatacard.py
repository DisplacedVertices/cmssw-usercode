from __future__ import division
from __future__ import absolute_import

import ROOT

import numpy as np

import script_configs as config
import helper_PyStorage_objects as sth
from io import open

"""
Naming conventions (Note: apparently if I put template as an input, the function refuses to change template, idk why)
    return_XX : it will give something back, append to template
    add_XX: overwrite template with the return value
    replace_XX: like add
    write_XX: overwrite template (apparently this can't be done)

The only stuff that are hard-coded are:
-Sig and bkg are called 0 and 1
-Sig and bkg are written in this order
"""

# Hard codes
n_proc = 2


#Globals
year = config.datacard["year"]
year_id = config.datacard["year_key"].index(year) # This is like the "int i" describing the location
nbins = config.datacard["nbins"]
bins = np.array(config.datacard["bins"])
sig_type = config.sig["type"]

year_to_tag = {"20161": "5", "20162": "6", "2017": "7", "2018": "8"} # used when we e.g. call background bkg5 to bkg8
year_tag = year_to_tag[year]






# SHORT FUNCTIONS

def pad(some_str, n, align_left=True):
    """Pad any given string to n characters, if existing length <= n (does not truncate string). Also, it will always ensure there is an extra space to one side."""
    if len(some_str) >= n-1:
        if align_left: return some_str + " "
        else: return " " + some_str
    elif align_left: return some_str + (n-len(some_str)) * " "
    else: return (n-len(some_str)) * " " + some_str

sig_nm = lambda sig_id : "  "+"sig"+year_tag+sig_id # sig-name
bkg_nm = lambda : "   "+"bkg"+year_tag # bkg-name
b_nm = lambda bn : "    "+"b"+year_tag+bn # bin-name

def return_sep():
    return "        "


def make_nuis_dcnm(nuis, siginfo):
    """
    Given a nuisance, return the name/s it will show up as.
    -If separate years, tag with year_tag
    -If separate bins (==corr/uncorr), tag b1, b2 etc
    """
    nuis_rootname = nuis.nuis_name
    if nuis.sep_yrs==True: nuis_rootname += year_tag

    if nuis.corr==True:
        return nuis_rootname
    elif nuis.corr==False:
        nuis_bybin = []
        for i in range(nbins):
            nuis_bybin.append(nuis_rootname + "b" + str(int(i+1)))
        return nuis_bybin
    else: raise Exception ("Unable to interpret nuisance for name->datacard conversion, for", nuis.nuis_name)


def return_newline():
    return """
________
"""


def return_no_dashes(template):
    new_template = template
    for d in range(4): # Change as needed
        new_template = new_template.replace('DASH%i' % d, d * pad("-", 7, False))
    return new_template






# LONG FUNCTIONS

def add_ijkmax(template, nuis_ls, nuis_bkg_ls, siginfo):
    new_template = template + """
imax """ + str(nbins) + """
jmax """ + "1" + """
kmax """

    k_ct = 0

    for nuis in nuis_ls+nuis_bkg_ls:
        if nuis.corr==True: # I think code logic forces these to agree, but need to check
            k_ct += 1
        elif nuis.corr==False:
            k_ct += nbins
        else:
            print "Warning: unable to count k due to bad nuisance object:", nuis.nuis_name

    new_template += str(k_ct)
    
    return new_template






def add_observations(template, f, siginfo, sig_id):

    new_template = template + pad("bin", 12)
    for i in range(nbins):
        new_template += b_nm(str(i))

    new_template += """
""" + pad("observation", 12)
    h_obs = ROOT.TH1D(f.Get('h_observed_%s' % year))
    for i in range(nbins):
        new_template += pad( str(int(h_obs.GetBinContent(i+1))), 7, False)
    h_obs.Delete()
    
    return new_template






def add_central_vals(template, f, sig_norm_ls, siginfo, sig_id):
    """
    -INPUTS-
    sig_norm_ls: list (probably empty), will store extracted signal values for Gamma-N
    """

    new_template = template + pad("bin", 12)
    for j in range(n_proc): # Write signal and background
        for i in range(nbins):
            new_template += b_nm(str(i))
        if (j!=n_proc-1): new_template += return_sep()

    new_template += """
""" + pad("process", 12) + nbins * (sig_nm(sig_id)) + return_sep() + nbins * (bkg_nm())
    new_template += """
""" + pad("process", 12) + nbins * pad("0", 7, False) + return_sep() + nbins * pad("1", 7, False)

    h_sig = f.Get(sig_nm(sig_id).replace(" ",""))
    h_bkg = f.Get(bkg_nm().replace(" ",""))
    to_write = [h_sig, h_bkg]

    new_template += """
""" + pad("rate", 12)
    for j in range(n_proc):
        for i in range(nbins):
            new_template += pad(str(to_write[j].GetBinContent(i+1)), 3, False)
            if (j==0): sig_norm_ls.append(to_write[j].GetBinContent(i+1)) # signal vals are stored for gamma-N
        if (j!=n_proc-1): new_template += return_sep()

    h_sig.Delete()
    h_bkg.Delete()

    return new_template, sig_norm_ls






def return_lnN_corr(f, ns_ls, siginfo, write_sig):
    """
    -Inputs-
    write_sig: Boolean. If true, it will write the first set, else it writes the second set
    """
    new_lines = """"""
    
    for nuis in ns_ls:
        try:
            if nuis.nuis_type != "lnN": continue
            if nuis.corr != True: continue
        except:
            raise Exception("Failure: Nuisance object not complete")

        dc_name = make_nuis_dcnm(nuis, siginfo)
        nuis_segment = ""
        
        for i in range(nbins):
            nuis_segment += pad(str(nuis.nuis_val[i]), 7, False)

        new_lines += """
""" + pad(dc_name, 10) + pad("lnN", 4)
        
        if write_sig==True: new_lines += nuis_segment + return_sep() + "DASH3"
        elif write_sig==False: new_lines += "DASH3" + return_sep() + nuis_segment
        else: raise Exception("Specify whether to write sigal or bkg")

    new_lines += """
"""
    return new_lines






def return_lnN_uncorr(f, ns_ls, siginfo, write_sig):
    """
    -Inputs-
    write_sig: Boolean. If true, it will write the first set, else it writes the second set
    """
    new_lines = """"""
    
    for nuis in ns_ls:
        try:
            if nuis.nuis_type != "lnN": continue
            if nuis.corr != False: continue
        except:
            raise Exception("Failure: Nuisance object not complete")

        dc_names = make_nuis_dcnm(nuis, siginfo)
        dash = pad("-", 7, False)
        
        for i in range(nbins):
            new_lines += """
""" + pad(dc_names[i], 10) + pad("lnN", 4)
            
            nuis_segment = ""
            for j in range(nbins):
                if j!=i: nuis_segment += dash
                else: nuis_segment += pad(str(nuis.nuis_val[j]), 7, False)
            
            if write_sig==True: new_lines += nuis_segment + return_sep() + "DASH3"
            elif write_sig==False: new_lines += "DASH3" + return_sep() + nuis_segment
            else: raise Exception("Specify whether to write sigal or bkg")

    new_lines += """
"""
    return new_lines






def return_shape_lines(f, ns_ls, siginfo, sig_id, write_sig=True):
    """
    Searches for shape uncertainty ROOT histograms, and writes them out as text on the datacard
    
    -Inputs-
    write_sig: Boolean. If true, it will write the first set, else it writes the second set
    """
    new_lines = """"""
    
    for nuis in ns_ls:
        if nuis.nuis_type != "shape": continue

        dc_name = make_nuis_dcnm(nuis, siginfo)
        if write_sig: process_htag = sig_nm(sig_id).replace(" ","")
        else: process_htag = bkg_nm().replace(" ","")

        hname_up = process_htag + "_"+dc_name+"Up"
        hname_dn = process_htag + "_"+dc_name+"Down"

        h_central = f.Get(process_htag)
        h_shape_up = f.Get(hname_up)
        h_shape_dn = f.Get(hname_dn)
        #h_updn_ls = [h_shape_up, h_shape_dn]
        

        nuis_segment = ""
        
        for i in range(nbins):
            try:
                nuis_segment += str(h_shape_dn.GetBinContent(i+1) / h_central.GetBinContent(i+1)) + "/" + str(h_shape_up.GetBinContent(i+1) / h_central.GetBinContent(i+1))
            except:
                nuis_segment += str(1.0) + "/" + str(1.0)
                print "Warning: division by 0 encountered in up/down variations. Filling fake 1.0 values. Error in", siginfo.fn, "bin", i, "."
            if i!= nbins-1: nuis_segment += " "

        new_lines += """
""" + pad(dc_name, 10) + pad("lnN", 4)
        
        if write_sig==True: new_lines += nuis_segment + return_sep() + "DASH3"
        elif write_sig==False: new_lines += "DASH3" + return_sep() + nuis_segment
        else: raise Exception("Specify whether to write sigal or bkg")

    new_lines += """
"""
    return new_lines






def return_special_lines(f, ns_ls, sig_norm_ls, siginfo, sig_id, write_sig=True):
    """
    If the nuisance type is recorded as "special", this section will trigger. The triggering is extremely ad-hoc.
    
    -Inputs-
    sig_norm_ls: list of floats. This should have been extracted in the get-signal stage.
    write_sig: Boolean. If true, it will write the first set, else it writes the second set
    """
    new_lines = """"""
    
    for nuis in ns_ls:
        try:
            if nuis.nuis_type == "lnN": continue
            if nuis.nuis_type == "shape": continue
        except:
            raise Exception("Failure: Nuisance object not complete")



        if nuis.nuis_type == "GammaN":
            if write_sig==False: raise Exception("GammaN not implemented for background")

            dc_names = make_nuis_dcnm(nuis, siginfo)
            dash = pad("-", 7, False)

            sig_cts_hname = "h_"+"sig"+sig_id+"_ngen_perbin_"+year
            h_sig_cts = f.Get(sig_cts_hname)

            for i in range(nbins):
                new_lines += """
""" + pad(dc_names[i], 10) + pad("gmN", 4) + pad(str(int(h_sig_cts.GetBinContent(i+1))), 6)

                nuis_segment = ""
                for j in range(nbins):
                    if j!=i: nuis_segment += dash
                    else:
                        try:
                            nuis_segment += pad(str(sig_norm_ls[j] / h_sig_cts.GetBinContent(j+1)), 7, False)
                        except:
                            print "Warning: division by 0 encountered in Gamma-N. Filling mean sumw as a placeholder. Error in", siginfo.fn, "bin", i, "."
                            nuis_segment += pad(str(sum(sig_norm_ls) / h_sig_cts.Integral()), 7, False)

                new_lines += nuis_segment + return_sep() + "DASH3"
            continue


        
        elif nuis.nuis_type == "special":

            if (nuis.extra_info[0]=="anti-lnN"):
                if (nuis.corr!=True): raise Exception("Anti-correlated lnN does not have un-correlated bins implemented")

                dc_name = make_nuis_dcnm(nuis, siginfo)
                nuis_segment = ""
        
                for i in range(nbins):
                    nuis_segment += pad(str(nuis.nuis_val[i]) + "/" + str(1/nuis.nuis_val[i]), 7, False)
                
                new_lines += """
""" + pad(dc_name, 10) + pad("lnN", 4)
        
                if write_sig==True: new_lines += nuis_segment + return_sep() + "DASH3"
                elif write_sig==False: new_lines += "DASH3" + return_sep() + nuis_segment

                continue


                
        else:
            print "Warning: nuisance", nuis.nuis_name, "has not been interpreted as a datacard line"
            if write_sig: print "Generated when evaluating signal\n"
            else: print "Generated when evaluating background\n"
            continue

    new_lines += """
"""
    return new_lines






def make_datacard(f, nuis_ls, nuis_bkg_ls, siginfo, sig_id, debug_mode=False):
    """
    -INPUTS-
    nuis_ls: list of nuisance objects, for signal
    nuis_bkg_ls: list of nuisance objects, for background
    siginfo: SigInfo object storing information about signal MiniTree
    sig_id: string, the integer indexing the signal
    #year: string, 4-5 digit year
    #year_tag: string/char, represents the year
    debug_mode: Bool, whether to make debug statements
    """

    sig_name = "sig"+year_tag+sig_id
    if debug_mode: print "\nSearching for signal named", sig_name
    

    # INITIALIZATION
    template = """# sample id in ROOT file """ + sig_id + """
# filename = """ + siginfo.fn + """
# total sig rate = """ + """FIXME, not implemented"""

    template = add_ijkmax(template=template, nuis_ls=nuis_ls, nuis_bkg_ls=nuis_bkg_ls, siginfo=siginfo)
    template += return_newline()

    template = add_observations(template=template, f=f, siginfo=siginfo, sig_id=sig_id)
    template += return_newline()

    sig_norm_ls = [] # store signal norms, for Gamma-N
    template, sig_norm_ls = add_central_vals(template=template, f=f, sig_norm_ls=sig_norm_ls, siginfo=siginfo, sig_id=sig_id)
    template += return_newline()


    # Nuis SIGNAL
    template += return_lnN_corr(f=f, ns_ls=nuis_ls, siginfo=siginfo, write_sig=True)
    template += return_lnN_uncorr(f=f, ns_ls=nuis_ls, siginfo=siginfo, write_sig=True)

    template += return_shape_lines(f=f, ns_ls=nuis_ls, siginfo=siginfo, sig_id=sig_id, write_sig=True)
    template += return_special_lines(f=f, ns_ls=nuis_ls, sig_norm_ls=sig_norm_ls, siginfo=siginfo, sig_id=sig_id, write_sig=True)


    # Nuis BACKGROUND
    template += return_lnN_corr(f=f, ns_ls=nuis_bkg_ls, siginfo=siginfo, write_sig=False)
    template += return_lnN_uncorr(f=f, ns_ls=nuis_bkg_ls, siginfo=siginfo, write_sig=False)

    template += return_shape_lines(f=f, ns_ls=nuis_bkg_ls, siginfo=siginfo, sig_id=sig_id, write_sig=False)

    
    template = return_no_dashes(template)

    if debug_mode: print "Printing DATACARD:\n"
    if debug_mode: print template


    dc_dict = config.datacard_out_loc
    out_dc_fn = dc_dict["out_folder"] + dc_dict["out_fn_prefix"] + siginfo.return_nuis_key() + dc_dict["out_fn_suffix"]

    datacard = open(out_dc_fn, "w")
    if debug_mode: print "Writing datacard to:", out_dc_fn
    datacard.write(unicode(template))
    datacard.close()
    
    
    return

