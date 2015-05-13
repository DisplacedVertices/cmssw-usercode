import sys, os

signals = [x for x in '''
mfv_neutralino_tau0100um_M0200
mfv_neutralino_tau0100um_M0300
mfv_neutralino_tau0100um_M0400
mfv_neutralino_tau0100um_M0600
mfv_neutralino_tau0100um_M0800
mfv_neutralino_tau0100um_M1000
mfv_neutralino_tau0300um_M0200
mfv_neutralino_tau0300um_M0300
mfv_neutralino_tau0300um_M0400
mfv_neutralino_tau0300um_M0600
mfv_neutralino_tau0300um_M0800
mfv_neutralino_tau0300um_M1000
mfv_neutralino_tau1000um_M0200
mfv_neutralino_tau1000um_M0300
mfv_neutralino_tau1000um_M0400
mfv_neutralino_tau1000um_M0600
mfv_neutralino_tau1000um_M0800
mfv_neutralino_tau1000um_M1000
mfv_neutralino_tau9900um_M0200
mfv_neutralino_tau9900um_M0300
mfv_neutralino_tau9900um_M0400
mfv_neutralino_tau9900um_M0600
mfv_neutralino_tau9900um_M0800
mfv_neutralino_tau9900um_M1000
'''.split('\n') if x]

try:
    signal = signals[int(sys.argv[1])]
    signals = [signal]
except (IndexError, ValueError):
    pass

toys = 'toys' in sys.argv

print signals, 'toys:', toys


sh = '''#!/bin/bash

echo date: $(date)
echo seed: $1
echo pwd: $(pwd)

export SCRAM_ARCH=slc6_amd64_gcc481
source /cvmfs/cms.cern.ch/cmsset_default.sh

scram project CMSSW CMSSW_7_1_5
cd CMSSW_7_1_5/src
eval `scram ru -sh`
tar zxf /eos/uscms/store/user/tucker/combine/combine2.tgz
scram b -j 4

cp /eos/uscms/store/user/tucker/combine/my-shapes.root .
cp /eos/uscms/store/user/tucker/combine/%(signal)s.txt %(signal)s.txt
seed=$1
'''

if toys:
    sh += '''
combine -M HybridNew --rule CLs --testStat LEP %(signal)s.txt -t 1 --seed $((121982 + seed))
'''
else:
    sh += '''
combine -M HybridNew --rule CLs --testStat LEP %(signal)s.txt --seed $((191982 + seed))
'''

jdl = '''universe = vanilla
Executable = %(signal)s.sh
arguments = $(Process)
Output = %(signal)s_$(Cluster)_$(Process).stdout
Error = %(signal)s_$(Cluster)_$(Process).stderr
Log = %(signal)s_$(Cluster)_$(Process).log
stream_output = false
stream_error  = false
notification  = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
'''

if toys:
    jdl += '''
Queue 500
'''
else:
    jdl += '''
Queue 10
'''

for signal in signals:
    if signal == 'mfv_neutralino_tau1000um_M0400' or signal == 'mfv_neutralino_tau1000um_M0800':
        continue

    d = 'jobs_'
    if toys:
        d += 'toys_'
    d += signal
    os.mkdir(d)
    os.chdir(d)
    open(signal + '.sh', 'wt').write(sh % locals())
    open(signal + '.jdl', 'wt').write(jdl % locals())
    os.system('condor_submit %s.jdl' % signal)
    os.chdir('..')
