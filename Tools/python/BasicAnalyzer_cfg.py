#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
from DVCode.Tools.CMSSWTools import *

process = basic_process('BasicAnalyzer')
report_every(process, 1000000)
tfileservice(process)

_add_analyzer = add_analyzer 
def add_analyzer(process, name, *args, **kwargs):
    return _add_analyzer(process, name, *args, **kwargs)
