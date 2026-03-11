from __future__ import division
from __future__ import absolute_import

import ROOT

import numpy as np

import script_configs as config
import nuisance_configs as ns_conf
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

year_to_tag = config.datacard["year_to_tag"]
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


def make_nuis_dcnm(nuis, siginfo, force_no_CADItag=False):
    """
    Given a nuisance, return the name/s it will show up as.
    -If analysis-specific, tag with CADI (unless forced not to)
    -If separate years, tag with year_tag
    -If separate bins (==corr/uncorr), tag b1, b2 etc
    """
    nuis_rootname = nuis.nuis_name
    if nuis.add_anaID==True and not(force_no_CADItag): nuis_rootname = ns_conf.nuis_names["CMS-CADI-tag"] + nuis_rootname
    if (nuis.sep_yrs or not(nuis.corr)) and not(force_no_CADItag): nuis_rootname = nuis_rootname + "_"
    if nuis.sep_yrs==True and not(force_no_CADItag): nuis_rootname += year_tag

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


def turn_info_to_line(ns_name, ns_type, strls, write_sig):
    """
    ns_name, ns_type: str
    strls: list of anything that becomes str
    write_sig: Boolean
    """
    if  (len(strls)!=nbins): raise Exception("Bad line input.")
    new_line = """
"""
    
    nuis_seg = ""
    dash = pad("-", 7, False)

    for i in range(nbins):
        if strls[i] == None: nuis_seg += dash
        else: nuis_seg += pad(str(strls[i]), 7, False)

    new_line += pad(ns_name, 30) + pad(ns_type, 5)
    if write_sig==True: new_line += nuis_seg + return_sep() + "DASH3"
    elif write_sig==False: new_line += "DASH3" + return_sep() + nuis_seg
    else: raise Exception("Specify whether to write signal or bkg")
    
    return new_line


def turn_info_to_nlines(ns_names, ns_type, strls, write_sig):
    """
    ns_names: list-like of str
    ns_type: str
    strls: list of anything that becomes str
    write_sig: Boolean
    """
    if (len(strls)!=nbins) or (len(ns_names)!=nbins): raise Exception("Bad line input.")
    new_lines = """"""
    
    for i in range(nbins):
        in_strls = []
        for j in range(nbins):
            if j!=i: in_strls.append(None)
            else: in_strls.append(strls[i])
        new_lines += turn_info_to_line(ns_names[i], ns_type, in_strls, write_sig)

    return new_lines


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
            if nuis.nuis_type=="special":
                if nuis.extra_info[0]=="updn_pair":
                    if nuis.extra_info[1]=="dn": continue # skip one of the pairs
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
        new_lines += turn_info_to_line(dc_name, "lnN", nuis.nuis_val, write_sig)

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
        new_lines += turn_info_to_nlines(dc_names, "lnN", nuis.nuis_val, write_sig)

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

        dc_name_for_h = make_nuis_dcnm(nuis, siginfo)
        dc_name = make_nuis_dcnm(nuis, siginfo)
        if write_sig: process_htag = sig_nm(sig_id).replace(" ","")
        else: process_htag = bkg_nm().replace(" ","")

        hname_up = process_htag + "_"+dc_name_for_h+"Up"
        hname_dn = process_htag + "_"+dc_name_for_h+"Down"

        h_central = f.Get(process_htag)
        h_shape_up = f.Get(hname_up)
        h_shape_dn = f.Get(hname_dn)
        #h_updn_ls = [h_shape_up, h_shape_dn]
        

        strls = []
        
        for i in range(nbins):
            try:
                strls.append(str(h_shape_dn.GetBinContent(i+1) / h_central.GetBinContent(i+1)) + "/" + str(h_shape_up.GetBinContent(i+1) / h_central.GetBinContent(i+1)))
            except:
                strls.append(str(1.0) + "/" + str(1.0))
                print "Warning: division by 0 encountered in up/down variations. Filling fake 1.0 values. Error in", siginfo.fn, "bin", i, "."

        new_lines += turn_info_to_line(dc_name, "lnN", strls, write_sig)

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

            sig_cts_hname = "h_"+"sig"+sig_id+"_ngen_perbin_"+year
            h_sig_cts = f.Get(sig_cts_hname)

            for i in range(nbins):
                strls = []
                for j in range(nbins):
                    if j!=i: strls.append(None)
                    else:
                        try:
                            strls.append(sig_norm_ls[j] / h_sig_cts.GetBinContent(j+1))
                        except:
                            print "Warning: division by 0 encountered in Gamma-N. Filling mean sumw as a placeholder. Error in", siginfo.fn, "bin", i, "."
                            if h_sig_cts.Integral()==0.0:
                                strls.append(0.0005)
                            else:
                                strls.append(sum(sig_norm_ls) / h_sig_cts.Integral())

                new_lines += turn_info_to_line(dc_names[i], "gmN "+pad(str(int(h_sig_cts.GetBinContent(i+1))),5), strls, write_sig)
            continue


        
        elif nuis.nuis_type == "special":

            if (nuis.extra_info[0]=="updn_pair"):
                if nuis.extra_info[1]=="up": #not processing down
                    pair_found = False
                    for n2 in ns_ls:
                        if (n2.nuis_name==nuis.nuis_name) and (n2.nuis_type==nuis.nuis_type):
                            if (n2.extra_info[1]=="dn"):
                                npair = n2
                                pair_found = True
                                break
                    if not(pair_found): raise Exception("The up-down pair marked UP has no corresponding pair")
                    dc_name = make_nuis_dcnm(nuis, siginfo)

                    strls = []
                    for i in range(nbins):
                        strls.append(str(n2.nuis_val[i]) + "/" + str(nuis.nuis_val[i]))
                    new_lines += turn_info_to_line(dc_name, "lnN", strls, write_sig)
                elif nuis.extra_info[1]!="dn": raise Exception("Bad extra_info field, use up or dn")
        
        
        
            if (nuis.extra_info[0]=="anti-lnN"):
                if (nuis.corr!=True): raise Exception("Anti-correlated lnN does not have un-correlated bins implemented")

                dc_name = make_nuis_dcnm(nuis, siginfo)

                strls = []
                for i in range(nbins):
                    strls.append(str(nuis.nuis_val[i]) + "/" + str(1/nuis.nuis_val[i]))

                new_lines += turn_info_to_line(dc_name, "lnN", strls, write_sig)


                
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


    #Tidy Template
    template = return_no_dashes(template)

    if debug_mode: print "Printing DATACARD:\n"
    if debug_mode: print template


    dc_dict = config.datacard_out_loc
    out_dc_fn = dc_dict["out_folder"] + dc_dict["out_fn_prefix"] + siginfo.trig_type + "_" + siginfo.return_nuis_key()
    if config.debug_settings["scale_bkg_fake"]: out_dc_fn += "_fakebkg"
    out_dc_fn += dc_dict["out_fn_suffix"]


    datacard = open(out_dc_fn, "w")
    if debug_mode: print "Writing datacard to:", out_dc_fn
    datacard.write(unicode(template))
    datacard.close()
    
    
    return

