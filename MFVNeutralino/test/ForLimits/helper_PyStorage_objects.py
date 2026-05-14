import ROOT
import numpy as np
import os
import pickle

import JMTucker.Tools.Samples as Samples
from JMTucker.Tools.Sample import MCSample, nevents_from_file
from JMTucker.Tools.ROOTTools import lerp, bilerp

import helper_ROOT_functions as ROOThelper
import script_configs as config
import sig_and_bkg_configs as sb_conf

nbins   = config.datacard["nbins"]
prt_dt  = sb_conf.printout_flags["PyStorage"]


class SignalROOTInfo(object):
    """Extract process name, lifetime, mass, year from a MiniTree filename."""

    def __init__(self, full_fn, root_exists=False, nbins=3):
        self.full_fn = full_fn
        bn = os.path.basename(full_fn)
        if bn.startswith("minitree"):
            # File lives inside condor_<samplename>/ -- use the directory name for parsing
            dirn = os.path.basename(os.path.dirname(full_fn))
            self.fn = dirn.replace("condor_", "", 1) + ".root"
        else:
            self.fn = bn

        success = self.get_processtag()
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
            try:
                self.mcsample = eval("Samples." + self.return_nuis_key())
                Samples._set_signal_stuff(self.mcsample)
            except Exception:
                raise ValueError("No Samples.py entry")

    def get_processtag(self):
        name_start = self.fn.split("tau")[0]
        success = True
        if name_start == self.fn:
            print("Unable to extract signal process tag. Is the name of the form __tau__ ?")
            print("Error reported for", self.full_fn)
            success = False
        self.proc = name_start[:-1]
        return success

    def get_type(self):
        if (self.proc in config.sig["bjet_sigs"]) and (self.proc in config.sig["lep_sigs"]):
            if prt_dt["sig_type_conflict"]:
                print("Note: this signal can be bjet or lep. Setting to match script_config.")
            self.trig_type = config.sig["type"]
        elif self.proc in config.sig["bjet_sigs"]:
            self.trig_type = "bjet"
        elif self.proc in config.sig["lep_sigs"]:
            self.trig_type = "lep"
        else:
            print("Signal " + self.fn + " not found in either bjet or lep lists.")
            self.trig_type = "none"

    def get_lifetime(self):
        self.lifetime = self.fn.split("tau")[1].split("_")[0]

    def get_mass(self):
        self.mass = self.fn.split("tau")[1].split("_")[1][1:]

    def get_year(self):
        self.year = self.return_nuis_key().split("_")[-1]

    def return_nuis_key(self):
        return self.fn.replace(".root", "").replace(".ROOT", "")

    def return_lifetime_in_unit(self, unit=None):
        if unit is None:
            return self.lifetime
        return ROOThelper.convert_units(to_unit=unit, from_expr=self.lifetime)

    def return_mass_as_int(self):
        return int(self.mass)

    def return_name2details(self, lifetime_unit="mm"):
        return [self.proc, self.return_lifetime_in_unit(unit=lifetime_unit), self.mass, self.year]

    def print_diagnostics(self, lifetime_unit="mm"):
        print("Full filename:", self.full_fn)
        print("Trigger type:", self.trig_type)
        print("Process, lifetime, mass, year", self.return_name2details(lifetime_unit=lifetime_unit))

    def get_sumw(self):
        if self.root_exists:
            return self.mcsample.sumw(self.sample_file)
        raise NotImplementedError()

    def get_ngen(self):
        if self.root_exists:
            return self.nevents
        raise NotImplementedError()

    def get_xsec(self):
        if self.root_exists:
            return self.mcsample.xsec
        raise NotImplementedError()


