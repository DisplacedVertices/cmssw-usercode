#!/usr/bin/env python

import os, sys

crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = %(scheduler)s
%(use_server)s

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = tuple_crab.py
get_edm_output = 1
%(job_control)s

[USER]
ui_working_dir = CCDIRECTORY
copy_data = 1
storage_element = T3_US_Cornell
publish_data = 1
publish_data_name = jtuple_CCVERSION_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
'''

from JMTucker.Tools.PATTuple_cfg import version
directory = 'crab/tuple/CCVERSION/crab_jtuple_CCVERSION_%(name)s'
crab_cfg = crab_cfg.replace('CCDIRECTORY', directory)
crab_cfg = crab_cfg.replace('CCVERSION',   version)

just_testing = 'testing' in sys.argv

def submit(sample):
    new_py = open(os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/Tools/python/PATTuple_cfg.py')).read()
    to_add = []

    if sample.is_mc:
        if sample.is_fastsim:
            to_add.append('input_is_fastsim()')
        if sample.is_pythia8:
            to_add.append('input_is_pythia8()')
        if 'mfv' in sample.name:
            to_add.append('keep_general_tracks()')
    else:
        magic = 'runOnMC = True'
        if magic not in new_py:
            raise ValueError('trying to submit on data, and tuple.py does not contain the magic string "%s"' % magic)
        new_py = new_py.replace(magic, 'runOnMC = False')

    new_py += '\n' + '\n'.join(to_add)
    open('tuple_crab.py', 'wt').write(new_py)
    open('crab.cfg', 'wt').write(crab_cfg % sample)

    if not just_testing:
        os.system('mkdir -p %s' % directory)
        os.system('crab -create -submit')
        os.system('cp tuple_crab.py %s' os.path.join()
        os.system('rm crab.cfg tuple_crab.py tuple_crab.pyc')
    else:
        print '.py diff:\n---------'
        os.system('diff -uN tuple.py tuple_crab.py')
        raw_input('ok?')
        print '\ncrab.cfg:\n---------'
        os.system('cat crab.cfg')
        raw_input('ok?')
        print

from JMTucker.Tools.Samples import background_samples, stop_signal_samples, mfv_signal_samples, data_samples
for sample in mfv_signal_samples + stop_signal_samples + background_samples + data_samples:
    submit(sample)
