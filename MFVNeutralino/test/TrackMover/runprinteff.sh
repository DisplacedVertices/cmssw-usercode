set -e
for year in 2017
do
  for tau in 000300 001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    python printeff.py /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverHistsUlv30lepmv2_20_tau${tau}um/SingleMuon${year}.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverHistsUlv30lepmv2_20_tau${tau}um/background_leptonpresel_${year}.root
    python printeff.py /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverHistsUlv30lepmv2_20_tau${tau}um/SingleElectron${year}.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverHistsUlv30lepmv2_20_tau${tau}um/background_leptonpresel_${year}.root
    sleep 5

  done
done
