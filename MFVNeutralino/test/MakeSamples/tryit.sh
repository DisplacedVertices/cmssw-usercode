# this script sets up a working directory like crab would do--don't
# run nstep.sh/cmsRun in the same shell, but rather make a new one as
# the print out will instruct

echo be sure to change year.txt and steering.sh to what you want, it was set for the last test
owd=$(pwd)
input_version=$CMSSW_VERSION
tmpdir=/dev/shm/$USER/nstep_tryit_$(date +%s)
echo $tmpdir
mkdir $tmpdir 
edmConfigDump dummy.py > $tmpdir/pset.py
cp nstep.sh todoify.sh lhe.py gensim.py modify.py dynamicconf.py scanpack.py rawhlt.py minbias.py minbias.txt.gz minbias_premix.txt.gz private_minbias.txt.gz reco.py fixfjr.py $tmpdir
for x in ntuple.py minitree.py; do
    cmsDumpPython.py ../$x > $tmpdir/$x
done
cd $tmpdir
scram project CMSSW $input_version
cd $input_version
cmsMakeTarball.py input.tgz
tar xf input.tgz
echo 2016 > $tmpdir/year.txt
cat > $tmpdir/steering.sh <<EOF
MAXEVENTS=100
EXPECTEDEVENTS=100
USETHISCMSSW=0
FROMLHE=0
TRIGFILTER=0
PREMIX=1
export DUMMYFORHASH=1526164939315868
OUTPUTLEVEL=minitree
TODO="todo=pdf,LHAPDF6:NNPDF23_lo_as_0130_qed/0000 todo=stop_dbardbar,1.0,800"
SALT="mfv_stopdbardbar_tau01000um_M0800_stop_dbardbar,1.0,800"
EOF
echo in new shell, issue e.g.
echo "cd $tmpdir/$input_version/src ; source /cvmfs/cms.cern.ch/cmsset_default.sh ; eval \$(scramv1 runtime -sh) ; cd ../.. ; ./nstep.sh 1"
cd $owd
