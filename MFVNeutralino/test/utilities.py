#!/usr/bin/env python

import sys, os
from pprint import pprint
from glob import glob
from JMTucker.Tools import Samples
from JMTucker.Tools import SampleFiles
from JMTucker.Tools.general import bool_from_argv
from JMTucker.Tools.hadd import hadd
from JMTucker.Tools.CMSSWTools import is_edm_file, merge_edm_files, cmssw_base
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
        if '10pc' in sys.argv:
            ex += '_10pc'
        for year in 2017,:
            if not glob('*%s%i*' % (ds, year)):
                continue
            os.system('mreport c*_%s%i*' % (ds, year))
            print 'jsondiff'
            os.system('compareJSON.py --diff processedLumis.json $CMSSW_BASE/src/JMTucker/MFVNeutralino/test/jsons/ana_avail_%i%s.json' % (year, ex))
            raw_input('ok?')
            os.rename('processedLumis.json', 'dataok_%i.json' % year)

def cmd_hadd_data():
    print 'skipping hadd_data, not yet implemented'
    return
    permissive = bool_from_argv('permissive')
    for ds in 'SingleMuon', 'JetHT', 'ZeroBias':
        print ds
        files = glob(ds + '*.root')
        if not files:
            print 'no files for this ds'
            continue
        files.sort()

        Halready = len([x for x in files if x.endswith('H.root')]) > 0
        f2015 = [ds + '2015%s.root' % x for x in 'CD']
        f2016 = [ds + '2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F', 'G', 'H2', 'H3')]
        f2016Halready = [ds + '2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F', 'G', 'H')]
        ok = True
        no2015 = False
        if files == f2016 or files == f2016Halready:
            print 'only 2016 files here, right?'
            no2015 = True
        elif files != f2015 + f2016 and files != f2015 + f2016Halready:
            print 'some files missing for', ds
            pprint(files)
            if not permissive:
                ok = False
        if ok:
            if not no2015:
                hadd_or_merge(ds + '2015.root', [ds + '2015%s.root' % x for x in 'CD'])
            H =  ('H',) if Halready else ('H2', 'H3')
            hadd_or_merge(ds + '2016.root', [ds + '2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F', 'G') + H])
            hadd_or_merge(ds + '2016BthruG.root', [ds + '2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F', 'G')])
            hadd_or_merge(ds + '2016BCD.root', [ds + '2016%s.root' % x for x in ('B3', 'C', 'D')])
            hadd_or_merge(ds + '2016EF.root', [ds + '2016%s.root' % x for x in ('E', 'F')])
            hadd_or_merge(ds + '2016BCDEF.root', [ds + '2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F')])
            if not Halready:
                hadd_or_merge(ds + '2016H.root', [ds + '2016%s.root' % x for x in ('H2', 'H3')])
            hadd_or_merge(ds + '2016GH.root', [ds + '2016%s.root' % x for x in ('G',) + H])
        if not no2015:
            hadd_or_merge(ds + '2015p6.root', [ds + '2015.root', ds + '2016.root'])

cmd_merge_data = cmd_hadd_data

def cmd_merge_background():
    permissive = bool_from_argv('permissive')
    for year_s, scale in ('_2017', -AnalysisConstants.int_lumi_2017 * AnalysisConstants.scale_factor_2017),:
        files = ['ttbar']
        files += ['qcdht%04i' % x for x in [700, 1000, 1500, 2000]]
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
            cmd = 'samples merge %f background%s.root ' % (scale, year_s)
            cmd += ' '.join(files2)
            print cmd
            os.system(cmd)

def cmd_effsprint():
    if 'allmc' in sys.argv:
        which = 'all'
        which_files = []
        for x in 'qcd', 'ttbar', 'mfv':
            which_files += [fn for fn in glob(x + '*.root')]
        which_files = ' '.join(sorted(which_files))
        todo = [(which, which_files)]
    else:
        todo = [('background', '.'), ('signals', '*mfv*root')]
    def do(cmd, outfn):
        cmd = 'python %s %s' % (cmssw_base('src/JMTucker/MFVNeutralino/test/effsprint.py'), cmd)
        print cmd
        os.system('%s | tee %s' % (cmd, outfn))
        print
    for which, which_files in todo:
        for ntk in (3,4,'3or4',5):
            for vtx in (1,2):
                cmd = 'ntk%s' % ntk
                if vtx == 1:
                    cmd += ' one'
                cmd += ' ' + which_files
                outfn = 'effsprint_%s_ntk%s_%iv' % (which, ntk, vtx)
                do(cmd, outfn)
    do('presel .', 'effsprint_presel')
    do('nocuts .', 'effsprint_nocuts')

def cmd_histos():
    cmd_report_data()
    cmd_hadd_data()
    cmd_merge_background()
    cmd_effsprint()

def cmd_minitree():
    cmd_report_data()

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
    cmd_report_data()

    hadd('SingleMuon2017.root', ['SingleMuon2017%s.root' % x for x in 'BCDEF'])

    for year_s, scale in ('_2017', -AnalysisConstants.int_lumi_2017),:
        for wqcd_s in '', '_wqcd':
            cmd = 'samples merge %f background%s%s.root ' % (scale, wqcd_s, year_s)
            files = 'ttbar.root wjetstolnu.root dyjetstollM10.root dyjetstollM50.root'
            if wqcd_s:
                files += ' qcdmupt15.root'
            files = files.replace('.root', year_s + '.root').split()
            for fn in files:
                if not os.path.isfile(fn):
                    raise RuntimeError('%s not found' % fn)
            cmd += ' '.join(files)
            print cmd
            os.system(cmd)

def cmd_merge_bquarks_nobquarks():
    for year in ['2015', '2016', '2015p6']:
        weights = '0.86,0.14' if year=='2015' else '0.78,0.22'
        for ntracks in [3,4,5,7]:
            files = ['One2Two/2v_from_jets_%s_%dtrack_bquarks_v15.root' % (year, ntracks), 'One2Two/2v_from_jets_%s_%dtrack_nobquarks_v15.root' % (year, ntracks)]
            for fn in files:
                if not os.path.isfile(fn):
                    raise RuntimeError('%s not found' % fn)
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o One2Two/2v_from_jets_%s_%dtrack_bquark_corrected_v15.root' % (weights, ' '.join(files), year, ntracks)
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
