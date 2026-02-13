from __future__ import with_statement
from __future__ import absolute_import

import ROOT
import numpy as np

import os
import pickle # save stuff

from JMTucker.Tools.Sample import MCSample, nevents_from_file
from JMTucker.Tools.ROOTTools import lerp, bilerp
import JMTucker.Tools.Samples as jmtsamples

import helper_ROOT_functions as ROOThelper
import script_configs as config
from io import open

"""
DEFINITION: SignalROOTInfo
-Store filename, extract information from filename

DEFINITION: NuisanceInfo
-Store information to write a nuisance parameter

DEFINITION: NuisanceTable
"""



class SignalROOTInfo(object):
    """
    Based on a ROOT MiniTree filename, extract information like process name, lifetime.
    -INPUTS-
    full_fn: full filename
    root_exists: Boolean. If True, it'll make an accompanying ROOT.TFile() and MCSample()
    """

    def __init__(self, full_fn, root_exists=False, nbins=3):
        self.full_fn = full_fn
        self.fn = os.path.basename(self.full_fn)

        success = False
        success = self.get_processtag() # I assume the filename makes sense iff processtag can be parsed
        if success:
            self.get_type()
            self.get_lifetime()
            self.get_mass()
            self.get_year()
        self.nbins = nbins

        self.root_exists = root_exists
        if root_exists:
            self.sample_file = ROOT.TFile.Open(self.full_fn)
            self.nevents = nevents_from_file(self.sample_file)
            self.mcsample = MCSample(self.return_nuis_key(), self.return_nuis_key(), self.nevents)
            print "DEBUG:", self.mcsample.name
            jmtsamples._set_signal_stuff(self.mcsample)
        return

    

    def get_processtag(self):
        """
        Get the process tag, e.g. mfv_stopdbardbar
        """
        name_start = self.fn.split("tau")[0]
        success = True
        if name_start == self.fn:
            print "Unable to extract signal process tag. Is the name of the form __tau__ ?"
            print "Error reported for ", self.full_fn
            success = False
        self.proc = name_start[:-1]
        return success
    

    
    def get_type(self):
        if self.proc in config.sig["bjet_sigs"]:
            self.trig_type = "bjet"
        elif self.proc in config.sig["lep_sigs"]:
            self.trig_type = "lep"
        else: print "Signal not found in either bjet or lep lists."
        return


    
    def get_lifetime(self):
        self.lifetime = self.fn.split("tau")[1].split("_")[0]
        return



    def get_mass(self):
        self.mass = self.fn.split("tau")[1].split("_")[1][1:]
        return



    def get_year(self):
        self.year = self.return_nuis_key().split("_")[-1]
        return



    def return_nuis_key(self):
        return self.fn.replace(".root", "").replace(".ROOT", "")



    def return_lifetime_in_unit(self, unit=None):
        """Returns original string if unit=None, else converts into whatever unit is inputted"""
        if unit==None:
            return self.lifetime

        result = ROOThelper.convert_units(to_unit=unit, from_expr=self.lifetime)
        return result



    def return_mass_as_int(self):
        return int(self.mass)



    def return_name2details(self, lifetime_unit="mm"):
        """This function is constructed to resemble name2details of the old code"""
        return [self.proc, self.return_lifetime_in_unit(unit=lifetime_unit), self.mass, self.year]

    

    def print_diagnostics(self, lifetime_unit="mm"):
        print "Full filename:", self.full_fn
        print "Trigger type:", self.trig_type
        print "Process, lifetime, mass, year", self.return_name2details(lifetime_unit=lifetime_unit)
        return

    

    def get_sumw(self):
        if self.root_exists: return self.mcsample.sumw(self.sample_file)
        else: raise NotImplementedError()
        return
    
    def get_ngen(self):
        if self.root_exists: return self.nevents
        else: raise NotImplementedError()
        return
    
    def get_xsec(self):
        if self.root_exists: return self.mcsample.xsec
        else: raise NotImplementedError()
        return

    def get_filteff(self):
        if self.root_exists: return self.mcsample.filt_eff
        else: raise NotImplementedError()
        return






