import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, add_analyzer

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.maxEvents.input = 100
process.source.fileNames = ['file:pat.root']
process.TFileService.fileName = 'resolutions_histos.root'

########################################################################

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.goodDataFilter = hltHighLevel.clone()
process.goodDataFilter.TriggerResultsTag = cms.InputTag('TriggerResults', '', 'PAT')
process.goodDataFilter.HLTPaths = ['eventCleaningAll'] # can set to just 'goodOfflinePrimaryVertices', for example
process.goodDataFilter.andOr = False # = AND

process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
process.triggerFilter.andOr = True # = OR

########################################################################

process.load('JMTucker.Tools.ResolutionsHistogrammer_cfi')

for x in ['WithTrigger']:
    setattr(process, 'histos' + x, process.histos.clone())

########################################################################

process.p0 = cms.Path(                        process.histos)
process.p1 = cms.Path(process.triggerFilter * process.histosWithTrigger)

if 'debug' in sys.argv:
    from JMTucker.Tools.CMSSWTools import file_event_from_argv
    file_event_from_argv(process)
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.histos.print_info = True
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                       maxEventsToPrint = cms.untracked.int32(100),
                                       src = cms.InputTag('genParticles'),
                                       printOnlyHardInteraction = cms.untracked.bool(False),
                                       useMessageLogger = cms.untracked.bool(False)
                                       )
    process.p0.insert(0, process.printList)

def run_on_data(dataset=None, datasets=None):
    if 'debug' in sys.argv:
        process.p.remove(process.printList)

    add_analyzer('EventIdRecorder')

    if dataset and datasets:
        veto_filter = cms.EDFilter('VetoOtherDatasets', datasets_to_veto = cms.vstring(*[d for d in datasets if d != dataset]))
        setattr(process, 'dataset%sOnly' % dataset, veto_filter)
        for path_name, path in process.paths_().iteritems():
            path.insert(0, veto_filter)

#run_on_data('MultiJet', ['MultiJet', 'JetHT', 'MuHad', 'ElectronHad'])

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    from JMTucker.Tools.Samples import background_samples, smaller_background_samples, mfv_signal_samples, data_samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    def pset_adder(sample):
        to_add = []
        if not sample.is_mc:
            to_add.append('run_on_data()')
        return to_add

    cs = CRABSubmitter('ResolutionsHistos',
                       total_number_of_events = -1,
                       events_per_job = 10000,
                       use_ana_dataset = True,
                       CMSSW_use_parent = 1,
                       pset_modifier = pset_adder
                       )

    samples = mfv_signal_samples + background_samples + [s for s in smaller_background_samples if name not in 'ttgjets ttwjets ttzjets']
    cs.submit_all(samples)