class SigRInf_Grp(object):
    """Group of SignalROOTInfo objects that behave as one (e.g., VH = ZH + WH+ + WH-)."""

    def __init__(self, full_fn_ls, root_exists=False, nbins=3, overwrite_proc=None):
        assert len(full_fn_ls) > 0
        self.sig_ls = [SignalROOTInfo(fn, root_exists=root_exists, nbins=nbins)
                       for fn in full_fn_ls]

        self.proc = overwrite_proc if overwrite_proc is not None else self.sig_ls[0].proc

        for s in self.sig_ls:
            assert s.trig_type == self.trig_type

        for item in ("fn", "full_fn"):
            old_val = getattr(self.sig_ls[0], item)
            setattr(self, item, old_val.replace(self.sig_ls[0].proc, self.proc))

    def return_nuis_key(self):
        return self.sig_ls[0].return_nuis_key().replace(self.sig_ls[0].proc, self.proc)

    def return_name2details(self, lifetime_unit="mm"):
        ls = self.sig_ls[0].return_name2details(lifetime_unit=lifetime_unit)
        ls[0] = ls[0].replace(self.sig_ls[0].proc, self.proc)
        return ls

    def print_diagnostics(self, lifetime_unit="mm"):
        if len(self.sig_ls) > 1:
            print("Overriding process name:", self.proc)
        for s in self.sig_ls:
            s.print_diagnostics(lifetime_unit=lifetime_unit)

    def get_sumw(self):
        return sum(s.get_sumw() for s in self.sig_ls)

    def get_ngen(self):
        return sum(s.get_ngen() for s in self.sig_ls)

    def get_xsec(self):
        return sum(s.get_xsec() for s in self.sig_ls)

    def __getattr__(self, name):
        """Delegate unknown attributes to the first list item."""
        if name in {}:
            return
        result = getattr(self.sig_ls[0], name)
        if isinstance(result, str):
            result = result.replace(self.sig_ls[0].proc, self.proc)
        return result


class NuisanceInfo(object):
    """Store information for one nuisance parameter line on a combine datacard.

    Convention: store e.g. 1.01 (not 0.01) for a ~1% fluctuation.
    """

    def __init__(self, nuis_name, nuis_val, make_updn, sep_yrs, corr,
                 nuis_type="lnN", nbins=3, ana_spec=False, add_era_tags=True, extra_info=None):
        if extra_info is None:
            extra_info = []

        try:
            test = float(nuis_val[0])
            self.nuis_val = np.array(nuis_val, dtype=float)
        except Exception:
            try:
                self.nuis_val = float(nuis_val) * np.ones(nbins)
            except Exception:
                raise Exception("Unable to parse nuis_val")

        # Resize nuis_val to match nbins when the array length doesn't match.
        # Shorter: pad with 1.0 (no effect) -- happens when nuisance tables
        #          were built for fewer bins than the current scheme.
        # Longer:  truncate -- happens when a hardcoded per-bin array (e.g.
        #          pileup [1.03, 1.04, 1.06]) is used with a coarser binning.
        if len(self.nuis_val) != nbins:
            if len(self.nuis_val) < nbins:
                self.nuis_val = np.concatenate(
                    [self.nuis_val, np.ones(nbins - len(self.nuis_val))])
            else:
                self.nuis_val = self.nuis_val[:nbins]

        if np.any(self.nuis_val < 0):
            raise Exception("Nuisance must be >=0. Also remember 1 (not 0) is the central value")

        if (make_updn is True and nuis_type != "shape") or (make_updn is not True and nuis_type == "shape"):
            raise Exception("If make_updn is True, nuis_type must be shape (and vice versa)")
        if nuis_type == "shape":
            if corr is False:
                raise Exception("Shape uncertainties should be initiated as bin-correlated")
            corr = True
        if nuis_type == "GammaN" and corr is True:
            print("Warning: GammaN pipeline assumes corr=False. Please double-check the input")

        self.nuis_name    = nuis_name
        self.make_updn    = bool(make_updn)
        self.sep_yrs      = sep_yrs
        self.corr         = corr
        self.nuis_type    = nuis_type
        self.nbins        = int(nbins)
        self.add_anaID    = ana_spec
        self.add_era_tags = add_era_tags
        self.extra_info   = extra_info

        if corr is False:
            if len(self.nuis_val) != nbins:
                raise Exception("Length of array must equal nbins")

    def print_diagnostics(self):
        msg = ("Nuisance name %s   Is shape? %s   Year-Sep %s   Correlation %s"
               "   Contents %s   Type %s   Bins %s" % (
                   self.nuis_name, self.make_updn, self.sep_yrs, self.corr,
                   self.nuis_val, self.nuis_type, self.nbins))
        if self.extra_info:
            msg += "   Notes: %s" % self.extra_info
        print(msg)


