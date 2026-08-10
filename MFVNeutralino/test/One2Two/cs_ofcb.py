# this crap is for checking submit's output files--found necessary when running from cms connect

import os
import ROOT; ROOT.gROOT.SetBatch()
from process import fromtree

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
        if not f.IsOpen() or f.IsZombie() or not f.Get('limit'):
            return False

        try:
            ft = fromtree(fn)
        except ValueError:
            return False
        else:
            return True

    elif bn.startswith('combine_output_'):
        return True
