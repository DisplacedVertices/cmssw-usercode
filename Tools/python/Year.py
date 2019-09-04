#!/usr/bin/env python

import os

year = None
magic = '#define MFVNEUTRALINO_'

for line in open(os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/Tools/interface/Year.h')):
    line = line.strip()
    if line.startswith(magic):
        if year is not None:
            assert line.startswith(magic + 'YEAR 201')
            continue
        year = int(line.replace(magic, ''))

assert year in (2015, 2016, 2017, 2018)

__all__ = ['year']
