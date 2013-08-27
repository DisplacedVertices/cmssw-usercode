#!/usr/bin/env python

import os
from JMTucker.Tools.CRABSubmitter import CRABSubmitter
from JMTucker.Tools.PATTuple_cfg import version as tuple_version
from JMTucker.Tools.Samples import background_samples

def modify(sample):
    to_add = []
    to_replace = []

    if sample.is_mc:
        if sample.is_fastsim:
            to_add.append('input_is_fastsim(process)')
        if sample.is_pythia8:
            to_add.append('input_is_pythia8(process)')
        if sample.no_skimming_cuts:
            to_add.append('no_skimming_cuts(process)')
        if sample.re_pat:
            to_add.append('re_pat(process)')
    else:
        magic = 'runOnMC = True'
        err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
        to_replace.append((magic, 'runOnMC = False', err))

    return to_add, to_replace

cs = CRABSubmitter('Tuple' + tuple_version.upper(),
                   pset_template_fn = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/Tools/python/PATTuple_cfg.py'),
                   pset_modifier = modify,
                   job_control_from_sample = True,
                   get_edm_output = True,
                   data_retrieval = 'fnal',
                   publish_data_name = 'jtuple_' + tuple_version
                   )

cs.submit_all(background_samples)
