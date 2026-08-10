from JMTucker.Tools.CMSSWTools import *

process = basic_process('Merge')
report_every(process, 500)
output_file(process, 'merge.root')

# Keeping Run/LumiSummary causes these sparse skims to be majorly
# bloated; not using them right now, so drop them. Also drop
# MEtoEDMConverter junk.
process.source.inputCommands = cms.untracked.vstring('keep *', 'drop *_MEtoEDMConverter_*_*')
process.out.outputCommands = cms.untracked.vstring('keep *', 'drop LumiDetails_lumiProducer_*_*', 'drop LumiSummary_lumiProducer_*_*', 'drop RunSummary_lumiProducer_*_*')

# Also don't need per-event metadata.
process.out.dropMetaData = cms.untracked.string('ALL')

cmssw_from_argv(process)
