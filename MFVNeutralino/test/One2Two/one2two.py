import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.general import typed_from_argv

process.source = cms.Source('EmptySource')
process.maxEvents.input = 0
process.TFileService.fileName = 'one2two.root'

min_ntracks = typed_from_argv(int, 5)

mfvOne2Two = cms.EDAnalyzer('MFVOne2Two',
                            min_ntracks = cms.int32(min_ntracks),
                            svdist2d_cut = cms.double(0.05),

                            tree_path = cms.string('mfvMiniTree/t'),
                            filenames = cms.vstring('crab/MiniTreeV18/qcdht1000.root'),
                            n1vs = cms.vint32(),
                            weights = cms.vdouble(),

                            seed = cms.int32(0),
                            toy_mode = cms.bool(False),
                            poisson_n1vs = cms.bool(False),
                            wrep = cms.bool(True),
                            npairs = cms.int32(50000),

                            find_gs = cms.bool(True),
                            find_fs = cms.bool(True),
                            form_dphi = cms.string('abs(x)**[0]/(3.14159265**([0]+1)/([0]+1))'),
                            form_dz = cms.string('1/sqrt(2*3.14159265*[0]**2)*exp(-x*x/2/[0]**2)'),
                            form_g_dz = cms.string('1/sqrt(2*3.14159265*[0]**2)*exp(-x*x/2/[0]**2)'),

                            use_f_dz = cms.bool(True),
                            max_1v_dz = cms.double(0.025),
                            max_1v_ntracks = cms.int32(1000000),
                            )


if 'toy' in sys.argv:
    mfvOne2Two.toy_mode = True

    try:
        mfvOne2Two.seed = int(sys.argv[sys.argv.index('toy')+1])
    except IndexError:
        pass

    process.TFileService.fileName = 'toy_histos_seed%i.root' % mfvOne2Two.seed.value()

    import JMTucker.Tools.Samples as Samples
    sample_info = [
        (Samples.qcdht0500,    1220),
        (Samples.qcdht1000,     112),
        (Samples.ttbardilep,      1),
        (Samples.ttbarhadronic,  44),
        (Samples.ttbarsemilep,   14),
        ]

    n1v_ttbardilep = 3 # 101 (23) 5- (8-)track 1v ttdil events in 20/fb...
    mfvOne2Two.filenames = ['crab/MiniTreeV18/%s.root' % s[0].name for s in sample_info]
    mfvOne2Two.n1vs = [s[1]*n1v_ttbardilep for s in sample_info]
    mfvOne2Two.weights = [s[0].partial_weight * 20000 for s in sample_info]

    if 'poisson' in sys.argv:
        mfvOne2Two.poisson_n1vs = True
    
else:
    for arg in sys.argv:
        if arg.endswith('.root') and os.path.isfile(arg):
            process.TFileService.fileName = os.path.basename(arg).replace('.root', '_histos.root')
            mfvOne2Two.filenames = [arg]


process.p = cms.Path()

for i in (5,6,7,8):
    o = mfvOne2Two.clone(min_ntracks = i)
    setattr(process, 'mfvOne2TwoNtracks%i' % i, o)
    process.p *= o
