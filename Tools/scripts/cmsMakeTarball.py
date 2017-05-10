#!/usr/bin/env python

import sys, os, argparse
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.CMSSWTools import make_tarball

parser = argparse.ArgumentParser(description = 'cmsMakeTarball.py: make a tarball suitable for distribution to grid sites a la crab')
parser.add_argument('tarball_fn', help='The desired tarball fn.')
parser.add_argument('--verbose', action='store_true', help='Turn on verbosity.')
parser.add_argument('--include-bin', action='store_true', help='Whether to include the bin dirs.')
parser.add_argument('--no-include-python', action='store_false', dest='include_python', help='Whether to include the python dirs.')
parser.add_argument('--no-include-interface', action='store_false', dest='include_interface', help='Whether to include the interface dirs.')
options = parser.parse_args()

if os.path.exists(options.tarball_fn):
    raise IOError('refusing to clobber %s' % options.tarball_fn)

make_tarball(options.tarball_fn,
             verbose=options.verbose,
             include_bin=options.include_bin,
             include_python=options.include_python,
             include_interface=options.include_interface)
