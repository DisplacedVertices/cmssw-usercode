from __future__ import print_function
from __future__ import absolute_import
import numpy as np

import script_configs as config
import helper_PyStorage_objects as sth
import uncerts_trkmvr as TM_unc
import nuisance_configs as ns_conf



proc_nm = set([
    "VH",
    "mfv_neu",
    "mfv_stopbbarbbar",
    "mfv_stopdbardbar",
    "ggHToSSTodddd",])
is_percent = True

pickle_prefix = ns_conf.pickle_prefixes["vtx_reco_TM"]



for p in proc_nm:

    arr_1612 = np.array(TM_unc.TM_Tables[p]["20161-2"].T)
    arr_178 = np.array(TM_unc.TM_Tables[p]["2017-8"].T)

    x_vals = TM_unc.TM_Tables[p]["x_vals"]
    y_vals = TM_unc.TM_Tables[p]["y_vals"]

    x_unit = TM_unc.TM_Tables[p]["x_unit"]
    y_unit = TM_unc.TM_Tables[p]["y_unit"]

    
    ntab = sth.NuisanceTable(p, x_vals, x_unit, y_vals, y_unit, as_percent=is_percent, years=set(["20161-2", "2017-8"]))

    ntab.add_array(p, x_vals, y_vals, "20161-2", arr_1612, x_unit=x_unit, y_unit=y_unit, debug_mode=False)
    ntab.add_array(p, x_vals, y_vals, "2017-8", arr_178, x_unit=x_unit, y_unit=y_unit, debug_mode=False)


    ntab.save_pickle(pickle_prefix)


    if True:
        print("\nSummary of", p)
        print(ntab.pretty_print_diagnostics())
        print("\n\n")


