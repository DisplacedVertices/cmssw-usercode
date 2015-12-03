import sys, FWCore.ParameterSet.Config as cms
from JMTucker.Tools.CMSSWTools import \
    basic_process, \
    files_from_file, \
    file_event_from_argv, \
    global_tag, \
    geometry_etc, \
    report_every, \
    tfileservice, \
    add_analyzer as _add_analyzer

process = basic_process('BasicAnalyzer')
report_every(process, 1000000)
tfileservice(process)

def add_analyzer(process, name, **kwargs):
    return _add_analyzer(process, name, **kwargs)

__all__ = [
    'cms',
    'process',
    'files_from_file',
    'file_event_from_argv',
    'geometry_etc',
    'global_tag',
    'tfileservice',
    'add_analyzer',
    'report_every'
    ]
