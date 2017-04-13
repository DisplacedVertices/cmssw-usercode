import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True

silence_messages(process, ['HLTConfigData'])
geometry_etc(process, '76X_mcRun2_asymptotic_v12' if is_mc else '76X_dataRun2_v15')
#report_every(process, 1)
#process.options.wantSummary = True
process.maxEvents.input = 100

process.source.fileNames = ['/store/mc/RunIIFall15DR76/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/0874DD13-DDA0-E511-AC76-001E67A3FD26.root']
if not is_mc:
    process.source.fileNames = ['/store/data/Run2015D/JetHT/AOD/16Dec2015-v1/00000/0A2C6696-AEAF-E511-8551-0026189438EB.root']

process.TFileService.fileName = 'tracking_tree.root'

process.load('JMTucker.Tools.MCStatProducer_cff')

process.goodVertices = cms.EDFilter('VertexSelector',
                                    filter = cms.bool(True),
                                    src = cms.InputTag('offlinePrimaryVertices'),
                                    cut = cms.string('!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2')
                                    )

process.tt = cms.EDAnalyzer('TrackingTreer',
                           beamspot_src = cms.InputTag('offlineBeamSpot'),
                           primary_vertices_src = cms.InputTag('goodVertices'),
                           tracks_src = cms.InputTag('generalTracks'),
                           assert_diag_cov = cms.bool(True),
                           )

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
setup_event_filter(process, 'p', need_pat=True)
process.p *= process.goodVertices * process.tt

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    samples = Samples.registry.from_argv(Samples.data_samples + Samples.qcdpt_samples)

    for s in samples:
        if s.is_mc:
            s.events_per = 50000
            s.total_events = s.nevents_orig/10
        else:
            s.json = '/uscms/home/tucker/work/mfv_763p2/src/JMTucker/MFVNeutralino/test/ana_10pc.json'
            s.lumis_per = 150
            s.total_lumis = -1

    def modify(sample):
        to_add = []
        to_replace = []

        if not sample.is_mc:
            magic = 'is_mcX=XTrue'.replace('X', ' ')
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))
            # JMTBAD different globaltags?

        return to_add, to_replace

    cs = CRABSubmitter('TrackTreeV3',
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       )

    cs.submit_all(samples)
