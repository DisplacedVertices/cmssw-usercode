MFV Displaced Vertex -- Limit Setting
======================================

Two environments needed:
  - CMSSW_10_6_48 (el7/apptainer) for datacard making
  - CMSSW_14_1_0_pre4 (el9, native) for combine


FIRST-TIME COMBINE SETUP (only once, on an el9 node)
-----------------------------------------------------
Build CMSSW + CombinedLimit:

    cmsrel CMSSW_14_1_0_pre4
    cd CMSSW_14_1_0_pre4/src && cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    scram b -j8

Then build the tarball that gets shipped to Condor workers:

    # from ForLimits/, with CMSSW_14_1_0_pre4 cmsenv active:
    bash make_combine_tarball.sh

This writes combine_env.tar.gz one level above CMSSW_BASE.
The path is hardcoded in submitCombine.py as COMBINE_TARBALL -- update it there if needed.


MAKING DATACARDS (el7 apptainer, CMSSW_10_6_48)
------------------------------------------------
Run makeLimitsInputROOT.py for each year/channel combo.
Outputs go to LimitsInput_4bin/ (ROOT histograms) and Datacards_4bin/ (combine .txt cards).

    python makeLimitsInputROOT.py --year 2018 --channel lep
    python makeLimitsInputROOT.py --year all  --channel lep
    bash run_limits_bjet_allyears.sh   # convenience wrapper for bjet all years

Config is in limits_config.yaml -- edit paths, bins, or year/channel defaults there.
The 4-bin setup is [0, 0.1, 0.4, 2.0, 4.0] cm and is the default.


RUNNING COMBINE (el9, CMSSW_14_1_0_pre4)
-----------------------------------------
Always run asymptotic first -- HybridNew uses the asymptotic result to set rMax.

    python submitCombine.py --tag 4bin --method asymptotic
    python submitCombine.py --tag 4bin --method hybridnew

Useful flags:
  --dry-run          write job files but don't submit
  --skip-existing    skip hypotheses that already have output
  --subset VH,mfv_neu   only submit these processes
  --sig-id VH_tau1mm_M15   only submit this one hypothesis
  --limit 5          cap at N jobs (good for testing)

The --tag 4bin flag routes everything through Datacards_4bin/, CombineOutput_4bin/, CombineCondor_4bin/.
ttH signals are skipped -- combineCards fails for those due to a negative signal rate corner case.


PLOTTING
--------
Run inside CMSSW_14_1_0_pre4 (has scipy + matplotlib).

    python3 plotLimits.py --combine-out CombineOutput_4bin --out-dir LimitPlots_4bin

Add --comparison-dir LimitPlots_4bin_Comparison to also make HybridNew vs Asymptotic overlays.
Add --subset VH,mfv_neu to only plot specific processes.


NUISANCE TABLES
---------------
Pickle files under NuisTabStore_*/ are precomputed and read at datacard-making time.
To regenerate them (usually not needed):

    python turn_7p4p1_to_2darr.py    # displaced trigger uncertainties
    python turn_TrkMvr_to_2darr.py   # TrackMover vertex reco uncertainties
    python turn_TrkRec_to_2darr.py   # track reco efficiency (VH only)
