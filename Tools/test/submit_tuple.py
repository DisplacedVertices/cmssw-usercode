#!/usr/bin/env python

import os, sys, re

crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = %(scheduler)s

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = psets/jtuple_CCVERSION_%(name)s.py
get_edm_output = 1
%(job_control)s

[USER]
ui_working_dir = CCDIRECTORY
copy_data = 1
storage_element = T3_US_FNALLPC
check_user_remote_dir = 0
publish_data = 1
publish_data_name = jtuple_CCVERSION_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
'''

from JMTucker.Tools.PATTuple_cfg import version
base_directory = os.path.join('crab/tuple', version)
directory = os.path.join(base_directory, 'crab_jtuple_CCVERSION_%(name)s')
crab_cfg = crab_cfg.replace('CCDIRECTORY', directory)
crab_cfg = crab_cfg.replace('CCVERSION',   version)

just_testing = 'testing' in sys.argv

def submit(sample):
    os.system('mkdir -p crab/psets')
    os.system('ln -sf crab/psets')

    py_fn = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/Tools/python/PATTuple_cfg.py')
    new_py_fn = 'psets/jtuple_%s_%s.py' % (version, sample.name)
    
    new_py = open(py_fn).read()
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

    new_py += '\n' + '\n'.join(to_add) + '\n'
    open(new_py_fn, 'wt').write(new_py)
    open('crab.cfg', 'wt').write(crab_cfg % sample)

    if not just_testing:
        os.system('mkdir -p %s' % base_directory)
        os.system('crab -create -submit')
        os.system('rm crab.cfg')
    else:
        print '.py diff:\n---------'
        os.system('diff -uN %s %s' % (py_fn, new_py_fn))
        raw_input('ok?')
        print '\ncrab.cfg:\n---------'
        os.system('cat crab.cfg')
        raw_input('ok?')
        print

#from JMTucker.Tools.Samples import all_samples
#for sample in all_samples:
    
from JMTucker.Tools.Samples import TupleOnlyMCSample
samples = [
    TupleOnlyMCSample('mfv_temp_gluino_tau0000um_M1000', '/mfv_gensimhlt_gluino_tau0000um_M1000/tucker-mfv_reco_gluino_tau0000um_M1000-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0000um_M200', '/mfv_gensimhlt_gluino_tau0000um_M200/tucker-mfv_reco_gluino_tau0000um_M200-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0000um_M400', '/mfv_gensimhlt_gluino_tau0000um_M400/tucker-mfv_reco_gluino_tau0000um_M400-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0000um_M600', '/mfv_gensimhlt_gluino_tau0000um_M600/tucker-mfv_reco_gluino_tau0000um_M600-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0000um_M800', '/mfv_gensimhlt_gluino_tau0000um_M800/tucker-mfv_reco_gluino_tau0000um_M800-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0010um_M1000', '/mfv_gensimhlt_gluino_tau0010um_M1000/tucker-mfv_reco_gluino_tau0010um_M1000-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0010um_M200', '/mfv_gensimhlt_gluino_tau0010um_M200/tucker-mfv_reco_gluino_tau0010um_M200-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0010um_M400', '/mfv_gensimhlt_gluino_tau0010um_M400/tucker-mfv_reco_gluino_tau0010um_M400-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0010um_M600', '/mfv_gensimhlt_gluino_tau0010um_M600/tucker-mfv_reco_gluino_tau0010um_M600-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0010um_M800', '/mfv_gensimhlt_gluino_tau0010um_M800/tucker-mfv_reco_gluino_tau0010um_M800-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0100um_M1000', '/mfv_gensimhlt_gluino_tau0100um_M1000/tucker-mfv_reco_gluino_tau0100um_M1000-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0100um_M200', '/mfv_gensimhlt_gluino_tau0100um_M200/tucker-mfv_reco_gluino_tau0100um_M200-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0100um_M400', '/mfv_gensimhlt_gluino_tau0100um_M400/tucker-mfv_reco_gluino_tau0100um_M400-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0100um_M600', '/mfv_gensimhlt_gluino_tau0100um_M600/tucker-mfv_reco_gluino_tau0100um_M600-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau0100um_M800', '/mfv_gensimhlt_gluino_tau0100um_M800/tucker-mfv_reco_gluino_tau0100um_M800-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau1000um_M1000', '/mfv_gensimhlt_gluino_tau1000um_M1000/tucker-mfv_reco_gluino_tau1000um_M1000-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau1000um_M200', '/mfv_gensimhlt_gluino_tau1000um_M200/tucker-mfv_reco_gluino_tau1000um_M200-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau1000um_M400', '/mfv_gensimhlt_gluino_tau1000um_M400/tucker-mfv_reco_gluino_tau1000um_M400-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau1000um_M600', '/mfv_gensimhlt_gluino_tau1000um_M600/tucker-mfv_reco_gluino_tau1000um_M600-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau1000um_M800', '/mfv_gensimhlt_gluino_tau1000um_M800/tucker-mfv_reco_gluino_tau1000um_M800-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau4000um_M1000', '/mfv_gensimhlt_gluino_tau4000um_M1000/tucker-mfv_reco_gluino_tau4000um_M1000-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau4000um_M200', '/mfv_gensimhlt_gluino_tau4000um_M200/tucker-mfv_reco_gluino_tau4000um_M200-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau4000um_M400', '/mfv_gensimhlt_gluino_tau4000um_M400/tucker-mfv_reco_gluino_tau4000um_M400-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau4000um_M600', '/mfv_gensimhlt_gluino_tau4000um_M600/tucker-mfv_reco_gluino_tau4000um_M600-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau4000um_M800', '/mfv_gensimhlt_gluino_tau4000um_M800/tucker-mfv_reco_gluino_tau4000um_M800-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau9900um_M1000', '/mfv_gensimhlt_gluino_tau9900um_M1000/tucker-mfv_reco_gluino_tau9900um_M1000-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau9900um_M200', '/mfv_gensimhlt_gluino_tau9900um_M200/tucker-mfv_reco_gluino_tau9900um_M200-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau9900um_M400', '/mfv_gensimhlt_gluino_tau9900um_M400/tucker-mfv_reco_gluino_tau9900um_M400-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau9900um_M600', '/mfv_gensimhlt_gluino_tau9900um_M600/tucker-mfv_reco_gluino_tau9900um_M600-4b815091ea4b0e75a52a1ca758900a17/USER'),
    TupleOnlyMCSample('mfv_temp_gluino_tau9900um_M800', '/mfv_gensimhlt_gluino_tau9900um_M800/tucker-mfv_reco_gluino_tau9900um_M800-4b815091ea4b0e75a52a1ca758900a17/USER'),
    ]

for sample in samples:
    mo = re.search(r'tau0*(\d+)um_M0*(\d+)', sample.name)
    sample.tau  = int(mo.group(1))
    sample.mass = int(mo.group(2))
    sample.is_pythia8 = True
    sample.scheduler_name = 'condor'
    sample.dbs_url_num = 2
    submit(sample)
