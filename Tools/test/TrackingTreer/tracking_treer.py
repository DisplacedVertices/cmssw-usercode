import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True

silence_messages(process, ['HLTConfigData'])
geometry_etc(process, '74X_mcRun2_asymptotic_v4' if is_mc else '74X_dataRun2_v5')
#report_every(process, 1)
#process.options.wantSummary = True
#process.maxEvents.input = 1000

process.source.fileNames = ['/store/user/tucker/F47E7F59-8A29-E511-8667-002590A52B4A.root']
if not is_mc:
    process.source.fileNames = ['/store/user/tucker/Run2015D_JetHT_AOD_PromptReco-v4_000_260_627_00000_78D8E6A7-6484-E511-89B4-02163E0134F6.root']

process.TFileService.fileName = 'tracking_tree.root'

if is_mc:
    process.load('JMTucker.Tools.MCStatProducer_cff')
    process.mcStat.histos = True

process.goodVertices = cms.EDFilter('VertexSelector',
                                    filter = cms.bool(True),
                                    src = cms.InputTag('offlinePrimaryVertices'),
                                    cut = cms.string('!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2')
                                    )

process.tt = cms.EDAnalyzer('TrackingTreer',
                           beamspot_src = cms.InputTag('offlineBeamSpot'),
                           primary_vertex_src = cms.InputTag('goodVertices'),
                           tracks_src = cms.InputTag('generalTracks'),
                           assert_diag_cov = cms.bool(True),
                           )

from JMTucker.MFVNeutralino.TriggerFilter import setup_trigger_filter
setup_trigger_filter(process, 'p', need_pat=True)
process.p *= process.goodVertices * process.tt

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    samples = Samples.registry.from_argv(Samples.data_samples + Samples.qcd_samples)

    for s in Samples.data_samples:
        s.json = '/uscms/home/tucker/private/mfv_7415p1/src/JMTucker/MFVNeutralino/test/ana_1pc.json'
        s.lumis_per = 1
        s.total_lumis = -1

    for s in Samples.data_samples:
        s.events_per = 50000
        s.total_events = s.nevents_orig/10

    def modify(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'is_mcX=XTrue'.replace('X', ' ')
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))
            # JMTBAD different globaltags?

        return to_add, to_replace

    cs = CRABSubmitter('TrackTreeV0',
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       )

    cs.submit_all(samples)
