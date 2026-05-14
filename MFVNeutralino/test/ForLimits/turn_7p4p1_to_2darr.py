from __future__ import absolute_import
import numpy as np

import script_configs as config # everything hard-coded goes into config
import helper_PyStorage_objects as sth
import uncerts_trigger as trig_unc # Python dictionaries
import uncerts_trigger_patch as trig_unc_patch # Extrapolation pack
import nuisance_configs as ns_conf


"""
-Make nuisance tables for 4 processes (based on total_uncerts of trigger_uncerts, which is the 7.4.1 summary.)
-Save information as pickles (check pickles can be re-read)
"""


proc_nm = set([
    "mfv_neu",
    "mfv_stopbbarbbar",
    "mfv_stopdbardbar",
    "ggHToSSTodddd",])
is_percent = False
x_unit = "mm"
y_unit = "GeV"

# output_str = """""" # Defunct method: write output to .txt
# save_loc = "7p4p1_trigger_unc.txt" # For manual
pickle_prefix = ns_conf.pickle_prefixes["disp_trig_uncerts"]



for p in proc_nm:

    x_vals = []
    y_vals = []

    x_vals, y_vals = sth.collect_xyvals_from_namearr(p, trig_unc.total_uncerts.keys(), x_unit, y_unit, debug_mode=True, nbins=3)
    
    
    ntab = sth.NuisanceTable(p, x_vals, x_unit, y_vals, y_unit, as_percent=is_percent, years=set(["2016", "2016APV", "2017", "2018"]))
    ntab.add_dictionary(trig_unc.total_uncerts, debug_mode=False)
    ntab.add_dictionary(trig_unc_patch.total_uncerts_patch, debug_mode=False)


    # Mess around with object
    ntab.get_point("2017", x_val=1.01, y_val=401, x_unit="mm", use_log=False, debug_mode=True)

    point_from_fn = ntab.get_point_from_fn("mfv_neu_tau010000um_M0400_2018", debug_mode=True)
    print "Searching mfv_neu_tau010000um_M0400_2018 returned", point_from_fn

    
    if False:
        print "\nSummary of", p
        print ntab.pretty_print_diagnostics()
        print "\n\n"

    ntab.save_pickle(pickle_prefix)

    # output_str += str(ntab.proc) + " = " + ntab.pretty_print_diagnostics() + "\n\n\n"


# Check if pickling is right
for p in proc_nm:
    ntab = sth.NuisanceTable(proc=p, pickle_loc=pickle_prefix)
    print "Successfully reconstructed:", ntab.proc

    if True:
        print "\nSummary of", p
        print ntab.pretty_print_diagnostics()
        print "\n\n"



#out_file = open(save_loc, "w")
#out_file.write(output_str)
#out_file.close()


