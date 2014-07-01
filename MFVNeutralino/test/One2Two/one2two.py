import sys, os, FWCore.ParameterSet.Config as cms
from collections import namedtuple

process = cms.Process('One2Two')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(0))
process.source = cms.Source('EmptySource')
process.TFileService = cms.Service('TFileService', fileName = cms.string('one2two.root'))


file_path = 'crab/MiniTreeV18/%s.root'
signal_samples = ['mfv_neutralino_tau0100um_M0400', 'mfv_neutralino_tau0300um_M0400', 'mfv_neutralino_tau1000um_M0400', 'mfv_neutralino_tau9900um_M0400']
nsignals = len(signal_samples)

process.mfvOne2Two = cms.EDAnalyzer('MFVOne2Two',
                                    min_ntracks = cms.int32(5),
                                    svdist2d_cut = cms.double(0.048),

                                    tree_path = cms.string('mfvMiniTree/t'),
                                    filenames = cms.vstring(file_path % 'qcdht1000'),
                                    n1vs = cms.vint32(),
                                    weights = cms.vdouble(),
                                    just_print = cms.bool(False),

                                    seed = cms.int32(0),
                                    toy_mode = cms.bool(False),
                                    poisson_n1vs = cms.bool(True),
                                    sampling_type = cms.int32(2),
                                    sample_only = cms.int32(-1),
                                    npairs = cms.int32(100000),

                                    max_1v_ntracks01 = cms.int32(1000000),

                                    signal_files = cms.vstring(*[file_path % n for n in signal_samples]),
                                    signal_weights = cms.vdouble(*([2e-4]*nsignals)),
                                    signal_contamination = cms.int32(-1),

                                    find_g_dphi = cms.bool(True),
                                    use_form_g_dphi = cms.bool(False),
                                    form_g_dphi = cms.string('([0] + [1]*abs(x-3.14159265/2))/([0]*3.14159265 + [1]*2.46740110)'),

                                    find_g_dz = cms.bool(True),
                                    use_form_g_dz = cms.bool(False),
                                    form_g_dz = cms.string('1/sqrt(2*3.14159265*[0]**2)*exp(-x*x/2/[0]**2)'),

                                    find_f_dphi = cms.bool(True),
                                    find_f_dphi_bkgonly = cms.bool(False),
                                    use_form_f_dphi = cms.bool(False),
                                    form_f_dphi = cms.string('abs(x)**[0]/(3.14159265**([0]+1)/([0]+1))'),

                                    find_f_dz = cms.bool(True),
                                    find_f_dz_bkgonly = cms.bool(False),
                                    use_form_f_dz = cms.bool(False),
                                    form_f_dz = cms.string('1/sqrt(2*3.14159265*[0]**2)*exp(-x*x/2/[0]**2)'),

                                    do_by_means = cms.bool(False),

                                    template_range = cms.vdouble(0, 6.1, 0.25),
                                    template_binning = cms.vdouble(20000, 0, 10),
                                    template_fn = cms.string(''),
                                    template_dir = cms.string('mfvOne2Two'),
                                    )

process.p = cms.Path(process.mfvOne2Two)


import JMTucker.Tools.Samples as Samples
SampleInfo = namedtuple('SampleInfo', 'sample events_rel')
sample_infos = [
    SampleInfo(Samples.qcdht0500,     (1220, 1463, 1737, 2247)),
    SampleInfo(Samples.qcdht1000,     ( 112,  133,  157,  200)),
    SampleInfo(Samples.ttbardilep,    (   1,    1,    1,    1)),
    SampleInfo(Samples.ttbarhadronic, (  44,   46,   48,   53)),
    SampleInfo(Samples.ttbarsemilep,  (  14,   15,   15,   16)),
    ]

n1v_scales_no500 = {5: 102, 6: 69, 7: 44, 8: 23}
n1v_scales = {5: 9, 6: 6, 7: 3, 8: 2}

