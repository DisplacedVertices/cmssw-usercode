#!/usr/bin/env python

version = 'V3p1'
per = 250

####

import sys, os, shutil
from pprint import pprint
from DVCode.Tools.CRAB3Tools import Config, crab_command
from DVCode.Tools.general import int_ceil, save_git_status, popen, touch
from DVCode.Tools import colors
from DVCode.Tools.Year import year

max_njobs = dict([(x, (int_ceil(y, per), per if y%per == 0 else y%per)) for x,y in [
            (('JetHT2016B3', 3), 19521),
            (('JetHT2016B3', 4), 2125),
            (('JetHT2016C', 3), 8559),
            (('JetHT2016C', 4), 945),
            (('JetHT2016D', 3), 14478),
            (('JetHT2016D', 4), 1659),
            (('JetHT2016E', 3), 8128),
            (('JetHT2016E', 4), 819),
            (('JetHT2016F', 3), 6480),
            (('JetHT2016F', 4), 687),
            (('JetHT2016G', 3), 22317),
            (('JetHT2016G', 4), 2427),
            (('JetHT2016H2', 3), 23550),
            (('JetHT2016H2', 4), 2572),
            (('JetHT2016H3', 3), 643),
            (('JetHT2016H3', 4), 66),
            (('JetHT2015C', 3), 46),
            (('JetHT2015C', 4), 8),
            (('JetHT2015D', 3), 5376),
            (('JetHT2015D', 4), 615),
            (('ttbar', 3), 12257),
            (('ttbar', 4), 1488),
            (('ttbar', 5), 184),
            (('ttbar_2015', 3), 9630),
            (('ttbar_2015', 4), 1156),
            (('ttbar_2015', 5), 122),
            (('qcdht0500sum', 3), 16),
            (('qcdht0500sum', 4), 0),
            (('qcdht0500sum', 5), 0),
            (('qcdht0700sum', 3), 4325),
            (('qcdht0700sum', 4), 531),
            (('qcdht0700sum', 5), 74),
            (('qcdht1000sum', 3), 40603),
            (('qcdht1000sum', 4), 5098),
            (('qcdht1000sum', 5), 789),
            (('qcdht1500sum', 3), 60851),
            (('qcdht1500sum', 4), 8551),
            (('qcdht1500sum', 5), 1552),
            (('qcdht2000sum', 3), 40015),
            (('qcdht2000sum', 4), 6340),
            (('qcdht2000sum', 5), 1337),
            (('qcdht0500sum_2015', 3), 15),
            (('qcdht0500sum_2015', 4), 2),
            (('qcdht0500sum_2015', 5), 0),
            (('qcdht0700sum_2015', 3), 2850),
            (('qcdht0700sum_2015', 4), 325),
            (('qcdht0700sum_2015', 5), 38),
            (('qcdht1000sum_2015', 3), 25123),
            (('qcdht1000sum_2015', 4), 2923),
            (('qcdht1000sum_2015', 5), 470),
            (('qcdht1500sum_2015', 3), 36943),
            (('qcdht1500sum_2015', 4), 5099),
            (('qcdht1500sum_2015', 5), 1040),
            (('qcdht2000sum_2015', 3), 25954),
            (('qcdht2000sum_2015', 4), 3972),
            (('qcdht2000sum_2015', 5), 888),
            ]])

sh_template = '''
#!/bin/bash

workdir=$(pwd)
job=$1

if [[ $job -eq %(njobs)i ]]; then
    nev=%(per_last_m1)i
else
    nev=%(per_m1)i
fi

echo date: $(date)
echo workdir: $workdir
echo job: $job
echo nev: $nev

cd %(cmssw_version)s/src
eval $(scram runtime -sh)

function xrdcpit {
    src=$1
    dst=$2
    echo $src to $dst

    xrdcpexit=99
    counter=0
    tries=10
    sleeptime=60
    while [[ $counter -lt $tries ]]; do
        xrdcp -f -t 5 $src $dst 2>&1
        xrdcpexit=$?
        if [[ $xrdcpexit -eq 0 ]]; then
            break
        fi
        if [[ $counter -lt $((tries-1)) ]]; then
            echo xrdcp exit was $xrdcpexit, sleeping $sleeptime then trying again
            sleep $sleeptime
        fi
        let counter++
    done

    if [[ $xrdcpexit -ne 0 ]]; then
        echo xrdcp never succeeded
    fi
    exit $xrdcpexit
}

echo start xrdcp input at $(date)
(xrdcpit root://cmsxrootd.fnal.gov//store/user/tucker/MiniTreeV14_forpick/prescales.root .) && \
(xrdcpit root://cmsxrootd.fnal.gov//store/user/tucker/MiniTreeV14_forpick/%(sample)s.root %(sample)s_tree.root) && \
(xrdcpit root://cmsxrootd.fnal.gov//store/user/tucker/skimpickv14/%(sample)s.root %(sample)s_edm.root)
xrdcpexit=$?
if [[ xrdcpexit -ne 0 ]]; then
    echo problem with one of the xrdcps
    exit 1
fi
echo end xrdcp input at $(date), ls -l \*.root
ls -l *.root

echo start cmsRun loop at $(date)
for i in $(seq 0 $nev); do
    echo start cmsRun \#$i at $(date)
    cmsRun -j tempfjr.xml ${workdir}/%(cmssw_py)s +batch +which-event $(((job-1)*%(per)s+i)) +sample %(sample)s +ntracks %(ntracks)s %(overlay_args)s 2>&1
    cmsexit=$?
    echo end cmsRun \#$i at $(date)
    if [[ $cmsexit -ne 0 ]]; then
        echo cmsRun exited with code $cmsexit
        exit $cmsexit
    fi
    ls -l
done
echo end cmsRun loop at $(date)

python $workdir/fixfjr.py
ls -l FrameworkJobReport.xml
cp FrameworkJobReport.xml $workdir

echo start hadd at $(date)
hadd overlay.root overlay_*.root 2>&1
haddexit=$?
echo end hadd at $(date)
if [[ $haddexit -ne 0 ]]; then
    echo hadd exited with code $haddexit
    exit $haddexit
fi
mv overlay.root $workdir

echo ls -l src
ls -l
echo ls -l workdir
ls -l $workdir

echo end job at $(date)
'''

