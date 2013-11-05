#!/usr/bin/env python

import os, sys
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
    ]

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.mfvVertices.histos = False
process.mfvVerticesToJets.histos = False
process.p = cms.Path(common_seq * process.mfvVertexSequence)

del process.outp
process.outp = cms.EndPath(process.mfvEvent * process.out)
''')

    if sample.is_mc and sample.re_pat:
        to_add.append("process.mfvEvent.cleaning_results_src = cms.InputTag('TriggerResults', '', 'PAT2')") # JMTBAD rework re_pat

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

if 'testsingle' in sys.argv:
    fn,pset = cs.pset(Samples.mfv_neutralino_tau0100um_M0400, '/dev/null')
    pset += 'process.options.wantSummary = True\nprocess.source.fileNames = %r' % Samples.mfv_neutralino_tau0100um_M0400.filenames(False)[:5]
    open('runme.py','wt').write(pset)
    sys.exit(os.system('logcms.py runme.py'))

samples = Samples.data_samples + Samples.auxiliary_data_samples + Samples.mfv_signal_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.smaller_background_samples + Samples.leptonic_background_samples
for sample in samples:
    if sample.is_mc:
        sample.total_events = -1

cs.submit_all(samples)
