#!/usr/bin/env python

import os, re

year = None
yre = re.compile(r'^#define MFVNEUTRALINO_(\d{4,5})$')

for line in open(os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/Tools/interface/Year.h')):
    mo = yre.match(line.strip())
    if mo:
        assert year is None
        year = int(mo.group(1))

assert year in (2017, 2018, 20161, 20162)

__all__ = ['year']
