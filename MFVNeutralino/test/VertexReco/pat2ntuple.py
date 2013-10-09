#!/usr/bin/env python

import os
from JMTucker.Tools.CRABSubmitter import CRABSubmitter
from JMTucker.Tools.PATTuple_cfg import version as tuple_version
import JMTucker.Tools.Samples as Samples

def modify(sample):
    to_add = []
    to_replace = []

    to_add.append('no_skimming_cuts(process)')

    if sample.is_mc:
        if sample.is_fastsim:
            to_add.append('input_is_fastsim(process)')
        if sample.is_pythia8:
            to_add.append('input_is_pythia8(process)')
        if sample.re_pat:
            to_add.append('re_pat(process)')
    else:
        magic = 'runOnMC = True'
        err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
        to_replace.append((magic, 'runOnMC = False', err))

    to_add.append('''
process.out.fileName = 'ntuple.root'
process.out.outputCommands = [
    'drop *',
    'keep MFVEvent_mfvEvent__*',
    'keep MFVVertexAuxs_mfvVerticesAux__*',
    'keep edmTriggerResults_TriggerResults__%s' % process.name_(),
    ]

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.mfvVertices.histos = False
process.mfvVerticesToJets.histos = False
process.p = cms.Path(common_seq * process.mfvVertexSequence * process.mfvEvent)
''')

    if not sample.is_mc or 'mfv' not in sample.name:
        to_add.append('process.mfvGenVertices.is_mfv = False')
        to_add.append('process.mfvEvent.is_mfv = False')
    if not sample.is_mc:
        to_add.append('process.mfvEvent.is_mc = False')

    return to_add, to_replace

cs = CRABSubmitter('MFVNtuple' + tuple_version.upper(),
                   pset_template_fn = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/Tools/python/PATTuple_cfg.py'),
                   pset_modifier = modify,
                   job_control_from_sample = True,
                   get_edm_output = True,
                   data_retrieval = 'fnal',
                   publish_data_name = 'mfvntuple_' + tuple_version,
                   max_threads = 3,
                   )

samples = Samples.data_samples + Samples.mfv_signal_samples + Samples.background_samples + Samples.smaller_background_samples

for sample in Samples.background_samples:
    sample.total_events = -1

cs.submit_all(samples)
