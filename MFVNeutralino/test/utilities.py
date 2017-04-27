#!/usr/bin/env python

import sys, os
from pprint import pprint
from glob import glob
from JMTucker.Tools import Samples
from JMTucker.Tools import SampleFiles
from JMTucker.Tools.general import bool_from_argv
from JMTucker.Tools.hadd import hadd
from JMTucker.Tools.CMSSWTools import is_edm_file, merge_edm_files
from JMTucker.MFVNeutralino import AnalysisConstants

def hadd_or_merge(out_fn, files):
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
        for year in 2015, 2016:
            if not glob('*%s%i*' % (ds, year)):
                continue
            os.system('mreport c*_%s%i*' % (ds, year))
            print 'jsondiff'
            os.system('compareJSON.py --diff processedLumis.json $CMSSW_BASE/src/JMTucker/MFVNeutralino/test/ana_avail_%i%s_10pc.json' % (year, ex))
            raw_input('ok?')
            os.rename('processedLumis.json', 'dataok_%i.json' % year)

def cmd_hadd_data():
    for ds in 'SingleMuon', 'JetHT':
        files = glob(ds + '*.root')
        if not files:
            continue
        files.sort()

        if files != [ds + '2015%s.root' % x for  x in 'CD'] + [ds + '2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F', 'G', 'H2', 'H3')]:
            print 'some files missing for', ds
            pprint(files)
        else:
            hadd_or_merge(ds + '2015.root', [ds + '2015%s.root' % x for x in 'CD'])
            hadd_or_merge(ds + '2016.root', [ds + '2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F', 'G', 'H2', 'H3')])
            hadd_or_merge(ds + '2016BthruG.root', [ds + '2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F', 'G')])
            hadd_or_merge(ds + '2016BCD.root', [ds + '2016%s.root' % x for x in ('B3', 'C', 'D')])
            hadd_or_merge(ds + '2016EF.root', [ds + '2016%s.root' % x for x in ('E', 'F')])
            hadd_or_merge(ds + '2016H.root', [ds + '2016%s.root' % x for x in ('H2', 'H3')])

cmd_merge_data = cmd_hadd_data

def cmd_hadd_qcd_sum():
    for is2015_s in '_2015', '':
        for x in [500, 700, 1000, 1500, 2000]:
            base = 'qcdht%04i' % x
            if is2015_s:
                a = base + '_2015.root'
                b = base + 'ext_2015.root'
            else:
                a = base + '.root'
                b = base + 'ext.root'
            if not os.path.isfile(a) or not os.path.isfile(b):
                print 'skipping', x, 'because at least one input file missing'
            else:
                hadd_or_merge(base + 'sum%s.root' % is2015_s, [a, b])

cmd_merge_qcd_sum = cmd_hadd_qcd_sum

def cmd_merge_background():
    permissive = bool_from_argv('permissive')
    for is2015_s, scale in ('', -AnalysisConstants.int_lumi_2016 * AnalysisConstants.scale_factor_2016), ('_2015', -AnalysisConstants.int_lumi_2015 * AnalysisConstants.scale_factor_2015):
        files = ['ttbar.root']
        files += ['qcdht%04isum.root' % x for x in [500, 700, 1000, 1500, 2000]]
        if is2015_s:
            files = [fn.replace('.root', '_2015.root') for fn in files]
        for fn in files:
            if not os.path.isfile(fn):
                msg = '%s not found' % fn
                if permissive:
                    print msg
                    files.remove(fn)
                else:
                    raise RuntimeError(msg)
        cmd = 'python ' + os.environ['CMSSW_BASE'] + '/src/JMTucker/Tools/python/Samples.py merge %f background%s.root ' % (scale, is2015_s)
        cmd += ' '.join(files)
        print cmd
        os.system(cmd)

def cmd_effsprint():
    for which, which_files in [('background', '.'), ('signals', '*mfv*root xx4j*root')]:
        for ntk in (3,4,'3or4',5):
            for vtx in (1,2):
                out = 'effsprint_%s_ntk%s_%iv' % (which, ntk, vtx)
                cmd = 'python ' + os.environ['CMSSW_BASE'] + '/src/JMTucker/MFVNeutralino/test/effsprint.py'
                cmd += ' ntk%s' % ntk
                if vtx == 1:
                    cmd += ' one'
                print cmd
                os.system('%s %s | tee %s' % (cmd, which_files, out))
                print

def cmd_histos():
    cmd_report_data()
    cmd_hadd_qcd_sum()
    cmd_merge_background()
    cmd_effsprint()

def cmd_minitree():
    cmd_report_data()
    cmd_hadd_qcd_sum()

def cmd_trigeff():
    cmd_report_data()

    hadd('SingleMuon2015.root', ['SingleMuon2015%s.root' % x for x in 'CD'])
    hadd('SingleMuon2016BthruG.root', ['SingleMuon2016%s.root' % x for x in ('B3', 'C', 'D', 'E', 'F', 'G')])
    hadd('SingleMuon2016H.root', ['SingleMuon2016%s.root' % x for x in ('H2', 'H3')])
    hadd('dyjetstollM10sum_2015.root', ['dyjetstollM10%s_2015.root' % x for x in '123'])
    hadd('dyjetstollM50sum_2015.root', ['dyjetstollM50%s_2015.root' % x for x in '123'])
    hadd('wjetstolnusum_2015.root', ['wjetstolnu%s_2015.root' % x for x in '123'])

    for is2015_s, scale in ('', -AnalysisConstants.int_lumi_2016), ('_2015', -AnalysisConstants.int_lumi_2015):
        for wqcd_s in '', '_wqcd':
            cmd = 'python ' + os.environ['CMSSW_BASE'] + '/src/JMTucker/Tools/python/Samples.py merge %f background%s%s.root ' % (scale, wqcd_s, is2015_s)
            if is2015_s:
                files = 'ttbar_2015.root wjetstolnusum_2015.root dyjetstollM10sum_2015.root dyjetstollM50sum_2015.root'.split()
            else:
                files = 'ttbar.root wjetstolnu.root dyjetstollM10.root dyjetstollM50.root'.split()
            if wqcd_s:
                files.append('qcdmupt15_2015.root' if is2015_s else 'qcdmupt15.root')
            for fn in files:
                if not os.path.isfile(fn):
                    raise RuntimeError('%s not found' % fn)
            cmd += ' '.join(files)
            print cmd
            os.system(cmd)

def cmd_merge_bquarks_nobquarks():
    for year in ['2015', '2016', '2015p6']:
        weights = '0.86,0.14' if year=='2015' else '0.77,0.23' if year=='2016' else '0.78,0.22'
        for ntracks in [3,4,5]:
            files = ['One2Two/2v_from_jets_%s_%dtrack_bquarks_v14.root' % (year, ntracks), 'One2Two/2v_from_jets_%s_%dtrack_nobquarks_v14.root' % (year, ntracks)]
            for fn in files:
                if not os.path.isfile(fn):
                    raise RuntimeError('%s not found' % fn)
            cmd = 'mergeTFileServiceHistograms -w %s -i %s -o One2Two/2v_from_jets_%s_%dtrack_vary_dbv_v14.root' % (weights, ' '.join(files), year, ntracks)
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
