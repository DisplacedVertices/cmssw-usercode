import gzip
from FWCore.PythonUtilities.LumiList import LumiList
from JMTucker.Tools.general import intlumi_from_brilcalc_csv as parse

# brilcalc lumi -i 2015.json -o 2015.byls.csv --byls --normtag=normtag_2015.json ; gzip 2015.byls.csv
# brilcalc lumi -i 2015.json -o 2015.byls.HLT_PFHT800.csv --byls --normtag=normtag_2015.json --hltpath=HLT_PFHT800_v\* ; gzip 2015.byls.HLT_PFHT800.csv
# brilcalc lumi -i 2016.json -o 2016.byls.csv --byls --normtag=normtag_2016.json ; gzip 2016.byls.csv
# brilcalc lumi -i 2016.json -o 2016.byls.HLT_PFHT900.csv --byls --normtag=normtag_2016.json --hltpath=HLT_PFHT900_v\* ; gzip 2016.byls.HLT_PFHT900.csv
# brilcalc lumi -i 2017.json -o 2017.byls.csv --byls --normtag=normtag_2017.json ; gzip 2017.byls.csv
# brilcalc lumi -i 2017.json -o 2017.byls.HLT_PFHT1050.csv --byls --normtag=normtag_2017.json --hltpath=HLT_PFHT1050_v\* ; gzip 2017.byls.HLT_PFHT1050.csv
# brilcalc lumi -i 2018.json -o 2018.byls.csv --byls --normtag=normtag_2018.json ; gzip 2018.byls.csv
# brilcalc lumi -i 2018.json -o 2018.byls.HLT_PFHT1050.csv --byls --normtag=normtag_2018.json --hltpath=HLT_PFHT1050_v\* ; gzip 2018.byls.HLT_PFHT1050.csv

# ils = [
#     (2017, (parse('/uscms/home/ali/nobackup/LLP/CornellCode/mfv_10_6_20/src/JMTucker/MFVNeutralino/test/jsons/json_UL/2017.byls.csv.gz',              False),
#             parse('/uscms/home/ali/nobackup/LLP/CornellCode/mfv_10_6_20/src/JMTucker/MFVNeutralino/test/jsons/json_UL/2017.byls.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight.csv.gz', True))),
#     (2018, (parse('/uscms/home/ali/nobackup/LLP/CornellCode/mfv_10_6_20/src/JMTucker/MFVNeutralino/test/jsons/json_UL/2018.byls.csv.gz',              False),
#             parse('/uscms/home/ali/nobackup/LLP/CornellCode/mfv_10_6_20/src/JMTucker/MFVNeutralino/test/jsons/json_UL/2018.byls.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight.csv.gz', True))),
#     ]

ils = [
    (2016, (parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2016/2016.byls.csv.gz',    False),
           # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2016/2016.byls.HLT_IsoMu27.csv.gz', True))),
            #parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2016/2016.byls.HLT_Mu50.csv.gz', True))),
            parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2016/2016.byls.HLT_Ele27_WPTight_Gsf.csv.gz', True))),
           # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2016/2016.byls.HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165.csv.gz', True))),
            #parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2016/2016.byls.HLT_Ele115_CaloIdVT_GsfTrkIdT.csv.gz', True))),
    # (2017, (parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2017/2017.byls.csv.gz',    False),
    #        # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2017/2017.byls.HLT_IsoMu27.csv.gz', True))),
    #        # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2017/2017.byls.HLT_Mu50.csv.gz', True))),
    #        # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2017/2017.byls.HLT_Ele35_WPTight_Gsf.csv.gz', True))),
    #        # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2017/2017.byls.HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165.csv.gz', True))),
    #         parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2017/2017.byls.HLT_Ele115_CaloIdVT_GsfTrkIdT.csv.gz', True))),
    (2018, (parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2018/2018.byls.csv.gz',    False),
           # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2018/2018.byls.HLT_IsoMu27.csv.gz', True)))
           # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2018/2018.byls.HLT_Mu50.csv.gz', True)))
            parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2018/2018.byls.HLT_Ele32_WPTight_Gsf.csv.gz', True)))
           # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2018/2018.byls.HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165.csv.gz', True)))
           # parse('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/jsons/json_UL/SingleLep/2018/2018.byls.HLT_Ele115_CaloIdVT_GsfTrkIdT.csv.gz', True)))
    
    ]

for year, ((wohlt, wohlt_sum), (whlt, whlt_sum)) in ils:
    print year, wohlt_sum/1e9, whlt_sum/1e9
    good_run_lses = []
    run_lses = sorted(set(wohlt.keys()) & set(whlt.keys()))
    for run_ls in run_lses:
        wohlt_l = wohlt[run_ls]
        whlt_l  = whlt [run_ls]
        if wohlt_l != whlt_l:
            print run_ls, wohlt_l, whlt_l
        else:
            good_run_lses.append(run_ls)
    LumiList(lumis=good_run_lses).writeJSON('ana_%i_ele2732.json' % year)
