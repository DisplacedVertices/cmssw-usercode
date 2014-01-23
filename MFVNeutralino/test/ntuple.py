#!/usr/bin/env python

import sys
from JMTucker.Tools.PATTuple_cfg import *
tuple_version = version

runOnMC = True # magic line, don't touch
process, common_seq = pat_tuple_process(runOnMC)

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

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
process.triggerFilter.andOr = True # = OR
for name, path in process.paths.items():
    if not name.startswith('eventCleaning'):
        path.insert(0, process.triggerFilter)
process.ptrig = cms.Path(process.triggerFilter)
process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('ptrig'))

del process.outp
process.outp = cms.EndPath(process.mfvEvent * process.out)

# We're not saving the PAT branches, but if the embedding is on then
# we can't match leptons by track to vertices.
process.patMuonsPF.embedTrack = False
process.patElectronsPF.embedTrack = False

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
    from JMTucker.Tools.SampleFiles import SampleFiles

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
                       #manual_datasets = SampleFiles['mfv300s'],
                       max_threads = 3,
                       )

    timing = { 'dyjetstollM10': 0.011203, 'dyjetstollM50': 0.019867, 'qcdbce020': 0.008660, 'qcdbce030': 0.007796, 'qcdbce080': 0.061260, 'qcdbce170': 0.328891, 'qcdbce250': 0.481813, 'qcdbce350': 0.519482, 'qcdem020': 0.010137, 'qcdem030': 0.01, 'qcdem080': 0.037925, 'qcdem170': 0.286123, 'qcdem250': 0.471398, 'qcdem350': 0.686303, 'qcdht0100': 0.008273, 'qcdht0250': 0.116181, 'qcdht0500': 0.738374, 'qcdht1000': 1.002745, 'qcdmu0020': 0.012301, 'qcdmu0030': 0.015762, 'qcdmu0050': 0.018178, 'qcdmu0080': 0.119300, 'qcdmu0120': 0.245562, 'qcdmu0170': 0.32, 'qcdmu0300': 0.419818, 'qcdmu0470': 0.584266, 'qcdmu0600': 0.455305, 'qcdmu0800': 0.879171, 'qcdmu1000': 1.075712, 'singletop_s': 0.093429, 'singletop_s_tbar': 0.146642, 'singletop_tW': 0.327386, 'singletop_tW_tbar': 0.184349, 'singletop_t': 0.092783, 'singletop_t_tbar': 0.060983, 'ttbarhadronic': 0.752852, 'ttbarsemilep': 0.419073, 'ttbardilep': 0.295437, 'ttgjets': 0.861987, 'ttwjets': 0.714156, 'ttzjets': 0.827464, 'wjetstolnu': 0.010842, 'ww': 0.046754, 'wz': 0.049839, 'zz': 0.059791, }

    for sample in Samples.all_mc_samples:
        if timing.has_key(sample.name):
            sample.events_per = 3.5*3600/timing[sample.name]
            sample.timed = True
            nj = sample.nevents_orig / float(sample.events_per)
            assert nj < 5000

    for s in Samples.mfv_signal_samples:
        s.events_per = 500
        s.timed = True

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
    elif 'qcdlep' in sys.argv:
        samples = []
        for s in Samples.auxiliary_background_samples:
            if (s.name != 'qcdmupt15' and 'qcdmu' in s.name) or 'qcdem' in s.name or 'qcdbce' in s.name:
                samples.append(s)
    elif 'data' in sys.argv:
        samples = Samples.data_samples[:1]
    elif 'auxdata' in sys.argv:
        samples = Samples.auxiliary_data_samples
    elif '100k' in sys.argv:
        samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples
    elif 'few' in sys.argv:
        samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400, Samples.ttbarhadronic, Samples.qcdht1000]
    elif 'mfv300' in sys.argv:
        samples = Samples.mfv300
    else:
        samples = Samples.mfv_signal_samples + Samples.ttbar_samples + Samples.qcd_samples

    for sample in samples:
        if sample.is_mc:
            sample.total_events = -1
            assert hasattr(sample, 'timed')

    cs.submit_all(samples)
