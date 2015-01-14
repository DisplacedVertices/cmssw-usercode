#!/usr/bin/env python

import sys
from JMTucker.Tools.PATTuple_cfg import *

runOnMC = True # magic line, don't touch
process, common_seq = pat_tuple_process(runOnMC)
no_skimming_cuts(process)

process.options.wantSummary=True

process.TFileService = cms.Service('TFileService', fileName = cms.string('beamprofile.root'))

del process.out
del process.outp

process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvEvent.cleaning_results_src = ''
process.mfvAnalysisCuts.apply_vertex_cuts = False
process.mfvAnalysisCuts.apply_cleaning_filters = False

cleaning_seq = process.eventCleaningAll._seq
for p in process.paths.keys():
    delattr(process, p)

process.p = cms.Path(cleaning_seq * common_seq * process.mfvEvent * process.mfvAnalysisCuts)

import JMTucker.MFVNeutralino.TriggerFilter
JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)
del process.pevtsel

process.bs = cms.EDAnalyzer('BeamSpotTreer',
                            beamspot_src = cms.InputTag('offlineBeamSpot'),
                            primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                            assert_diag_cov = cms.bool(False),
                            )

process.p *= process.bs

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    def modify(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'runOnMC = True'
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'runOnMC = False', err))
            if sample.name.startswith('MultiJetPk2012'):
                for name_part, tag in [
                    ('2012B', 'FT_53_V6C_AN4'),
                    ('2012C1', 'FT53_V10A_AN4'),
                    ('2012C2', 'FT_P_V42C_AN4'),
                    ('2012D1', 'FT_P_V42_AN4'),
                    ('2012D2', 'FT_P_V42D_AN4'),
                    ]:
                    if name_part in sample.name:
                        to_add.append('process.GlobalTag.globaltag = "%s::All"' % tag)
            to_add.append('process.dummyToMakeDiffHash = cms.PSet(submitName = cms.string("%s"))' % (sample.name + 'hello'))

        return to_add, to_replace

    cs = CRABSubmitter('BeamProfile',
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       get_edm_output = False,
                       data_retrieval = 'cornell',
                       publish_data_name = 'beamprofile' + ex,
                       max_threads = 3,
                       )

    samples = Samples.from_argv(Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples)

    for sample in samples:
        if sample.is_mc:
            sample.total_events = -1
        else:
            sample.json = '../ana_all.json'
            sample.total_lumis = -1

    cs.submit_all(samples)
