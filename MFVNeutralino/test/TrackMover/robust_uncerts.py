import ROOT
import numpy as np


# FUNCTIONS USED
#############################################################################################

def shiftTOC(num, den, sint, fr):
    s_num = ROOT.TH1D("shifted_num", "", 80, 0, 80)
    s_den = ROOT.TH1D("shifted_den", "", 80, 0, 80)

    fr = 1.0-fr

    for b in range(0,80):
        s_num.SetBinContent(b, fr*num.GetBinContent(b+sint) + (1-fr)*num.GetBinContent(b+1+sint))
        s_num.SetBinError(b, np.hypot(fr*num.GetBinError(b+sint), (1-fr)*num.GetBinError(b+1+sint)))

        #print(" Before : den"+str(int(b))+ " " + str(den.GetBinContent(b)))
        s_den.SetBinContent(b, fr*den.GetBinContent(b+sint) + (1-fr)*den.GetBinContent(b+1+sint))
        #print(" After : den"+str(int(b))+ " " + str(s_den.GetBinContent(b)))
        s_den.SetBinError(b, np.hypot(fr*den.GetBinError(b+sint), (1-fr)*den.GetBinError(b+1+sint)))

    s_num.Divide(s_den)
    return s_num

def shiftTOC_alt(curve, sint, fr):
    s_curve = ROOT.TH1D("shifted_curve", "", 80, 0, 80)
    fout = ROOT.TFile("shifttoc.root", "recreate")
    fr = 1.0-fr

    for b in range(0,80):
        s_curve.SetBinContent(b, fr*curve.GetBinContent(b+sint) + (1-fr)*curve.GetBinContent(b+1+sint))
        s_curve.SetBinError(b, np.hypot(fr*curve.GetBinError(b+sint), (1-fr)*curve.GetBinError(b+1+sint)))

        #print(" Before : den"+str(int(b))+ " " + str(curve.GetBinContent(b)))
        s_curve.SetBinContent(b, fr*curve.GetBinContent(b+sint) + (1-fr)*curve.GetBinContent(b+1+sint))
        #print(" After : den"+str(int(b))+ " " + str(s_curve.GetBinContent(b)))
        s_curve.SetBinError(b, np.hypot(fr*curve.GetBinError(b+sint), (1-fr)*curve.GetBinError(b+1+sint)))
    s_curve.Write()
    return s_curve

def scaledTOC(sig_curve, data_curve, sim_curve):
    s_curve = ROOT.TH1D("scaled_curve", "", 80, 0, 80)
    fout = ROOT.TFile("scaledtoc.root", "recreate")
    #data_curve.Divide(sim_curve) 
    #sig_curve.Multiply(data_curve)
    for b in range(0,80):
        if (sim_curve.GetBinContent(b) > 0):
            s_curve.SetBinContent(b, sig_curve.GetBinContent(b)*data_curve.GetBinContent(b)/sim_curve.GetBinContent(b))
            s_curve.SetBinError(b, sig_curve.GetBinError(b)*data_curve.GetBinContent(b)/sim_curve.GetBinContent(b))
    s_curve.Write()
    return s_curve

def cutZero(curve, name):
    #fout = ROOT.TFile(name+".root", "recreate")
    #data_curve.Divide(sim_curve) 
    #sig_curve.Multiply(data_curve)
    for b in range(0,80):
        curve.SetBinContent(1, 0)
        curve.SetBinError(1, 0)
        curve.SetBinContent(2, 0)
        curve.SetBinError(2, 0)
    #curve.Write()
    #fout.Close()
    return curve

#############################################################################################

def shiftDIST(den, sint, fr):
    s_den = ROOT.TH1D("placeholder", "", 80, 0, 80)

    fr = 1.0-fr

    for b in range(0,80):
        s_den.SetBinContent(b, fr*den.GetBinContent(b+sint) + (1-fr)*den.GetBinContent(b+1+sint))
        s_den.SetBinError(b, np.hypot(fr*den.GetBinError(b+sint), (1-fr)*den.GetBinError(b+1+sint)))

    return s_den

################################################################################################

#def assessUncerts(slide_uncerts, scale_uncerts, toc_shift_uncerts, stat_uncerts):
def assessUncerts(scale_uncerts, stat_uncerts):
    out_uncerts = []
    #for i in range(0, len(slide_uncerts)):


    #central_val = (slide_uncerts[i] + scale_uncerts[i])/2.0
    central_val = scale_uncerts[i]
    #sigma_avg   = abs(slide_uncerts[i] - scale_uncerts[i])/2.0
        
    out_uncerts.append( round(central_val/100.0 ,3) )

    # Add signs to these - central val?
    total = np.sqrt (central_val**2 + stat_uncerts[i]**2)

    #print( "Uncert central +/- stat +/- sys_meth +/- sys_tocshift : %.3f +- %.3f +- %.3f +- %.3f     Total: %.3f" % (central_val, stat_uncerts[i], sigma_avg, toc_shift_uncerts[i], total) )
    print( "Uncert central +/- stat : %.3f +- %.3f     Total: %.3f" % (central_val, stat_uncerts[i], total) )
    print(out_uncerts)

    return None

