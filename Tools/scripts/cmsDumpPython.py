#!/usr/bin/env python

import os, sys, tempfile
from DVCode.Tools.general import bool_from_argv

remove_newlines = bool_from_argv('remove_newlines')
remove_blanks = bool_from_argv('remove_blanks')

in_fn = sys.argv[1]
tmp_f, tmp_fn = tempfile.mkstemp()
out_f, out_fn = tempfile.mkstemp()

file = os.fdopen(tmp_f, 'wt')
file.write(open(in_fn).read())
file.write('\nopen("%s", "wt").write(process.dumpPython())\n' % out_fn)
file.close()
os.system('python %s > /dev/null' % tmp_fn)

parens = 0

for line in os.fdopen(out_f):
    if remove_newlines:
        for c in line:
            if c in '{[(':
                parens += 1
            elif c in '}])':
                parens -= 1
        if parens:
            line = line.strip()
    if not remove_blanks or line.strip():
        print line,
