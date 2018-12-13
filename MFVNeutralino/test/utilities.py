#!/usr/bin/env python

import sys, os, shutil
from pprint import pprint
from glob import glob
from time import time
from JMTucker.Tools import Samples
from JMTucker.Tools import SampleFiles
from JMTucker.Tools.general import bool_from_argv
from JMTucker.Tools.hadd import hadd
from JMTucker.Tools.CMSSWTools import is_edm_file, merge_edm_files, cmssw_base, json_path
from JMTucker.MFVNeutralino import AnalysisConstants

def hadd_or_merge(out_fn, files):
    files = [fn for fn in files if os.path.exists(fn)]
    print out_fn, files
    if not files:
        print 'skipping', out_fn, 'because no files'
    is_edm = set([is_edm_file(f) for f in files])
    if len(is_edm) != 1:
        raise ValueError('uh you have a mix of edm and non-edm files?')
    is_edm = is_edm.pop()
    (merge_edm_files if is_edm else hadd)(out_fn, files)

_leptonpresel = bool_from_argv('leptonpresel')
_presel_s = '_leptonpresel' if _leptonpresel else ''

####

def cmd_hadd_vertexer_histos():
    ntuple = sys.argv[2]
    samples = Samples.registry.from_argv(
            Samples.data_samples_2015 + \
            Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015 + \
            Samples.data_samples + \
            Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext)
    for s in samples:
        s.set_curr_dataset(ntuple)
        hadd(s.name + '.root', ['root://cmseos.fnal.gov/' + fn.replace('ntuple', 'vertex_histos') for fn in s.filenames])

def cmd_report_data():
    for ds, ex in ('SingleMuon', '_mu'), ('JetHT', ''):
        pc = ''
        if '10pc' in sys.argv:
            pc = '10pc'
            ex += '_10pc'
        elif '1pc' in sys.argv:
            pc = '1pc'
            ex += '_1pc'

        for year in 2017, 2018:
            if not glob('*%s%i*' % (ds, year)):
                continue

            os.system('mreport c*_%s%i* %s' % (ds, year, pc))
            json_fn = 'processedLumis.json'
            if not os.path.isfile(json_fn):
                raise IOError('something went wrong with mreport?')

            print 'jsondiff'
            avail_fn = json_path('ana_avail_%i%s.json' % (year, ex))
            ok = False
            if not os.path.isfile(avail_fn):
                if raw_input('no file %s, enter y to create it: ' % avail_fn)[0] == 'y':
                    shutil.copy(json_fn, avail_fn)
                    ok = True
            else:
                os.system('compareJSON.py --diff %s %s' % (json_fn, avail_fn))
                if raw_input('enter y if ok: ') == 'y':
                    ok = True
            if ok:
                os.rename('processedLumis.json', 'dataok_%i.json' % year)
            else:
                bad_fn = '%s.bad.%i' % (json_fn, int(time()))
                print 'saving %s as %s' % (json_fn, bad_fn)
                os.rename(json_fn, bad_fn)

def cmd_hadd_data():
    permissive = bool_from_argv('permissive')
    for ds in 'SingleMuon', 'JetHT', 'ZeroBias':
        print ds
        files = set(glob(ds + '*.root'))
        if not files:
            print 'no files for this ds'
            continue

        have = []
        year_eras = [
            ('2017', 'BCDEF'),
            ('2018', 'ABCD'),
            ]

        for year, eras in year_eras:
            files = [f for x in eras for f in glob('%s%s%s.root' % (ds, year, x))]
            ok = len(files) == len(eras)
            if not ok:
                print 'some files missing for %s %s: only have %r' % (ds, year, files)
            if ok or permissive:
                hadd_or_merge('%s%s.root' % (ds, year), files)
                have.append(year)

        if '2017' in have and '2018' in have:
            hadd_or_merge(ds + '2017p8.root', ['%s%s.root' % (ds, year) for year in '2017', '2018'])

cmd_merge_data = cmd_hadd_data

def _mc_parts():
    for year in 2017,:
        for base in 'dyjetstollM50', 'wjetstolnu':
            a = '%s_%s.root' % (base, year)
            b = '%sext_%s.root' % (base, year)
            c = '%ssum_%s.root' % (base, year)
            yield (year,base), (a,b,c)

def cmd_hadd_mc_sums():
    for (year,base), (a,b,c) in _mc_parts():
        if not os.path.isfile(a) or not os.path.isfile(b):
            print 'skipping', year, base, 'because at least one input file missing'
        elif os.path.isfile(c):
            print 'skipping', year, base, 'because', c, 'already exists'
        else:
            hadd_or_merge(c, [a, b])

cmd_merge_mc_sums = cmd_hadd_mc_sums

def cmd_rm_mc_parts():
    for (year,base), (a,b,c) in _mc_parts():
        if os.path.isfile(c):
            for y in a,b:
                if os.path.isfile(y):
                    print y
                    os.remove(y)

def _background_samples(trigeff=False):
    if _leptonpresel or trigeff:
        x = ['ttbar', 'wjetstolnusum', 'dyjetstollM10', 'dyjetstollM50sum', 'qcdmupt15']
        if not trigeff:
            x += ['qcdempt%03i' % x for x in [15,20,30,50,80,120,170,300]]
            x += ['qcdbctoept%03i' % x for x in [15,20,30,80,170,250]]
    else:
        x = ['qcdht%04i' % x for x in [700, 1000, 1500, 2000]] + ['ttbarht%04i' % x for x in [600, 800, 1200, 2500]]
    return x

