import os

for kind in ["mfv_neu", "mfv_stopdbardbar"] :
    for tau in ["000100","000200","000300","000700","000800","000900","001000","003000","007000","010000","028000","030000","100000"] :
        for mass in ["0300","0400","0500","0600","0700","0800","0900","1000","1100","1200","1500","1800","2200","2700","2900","3000"] :
            for year in ["2017","2018"] :
                os.system("python limitsinput.py uncert %s_tau%sum_M%s_%s" % (kind, tau, mass, year))
