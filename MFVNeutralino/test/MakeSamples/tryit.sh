# this script sets up a working directory like crab would do--don't
# run nstep.sh/cmsRun in the same shell, but rather make a new one as
# the print out will instruct

owd=$(pwd)
input_version=$CMSSW_VERSION
tmpdir=/uscmst1b_scratch/lpc1/3DayLifetime/$USER/$(date +%s)
mkdir $tmpdir 
edmConfigDump dummy.py > $tmpdir/pset.py
cp nstep.sh todoify.sh lhe.py gensim.py modify.py dynamicconf.py rawhlt.py minbias.py minbias.txt.gz minbias_premix.txt.gz reco.py fixfjr.py $tmpdir
cd $tmpdir
scram project CMSSW $input_version
cd $input_version
cmsMakeTarball.py input.tgz
tar xf input.tgz
echo in new shell, issue e.g.
echo "cd $tmpdir/$input_version/src ; source /cvmfs/cms.cern.ch/cmsset_default.sh ; eval \$(scramv1 runtime -sh) ; cd ../.. ; ./nstep.sh 1 maxevents=2 salt=mfv_neu_tau10000um_M0800todo=mfv_neutralino,10.0,800 usethiscmssw=1 fromlhe=0 premix=0 dummyforhash=1494430883486142 outputlevel=reco todo=mfv_neutralino,10.0,800 todo2=placeholder"
cd $owd