class NuisanceInfo(object):
    """
    Object to store information to make a nuisance parameter. This object was defined assuming log-normal parameters, but it can be adjusted to non-log-normal parameters.

    The convention is to store e.g. 1.01 (NOT 0.01) if some fluctuation is ~1%.

    -INPUTS-
    nuis_name: string.
    nuis_val: int or arr-like. Note this is meaningless if type is shape, but provide something anyway otherwise it'll crash.
    make_updn: Boolean. Will this make a shape uncertainty?
    sep_yrs: Boolean. If true, the nuis_name will be tagged with year number, e.g. lepSF -> lepSF8 (prevents ROOT chaining unrelated nuisances together)
    -Optional Inputs-
    corr: Boolean. Will this nuisance produce one line on the datacard, or more than one? If non-correlated, it will produce nuisb1, nuisb2 (or nuis7b1) etc
    nuis_type: string. If make_updn is True, it MUST be "shape".
    nbins: int
    extra_info: list

    -Other Things Stored-
    """

    
    def __init__(self, nuis_name, nuis_val, make_updn, sep_yrs, corr, nuis_type="lnN", nbins=3, extra_info=[]):
        """
        It will always expand one entry into an array of size nbins. If you don't want this behavior, give it e.g. [1, 1.05, 1] so some bins don't fluctuate.
        """
        
        try:
            test = float(nuis_val[0])
            self.nuis_val = np.array(nuis_val)
        except:
            try:
                self.nuis_val = float(nuis_val) * np.ones(nbins)
            except:
                raise Exception ("Unable to parse nuis_val")
        if sum(self.nuis_val<0)>0: raise Exception ("Nuisance must be >=0. Also remember 1 (not 0) is the central value")

        if (make_updn==True and nuis_type!="shape") or (make_updn!=True and nuis_type=="shape"):
            raise Exception("If make_updn is True, nuis_type must be shape (and vice versa)")
        if (nuis_type=="shape"):
            corr = True # This becomes one line on the datacard, not N lines
        if (nuis_type=="GammaN" and corr==True):
            print "Warning: The following pipeline is written assuming GammaN has corr=False. Please double-check the input"
        
        self.nuis_name = nuis_name
        self.make_updn = bool(make_updn)
        self.sep_yrs = sep_yrs
        self.corr = corr
        self.nuis_type = nuis_type
        self.nbins = int(nbins)
        self.extra_info = extra_info

        if corr==False:
            if len(self.nuis_val) != nbins: raise Exception("Length of array must equal nbins")
        return


    
    def print_diagnostics(self):
        if self.extra_info != []:
            print "Nuisance name", self.nuis_name, "   Is shape?", self.make_updn, "   Year-Sep", self.sep_yrs, "   Correlation", self.corr, "   Contents", self.nuis_val, "   Type", self.nuis_type, "   Bins", self.nbins, "   Notes:", self.extra_info
            return
        
        print "Nuisance name", self.nuis_name, "   Is shape?", self.make_updn, "   Year-Sep", self.sep_yrs, "   Correlation", self.corr, "   Contents", self.nuis_val, "   Type", self.nuis_type, "   Bins", self.nbins
        return






