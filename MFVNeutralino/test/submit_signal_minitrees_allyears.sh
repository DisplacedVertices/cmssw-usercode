#!/bin/bash
# ============================================================
# Submit signal MiniTrees for all four Run 2 years.
#
# OVERVIEW
# --------
# Two scripts are provided:
#   minitree_signal_VH.py   -- lepton channel: ZH + WH+ + WH- + ggZH_bbbb + ggZH_dddd
#   minitree_signal_bjet.py -- bjet channel:   mfv_neu + mfv_stopdbardbar + ggH
#
# They must be submitted year by year because:
#   (a) Year.h embeds the year at compile time (MFVNEUTRALINO_YEAR macro).
#   (b) NtupleCommon.py must have the correct trigger scheme set.
#
# MANUAL STEPS BEFORE EACH YEAR
# ------------------------------
#
# --- Lepton channel (run once per year) ---
#   1. Edit JMTucker/Tools/interface/Year.h:
#        Change  #define MFVNEUTRALINO_XXXX
#        to      #define MFVNEUTRALINO_<YEAR>
#      Valid values: MFVNEUTRALINO_20161, MFVNEUTRALINO_20162,
#                    MFVNEUTRALINO_2017,  MFVNEUTRALINO_2018
#
#   2. Verify NtupleCommon.py has:
#        use_Lepton_triggers = True
#        use_btag_vetoLepHT_triggers = False
#      (this is the default; no change should be needed)
#
#   3. scram b -j8
#
#   4. cmsenv  (re-source the environment after rebuild)
#
#   5. cd test/
#      python minitree_signal_VH.py submit
#
# --- Bjet channel (run once per year) ---
#   1. Edit Year.h as above for the desired year.
#
#   2. Edit NtupleCommon.py:
#        use_btag_vetoLepHT_triggers = True    # change this
#        use_Lepton_triggers = False            # change this
#
#   3. scram b -j8
#
#   4. cmsenv
#
#   5. cd test/
#      python minitree_signal_bjet.py submit
#
#   6. After submission, restore NtupleCommon.py:
#        use_Lepton_triggers = True
#        use_btag_vetoLepHT_triggers = False
#      and rebuild: scram b -j8
#
# REMINDER: The CRAB/Condor jobs will pick up the year from the compiled
# MFVNEUTRALINO_YEAR macro. If you forget to rebuild, all jobs will run
# with the wrong year settings.
#
# SUBMISSION ORDER (suggested: 2018 first, as it has the most statistics)
#   2018, 2017, 20162, 20161
# ============================================================

echo "This script documents the manual steps required."
echo "Edit Year.h and NtupleCommon.py per the instructions above,"
echo "then run scram b and submit each script individually."
echo ""
echo "Lepton channel VH:    python minitree_signal_VH.py submit"
echo "Bjet channel signals: python minitree_signal_bjet.py submit"
