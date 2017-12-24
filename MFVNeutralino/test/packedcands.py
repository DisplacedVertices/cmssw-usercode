from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
repro = False
prints = True

####

process.source.fileNames = ['file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/A00610B3-00B7-E611-8546-A0000420FE80.only_events_in_parent.root']
process.source.secondaryFileNames = cms.untracked.vstring('file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/2A6D6695-3BB2-E611-BA91-24BE05C626B1.root')

process.TFileService.fileName = 'packedcands.root'
geometry_etc(process, which_global_tag(is_mc, year, H, repro))
report_every(process, 1 if prints else 1000000)

process.mfvPackedCands = cms.EDAnalyzer('MFVPackedCandidates',
                                        max_closest_cd_dist = cms.double(0.111e-3),
                                        prints = cms.bool(prints),
                                        )
process.p = cms.Path(process.mfvPackedCands)

import JMTucker.MFVNeutralino.EventFilter
JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, 'p')
