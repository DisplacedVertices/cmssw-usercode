from __future__ import print_function
from __future__ import absolute_import
import numpy as np

import script_configs as config # everything hard-coded goes into config
import helper_PyStorage_objects as sth
import uncerts_trkrec as tkrc_unc # Python dictionaries
import nuisance_configs as ns_conf


"""
-Make nuisance tables, for central/up/down
-Save information as pickles (check pickles can be re-read)
"""


proc_nm = set([
    "VH",])
is_percent = False
x_unit = "mm"
y_unit = "GeV"

prefix_dict = ns_conf.pickle_triple_prefixes["tk_reco_eff"]
pickle_prefix_base = prefix_dict["base"]

pickle_prefix_ct = pickle_prefix_base + prefix_dict["central"]
pickle_prefix_up = pickle_prefix_base + prefix_dict["up"]
pickle_prefix_dn = pickle_prefix_base + prefix_dict["dn"]



for p in proc_nm:

    x_vals = []
    y_vals = []

    x_vals, y_vals = sth.collect_xyvals_from_namearr(p, tkrc_unc.trkdisp_central.keys(), x_unit, y_unit, debug_mode=True)
    
    
    ct_ntab = sth.NuisanceTable(p, x_vals, x_unit, y_vals, y_unit, as_percent=is_percent, years=set(["20161", "20162", "2017", "2018"]), nbin_len=True)
    ct_ntab.add_dictionary(tkrc_unc.trkdisp_central, debug_mode=False)

    up_ntab = sth.NuisanceTable(p, x_vals, x_unit, y_vals, y_unit, as_percent=is_percent, years=set(["20161", "20162", "2017", "2018"]), nbin_len=True)
    up_ntab.add_dictionary(tkrc_unc.trkdisp_up, debug_mode=False)

    dn_ntab = sth.NuisanceTable(p, x_vals, x_unit, y_vals, y_unit, as_percent=is_percent, years=set(["20161", "20162", "2017", "2018"]), nbin_len=True)
    dn_ntab.add_dictionary(tkrc_unc.trkdisp_dn, debug_mode=False)


    # Mess around with object
    ct_ntab.get_point("2017", x_val=1, y_val=40, x_unit="mm", use_log=False, debug_mode=True)

    point_from_fn = ct_ntab.get_point_from_fn("VH_tau1mm_M040_2018", debug_mode=True)
    print("Searching VH_tau1mm_M040_2018 returned", point_from_fn)

    point_from_fn = up_ntab.get_point_from_fn("VH_tau1mm_M040_2018", debug_mode=True)
    print("Searching VH_tau1mm_M040_2018 returned", point_from_fn)

    point_from_fn = dn_ntab.get_point_from_fn("VH_tau1mm_M040_2018", debug_mode=True)
    print("Searching VH_tau1mm_M040_2018 returned", point_from_fn)

    
    if True:
        print("\nSummary of", p)
        print(ct_ntab.pretty_print_diagnostics())
        print(up_ntab.pretty_print_diagnostics())
        print(dn_ntab.pretty_print_diagnostics())
        print("\n\n")

    ct_ntab.save_pickle(pickle_prefix_ct)
    up_ntab.save_pickle(pickle_prefix_up)
    dn_ntab.save_pickle(pickle_prefix_dn)

    # output_str += str(ntab.proc) + " = " + ntab.pretty_print_diagnostics() + "\n\n\n"


# Check if pickling is right
for p in proc_nm:
    ct_ntab = sth.NuisanceTable(proc=p, pickle_loc=pickle_prefix_ct)
    print("Successfully reconstructed:", ct_ntab.proc)

    if False:
        print("\nSummary of", p)
        print(ct_ntab.pretty_print_diagnostics())
        print("\n\n")



#out_file = open(save_loc, "w")
#out_file.write(output_str)
#out_file.close()


