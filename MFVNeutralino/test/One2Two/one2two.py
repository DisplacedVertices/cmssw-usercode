import sys, os
from collections import namedtuple
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.general import typed_from_argv

process.source = cms.Source('EmptySource')
process.maxEvents.input = 0
process.TFileService.fileName = 'one2two.root'

file_path = 'crab/MiniTreeV18/%s.root'

process.mfvOne2Two = cms.EDAnalyzer('MFVOne2Two',
                                    min_ntracks = cms.int32(5),
                                    svdist2d_cut = cms.double(0.048),

                                    tree_path = cms.string('mfvMiniTree/t'),
                                    filenames = cms.vstring(file_path % 'qcdht1000'),
                                    n1vs = cms.vint32(),
                                    weights = cms.vdouble(),

                                    seed = cms.int32(0),
                                    toy_mode = cms.bool(False),
                                    poisson_n1vs = cms.bool(False),
                                    wrep = cms.bool(True),
                                    npairs = cms.int32(100000),

                                    find_g_dz = cms.bool(True),
                                    form_g_dz = cms.string('1/sqrt(2*3.14159265*[0]**2)*exp(-x*x/2/[0]**2)'),

                                    find_f_dphi = cms.bool(True),
                                    form_f_dphi = cms.string('abs(x)**[0]/(3.14159265**([0]+1)/([0]+1))'),

                                    find_f_dz = cms.bool(True),
                                    form_f_dz = cms.string('1/sqrt(2*3.14159265*[0]**2)*exp(-x*x/2/[0]**2)'),

                                    use_f_dz = cms.bool(True),
                                    max_1v_dz = cms.double(0.025), # only used if use_f_dz false
                                    max_1v_ntracks = cms.int32(1000000),
                                    )

process.p = cms.Path(process.mfvOne2Two)


if 'env' not in sys.argv:
    for arg in sys.argv:
        if arg.endswith('.root') and os.path.isfile(arg):
            process.TFileService.fileName = os.path.basename(arg).replace('.root', '_histos.root')
            process.mfvOne2Two.filenames = [arg]
else:
    env = os.environ
    def env_var(name):
        return 'mfvo2t_' + name
    def from_env(name, type_):
        key = env_var(name)
        if env.has_key(key):
            val = type_(env[key])
            setattr(process.mfvOne2Two, name, val)

    from_env('min_ntracks',  int)
    from_env('svdist2d_cut', float)
    from_env('seed',         int)
    from_env('poisson_n1vs', bool)
    from_env('wrep',         bool)
    from_env('npairs',       int)

    phiexp = env.get(env_var('phiexp'), '[0]')
    process.mfvOne2Two.form_f_dphi = process.mfvOne2Two.form_f_dphi.value().replace('[0]', phiexp)

    sample = env.get(env_var('sample'), 'qcdht1000')
    if sample != 'toy':
        process.mfvOne2Two.filenames = [file_path % sample]
    else:
        process.mfvOne2Two.toy_mode = True

        import JMTucker.Tools.Samples as Samples
        SampleInfo = namedtuple('SampleInfo', ['sample', 'events_rel'])
        sample_infos = [
            SampleInfo(Samples.qcdht0500,    1220),
            SampleInfo(Samples.qcdht1000,     112),
            SampleInfo(Samples.ttbardilep,      1),
            SampleInfo(Samples.ttbarhadronic,  44),
            SampleInfo(Samples.ttbarsemilep,   14),
            ]

        use_qcd500 = bool(env.get('mfvo2t_use_qcd500', ''))
        if not use_qcd500:
            sample_infos.pop(0)

        n1v_scale = int(env.get('mfvo2t_n1v_scale', '3'))   # 101 (23) 5- (8-)track 1v ttdil events in 20/fb...
        int_lumi = float(env.get('mfvo2t_int_lumi', '20000'))

        process.mfvOne2Two.filenames = [file_path % s.sample.name for s in sample_infos]
        process.mfvOne2Two.n1vs = [s.events_rel*n1v_scale for s in sample_info]
        process.mfvOne2Two.weights = [s.sample.partial_weight * int_lumi for s in sample_info]

print 'CFG BEGIN'
print process.mfvOne2Two.dumpPython()
print 'CFG END'
