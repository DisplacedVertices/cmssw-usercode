from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source = cms.Source('EmptySource')
process.maxEvents.input = 0
process.TFileService.fileName = 'one2two.root'

mfvOne2Two = cms.EDAnalyzer('MFVOne2Two',
                            min_ntracks = cms.int32(5),
                            svdist2d_cut = cms.double(0.048),

                            tree_path = cms.string('mfvOne2Two/t'),
                            filenames = cms.vstring(),
                            n1vs = cms.vint32(),
                            weights = cms.vdouble(),

                            seed = cms.int32(-1),
                            poisson_n1vs = cms.bool(False),
                            wrep = cms.bool(True),
                            npairs = cms.int32(-1),

                            use_f_dz = cms.bool(False),
                            max_1v_dz = cms.double(0.025),
                            max_1v_ntracks = cms.int32(1000000),
                            form_dphi = cms.string('abs(x)**2.5/15.702056'),
                            form_dz = cms.string('1/sqrt(2*3.14159265*0.01635**2)*exp(-x*x/2/0.01635**2)'),
                            )

process.p = cms.Path()

for i in (5,6,7,8):
    o = process.mfvOne2Two.clone(min_ntracks = i)
    setattr(process, 'mfvOne2TwoNtracks%i' % i, o)
    process.p *= o
