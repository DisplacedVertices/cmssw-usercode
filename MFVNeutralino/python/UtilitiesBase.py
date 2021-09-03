#!/usr/bin/env python

import sys, os, shutil
from pprint import pprint
from glob import glob
from time import time
from DVCode.Tools import Samples, SampleFiles, colors
from DVCode.Tools.general import bool_from_argv
from DVCode.Tools.hadd import hadd
from DVCode.Tools.CMSSWTools import is_edm_file, merge_edm_files, cmssw_base, json_path
from DVCode.MFVNeutralino import AnalysisConstants

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

def main(cmds):
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''

    if not cmds.has_key('cmd_' + cmd):
        print 'valid cmds are:'
        for cmd in sorted(cmds.keys()):
            if cmd.startswith('cmd_'):
                print cmd.replace('cmd_', '')
        sys.exit(1)

    cmds['cmd_' + cmd]()
