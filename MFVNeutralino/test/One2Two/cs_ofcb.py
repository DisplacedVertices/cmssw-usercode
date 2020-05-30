# this crap is for checking submit's output files--found necessary when running from cms connect

import os
import ROOT; ROOT.gROOT.SetBatch()
from process import fromtree, ntoysperjob

def outputfile_callback(fn,job):
    bn = os.path.basename(fn)
    if bn.endswith('.root'):
        is_obs = bn.startswith('observed_')
        if is_obs:
            if job != 0:
                return True
            fn = fn.replace('_0','')
        else:
            assert bn.startswith('expected_')

        f = ROOT.TFile.Open(fn)
        if not f.IsOpen() or f.IsZombie():
            return False

        ft = fromtree(fn)
        if is_obs:
            return len(ft) == 1
        else:
            return len(ft) == ntoysperjob

    elif bn.startswith('combine_output_'):
        return True