def cmd_merge_background():
    permissive = bool_from_argv('permissive')
    for year_s, scale in ('_2017', -AnalysisConstants.int_lumi_2017 * AnalysisConstants.scale_factor_2017),:
        files = _background_samples()
        files = ['%s%s.root' % (x, year_s) for x in files]
        files2 = []
        for fn in files:
            if not os.path.isfile(fn):
                msg = '%s not found' % fn
                if permissive:
                    print msg
                else:
                    raise RuntimeError(msg)
            else:
                files2.append(fn)
        if files2:
            cmd = 'samples merge %f background%s%s.root ' % (scale, _presel_s, year_s)
            cmd += ' '.join(files2)
            print cmd
            os.system(cmd)

def cmd_effsprint():
    background_fns = ' '.join(x + '_2017.root' for x in _background_samples())
    todo = [('background', background_fns), ('signals', 'mfv*root')]
    def do(cmd, outfn):
        cmd = 'python %s %s' % (cmssw_base('src/JMTucker/MFVNeutralino/test/effsprint.py'), cmd)
        print cmd
        os.system('%s | tee %s' % (cmd, outfn))
        print
    for which, which_files in todo:
        for ntk in 3,4,'3or4',5:
            for vtx in 1,2:
                cmd = 'ntk%s' % ntk
                if which == 'background':
                    cmd += ' sum'
                if vtx == 1:
                    cmd += ' one'
                cmd += ' ' + which_files
                outfn = 'effsprint_%s%s_ntk%s_%iv' % (which, _presel_s, ntk, vtx)
                do(cmd, outfn)
    do('presel sum ' + background_fns, 'effsprint_presel')
    do('nocuts sum ' + background_fns, 'effsprint_nocuts')

def cmd_histos():
    cmd_report_data()
    cmd_hadd_data()
    cmd_merge_background()
    cmd_effsprint()

def cmd_presel():
    cmd_report_data()
    cmd_hadd_data()
    cmd_merge_background()

def cmd_vpeffs():
    cmd_report_data()
    cmd_hadd_data()
    cmd_merge_background()

def cmd_minitree():
    cmd_report_data()
    cmd_hadd_data()

def cmd_trackmover():
    cmd_report_data()
    cmd_hadd_data()

def cmd_v0eff():
    cmd_hadd_data()
    scale = -AnalysisConstants.int_lumi_2015p6 * AnalysisConstants.scale_factor_2015p6
    for fn,files in [
        ('qcd.root', ['qcdht%04isum.root' % x for x in (500, 700, 1000, 1500, 2000)]),
        ('qcdht1000and1500.root', ['qcdht%04isum.root' % x for x in (1000, 1500)]),
        ('qcdht1000and1500_hip1p0_mit.root', ['qcdht%04i_hip1p0_mit.root' % x for x in (1000, 1500)]),
        ]:
        cmd = 'python ' + os.environ['CMSSW_BASE'] + '/src/JMTucker/Tools/python/Samples.py merge %f %s %s' % (scale, fn, ' '.join(files))
        print cmd
        os.system(cmd)
    os.mkdir('no')
    for fn in ['qcdht%04i%s.root' % (x,y) for x in [500, 700, 1000, 1500, 2000] for y in ['', 'ext', 'sum']] + ['qcdht1000_hip1p0_mit.root', 'qcdht1500_hip1p0_mit.root'] + ['%s2016H%i.root' % (x,y) for x in ['JetHT', 'ZeroBias'] for y in [2,3]]:
        os.rename(fn, 'no/' + fn)

def cmd_trigeff():
    cmd_hadd_mc_sums()
    cmd_report_data()
    cmd_hadd_data()

    permissive = bool_from_argv('permissive')
    for year_s, scale in ('_2017', -AnalysisConstants.int_lumi_2017),:
        for wqcd_s in '', '_wqcd':
            files = _background_samples(trigeff=True)
            if not wqcd_s:
                files.remove('qcdmupt15')
            files = ['%s%s.root' % (x, year_s) for x in files]
            files2 = []
            for fn in files:
                if not os.path.isfile(fn):
                    msg = '%s not found' % fn
                    if permissive:
                        print msg
                    else:
                        raise RuntimeError(msg)
                else:
                    files2.append(fn)

            if files2:
                cmd = 'samples merge %f background%s%s.root %s' % (scale, wqcd_s, year_s, ' '.join(files2))
                print cmd
                os.system(cmd)

def cmd_merge_bquarks_nobquarks():
    for year in ['2017']:
        weights = '0.79,0.21'
        for ntracks in [3,4,5,7]:
            files = ['One2Two/2v_from_jets_%s_%dtrack_bquarks_v21m.root' % (year, ntracks), 'One2Two/2v_from_jets_%s_%dtrack_nobquarks_v21m.root' % (year, ntracks)]
            for fn in files:
                if not os.path.isfile(fn):
                    raise RuntimeError('%s not found' % fn)
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o One2Two/2v_from_jets_%s_%dtrack_bquark_corrected_v21m.root' % (weights, ' '.join(files), year, ntracks)
            print cmd
            os.system(cmd)

####

cmd = sys.argv[1] if len(sys.argv) > 1 else ''
cmds = locals()

if not cmds.has_key('cmd_' + cmd):
    print 'valid cmds are:'
    for cmd in sorted(cmds.keys()):
        if cmd.startswith('cmd_'):
            print cmd.replace('cmd_', '')
    sys.exit(1)

cmds['cmd_' + cmd]()