################################################################################################

def calcTocShiftUncert(low, cent, hi):

    outRmsVals = []

    for i in range(0, len(low)):
        rms =  np.sqrt( ((cent[i] - low[i])**2 + (cent[i]-hi[i])**2)/2 )
        rms = round(rms, 3)
        outRmsVals.append(rms)

    return outRmsVals



################################################################################################


# Initialize stuff:

year = '2017'
doShift  = True
reweight = True
toc_shift = 0.0   # How much to move the turn-on curve by
shift_fr  = 0.0   # How much to slide the closeseedtk dist by (decimal part)
shift_val = 0     # How much to slide the closeseedtk dist by (integer part)


masses = ['55',]
#masses = ['0800']
ctaus       = ['1',]
toc_nudges  = [0.0,] #[-0.1, 0.0, 0.1]
psd_methods = ['slide', 'scale']

if year == '2018': 
    shift_val = 2 #FIXME
    shift_fr  = 0.0 #FIXME
    toc_shift = 1.0 #FIXME 
if year == '2017': 
    shift_val = 0 #FIXME
    shift_fr  = 0.037 #FIXME 
    toc_shift = 1.0 #FIXME


# Start actually doing stuff

uncertArray = []
all_stat_uncerts = {}

for psd_method in psd_methods:
    for toc_nudge in toc_nudges:
    
        for mass in masses:
            effArray = []
            errArray = []
            stat_uncerts = []
        
            #print("\n")
            for ctau in ctaus:
        
                sim_str = ''
                dat_str = ''
        
                if not reweight:
                    #sim_str = '../combined_extrastats_multijet/bg' + year + '_' + ctau + 'um_merged.root'
                    sim_str = '~/nobackup/crabdirs/TrackMoverJetByJetHistsOnnormdzulv30lepmumv5_20_tau00'+str(int(ctau)*1000)+'um_noCorrection/background_leptonpresel_'+ year +'.root'
                    dat_str = '~/nobackup/crabdirs/TrackMoverJetByJetHistsOnnormdzulv30lepmumv5_20_tau00'+str(int(ctau)*1000)+'um_noCorrection/SingleMuon'+ year +'.root'
        
                else:
                    sim_str = '~/nobackup/crabdirs/TrackMoverJetByJetHistsOnnormdzulv30lepmumv5_20_tau00'+str(int(ctau)*1000)+'um_2Djetdrjet1sump1Dmovedist3VetoQCDCorrection/background_leptonpresel_'+ year +'.root'
                    dat_str = '~/nobackup/crabdirs/TrackMoverJetByJetHistsOnnormdzulv30lepmumv5_20_tau00'+str(int(ctau)*1000)+'um_2Djetdrjet1sump1Dmovedist3VetoQCDV2Correction/SingleMuon'+ year +'.root'
        
                tm_sim  = ROOT.TFile(sim_str)
                tm_dat  = ROOT.TFile(dat_str)
                signal  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruthVetoPUPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv5/WplusHToSSTodddd_tau'+ctau+'mm_M'+ mass +'_'+ year +'.root')
                
                dat_den = tm_dat.Get('all_closeseedtks_den')
                dat_den = cutZero(dat_den, "dat_den") 
                sim_den = tm_sim.Get('all_closeseedtks_den')
                sim_den = cutZero(sim_den, "sim_den") 
                
                dat_num = tm_dat.Get('all_closeseedtks_num')
                dat_num = cutZero(dat_num, "dat_num") 
                sim_num = tm_sim.Get('all_closeseedtks_num')
                sim_num = cutZero(sim_num, "sim_num") 
                
                sig_dist = signal.Get('nocuts_closeseedtks_den')
                sig_dist = cutZero(sig_dist, "sig_dist") 
                
                sig_denom = signal.Get('all_closeseedtks_den') 
                sig_denom = cutZero(sig_denom, "sig_denom") 
                sig_aaaaa = signal.Get('all_closeseedtks_num')
                sig_aaaaa = cutZero(sig_aaaaa, "sig_aaaaa") 
                sig_curve = sig_aaaaa.Clone()
                temp_sig_num = sig_curve.Clone()
                temp_sig_den = sig_denom.Clone()
                psd_dist = ROOT.TH1D("psd_dist", "test", 80, 0, 80)
        
                # Calculate the scale factors
                scale_factors = dat_den.Clone()
                scale_divisor = sim_den.Clone()
                scale_factors.Scale(1.0/scale_factors.Integral())
                scale_divisor.Scale(1.0/scale_divisor.Integral())
                scale_factors.Divide(scale_divisor)

                # Fill pseudodata distribution
                if psd_method == 'slide':
                    psd_dist = shiftDIST(sig_dist, shift_val, shift_fr)
                if psd_method == 'scale':
                    psd_dist = sig_dist.Clone()
                    psd_dist.Multiply(scale_factors)

                # Draw stuff #######################