class NuisanceTable(object):
    """2-D (lifetime x mass) nuisance table with bilinear interpolation.

    Values are always stored as fractions (not percent); set as_percent=True
    if the input data is in percent.
    """

    def __init__(self, proc="", x_vals=None, x_unit=None, y_vals=None, y_unit=None,
                 as_percent=None,
                 years=None,
                 nbin_len=False, dtype=float, pickle_loc=None,
                 make_pickle_fn=True, trig_for_pickle=None):
        if years is None:
            years = set(["20161", "20162", "2017", "2018"])

        if pickle_loc is None:
            if any(v is None for v in [proc, x_vals, x_unit, y_vals, y_unit, as_percent]):
                raise Exception("Missing inputs")
            self.arr_len = nbins if nbin_len else 0
            self.nuis_dict = {}
            try:
                self.nuis_dict.update({
                    "proc":     str(proc),
                    "x_vals":   np.sort(np.array(x_vals, dtype=float)),
                    "y_vals":   np.sort(np.array(y_vals, dtype=float)),
                    "x_unit":   str(x_unit),
                    "y_unit":   str(y_unit),
                    "perc":     as_percent,
                    "years":    years,
                    "arr_len":  self.arr_len,
                    "dtype":    dtype,
                })
            except Exception:
                raise Exception("Error: input cannot be converted into arrays/strings")
            self.proc = str(proc)
            self.perc = as_percent

            for y in years:
                if self.arr_len == 0:
                    arr = np.empty((len(self.nuis_dict["x_vals"]), len(self.nuis_dict["y_vals"])), dtype=dtype)
                else:
                    arr = np.empty((len(self.nuis_dict["x_vals"]), len(self.nuis_dict["y_vals"]), self.arr_len), dtype=dtype)
                arr.fill(np.nan)
                self.nuis_dict[y] = arr
        else:
            pickle_loc_tosearch = pickle_loc
            try:
                if make_pickle_fn:
                    pickle_loc_tosearch += "_" + proc + ".pkl"
                with open(pickle_loc_tosearch, "rb") as fh:
                    use_dict = pickle.load(fh)
            except Exception:
                could_find = False
                for alias in config.sig["aliases"][trig_for_pickle][proc]:
                    try:
                        pickle_loc_tosearch = pickle_loc
                        if make_pickle_fn:
                            pickle_loc_tosearch += "_" + alias + ".pkl"
                        with open(pickle_loc_tosearch, "rb") as fh:
                            use_dict = pickle.load(fh)
                        could_find = True
                        print("Warning: redirected pickle name to " + alias)
                        break
                    except Exception:
                        pass
                if not could_find:
                    raise Exception("Did not find any valid pickle to read, for " + proc)

            self.nuis_dict = use_dict
            self.proc      = self.nuis_dict["proc"]
            self.perc      = self.nuis_dict["perc"]
            self.arr_len   = self.nuis_dict["arr_len"]

    def add_entry(self, proc, x_val, y_val, year, val, x_unit=None, y_unit=None, debug_mode=False):
        if proc != self.proc:
            return
        if year not in self.nuis_dict["years"]:
            raise Exception("Queried year %s not in entries" % year)

        tau  = x_val if x_unit is None else ROOThelper.convert_units(to_unit=self.nuis_dict["x_unit"], from_num=x_val, from_unit=x_unit)
        mass = y_val if y_unit is None else ROOThelper.convert_units(to_unit=self.nuis_dict["y_unit"], from_num=y_val, from_unit=y_unit)

        x_ind = np.where(self.nuis_dict["x_vals"] == tau)[0][0]
        y_ind = np.where(self.nuis_dict["y_vals"] == float(mass))[0][0]

        to_fill = val * 0.01 if self.perc else val
        if np.prod(np.isfinite(self.nuis_dict[year][x_ind, y_ind])):
            raise Exception("Overwriting non-nan value")
        self.nuis_dict[year][x_ind, y_ind] = to_fill
        if debug_mode:
            print("Filled", x_ind, ",", y_ind, "of", year)

    def add_entry_from_fn(self, file_info, val, debug_mode=False):
        try:
            new_sig = SignalROOTInfo(file_info)
        except Exception:
            new_sig = file_info
        proc, tau, mass, yr = new_sig.return_name2details(lifetime_unit=self.nuis_dict["x_unit"])
        self.add_entry(proc=proc, x_val=tau, y_val=mass, year=yr, val=val, debug_mode=debug_mode)

    def add_dictionary(self, in_dict, debug_mode=False):
        for k in in_dict.keys():
            self.add_entry_from_fn(k, in_dict[k], debug_mode=debug_mode)

    def add_array(self, proc, x_vals, y_vals, year, val_arr, x_unit=None, y_unit=None, debug_mode=False):
        if len(x_vals) != len(self.nuis_dict["x_vals"]) or len(y_vals) != len(self.nuis_dict["y_vals"]):
            raise Exception("Input array dimensions incompatible.")
        val_arr = np.array(val_arr)
        if val_arr.shape != self.nuis_dict[year].shape:
            raise Exception("Bad array dimensions, or wrong year.")
        for i in xrange(len(x_vals)):
            for j in xrange(len(y_vals)):
                self.add_entry(proc, x_vals[i], y_vals[j], year, val_arr[i, j],
                               x_unit=x_unit, y_unit=y_unit, debug_mode=debug_mode)

    def get_point(self, year, x_val, y_val, x_unit=None, y_unit=None, use_log=False, debug_mode=False):
        """Interpolate the table at (x_val, y_val). Returns None if outside grid."""
        if year not in self.nuis_dict["years"]:
            raise Exception("%s not in list of years." % year)

        if x_unit is None:
            x_unit = self.nuis_dict["x_unit"]
        if y_unit is None:
            y_unit = self.nuis_dict["y_unit"]
        x_val, y_val = float(x_val), float(y_val)

        xy_vals   = [x_val, y_val]
        xy_units  = [x_unit, y_unit]
        dict_unit_k = ["x_unit", "y_unit"]
        dict_vals_k = ["x_vals", "y_vals"]
        s_ind = []
        vsu_ls = []

        for i in xrange(len(xy_vals)):
            su  = self.nuis_dict[dict_unit_k[i]]
            ua  = self.nuis_dict[dict_vals_k[i]]
            vsu = ROOThelper.convert_units(su, from_num=xy_vals[i], from_unit=xy_units[i])
            vsu_ls.append(vsu)

            if vsu in ua:
                s_ind.append([np.where(ua == vsu)[0][0]])
            else:
                if vsu < ua[0] or vsu > ua[-1]:
                    print("Warning: requested", vsu, su, "is outside the storage grid.")
                    print("Extrapolation from 2D array not implemented. Ending function.")
                    return None
                low_ele = np.where(ua < vsu)[0][-1]
                upp_ele = np.where(ua > vsu)[0][0]
                s_ind.append([low_ele, upp_ele])

        if debug_mode:
            print("Searching coordinates:", s_ind, "corresponding to", vsu_ls, "(in same units as grid)")

        interp_q = 0.0

        if len(s_ind[0]) == 1 and len(s_ind[1]) == 1:
            interp_q = self.nuis_dict[year][s_ind[0][0], s_ind[1][0]]
            if debug_mode:
                print("Extracted", interp_q)

        elif len(s_ind[0]) == 1 and len(s_ind[1]) != 1:
            if use_log:
                y, y0, y1 = np.log([vsu_ls[1], self.nuis_dict["y_vals"][s_ind[1][0]], self.nuis_dict["y_vals"][s_ind[1][1]]])
            else:
                y, y0, y1 = vsu_ls[1], self.nuis_dict["y_vals"][s_ind[1][0]], self.nuis_dict["y_vals"][s_ind[1][1]]
            q0 = self.nuis_dict[year][s_ind[0][0], s_ind[1][0]]
            q1 = self.nuis_dict[year][s_ind[0][0], s_ind[1][1]]
            interp_q = lerp(y, y0, y1, q0, q1)
            if debug_mode:
                print("Interpolated y-axis", y0, y1, "with nuis", q0, q1, "to get y=", y, "as", interp_q)

        elif len(s_ind[0]) != 1 and len(s_ind[1]) == 1:
            if use_log:
                x, x0, x1 = np.log([vsu_ls[0], self.nuis_dict["x_vals"][s_ind[0][0]], self.nuis_dict["x_vals"][s_ind[0][1]]])
            else:
                x, x0, x1 = vsu_ls[0], self.nuis_dict["x_vals"][s_ind[0][0]], self.nuis_dict["x_vals"][s_ind[0][1]]
            q0 = self.nuis_dict[year][s_ind[0][0], s_ind[1][0]]
            q1 = self.nuis_dict[year][s_ind[0][1], s_ind[1][0]]
            interp_q = lerp(x, x0, x1, q0, q1)
            if debug_mode:
                print("Interpolated x-axis", x0, x1, "with nuis", q0, q1, "to get x=", x, "as", interp_q)

        elif len(s_ind[0]) != 1 and len(s_ind[1]) != 1:
            if use_log:
                x, x1, x2 = np.log([vsu_ls[0], self.nuis_dict["x_vals"][s_ind[0][0]], self.nuis_dict["x_vals"][s_ind[0][1]]])
                y, y1, y2 = np.log([vsu_ls[1], self.nuis_dict["y_vals"][s_ind[1][0]], self.nuis_dict["y_vals"][s_ind[1][1]]])
            else:
                x, x1, x2 = vsu_ls[0], self.nuis_dict["x_vals"][s_ind[0][0]], self.nuis_dict["x_vals"][s_ind[0][1]]
                y, y1, y2 = vsu_ls[1], self.nuis_dict["y_vals"][s_ind[1][0]], self.nuis_dict["y_vals"][s_ind[1][1]]
            q11 = self.nuis_dict[year][s_ind[0][0], s_ind[1][0]]
            q12 = self.nuis_dict[year][s_ind[0][0], s_ind[1][1]]
            q21 = self.nuis_dict[year][s_ind[0][1], s_ind[1][0]]
            q22 = self.nuis_dict[year][s_ind[0][1], s_ind[1][1]]
            points = [(x1, y1, q11), (x1, y2, q12), (x2, y1, q21), (x2, y2, q22)]
            interp_q = bilerp(x, y, points)
            if debug_mode:
                print("Interpolated nuis", interp_q, "from nuis", [q11, q12, q21, q22],
                      "at x's", [x1, x2], "and y's", [y1, y2])
        else:
            raise Exception("Error: coordinate list is not 1x1-2x2")

        if self.arr_len == 0:
            if not np.isfinite(interp_q):
                print("Warning: unable to interpolate, likely missing grid value. Exiting code.")
                return None
        return interp_q

    def get_point_from_fn(self, file_info, overrides=None, use_log=False, debug_mode=False):
        try:
            new_sig = SignalROOTInfo(file_info)
        except Exception:
            new_sig = file_info
        proc, tau, mass, yr = new_sig.return_name2details(lifetime_unit=self.nuis_dict["x_unit"])
        if proc != self.proc:
            return None
        if overrides is not None:
            for k in overrides:
                if k == "yr":
                    yr = overrides[k]
        return self.get_point(yr, tau, mass, use_log=use_log, debug_mode=debug_mode)

    def print_diagnostics(self):
        print(self.nuis_dict)

    def save_pickle(self, to_fn_prefix, tag_proc=True, to_fn_suffix=".pkl", debug_mode=False):
        out_fn = to_fn_prefix
        if tag_proc:
            out_fn += "_" + self.proc
        out_fn += to_fn_suffix
        with open(out_fn, "wb") as fh:
            pickle.dump(self.nuis_dict, fh)
        if debug_mode:
            print("Saved pickle:", out_fn)

    def pretty_print_diagnostics(self):
        str_out = str(self.nuis_dict).replace(", '", """,\n    '""")
        temp_yr_dict = {"years": self.nuis_dict["years"]}
        str_yr_replace = str(temp_yr_dict)[1:-1]
        str_out = str_out.replace(
            str_yr_replace.replace(", '", """,\n    '"""),
            str_yr_replace)
        return str_out


def collect_xyvals_from_namearr(p, fns, x_unit, y_unit, debug_mode=False, **kwargs):
    """Scan filenames and return sorted lists of unique x (lifetime) and y (mass) values."""
    x_vals = []
    y_vals = []

    for k in fns:
        new_sig = SignalROOTInfo(k, **kwargs)
        proc, tau, mass, _ = new_sig.return_name2details(lifetime_unit=x_unit)
        if proc != p:
            continue
        for val, ls in [(tau, x_vals), (mass, y_vals)]:
            if val not in ls:
                ls.append(val)

    x_vals.sort()
    y_vals.sort()

    if debug_mode:
        print("Identified x-s:", x_vals, "in", x_unit)
        print("Identified y-s:", y_vals)

    return x_vals, y_vals