class NuisanceTable(object):
    """
    Make and query a table of nuisances.
    
    -STORAGE-
    Nuisance grid: Indexed by year (string). The values are ALWAYS interpreted as fractions (not percent).
    """

    def __init__(self, proc="", x_vals=None, x_unit=None, y_vals=None, y_unit=None, as_percent=None, years=set(["20161", "20162", "2017", "2018"]), pickle_loc=None, make_pickle_fn=True):
        """
        -INPUTS-
        as_percent: Boolean. If True, input 10 -> store 0.1. If False, stores exactly the input. The value stored is always interpreted as a FRACTION.
        years: array-like, must be strings
        pickle_loc: if not None, it will un-pickle the specified dictionary, and construct itself.
        make_pickle_fn: if True, it will add pickle_loc + "_" + proc + ".pkl"
        """
        if pickle_loc is None:
            if (proc==None or x_vals==None or x_unit==None or y_vals==None or y_unit==None or as_percent==None): raise Exception("Missing inputs")
            self.nuis_dict = {}
            try:
                self.nuis_dict.update({
                    "proc" : str(proc),
                    "x_vals" : np.sort(np.array(x_vals, dtype=float)),
                    "y_vals" : np.sort(np.array(y_vals, dtype=float)),
                    "x_unit" : str(x_unit),
                    "y_unit" : str(y_unit),
                    "perc" : as_percent,
                    "years": years,
                })
            except:
                raise Exception("Error: input cannot be converted into arrays/strings")
            self.proc = str(proc)
            self.perc = as_percent
        
            for y in years:
                initial_arr = np.ones((len(self.nuis_dict["x_vals"]), len(self.nuis_dict["y_vals"])))
                initial_arr.fill(np.nan)
                self.nuis_dict.update({y : initial_arr})
            return


        else:
            pickle_loc_tosearch = pickle_loc
            if make_pickle_fn:
                pickle_loc_tosearch += "_"+proc+".pkl"
            
            with open(pickle_loc_tosearch, 'rb') as file:
                use_dict = pickle.load(file)
            self.nuis_dict = use_dict
            self.proc = self.nuis_dict["proc"]
            self.perc = self.nuis_dict["perc"]



    def add_entry(self, proc, x_val, y_val, year, val, x_unit=None, y_unit=None, debug_mode=False):
        """
        Write one entry in the table. This is the most fundamental function for entry-adding.
        
        -INPUTS-
        proc: string
        x_val: float or int
        y_val: float or int
        year: string
        x_unit, y_unit: string. If None, assumes is dictionary unit
        """
        if (proc!=self.proc): return # ignore everything not matching this process
        if year not in self.nuis_dict["years"]: raise Exception("Queried year", year, "not in entries")

        if x_unit is not None: tau = ROOThelper.convert_units(to_unit=self.nuis_dict["x_unit"], from_num=x_val, from_unit=x_unit)
        else: tau = x_val
        if y_unit is not None: mass = ROOThelper.convert_units(to_unit=self.nuis_dict["y_unit"], from_num=y_val, from_unit=y_unit)
        else: mass = y_val
        x_ind = np.where(self.nuis_dict["x_vals"]==tau)[0][0]
        y_ind = np.where(self.nuis_dict["y_vals"]==float(mass))[0][0]

        if (self.perc): to_fill = val * 0.01
        else: to_fill = val

        self.nuis_dict[year][x_ind, y_ind] = to_fill
        if debug_mode: print "Filled", x_ind, ",", y_ind, "of", year
        return



    def add_entry_from_fn(self, file_info, val, debug_mode=False):
        """
        file_info: string or SigInfo object (will auto-convert)
        """
        try: # Take a string or SigInfo object
            new_sig = SignalROOTInfo(file_info)
        except:
            new_sig = file_info # Always a SigInfo object
        proc, tau, mass, yr = new_sig.return_name2details(lifetime_unit=self.nuis_dict["x_unit"])

        self.add_entry(proc=proc, x_val=tau, y_val=mass, year=yr, val=val, debug_mode=debug_mode)
        return



    def add_dictionary(self, in_dict, debug_mode=False):
        """Given an existing dictionary (pairs: file-like; value), read every entry and put it into storage"""
        for k in in_dict.keys():
            self.add_entry_from_fn(k, in_dict[k], debug_mode=debug_mode)
        return



    def add_array(self, proc, x_vals, y_vals, year, val_arr, x_unit=None, y_unit=None, debug_mode=False):
        """Given an existing array, write the array"""
        if len(x_vals)!=len(self.nuis_dict["x_vals"]) or len(y_vals)!=len(self.nuis_dict["y_vals"]): raise Exception("Input array dimensions incompatible.")
        val_arr = np.array(val_arr)
        if val_arr.shape != self.nuis_dict[year].shape: raise Exception("Bad array dimensions, or wrong year.")

        for i in xrange(len(x_vals)):
            for j in xrange(len(y_vals)):
                self.add_entry(proc, x_vals[i], y_vals[j], year, val_arr[i,j], x_unit=x_unit, y_unit=y_unit, debug_mode=debug_mode)
        
        return



    def get_point(self, year, x_val, y_val, x_unit=None, y_unit=None, use_log=True, debug_mode=False):
        """
        Get nuisance value at a given tau-mass (x-y) parameter. Code will interpolate, if necessary. Currently rejects attempts to extrapolate.
        
        year: string, must be dictionary key
        x_unit, y_unit: if None, will be dictionary default
        use_log: if True, will interpolate in log-space
        """
        if year not in self.nuis_dict["years"]: raise Exception(year, "not in list of years.")

        if x_unit==None: x_unit=self.nuis_dict["x_unit"]
        if y_unit==None: y_unit=self.nuis_dict["y_unit"]
        x_val, y_val = float(x_val), float(y_val)
        
        xy_vals, xy_units, dict_unit_k, dict_vals_k = [x_val, y_val], [x_unit, y_unit], ["x_unit", "y_unit"], ["x_vals", "y_vals"]
        s_ind = [] # x and y, search-indices
        vsu_ls = [] # Values in storage unit
        
        for i in xrange(len(xy_vals)):
            su = self.nuis_dict[dict_unit_k[i]] # stored unit, x- or y- (e.g. "mm" or "GeV")
            ua = self.nuis_dict[dict_vals_k[i]] # unit-array corresponding to su
            vsu = 0.0 # Used to be val_in_storage_unit
            vsu = ROOThelper.convert_units(su, from_num=xy_vals[i], from_unit=xy_units[i])
            vsu_ls.append(vsu)
            
            if vsu in ua:
                s_ind.append([np.where(ua==vsu)[0][0]])
            else:
                if vsu < ua[0] or vsu > ua[-1]:
                    print "Warning: requested", vsu, su, "is outside the storage grid."
                    print "Extrapolation from 2D array not implemented. Ending function."
                    return
                low_ele = np.where(ua<vsu)[0][-1] #Which indices to check
                upp_ele = np.where(ua>vsu)[0][0]
                s_ind.append([low_ele, upp_ele])
        if debug_mode: print "Searching coordinates:", s_ind, "corresponding to", vsu_ls, "(in same units as grid)"


        interp_q = 0.0

        if len(s_ind[0])==1 and len(s_ind[1])==1:
            interp_q = self.nuis_dict[year][s_ind[0][0], s_ind[1][0]]
            if debug_mode: print "Extracted", interp_q

            
        elif len(s_ind[0])==1 and len(s_ind[1])!=1:
            if use_log: y, y0, y1 = np.log([vsu_ls[1], self.nuis_dict["y_vals"][s_ind[1][0]], self.nuis_dict["y_vals"][s_ind[1][1]]])
            else: y, y0, y1 = vsu_ls[1], self.nuis_dict["y_vals"][s_ind[1][0]], self.nuis_dict["y_vals"][s_ind[1][1]]
            q0, q1 = self.nuis_dict[year][s_ind[0][0], s_ind[1][0]], self.nuis_dict[year][s_ind[0][0], s_ind[1][1]]
            
            interp_q = lerp(y, y0, y1, q0, q1)
            if debug_mode: print "Interpolated y-axis", y0, y1, "with nuis", q0, q1, "to get y=", y, "as", interp_q

        elif len(s_ind[0])!=1 and len(s_ind[1])==1:
            if use_log: x, x0, x1 = np.log([vsu_ls[0], self.nuis_dict["x_vals"][s_ind[0][0]], self.nuis_dict["x_vals"][s_ind[0][1]]])
            else: x, x0, x1 = vsu_ls[0], self.nuis_dict["x_vals"][s_ind[0][0]], self.nuis_dict["x_vals"][s_ind[0][1]]
            q0, q1 = self.nuis_dict[year][s_ind[0][0], s_ind[1][0]], self.nuis_dict[year][s_ind[0][1], s_ind[1][0]]
            
            interp_q = lerp(x, x0, x1, q0, q1)
            if debug_mode: print "Interpolated x-axis", x0, x1, "with nuis", q0, q1, "to get x=", x, "as", interp_q

        
        elif len(s_ind[0])!=1 and len(s_ind[1])!=1:
            if use_log: # 0-1 and 1-2 convention matches JMTucker
                x, x1, x2 = np.log([vsu_ls[0], self.nuis_dict["x_vals"][s_ind[0][0]], self.nuis_dict["x_vals"][s_ind[0][1]]])
                y, y1, y2 = np.log([vsu_ls[1], self.nuis_dict["y_vals"][s_ind[1][0]], self.nuis_dict["y_vals"][s_ind[1][1]]])
            else:
                x, x1, x2 = vsu_ls[0], self.nuis_dict["x_vals"][s_ind[0][0]], self.nuis_dict["x_vals"][s_ind[0][1]]
                y, y1, y2 = vsu_ls[1], self.nuis_dict["y_vals"][s_ind[1][0]], self.nuis_dict["y_vals"][s_ind[1][1]]

            q11, q12, q21, q22 = [
                self.nuis_dict[year][s_ind[0][0], s_ind[1][0]],
                self.nuis_dict[year][s_ind[0][0], s_ind[1][1]],
                self.nuis_dict[year][s_ind[0][1], s_ind[1][0]],
                self.nuis_dict[year][s_ind[0][1], s_ind[1][1]]
            ]
            points = [(x1, y1, q11), (x1, y2, q12), (x2, y1, q21), (x2, y2, q22)]

            interp_q = bilerp(x, y, points)
            if debug_mode: print "Interpolated nuis", interp_q, "from nuis", [q11, q12, q21, q22], "at x's", [x1, x2], "and y's", [y1,y2]

        else:
            raise Exception("Error: coordinate list is not 1x1-2x2")


        if not np.isfinite(interp_q):
            print "Warning: unable to interpolate, likely missing grid value. Exiting code."
            return
        return interp_q



    def get_point_from_fn(self, file_info, overrides=None, use_log=True, debug_mode=False):
        """
        Gets point corresponding to a filename

        -INPUTS-
        override: dictionary (str; str). Only "yr" implemented (because year naming conventions are a mess)
        """
        try:
            new_sig = SignalROOTInfo(file_info)
        except:
            new_sig = file_info
        proc, tau, mass, yr = new_sig.return_name2details(lifetime_unit=self.nuis_dict["x_unit"])
        if proc!=self.proc: return

        if overrides is not None:
            for k in overrides.keys():
                if k=="yr": yr=overrides[k]

        interp_q = self.get_point(yr, tau, mass, use_log=use_log, debug_mode=debug_mode)
        return interp_q



    def print_diagnostics(self):
        print self.nuis_dict
        return



    def save_pickle(self, to_fn_prefix, tag_proc=True, to_fn_suffix=".pkl", debug_mode=False):
        """
        Object will pickle its dictionary component (didn't implement pickling the whole thing), so it can be re-read later.

        -INPUTS-
        tag_proc: if True, the output will be to_fn_prefix + _ + [process name] + suffix
        """
        out_fn = to_fn_prefix
        if tag_proc: out_fn += "_" + self.proc
        out_fn += to_fn_suffix

        with open(out_fn, 'wb') as file:
            pickle.dump(self.nuis_dict, file)
        if debug_mode: print "Saved pickle:", out_fn
        return



    def pretty_print_diagnostics(self):
        """Print the dictionary really nicely. This is heritage code (I thought I had to express the dictionary as text) and is NOT useful."""
        str_out = str(self.nuis_dict).replace(", '", """,
    '""")
        # Except this breaks when printing the years. Fix below
        temp_yr_dict = {"years": self.nuis_dict["years"]}
        str_yr_replace = str(temp_yr_dict)[1:-1]
        str_out = str_out.replace(str_yr_replace.replace(", '", """,
    '"""), str_yr_replace)
        return str_out






def collect_xyvals_from_namearr(p, fns, x_unit, y_unit, debug_mode=False, **kwargs):
    """
    There is currently nothing to collect signal names. Please put it in by hand.

    -INPUTS-
    p: string. The target process to collect information for
    fns: arr- or set-like. List of filenames that can be parsed into a SigInfo
    x-, y-unit: string
    """
    x_vals = []
    y_vals = []

    for k in fns:
        new_sig = SignalROOTInfo(k, **kwargs)
        proc, tau, mass, temp = new_sig.return_name2details(lifetime_unit=x_unit)
        if (proc!=p): continue
        
        vals_check = [tau, mass]
        ls_check = [x_vals, y_vals]
        for i in xrange(len(vals_check)):
            if vals_check[i] not in ls_check[i]:
                ls_check[i].append(vals_check[i])

    x_vals.sort()
    y_vals.sort()

    if debug_mode:
        print "Identified x-s:", x_vals, "in", x_unit
        print "Identified y-s:", y_vals

    return x_vals, y_vals

            
