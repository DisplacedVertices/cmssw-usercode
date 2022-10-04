#!/usr/bin/env python

import sys
import os
import subprocess
import stat
from JMTucker.Tools.CMSSWTools import cmssw_base

def make_bash_file(cmssw_tar_path, bash_file_path):
  cmssw_name = cmssw_base().rsplit("/")[-1]
  bash_meat = '''#!/bin/bash
workdir=$(pwd)
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
export SCRAM_ARCH=__SCRAM_ARCH__
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project CMSSW __CMSSW_VERSION__ 2>&1 > /dev/null
scramexit=$?
if [[ $scramexit -ne 0 ]]; then
    echo scram exited with code $scramexit
    exit $scramexit
fi
cd __CMSSW_VERSION__
tar xf ${workdir}/input.tgz
cd src
eval `scram ru -sh`
scram b -j 2 2>&1 > /dev/null

#python JMTucker/Tools/python/hadd.py $1 ${@:2}
cd ${workdir}
hadd.py $1 ${@:2}
''' \
.replace('__SCRAM_ARCH__',    os.environ['SCRAM_ARCH']) \
.replace('__CMSSW_VERSION__', os.environ['CMSSW_VERSION'])

  bash_file = open(bash_file_path+'/bash_condor.sh', 'w')
  bash_file.write(bash_meat)
  bash_file.close()
  subprocess.check_call(['chmod', '+x', bash_file_path+'/bash_condor.sh'])
  return


def hadd_on_condor(new_name, job_dir, cmssw_tar_path, input_files):
  output_file_path = os.path.dirname(os.path.abspath(new_name))
  new_nice_name = (new_name.rsplit("/")[-1]).replace('.root','')
  job_dir = os.path.abspath(job_dir)
  cmssw_tar_path = os.path.abspath(cmssw_tar_path)
  is_eos = '/store/' in new_name
  if not is_eos:
    new_name = new_nice_name+'.root'
    
  hadd_job_dir = job_dir+'/mhadd/'
  if not os.path.exists(hadd_job_dir):
    os.mkdir(hadd_job_dir)

  make_bash_file(cmssw_tar_path, hadd_job_dir)
  
  #requirements necessary for wisconsin machines -- comment out if not needed
  #    the CentOS == 7 requires proxy with 2048 bit and will fail with usual 1024
  #    voms-proxy-init -rfc -valid 144:00 -voms cms -bits 2048
  condorFile = open(hadd_job_dir+'/submit_'+new_nice_name, 'w')
  condorFile.write('universe              = vanilla\n')
  condorFile.write('executable            = '+hadd_job_dir+'/bash_condor.sh\n')
  condorFile.write('arguments             = '+new_name+' ' + ' '.join(input_files) + '\n')
  condorFile.write('log                   = '+hadd_job_dir+'/hadd.log\n')
  condorFile.write('output                = '+hadd_job_dir+'/hadd.out\n')
  condorFile.write('error                 = '+hadd_job_dir+'/hadd.err\n')
  condorFile.write('requirements = TARGET.HAS_OSG_WN_CLIENT =?= TRUE\n')
  condorFile.write('requirements = TARGET.OpSysMajorVer == 7\n')
  condorFile.write('should_transfer_files = yes\n')
  condorFile.write('when_to_transfer_output = ON_EXIT\n')
  condorFile.write('transfer_input_files  = '+cmssw_tar_path+'\n')
  
  if not is_eos:
    condorFile.write('Transfer_Output_Files = '+new_nice_name+'.root, '+new_nice_name+'.root.haddlog'+'\n')

  condorFile.write('queue\n')
  condorFile.close()

  submit_path = os.getcwd()
  if not is_eos:
    submit_path = output_file_path
  args = ['condor_submit '+hadd_job_dir+'/submit_'+new_nice_name]
  p = subprocess.Popen(args =args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=submit_path)
    
  print p.stdout.read()
    
  return p

_all__ = [
    'make_bash_file',
    'hadd_on_condor',
    ]
  
if __name__ == '__main__':

  hadd_on_condor(sys.argv[1], sys.argv[2], sys.argv[3:])