#                psd_dist.SetTitle('Mass: %s   ct: %s    %s' % (mass, ctau, psd_method))
#                psd_dist.Scale(1.0/psd_dist.Integral())
#                psd_dist.SetLineColor(ROOT.kRed)
#                psd_dist.SetLineWidth(2)
#
#                sig_dist.Scale(1.0/sig_dist.Integral())
#                sig_dist.SetLineColor(ROOT.kBlue)
#                sig_dist.SetLineWidth(2)
#
#                leg = ROOT.TLegend(0.7, 0.75, 0.99, 0.95)
#                leg.AddEntry(sig_dist, "Signal MC")
#                leg.AddEntry(psd_dist, "Pseudodata")
#
#                psd_dist.Draw()
#                sig_dist.Draw("same")
#                leg.Draw("same")
#                wait = raw_input("wait")

                #####################################

        
                # Make the TM data and TM sim turn-on curves

                dat_num.Divide(dat_den)
                sim_num.Divide(sim_den)
                # Make the pseudodata turn-on curve
                temp_shift = toc_shift + toc_nudge
                temp_shift *= -1
                #psd_curve = shiftTOC(temp_sig_num, temp_sig_den, int(temp_shift//1), (temp_shift % 1) )
                # Make the signal turn-on curve
                sig_curve.Divide(sig_denom)
                #psd_curve = shiftTOC_alt(sig_curve, int(temp_shift//1), (temp_shift % 1) )
                psd_curve = scaledTOC(sig_curve, dat_num, sim_num)
                
                possible_sim = sig_dist.Integral()
                possible_psd = psd_dist.Integral()
                fsout = ROOT.TFile("sig_distcurve.root", "recreate")
                sig_dist.Multiply(sig_curve)
                sig_dist.Write() 
                fsout.Close()
                if doShift:
                    fout = ROOT.TFile(psd_method+"_distcurve.root", "recreate")
                    psd_dist.Multiply(psd_curve)
                    psd_dist.Write() 
                    fout.Close()
                else:
                    psd_dist.Multiply(sig_curve)
                
                pass_sim = sig_dist.Integral()
                pass_psd = psd_dist.Integral()
        
                eff_sim = pass_sim/possible_sim
                eff_psd = pass_psd/possible_psd
       
                print(" eff_sim "+str(eff_sim))
                print(" eff_data "+str(eff_psd))
                err_sim = np.sqrt(eff_sim * (1-eff_sim)/possible_sim)
                err_psd = np.sqrt(eff_psd * (1-eff_psd)/possible_psd)
        
                tot_err_one = 2*err_psd/eff_sim
                tot_err_two = 2*eff_psd*err_sim/(eff_sim**2)
    
                print("Nudge: %.2f    Mass: %s   ct: %s     Uncert: %.3f" % (toc_nudge, mass, ctau, 200*(1-eff_psd/eff_sim)) )
        
                effArray.append( round(200*(1-eff_psd/eff_sim), 3))
                stat_uncerts.append( round (100*np.hypot(tot_err_one, tot_err_two), 3)  )

            uncertArray.append(effArray)
            if toc_nudge == 0.0:
                all_stat_uncerts[mass] = stat_uncerts 

#print(uncertArray)
#print(len(uncertArray))
#print(len(toc_nudges), len(masses))

toc_shift_uncerts = {}

#for i in range(0, len(psd_methods)):
#    k = i*len(masses)*len(toc_nudges)
#    for j in range(0, len(masses)):
#        print("Mass: %s     Method: %s \n----------------------------" % (masses[j], psd_methods[i]))
#        print(calcTocShiftUncert(uncertArray[k+j], uncertArray[k+j+len(masses)], uncertArray[k+j+len(masses)*2]))
         #toc_shift_uncerts[masses[j]] = calcTocShiftUncert(uncertArray[k+j], uncertArray[k+j+len(masses)], uncertArray[k+j+len(masses)*2])
#        print('\n')

for i in range(0, len(toc_nudges)):
    k = i*len(masses)
    for j in range(0, len(masses)):
        print("Mass: %s     Nudge: %.2f\n----------------------------" % (masses[j], toc_nudges[i]) )
        #assessUncerts( uncertArray[k+j], uncertArray[k+j+len(masses)*len(toc_nudges)], toc_shift_uncerts[masses[j]], all_stat_uncerts[masses[j]] )
        assessUncerts( uncertArray[k+j], all_stat_uncerts[masses[j]] )
        print("\n")
