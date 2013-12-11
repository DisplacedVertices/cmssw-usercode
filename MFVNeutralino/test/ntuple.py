#!/usr/bin/env python

import sys
from JMTucker.Tools.PATTuple_cfg import *
tuple_version = version

no_skimming_cuts(process)

process.out.fileName = 'ntuple.root'
process.out.outputCommands = [
    'drop *',
    'keep MFVEvent_mfvEvent__*',
    'keep MFVVertexAuxs_mfvVerticesAux__*',
    ]
process.out.dropMetaData = cms.untracked.string('ALL')

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.p = cms.Path(common_seq * process.mfvVertexSequence)

del process.outp
process.outp = cms.EndPath(process.mfvEvent * process.out)


if 'histos' in sys.argv:
    process.TFileService = cms.Service('TFileService', fileName = cms.string('ntuple_histos.root'))
    process.mfvVertices.histos = True
    process.mfvVerticesToJets.histos = True
    process.load('JMTucker.MFVNeutralino.Histos_cff')
    process.outp.replace(process.mfvEvent, process.mfvEvent * process.mfvHistos) # in outp because histos needs to read mfvEvent

if 'test' in sys.argv:
    process.source.fileNames = [
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_2_2_vbl.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_3_2_yEE.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_4_1_vkj.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_5_3_Tce.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_6_1_a0t.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_7_2_Qv8.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_8_1_3WZ.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_9_1_ANl.root',
    ]
    process.maxEvents.input = 100
    input_is_pythia8(process)
    re_pat(process)
    process.mfvEvent.cleaning_results_src = cms.InputTag('TriggerResults', '', 'PAT2')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    def modify(sample):
        to_add = []
        to_replace = []

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

        if sample.is_mc and sample.re_pat:
            to_add.append("process.mfvEvent.cleaning_results_src = cms.InputTag('TriggerResults', '', 'PAT2')") # JMTBAD rework re_pat

        return to_add, to_replace

    cs = CRABSubmitter('MFVNtuple' + tuple_version.upper(),
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       get_edm_output = True,
                       data_retrieval = 'fnal_eos',
                       #publish_data_name = 'mfvntuple_' + tuple_version,
                       max_threads = 3,
                       )

    x = Samples.mfv_signal_samples
    Samples.mfv_signal_samples = []
    Samples.mfv300 = []
    for y in x:
        if '300' in y.name:
            Samples.mfv300.append(y)
        else:
            Samples.mfv_signal_samples.append(y)
    
    if 'smaller' in sys.argv:
        samples = Samples.smaller_background_samples
    elif 'leptonic' in sys.argv:
        samples = Samples.leptonic_background_samples
    elif 'data' in sys.argv:
        samples = Samples.data_samples
    elif 'auxdata' in sys.argv:
        samples = Samples.auxiliary_data_samples
    elif '100k' in sys.argv:
        samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples
    elif 'mfv300' in sys.argv:
        samples = Samples.mfv300
    else:
        samples = Samples.mfv_signal_samples + Samples.ttbar_samples + Samples.qcd_samples

    for sample in samples:
        if sample.is_mc:
            sample.total_events = -1

    cs.submit_all(samples)