def submit(samples, ntracks, overlay_args, batch_name_ex=''):
    testing = 'testing' in sys.argv

    batch_name = 'ntk%i' % ntracks
    batch_name += batch_name_ex
    if testing:
        batch_name += '_TEST'

    work_area = '/uscms_data/d2/%s/crab_dirs/Overlay%s/%s' % (os.environ['USER'], version, batch_name)
    
    inputs_dir = os.path.join(work_area, 'inputs')
    os.makedirs(inputs_dir)
    save_git_status(os.path.join(work_area, 'gitstatus'))

    cmssw_py = 'overlay.py'
    cmssw_py_fn = os.path.join(inputs_dir, cmssw_py)
    shutil.copy2(cmssw_py, cmssw_py_fn)
    
    tool_path = os.path.join(os.environ['CMSSW_BASE'], 'src/DVCode/MFVNeutralino/test/MakeSamples') # JMTBAD put dummy.py and fixfjr.py somewhere better

    config = Config()
    config.General.transferLogs = True
    config.General.transferOutputs = True
    config.General.workArea = work_area
    config.JobType.pluginName = 'PrivateMC'
    config.JobType.psetName = os.path.join(tool_path, 'dummy.py')
    config.JobType.sendPythonFolder = True
    config.JobType.inputFiles = [cmssw_py_fn, os.path.join(tool_path, 'fixfjr.py')]
    config.JobType.outputFiles = ['overlay.root']
    config.Data.splitting = 'EventBased'
    config.Data.unitsPerJob = 1
    config.Data.publication = False
    config.Site.storageSite = 'T3_US_FNALLPC'
    config.Site.whitelist = 'T1_US_*,T2_US_*,T3_US_Baylor,T3_US_FIU,T3_US_FSU,T3_US_JHU,T3_US_Kansas,T3_US_NERSC,T3_US_NU,T3_US_NotreDame,T3_US_OSG,T3_US_OSU,T3_US_Omaha,T3_US_Princeton_ICSE,T3_US_PuertoRico,T3_US_Rice,T3_US_SDSC,T3_US_TAMU,T3_US_TTU,T3_US_UCD,T3_US_UCSB,T3_US_UMD'.split(',')
    
    for sample in samples:
        njobs, per_last = max_njobs[(sample, ntracks)]
        sh_vars = {
            'per': per,
            'njobs': njobs,
            'per_m1': per - 1,
            'per_last_m1': per_last - 1,
            'ntracks': ntracks,
            'sample': sample,
            'overlay_args': overlay_args,
            'cmssw_version': os.environ['CMSSW_VERSION'],
            'cmssw_py': cmssw_py,
            }
        sh_fn = os.path.join(inputs_dir, 'run.%s.sh' % sample)
        open(sh_fn, 'wt').write(sh_template % sh_vars)
        os.chmod(sh_fn, 0755)

        config.General.requestName = '%s_%s' % (batch_name, sample)
        config.JobType.scriptExe = sh_fn
        config.Data.totalUnits = njobs

        print colors.boldwhite('%s, %s' % (batch_name, sample))
        if not testing:
            output = crab_command('submit', config=config)
            print output['stdout']
        else:
            print config
            print

if year == 2015:
    samples = ['qcdht0700sum_2015', 'qcdht1000sum_2015', 'qcdht1500sum_2015', 'qcdht2000sum_2015', 'ttbar_2015']
elif year == 2016:
    samples = ['qcdht0700sum', 'qcdht1000sum', 'qcdht1500sum', 'qcdht2000sum', 'ttbar']

oes = [
#    ('', ''),
    ('+z-model deltasv',  '_deltasv'),
    ('+no-rest-of-event', '_noevent'),
    ('+z-width 0.06',     '_zwidth2x'),
    ('+found-dist 0.016', '_found2sig'),
    ]
for overlay_args, ex in oes:
    for ntracks in [3,4,5]:
        submit(samples, ntracks, overlay_args, ex)
