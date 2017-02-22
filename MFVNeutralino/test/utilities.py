#!/usr/bin/env python

import sys, os
from JMTucker.Tools import Samples
from JMTucker.Tools import SampleFiles
from JMTucker.Tools.hadd import hadd
from JMTucker.MFVNeutralino import AnalysisConstants
 
def cmd_hadd_vertexer_histos():
    ntuple = sys.argv[2]
    samples = Samples.registry.from_argv()

    for s in samples:
        s.set_curr_dataset(ntuple)
        hadd(s.name + '.root', ['root://cmseos.fnal.gov/' + fn.replace('ntuple', 'vertex_histos') for fn in s.filenames])

def cmd_hadd_qcd_sum():
    for x in [500, 700, 1000, 1500, 2000]:
        base = 'qcdht%04i' % x
        a = base + '.root'
        b = base + 'ext.root'
        if not os.path.isfile(a) or not os.path.isfile(b):
            print 'skipping', x, 'because at least one input file missing'
        else:
            hadd(base + 'sum.root', a, b)

def cmd_merge_background():
    files = ['ttbar.root']
    files += ['qcdht%04isum.root' % x for x in [500, 700, 1000, 1500, 2000]]
    for fn in files:
        if not os.path.isfile(fn):
            raise RuntimeError('%s not found' % fn)
    scale = -AnalysisConstants.int_lumi * AnalysisConstants.scale_factor
    cmd = 'python ' + os.environ['CMSSW_BASE'] + '/src/JMTucker/Tools/python/Samples.py merge %f background.root ' % scale
    cmd += ' '.join(files)
    print cmd
    os.system(cmd)

def cmd_effsprint():
    for which, which_files in [('background', '.'), ('signals', 'mfv*root xx4j*root')]:
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
