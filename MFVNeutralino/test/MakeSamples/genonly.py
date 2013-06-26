from gensimhlt import cms, process
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.output_step)
process.maxEvents.input = 1000
