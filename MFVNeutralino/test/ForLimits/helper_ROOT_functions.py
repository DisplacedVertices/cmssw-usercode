from __future__ import division
from __future__ import absolute_import

import ROOT

import sig_and_bkg_configs as sb_conf


def search_dict_w_startkey(dt, p):
    """Look up p in dt; fall back to prefix-matched entry in dt['index_start'], then dt['others']."""
    if p in dt.keys():
        return dt[p]
    else:
        for st in dt["index_start"].keys():
            str_loc = p.find(st)
            if str_loc == 0:
                return dt["index_start"][st]
    return dt["others"]


def mult_hist_w_array(h, arr):
    """Multiply each bin content and error of h by the corresponding element of arr."""
    if (h.GetNbinsX() != len(arr)):
        raise Exception("Bad multiplicative array dimensions for ROOT histogram")
    for i in range(h.GetNbinsX()):
        h.SetBinContent(i+1, h.GetBinContent(i+1) * arr[i])
        h.SetBinError(i+1, h.GetBinError(i+1) * arr[i])
    return


def convert_units(to_unit, from_num=None, from_unit=None, from_expr=None):
    """Convert a displacement value between mm and um.

    -INPUTS-
    to_unit, from_unit: str
    from_num: int, float, str, or anything that can be put into a float()
    from_expr: if given, interprets the last 2 chars as the unit (filename convention).
    """
    if "eV" in to_unit and "eV" in from_unit:
        return from_num

    if from_expr is not None:
        from_num  = float(from_expr[:-2])
        from_unit = from_expr[-2:]

    num_asfloat = float(from_num)
    if from_unit == "mm":
        num_in_mm = num_asfloat
    elif from_unit == "um":
        num_in_mm = num_asfloat * 1e-3
    else:
        raise Exception("Unit input %s not recognized" % from_unit)

    if to_unit == "mm":
        return num_in_mm
    elif to_unit == "um":
        return num_in_mm * 1e3
    else:
        raise Exception("Unit requested %s not recognized" % to_unit)
