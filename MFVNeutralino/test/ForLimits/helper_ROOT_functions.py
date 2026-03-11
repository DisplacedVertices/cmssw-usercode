from __future__ import division
from __future__ import absolute_import

import ROOT

import sig_and_bkg_configs as sb_conf

"""
Is JMTucker-specific
-Get sumw for signal normalization, from TTree

ROOT Functions
-Make new Th1D from given histogram
-Move overflow into last bin

Not ROOT
-Convert units
"""


# Is Pipeline-Specific

"""
def get_hsum_bin(siginfo, bin_label="sum_gen_weight_total"):
    """
    #Based on sumw() in sums_from_file() of Sample.py of JMTucker
    
    #Input: siginfo pointing to TTree from MiniTree-maker (but non-TTrees may work if file conventions match)
"""
    f_temp = ROOT.TFile.Open(siginfo.full_fn)
    
    h = f_temp.Get('mfvWeight/h_sums')
    labels = [h.GetXaxis().GetBinLabel(ibin) for ibin in xrange(1, h.GetNbinsX()+1)]
    sumw = h.GetBinContent(labels.index(bin_label)+1)
    f_temp.Close()
    
    return sumw
"""



def search_dict_w_startkey(dt, p):
    """
    Ad-hoc method, deals with dictionaries that index 1) processnames, and 2) starting letters.
    
    Inputs: dictionary, process (str)
    """

    if p in dt.keys():
        return dt[p]
    else:
        for st in dt["index_start"].keys():
            str_loc = p.find(st)
            if str_loc == 0:
                return dt["index_start"][st]
    return dt["others"]



"""
def get_xsec(siginfo, debug_mode=False):
    """
    #Get x-sec for a siginfo object
"""
    found_xs = search_dict_w_startkey(sb_conf.sig_xsecs, siginfo.proc)

    if debug_mode: print "X-Sec:", found_xs
    return found_xs
"""



"""
def get_filtereff(siginfo, debug_mode=False):
    found_ft = search_dict_w_startkey(sb_conf.sig_filtereffs, siginfo.proc)

    if debug_mode: print "Filter-Eff:", found_ft
    return found_ft
"""






# Is ROOT

"""
def to_TH1D(h, name): # Copied from JMTucker
    hh = ROOT.TH1D(name, h.GetTitle(), h.GetNbinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
    hh.Sumw2()
    for ibin in xrange(h.GetNbinsX()+2):
        hh.SetBinContent(ibin, h.GetBinContent(ibin))
        hh.SetBinError  (ibin, h.GetBinError  (ibin))
    hh.SetEntries(h.GetEntries())
    return hh
"""



"""
def move_overflow_into_last_bin(h):
"""
# h: ROOT 1D histogram
"""
    nbx = h.GetXaxis().GetNbins()
    h.SetBinContent(nbx, h.GetBinContent(nbx)+h.GetBinContent(nbx+1))
    h.SetBinError(nbx, (h.GetBinError(nbx)**2+h.GetBinError(nbx+1)**2)**0.5)
    h.SetBinContent(nbx+1, 0)
    h.SetBinError(nbx+1, 0)
    return
"""



def mult_hist_w_array(h, arr):
    """
    Multiply an n-bin histogram by an array
    """
    if (h.GetNbinsX() != len(arr)): raise Exception("Bad multiplicative array dimensions for ROOT histogram")

    for i in range(h.GetNbinsX()):
        h.SetBinContent(i+1, h.GetBinContent(i+1) * arr[i])
        h.SetBinError(i+1, h.GetBinError(i+1) * arr[i])
    return






# NOT ROOT

def convert_units(to_unit, from_num=None, from_unit=None, from_expr=None):
    """
    Converts from_num in unit from_unit into unit to_unit. Only accepts mm and um right now.

    num: int, float, str, or anything that can be put into a float()
    unit: str
    from_expr: if not None, it will interpret the last 2 characters as the unit, and the rest as a number (inherited from filename convention).
    """
    if "eV" in to_unit and "eV" in from_unit:
        return from_num # not processing eVs at all

    if from_expr is not None:
        from_num = float(from_expr[:-2])
        from_unit = from_expr[-2:]

    num_asfloat = float(from_num)
    if from_unit=="mm":
        num_in_mm = num_asfloat
    elif from_unit=="um":
        num_in_mm = num_asfloat * 1e-3
    else:
        raise Exception("Unit input", from_unit, "not recognized")

    if to_unit=="mm":
        return num_in_mm
    elif to_unit=="um":
        return num_in_mm * 1e3
    else:
        raise Exception("Unit requested", unit, "not recognized")
    return



"""
def lerp(x, x0, x1, q0, q1): #Copied from JMTucker
    xd = (x - x0) / float(x1 - x0)
    return q0 * (1 - xd) + q1 * xd
"""



"""
def bilerp(x,y, points): #Copied from JMTucker # https://stackoverflow.com/questions/8661537/how-to-perform-bilinear-interpolation-in-python
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = sorted(points)
    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')
    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)   ) / ((x2 - x1) * (y2 - y1) + 0.0)
"""


