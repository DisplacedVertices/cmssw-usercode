#!/usr/bin/env python

import sys, os, argparse
from DVCode.Tools.CMSSWTools import make_tarball

parser = argparse.ArgumentParser(description = 'cmsMakeTarball.py: make a tarball suitable for distribution to grid sites a la crab')
parser.add_argument('tarball_fn', help='The desired tarball fn.')
parser.add_argument('--verbose', action='store_true', help='Turn on verbosity.')
parser.add_argument('--include-bin', action='store_true', help='Whether to include the bin dirs.')
parser.add_argument('--no-include-python', action='store_false', dest='include_python', help='Whether to include the python dirs.')
parser.add_argument('--no-include-interface', action='store_false', dest='include_interface', help='Whether to include the interface dirs.')
parser.add_argument('--standalone', action='store_true', help='Instead of running make_tarball, dump this script to stdout in standalone version. (You still have to supply a dummy arg for the tarball name.)')
options = parser.parse_args()

if options.standalone:
    import inspect
    script = inspect.getsource(inspect.getmodule(inspect.currentframe()))
    fcn = inspect.getsource(make_tarball)
    print script.replace('from DVCode.Tools.CMSSWTools import make_tarball\n', fcn)
else:
    if os.path.exists(options.tarball_fn):
        raise IOError('refusing to clobber %s' % options.tarball_fn)

    make_tarball(options.tarball_fn,
                 verbose=options.verbose,
                 include_bin=options.include_bin,
                 include_python=options.include_python,
                 include_interface=options.include_interface)