def sample_name(fn):
    return os.path.basename(fn).replace('.root', '')


if False:
    for arg in sys.argv:
        if arg.endswith('.root') and os.path.isfile(arg):
            process.TFileService.fileName = sample_name(arg) + '_histos.root'
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
            return val

    from_env('min_ntracks', int)
    min_ntracks = process.mfvOne2Two.min_ntracks.value()
    if not 5 <= min_ntracks <= 8:
        raise ValueError('min_ntracks must be 5-8')
    from_env('svdist2d_cut', float)
    from_env('just_print',   bool)
    from_env('seed',         int)
    toy_mode = from_env('toy_mode', bool)
    from_env('poisson_n1vs', bool)
    from_env('sampling_type',int)
    from_env('sample_only',  int)
    from_env('npairs',       int)
    from_env('signal_contamination', int)

    signal_scale = env.get('mfvo2t_signal_scale', None)
    if signal_scale:
        signal_scale = float(signal_scale)
        process.mfvOne2Two.signal_weights = [signal_scale*w for w in process.mfvOne2Two.signal_weights.value()]

    phi_exp = env.get(env_var('phi_exp'), '[0]')
    process.mfvOne2Two.form_f_dphi = process.mfvOne2Two.form_f_dphi.value().replace('[0]', phi_exp)

    sample = env.get(env_var('sample'), 'qcdht1000')
    if sample != 'all':
        process.mfvOne2Two.filenames = [file_path % sample]
    else:
        process.mfvOne2Two.toy_mode = toy_mode = True

        use_qcd500 = bool(env.get('mfvo2t_use_qcd500', ''))
        if not use_qcd500:
            n1v_scales = n1v_scales_no500
            sample_infos.pop(0)

        process.mfvOne2Two.filenames = [file_path % s.sample.name for s in sample_infos]

    samples = [sample_name(fn) for fn in process.mfvOne2Two.filenames]

    if toy_mode:
        int_lumi = float(env.get('mfvo2t_int_lumi', '20000'))

        n1vs, weights = [], []
        for s in sample_infos:
            if s.sample.name in samples:
                n1vs.append(s.events_rel[min_ntracks - 5] * n1v_scales[min_ntracks])
                weights.append(s.sample.partial_weight * int_lumi if len(samples) > 1 else 1)

        process.mfvOne2Two.n1vs = n1vs
        process.mfvOne2Two.weights = weights

    job_num = env.get('mfvo2t_job_num', '')
    if job_num:
        print 'in batch mode, job number', job_num, '\n'
        process.TFileService.fileName = '%s.one2two.root' % job_num
    
print 'CFG BEGIN'
for var in 'min_ntracks svdist2d_cut tree_path filenames n1vs weights just_print seed toy_mode poisson_n1vs sampling_type sample_only npairs max_1v_ntracks01 signal_files signal_weights signal_contamination find_g_dphi use_form_g_dphi form_g_dphi find_g_dz use_form_g_dz form_g_dz find_f_dphi find_f_dphi_bkgonly use_form_f_dphi form_f_dphi find_f_dz find_f_dz_bkgonly use_form_f_dz form_f_dz do_by_means template_binning template_fn template_dir'.split():
    print var.ljust(25), getattr(process.mfvOne2Two, var).value()
print 'CFG END'

'''
foreach sam (qcdht0100 qcdht0250 qcdht0500 qcdht1000 ttbardilep ttbarhadronic ttbarsemilep mfv_neutralino_tau0100um_M0400 mfv_neutralino_tau0300um_M0400 mfv_neutralino_tau1000um_M0400 mfv_neutralino_tau9900um_M0400)
  foreach ntk (5 6 7 8)
    env mfvo2t_just_print=1 mfvo2t_sample=$sam mfvo2t_min_ntracks=$ntk cmsRun one2two.py env >&! out.justprint_${ntk}_${sam}
  end
end
'''
