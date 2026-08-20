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
submitCombine.py picks it up from $COMBINE_TARBALL, falling back to a default path in
submitCombine.py -- export the variable rather than editing the file.


MAKING DATACARDS (el7 apptainer, CMSSW_10_6_48)
------------------------------------------------
Get into the el7 container first. --bind /uscms_data is required, without it nothing under
nobackup resolves inside the container:

    /cvmfs/cms.cern.ch/common/cmssw-el7 --bind /uscms_data -- bash
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    cd <your CMSSW_10_6_48>/src && eval `scramv1 runtime -sh`
    cd JMTucker/MFVNeutralino/test/ForLimits

Note that inside the container you have to use the real /uscms_data/d3/<user>/... paths;
the ~/nobackup symlink does not resolve there.

Run makeLimitsInputROOT.py for each year/channel combo. Three paths are required on
every run -- nothing in limits_config.yaml points at anyone's personal area, so there
are no defaults to accidentally inherit and nothing to overwrite in someone else's
directory:

    --minitree-dir       signal MiniTrees for the channel you are running
    --bkg-template-dir   background templates for that channel
    --out-dir            base output folder

Under --out-dir you get LimitsInput_4bin/<channel>/ (ROOT histograms) and
Datacards_4bin/<channel>/ (combine .txt cards). Both are created if missing.

    python makeLimitsInputROOT.py --year 2018 --channel lep \
        --minitree-dir     /path/to/MiniTree_tag001Lepm_VH \
        --bkg-template-dir /path/to/templates/lep \
        --out-dir          /path/to/output

    bash run_limits_bjet_allyears.sh <minitree-dir> <bkg-template-dir> <out-dir>  # bjet, all years

BackgroundTemplates_EXAMPLE/ in this directory is a reference copy showing the expected
file names and layout. It is not an input; point --bkg-template-dir at your own set.

The rest of limits_config.yaml (bins, observations, default year/channel, file-name
patterns) is shared config and normally does not need editing. The 4-bin setup is
[0, 0.1, 0.4, 2.0, 4.0] cm and is the default.

If you only have some of the signals that is fine, the code runs over whatever it finds.
Signal clusters like VH are the exception: all four of ZH, W+H, W-H and ggZH are summed into
one process, so two or three of the four present is an error rather than a silent skip. A point
where only ggZH exists is skipped with a message, since ggZH is generated at 12 lifetimes and
W+-H only at 6, so those are simply not VH points.


RUNNING COMBINE (el9, CMSSW_14_1_0_pre4)
-----------------------------------------
Always run asymptotic first -- HybridNew uses the asymptotic result to set rMax.

    python submitCombine.py --tag 4bin --method asymptotic --out-dir /path/to/output
    python submitCombine.py --tag 4bin --method hybridnew  --out-dir /path/to/output

--out-dir must be the same one you gave makeLimitsInputROOT.py. Leave it off only if you
wrote the cards into this ForLimits directory.

Useful flags:
  --dry-run          write job files but don't submit
  --skip-existing    skip hypotheses that already have output
  --subset VHToSSTodddd,mfv_neu   only submit these processes
  --sig-id VHToSSTodddd_tau1mm_M15   only submit this one hypothesis
  --limit 5          cap at N jobs (good for testing)

The --tag 4bin flag routes everything through Datacards_4bin/, CombineOutput_4bin/, CombineCondor_4bin/.
Those are looked for in this directory unless you pass --out-dir, which must be the same
--out-dir you gave makeLimitsInputROOT.py, otherwise combine runs on a different set of cards.
ttH signals still get submitted, but combineCards fails on them (negative signal rate corner
case) and the job is skipped with a WARNING. Nothing filters them out up front.


PLOTTING
--------
Run inside CMSSW_14_1_0_pre4 (has scipy + matplotlib).

    python3 plotLimits.py --combine-out /path/to/output/CombineOutput_4bin \
        --out-dir /path/to/output/LimitPlots_4bin

Add --comparison-dir LimitPlots_4bin_Comparison to also make HybridNew vs Asymptotic overlays.
Add --subset VHToSSTodddd,mfv_neu to only plot specific processes.


NUISANCE TABLES
---------------
Pickle files under NuisTabStore_*/ are precomputed and read at datacard-making time.
They live in the repo, so they need no path argument. Same for the VH factorization
scale table, TheoryTables/fac_scale_shape_bins.csv -- everyone should be on the same
copy of that one.

To regenerate the pickles (usually not needed). Note turn_TrkRec_to_2darr.py does NOT
currently work: uncerts_trkrec.py still holds 3-bin lists while the config is 4-bin, so it
fails on the array size. See the review notes:

    python turn_7p4p1_to_2darr.py    # displaced trigger uncertainties
    python turn_TrkMvr_to_2darr.py   # TrackMover vertex reco uncertainties
    python turn_TrkRec_to_2darr.py   # track reco efficiency (VH only)


PYTHON VERSIONS
---------------
Every .py file here is syntax-clean under both Python 2 and Python 3. In practice the
datacard stage only runs under Python 2 (CMSSW_10_6_48) because it imports JMTucker.Tools and
ROOT from there, and the stored pickles were written by Python 2 so they would need
encoding="latin1" to be read by Python 3. plotLimits.py is the part that actually runs under
Python 3 in CMSSW_14_1_0_pre4.

Keep the "from __future__ import print_function" lines, use print() calls, and avoid
Python-2-only builtins like xrange, so the files stay loadable from both sides.
