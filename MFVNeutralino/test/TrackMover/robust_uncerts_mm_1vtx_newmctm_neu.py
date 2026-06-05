#!/usr/bin/env python

import os
import sys
from JMTucker.Tools.ROOTTools import *

import ROOT
import numpy as np
import math



# FUNCTIONS USED
#############################################################################################

def shiftTOC(num, den, sint, fr):
    ### OBSOLETE ###
    s_num = num.Clone()
    s_den = den.Clone()
    s_curve = num.Clone()
    s_curve.Divide(s_curve, s_den, 1, 1, "B")
    n_num = num.Integral()
    n_den = den.Integral() 
    
    for b in range(0,s_den.GetNbinsX()):
      if (fr + sint + 1 < 0): 
        s_num.SetBinContent(b, (1-fr)*s_num.GetBinContent(b+sint) + (fr)*s_num.GetBinContent(b+1+sint))
        s_den.SetBinContent(b, (1-fr)*s_den.GetBinContent(b+sint) + (fr)*s_den.GetBinContent(b+1+sint))
      else:
        s_num.SetBinContent(b, (1-fr)*s_num.GetBinContent(b+sint) + (fr)*s_num.GetBinContent(b+1+sint))
        s_den.SetBinContent(b, (1-fr)*s_den.GetBinContent(b+sint) + (fr)*s_den.GetBinContent(b+1+sint))
      
      if s_den.GetBinContent(b) == 0:
        continue
      if (s_num.GetBinContent(b)/s_den.GetBinContent(b) < 0.0 or s_den.GetBinContent(b) < 0.0 ) : 
        bincontent_err = 0.0
        bincontent = 0.0
      elif (s_num.GetBinContent(b)/s_den.GetBinContent(b) > 1.0):
        bincontent_err = 0.0
        bincontent = 1.0
      else:
        bincontent = s_num.GetBinContent(b)/s_den.GetBinContent(b)
        bincontent_err = math.sqrt(bincontent*(1-bincontent)/s_den.GetBinContent(b))
        
      s_curve.SetBinContent(b, bincontent)
      s_curve.SetBinError(b, bincontent_err)
   
    return s_curve

def scaledDist(dist):
    ### OBSOLETE ###
    s_dist = dist.Clone()
    for b in range(0,dist.GetNbinsX()):
        if (s_dist.GetBinContent(b) != 0):
          if (b == 1):
            s_dist.SetBinContent(1, 0.0)
            s_dist.SetBinError(1, 0.0)
          elif (b == 2):
            s_dist.SetBinContent(2, 0.01)
            s_dist.SetBinError(2, 0.01)
          else:
            s_dist.SetBinContent(b, dist.GetBinContent(b)*0.99/dist.Integral(3,100))
            s_dist.SetBinError(b, dist.GetBinError(b)*0.99/dist.Integral(3,100))
    return s_dist

def scaledTOC(sig_num, sig_den, data_curve, mc_curve):
    s_num = sig_num.Clone()
    s_den = sig_den.Clone()
    s_curve = s_num.Clone()
    s_curve.Divide(s_curve, s_den, 1, 1, "B")
    
    
    for b in range(0,s_den.GetNbinsX()):
        if (mc_curve.GetBinContent(b) != 0 and sig_den.GetBinContent(b) != 0 ):
            #scale = 1*(sig_curve.GetBinContent(b)*data_curve.GetBinContent(b)/mc_curve.GetBinContent(b) > 1) + (data_curve.GetBinContent(b)/mc_curve.GetBinContent(b))*( sig_curve.GetBinContent(b)*data_curve.GetBinContent(b)/mc_curve.GetBinContent(b) < 1)
            scale = data_curve.GetBinContent(b)/mc_curve.GetBinContent(b) 
           
            if (sig_num.GetBinContent(b)/sig_den.GetBinContent(b) > 1.0):
              bincontent_err = 0.0
              bincontent = 1.0
            elif (sig_num.GetBinContent(b)/sig_den.GetBinContent(b) < 0.0 or sig_den.GetBinContent(b) < 0.0):
              bincontent_err = 0.0
              bincontent = 0.0
            else:
              bincontent = sig_num.GetBinContent(b)/sig_den.GetBinContent(b)
              bincontent_err = math.sqrt(bincontent*(1-bincontent)/sig_den.GetBinContent(b));
            
            if (np.fabs(bincontent*scale) > 1.0):
              s_curve.SetBinContent(b, bincontent)
              s_curve.SetBinError(b, bincontent_err)
            else:
              s_curve.SetBinContent(b, bincontent*scale)
              s_curve.SetBinError(b, bincontent_err*scale)
    return s_curve


#############################################################################################


def shiftDIST(den, sint, fr):
    s_den = den.Clone() 
    for b in range(0, den.GetNbinsX()):
        s_den.SetBinContent(b, (1-fr)*den.GetBinContent(b+sint) + (fr)*den.GetBinContent(b+1+sint))
        s_den.SetBinError(b, np.hypot((1-fr)*den.GetBinError(b+sint), (fr)*den.GetBinError(b+1+sint)))
    return s_den


#############################################################################################

def scaleDIST(den, fr):
    s_den = den.Clone() 
    for b in range(0, den.GetNbinsX()):
        s_den.SetBinContent(b, fr*den.GetBinContent(b))
        s_den.SetBinError(b, fr*den.GetBinError(b))
    return s_den


#############################################################################################

def FindshiftTOC(dat, sim):
    dat_curve = dat.Clone() #ROOT.TH1D("placeholder", "", 80, 0, 80)
    sim_curve = sim.Clone() #ROOT.TH1D("placeholder", "", 80, 0, 80)
    
    dat_blow = 0.0
    dat_bhigh = 0.0
    sim_blow = 0.0
    sim_bhigh = 0.0
    for b in range(0,dat_curve.GetNbinsX()):
      if dat_curve.GetBinContent(b) > 0.65:
           dat_bhigh = b 
           dat_blow = b-1
           break
    for b in range(0,sim_curve.GetNbinsX()):
      if sim_curve.GetBinContent(b) > 0.65:
           sim_bhigh = b 
           sim_blow = b-1
           break
    dat_b = dat_blow + ((0.65-dat_curve.GetBinContent(dat_blow))/(dat_curve.GetBinContent(dat_bhigh)-dat_curve.GetBinContent(dat_blow)))
    sim_b = sim_blow + ((0.65-sim_curve.GetBinContent(sim_blow))/(sim_curve.GetBinContent(sim_bhigh)-sim_curve.GetBinContent(sim_blow)))
    shift = dat_b - sim_b
    return shift

################################################################################################

def assessRatioEffPropagateUncerts(den, num): #To report pseudo-data efficiency error 
    d_den = den.Clone() 
    n_num = num.Clone()

    es0 = ROOT.Double(0) 
    is0 = d_den.IntegralAndError(0,den.GetNbinsX(),es0)
    es1 = ROOT.Double(0) 
    is1 = n_num.IntegralAndError(0,num.GetNbinsX(),es1)
    if is0 == 0.0 or is1 == 0.0:
      rat_err = 0.0
    else:
      rat_err = (is1/is0)*np.hypot(es0/is0, es1/is1) 
    
    return rat_err


def assessCorrelatedDiffEffUncerts(eff_pseudo, eff_sig, denominator): #To report difference error in pseudo-data efficiency and signal efficiency that are correlated 
    # eff is normalized to 1 
    rat_err = round (math.sqrt(math.fabs(eff_pseudo*denominator - eff_sig*denominator))/denominator, 2)  

    return rat_err


def assessSignalEffUncerts(den, num): #To report signal efficiency error from a binomial distributionof events 
    # eff is normalized to 1
    d_den = den.Clone() 
    n_num = num.Clone()
    if d_den.Integral() == 0:
      return 0
    eff_sig = n_num.Integral()/d_den.Integral()
    denominator = den.Integral() 
    eff_sig = abs(eff_sig)
    rat_err = round (math.sqrt(eff_sig*(1-eff_sig)/(denominator)), 2)  

    return rat_err

def assessRatioEffUncerts(eff_num, err_eff_num, eff_den, err_eff_den):
    # eff is normalzied to 1
    tot_err_one = err_eff_num/eff_den #FIXME needs a factor of two 
    tot_err_two = eff_num*err_eff_den/(eff_den**2) #FIXME needs a factor of two 

    rat_err = round (np.hypot(tot_err_one, tot_err_two), 2)  

    return rat_err


################################################################################################

def assessMCToDataUncerts(eff_slide, err_slide, eff_scale, err_scale, eff_toc, err_toc, tkscl_uncerts, stat_unc, eff_sig, err_sig):

    slide_uncerts = round(100*(1-(eff_slide/eff_sig)), 2)
    err_slide_uncerts = assessRatioEffUncerts(eff_slide, err_slide, eff_sig, err_sig)
    scale_uncerts = round(100*(1-(eff_scale/eff_sig)), 2)
    err_scale_uncerts = assessRatioEffUncerts(eff_scale, err_scale, eff_sig, err_sig)
    toc_uncerts = round(100*(1-(eff_toc/eff_sig)), 2)
    err_toc_uncerts = assessRatioEffUncerts(eff_toc, err_toc, eff_sig, err_sig)
    
    print("01 TMMC-TMData : slide distr %.2f +/- %.2f and scale distr %.2f +/- %.2f" % (slide_uncerts, err_slide_uncerts, scale_uncerts, err_scale_uncerts))
    total = np.sqrt (slide_uncerts**2 + toc_uncerts**2 + tkscl_uncerts**2 + stat_unc**2) #FIXME tkrescl
    err_total = np.sqrt(err_slide_uncerts**2 + err_toc_uncerts**2)
    
    print( " 1-vtx Unc. by SF_{nclsedtks,non} : %.2f +/- %.2f (sys_distr) +/- %.2f +/- %.2f (sys_scale_toc) +/- %.2f (sys_stat) +/- %.2f (sys_tkrescl) : %.2f +/- %.2f%% " % (slide_uncerts, err_slide_uncerts, toc_uncerts, err_toc_uncerts, stat_unc, tkscl_uncerts, total, err_total) )

    return total

################################################################################################

def assessSigToTMMCUncerts(eff_slide, err_slide, eff_scale, err_scale, eff_toc, err_toc, eff_sig, err_sig):

    slide_uncerts = round(100*(1-(eff_slide/eff_sig)), 2)
    err_slide_uncerts = assessRatioEffUncerts(eff_slide, err_slide, eff_sig, err_sig)
    scale_uncerts = round(100*(1-(eff_scale/eff_sig)), 2)
    err_scale_uncerts = assessRatioEffUncerts(eff_scale, err_scale, eff_sig, err_sig)
    toc_uncerts = round(100*(1-(eff_toc/eff_sig)), 2)
    err_toc_uncerts = assessRatioEffUncerts(eff_toc, err_toc, eff_sig, err_sig)
    
    print("02 sigMC-TMMC :  slide distr %.2f +/- %.2f and toc %.2f +/- %.2f" % (slide_uncerts, err_slide_uncerts, toc_uncerts, err_toc_uncerts))
    total = np.sqrt (toc_uncerts**2)
    err_total = np.sqrt(err_toc_uncerts**2)
    
    print( " 1-vtx Unc. by SF_{TMMC-to-signalMC} : %.2f +/- %.2f (sys_scale_toc)%% " % (total, err_total) )

    return total

################################################################################################

def calcTocShiftUncert(low, cent, hi):

    outRmsVals = []

    for i in range(0, len(low)):
        rms =  np.sqrt( ((cent[i] - low[i])**2 + (cent[i]-hi[i])**2)/2 )
        rms = round(rms, 2)
        outRmsVals.append(rms)

    return outRmsVals



################################################################################################


# Initialize stuff:

years = [ '20161p2', '2017p8'] #FIXME
#years = [ '2017p8'] #FIXME
doShift  = True
reweight = True
#toc_shift = 0.0   # How much to move the turn-on curve by
#shift_fr  = 0.0   # How much to slide the closeseedtk dist by (decimal part)
#shift_val = 0     # How much to slide the closeseedtk dist by (integer part)

mass = str(sys.argv[1])
if mass != '0200' and mass != '0400' and mass != '0800':
    sys.exit("invalid mass %s" % mass)

ctaus       = ['000100', '000300', '001000', '010000', '030000',] #['1000', '3000', '30000'] 
psd_methods = ['none', 'slide_distr', 'scale_distr', 'scale_toc'] # 'trackrescl']

if mass == '0400' : ctaus       = ['000100', '000300', '001000']
if mass == '0800' : ctaus       = ['000100', '000300']

# Start actually doing stuff

uncertArray = []
all_stat_uncerts = {}
all_overlap_uncerts = {}

list_eff = []
list_eff_2 = []
list_ctau = [ 0.1, 0.3, 1.0, 10.0, 30.0]
list_ctau = np.log10(list_ctau)
list_err = []
list_err_2 = []
list_relerr = []
list_relerr_2 = []
list_data_MC_ratio = []
list_data_MC_ratio_2 = []
list_new_err = []
list_new_err_2 = []
list_new_relerr = []
list_new_relerr_2 = []

for year in years:  
  for ctau in ctaus:
    possible_eta = { "Low" : 0, "High": 0 }
    eff_eta = { "Low" : 0.0, "High": 0.0 }
    err_eta = { "Low" : 0.0, "High": 0.0 }
    new_err_eta = { "Low" : 0.0, "High": 0.0 }
    data_MC_ratio_eta = { "Low" : 0.0, "High": 0.0 }
    data_MC_ratio_mass_tau = 0.0
    tot_err_mass_tau = 0.0
    tot_eff_mass_tau = 0.0
    for eta in ['Low','High']:
    #for eta in ['Low']:

        effArray = []
        errArray = []
        effArray_emu = []
        errArray_emu = []
        DiffeffArray = []
        DifferrArray = []
        DiffeffArray_emu = []
        DifferrArray_emu = []
        none_sig_integral = 0.0
        none_tmdat_integral = 0.0
        none_tmmc_integral = 0.0
        err_none_tmdat_integral = 0.0
        err_none_tmmc_integral = 0.0
        none_tmdat_eff = 0.0
        none_tmmc_eff = 0.0
        err_none_tmdat_eff = 0.0
        err_none_tmmc_eff = 0.0
        stat_uncerts = 0.0
        overlap_uncerts = 0.0
        frac_vetoodvv = 0.0
        frac_vetopdvv = 0.0
        dataMC_unc = 0.0
        stat_unc = 0.0
        emulate_unc = 0.0
        dvv_unc = 0.0
        ovp_unc = 0.0
        for psd_method in psd_methods:
                
                sim_str = ''
                dat_str = ''

                if not reweight:
                    sim_str = "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_%sMoveVecEta_NoPreSelRelaxBSPNotwVetodR0p4JetBySameDecayJetHistsOnnormdzulv30bmofftosspreselv10_32_noCorrection/background_btagpresel_%s.root" % (eta,year)
                    dat_str = "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_%sMoveVecEta_NoPreSelRelaxBSPNotwVetodR0p4JetBySameDecayJetHistsOnnormdzulv30bmofftosspreselv10_32_noCorrection/BTagDispl%s.root" % (eta,year)
                    #sim_str = "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_%sMoveVecEta_NoPreSelRelaxBSPNotwVetodR0p4JetBySameDecayJetHistsOnnormdzulv30mofftosspreselv10_32_noCorrection/background_jethtpresel_%s.root" % (eta,year)
                    #dat_str = "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_%sMoveVecEta_NoPreSelRelaxBSPNotwVetodR0p4JetBySameDecayJetHistsOnnormdzulv30mofftosspreselv10_32_noCorrection/JetHT%s.root" % (eta,year)
                else:
                    sim_str = "/uscms/home/joeyr/nobackup/crabdirs/Peace_TrackMover/TrackMover_%sMoveVecEta_NoPreSelRelaxBSPNotwVetodR0p4JetBySameDecayJetHistsOnnormdzulv30bmofftosspreselv10_32_tau%06ium_M%i_2DCorrection/background_btagpresel_%s.root" % (eta,int(ctau), int(mass), year)
                    dat_str = "/uscms/home/joeyr/nobackup/crabdirs/Peace_TrackMover/TrackMover_%sMoveVecEta_NoPreSelRelaxBSPNotwVetodR0p4JetBySameDecayJetHistsOnnormdzulv30bmofftosspreselv10_32_tau%06ium_M%i_2DCorrection/BTagDispl%s.root" % (eta,int(ctau), int(mass), year)
                    #sim_str = "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_%sMoveVecEta_NoPreSelRelaxBSPNotwVetodR0p4JetBySameDecayJetHistsOnnormdzulv30mofftosspreselv10_32_tau%06ium_M%i_2DCorrection/background_jethtpresel_%s.root" % (eta,int(ctau), int(mass), year)
                    #dat_str = "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_%sMoveVecEta_NoPreSelRelaxBSPNotwVetodR0p4JetBySameDecayJetHistsOnnormdzulv30mofftosspreselv10_32_tau%06ium_M%i_2DCorrection/JetHT%s.root" % (eta,int(ctau), int(mass), year)

                  
                tm_sim  = ROOT.TFile(sim_str)
                tm_dat  = ROOT.TFile(dat_str)
                
                
                dat_den = tm_dat.Get('all_closeseedtks_den')
                sim_den = tm_sim.Get('all_closeseedtks_den')
                
                dat_num = tm_dat.Get('all_closeseedtks_num')
                sim_num = tm_sim.Get('all_closeseedtks_num')
                sim_curve = sim_num.Clone()
                sim_den = sim_den.Clone()
                sim_curve.Divide(sim_curve, sim_den, 1, 1, "B")


                dat_curve = dat_num.Clone()
                dat_den = dat_den.Clone()
                dat_curve.Divide(dat_curve, dat_den, 1, 1, "B")

                str_ctau = ''
                if (int(ctau) > 500):
                   str_ctau = str(int(ctau)/1000)+'mm'
                else:
                   str_ctau = str(ctau)+'um'

                #print(ctau, str_ctau)
                signal  = ROOT.TFile('/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_'+eta+'MoveVecEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetBySameDecayMiniJetHistsOnnormdzUlv30bmpreselv6/mfv_neu_tau'+ctau+'um_M'+mass+'_'+ year +'.root')
                
                sig_dist = signal.Get('nocuts_closeseedtks_den')
                sig_denom = sig_dist.Clone()
                sig_aaaaa = signal.Get('all_closeseedtks_num')
                sig_curve = sig_aaaaa.Clone()
                #psd_dist = ROOT.TH1D("psd_dist", "M"+mass+"ctau"+ctau+"um", 80, 0, 80)
                sig_curve.Divide(sig_curve, sig_denom, 1, 1, "B")
                
                signal_non  = ROOT.TFile('/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_'+eta+'MoveVecEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetBySameDecayMiniJetHistsOnnormdzUlv30bmpreselv6/mfv_neu_tau'+ctau+'um_M'+mass+'_'+ year +'.root')
                
                signon_dist = signal_non.Get('nocuts_closeseedtks_den')
                non_denom = signon_dist.Clone() 
                non_aaaaa = signal_non.Get('all_closeseedtks_num')
                signon_curve = non_aaaaa.Clone()
                signon_curve.Divide(signon_curve, non_denom, 1, 1, "B")
                
                signal_vetopdvv  = ROOT.TFile('/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_'+eta+'MoveVecEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetBySameDecayMiniJetHistsOnnormdzUlv30bmpreselv6/mfv_neu_tau'+ctau+'um_M'+mass+'_'+ year +'.root')
                
                sigovp_dist = signal_vetopdvv.Get('nocuts_dvv_den')
                ovp_denom = sigovp_dist.Clone() 
                ovp_aaaaa = signal_vetopdvv.Get('all_dvv_num')
                sigovp_curve = ovp_aaaaa.Clone()
                sigovp_curve.Divide(sigovp_curve, ovp_denom, 1, 1, "B")

                # Calculate the scale factors
                scale_factors = dat_den.Clone() 
                scale_divisor = sim_den.Clone() 
                scale_factors.Scale(1.0/(scale_factors.Integral() + 1e-16)) #FIXME
                scale_divisor.Scale(1.0/(scale_divisor.Integral() + 1e-16)) #FIXME
                #scale_factors = scaledDist(scale_factors) #FIXME
                #scale_divisor = scaledDist(scale_divisor) #FIXME
                scale_factors.Divide(scale_factors, scale_divisor, 1, 1, "B")

                scale_factors_emu = sim_den.Clone()
                scale_divisor_emu = signon_dist.Clone()
                scale_factors_emu.Scale(1.0/(scale_factors_emu.Integral() + 1e-16)) #FIXME
                scale_divisor_emu.Scale(1.0/(scale_divisor_emu.Integral() + 1e-16)) #FIXME
                #scale_factors_emu = scaledDist(scale_factors_emu) #FIXME
                #scale_divisor_emu = scaledDist(scale_divisor_emu) #FIXME
                scale_factors_emu.Divide(scale_factors_emu, scale_divisor_emu, 1, 1, "B")

                # Fill pseudodata distribution
                psd_dist = sig_dist.Clone()
                psd_emu_dist = signon_dist.Clone()
                psdtmmc_dist = sim_den.Clone()
                
                if psd_method == 'slide_distr':
                    #print(" sig mean : ", sig_dist.GetMean())
                    #print(" TM data mean : ", dat_den.GetMean())
                    #print(" TM MC mean : ", sim_den.GetMean())
                    shift_val = sim_den.GetMean()-dat_den.GetMean()
                    shift_int = int(shift_val) - 1
                    shift_fr = shift_val - shift_int
                    #print(" Dist shift (red) : ", -1*round(shift_val,2))  #negative means shifting signal distr. to the left and positive means shifting signal distr. to the right  
                    psd_dist = shiftDIST(psd_dist, shift_int, shift_fr) 
                    #print(" psd mean : ", psd_dist.GetMean())
                    psdtmmc_dist = shiftDIST(psdtmmc_dist, shift_int, shift_fr)
                    #print(" psdtmmc mean : ", psdtmmc_dist.GetMean())
                    
                    shift_emu_val = signon_dist.GetMean()-sim_den.GetMean() 
                    shift_emu_int = int(shift_emu_val) - 1 
                    shift_emu_fr = shift_emu_val - shift_emu_int
                    #print(" Dist shift (green) : ", -1*round(shift_emu_val,2)) #negative means shifting signal distr. to the left and positive means shifting signal distr. to the right   
                    #print(" novp sig mean : ", signon_dist.GetMean())
                    #print(" TM MC mean : ", sim_den.GetMean())
                    psd_emu_dist = shiftDIST(psd_emu_dist, shift_emu_int, shift_emu_fr) 
                    #print(" psd emu mean : ", psd_emu_dist.GetMean())
                
                if psd_method == 'scale_distr':
                    psd_dist.Multiply(scale_factors)
                    psdtmmc_dist.Multiply(scale_factors)
                    psd_emu_dist.Multiply(scale_factors_emu)
                    #psd_dist.Scale(sig_dist.Integral()/psd_dist.Integral())
                    #psdtmmc_dist.Scale(sim_den.Integral()/psdtmmc_dist.Integral())
                    #psd_emu_dist.Scale(signon_dist.Integral()/psd_emu_dist.Integral())
               
                psd_dist.Scale(1.0/(psd_dist.Integral() + 1e-16))

                psdtmmc_dist.Scale(1.0/(psdtmmc_dist.Integral() + 1e-16))

                psd_emu_dist.Scale(1.0/(psd_emu_dist.Integral() + 1e-16))
                # Make the TM data and TM sim turn-on curves
                none_tmdat_eff = dat_num.Integral()/(dat_den.Integral() + 1e-16)
                none_tmmc_eff = sim_num.Integral()/(sim_den.Integral() + 1e-16)
                pre_tmdat_dist = dat_den.Clone()
                pre_tmmc_dist = sim_den.Clone()
                
                if psd_method == 'none':
                    psdtmdat_dist = dat_den.Clone()
                    psdtmdat_dist.Scale(1.0/(psdtmdat_dist.Integral() + 1e-16))
                
                tmdat_dist = dat_num.Clone()
                tmmc_dist = sim_num.Clone()
                dat_num.Divide(dat_num, dat_den, 1, 1, "B")
                sim_num.Divide(sim_num, sim_den, 1, 1, "B")
                
                if psd_method == 'none':
                    psdtmdat_curve = dat_num.Clone()
                
                # Make the pseudodata turn-on curve
                 
                psd_curve = shiftDIST(sig_curve, 0, 0.0) #sig_curve
                psdtmmc_curve = shiftDIST(sim_num, 0, 0.0) #sim_num
                psd_emu_curve = shiftDIST(signon_curve, 0, 0.0) #signon_curve
                if psd_method == 'scale_toc':
                    psd_curve = scaledTOC(sig_aaaaa, sig_denom, dat_num, sim_num)
                    psdtmmc_curve = scaledTOC(tmmc_dist, pre_tmmc_dist, dat_num, sim_num)
                    psd_emu_curve = scaledTOC(non_aaaaa, non_denom, sim_num, signon_curve)
                    #psd_curve.Scale(sig_curve.Integral()/psd_curve.Integral())
                    #psdtmmc_curve.Scale(sim_num.Integral()/psdtmmc_curve.Integral())
                    #psd_emu_curve.Scale(signon_curve.Integral()/psd_emu_curve.Integral())
                if psd_method == 'slide_toc':
                    shift = FindshiftTOC(dat_num, sim_num)
                    shift_int = int(shift) - 1
                    shift_fr = shift - shift_int
                    #print(" TOC shift (red) : ", round(shift,3))   #negative means shifting signal TOC. to the left and positive means shifting signal TOC. to the right because pseudo TOC should turn on before/after signal TOC 
                    psd_curve = shiftDIST(sig_curve, shift_int, shift_fr)   
                    psdtmmc_curve = shiftDIST(sim_num, shift_int, shift_fr)
                    
                    
                    shift_emu = FindshiftTOC(sim_num, signon_curve)
                    shift_int_emu = int(shift_emu) - 1
                    shift_fr_emu = shift_emu - shift_int_emu
                    #print(" TOC shift (green) : ", round(shift_emu,3))  #negative means shifting signal TOC. to the left and positive means shifting signal TOC. to the right because pseudo TOC should turn on before/after signal TOC 
                    psd_emu_curve = shiftDIST(signon_curve, shift_int_emu, shift_emu_fr)
                
                
                #possible_sig = sig_dist.Integral() + 1e-16
                possible_signon = signon_dist.Integral() + 1e-16
                possible_sigovp = sigovp_dist.Integral() + 1e-16
                possible_ovpfail = sigovp_dist.Integral(sigovp_dist.FindBin(0.0300), sigovp_dist.FindBin(0.0360)) + 1e-16 #20% vertex position discrepancy between data and MC leads to overlapping boundary discrepancy 
                possible_all = sigovp_dist.Integral() + signon_dist.Integral() + 1e-16
                
                possible_psd = psd_dist.Integral() + 1e-16
                possible_psd_emu = psd_emu_dist.Integral() + 1e-16
               
                #pre_sig_dist = sig_dist.Clone()
                pre_signon_dist = signon_dist.Clone()
                pre_sigovp_dist = sigovp_dist.Clone()
                pre_psd_dist = psd_dist.Clone()
                pre_psd_emu_dist = psd_emu_dist.Clone()
              
                #sig_dist.Multiply(sig_curve)
                signon_dist.Multiply(signon_curve)
                sigovp_dist.Multiply(sigovp_curve)
                psd_dist.Multiply(psd_curve)
                psd_emu_dist.Multiply(psd_emu_curve)

                #fpsdout3 = ROOT.TFile(psd_method+"_"+"_"+mass+"_"+ctau+"_"+eta+"_curve.root", "recreate")
                #psd_curve.Write()
                #fpsdout3.Close()
                
                pass_signon = signon_dist.Integral()
                pass_sigovp =  sigovp_dist.Integral() 
                pass_psd = psd_dist.Integral()
                pass_psd_emu = psd_emu_dist.Integral()
                
                possible_eta[eta] = possible_all
                
                eff_sig = 1e-16 + (pass_signon+pass_sigovp)/(possible_all)
                eff_signon = 1e-16 + (pass_signon/possible_signon)
                eff_sigovp = 1e-16 + (pass_sigovp/possible_sigovp)
                eff_psd = 1e-16 + (pass_psd/possible_psd)
                eff_psd_emu = 1e-16 + (pass_psd_emu/possible_psd_emu)
                eff_eta[eta] = 1e-16 + eff_sig 

                dvv_unc = (possible_ovpfail*(eff_signon - eff_sigovp))/((possible_all)*eff_sig) #discrepancy with respect to yield
                ovp_unc = (possible_sigovp*(eff_sigovp - (eff_sigovp/2.0)))/((possible_all)*eff_sig) 

                err_signon = assessSignalEffUncerts(pre_signon_dist, signon_dist)#assessRatioEffPropagateUncerts(pre_signon_dist, signon_dist) #FIXME NOW
                err_sigovp = assessSignalEffUncerts(pre_sigovp_dist, sigovp_dist)#assessRatioEffPropagateUncerts(pre_signon_dist, signon_dist) #FIXME NOW
                err_sig = np.sqrt((err_signon/eff_signon)**2 +  (err_sigovp/eff_sigovp)**2)
                
                err_psd = assessRatioEffPropagateUncerts(pre_psd_dist, psd_dist)
                err_psd_emu = assessRatioEffPropagateUncerts(pre_psd_emu_dist, psd_emu_dist)
                
                effArray.append(eff_psd)
                errArray.append(err_psd)
                effArray_emu.append(eff_psd_emu)
                errArray_emu.append(err_psd_emu)

                if psd_method == 'none':
                    none_signon_integral = round(possible_signon,2) 
                    none_sigovp_integral = round(possible_sigovp,2) 
                    frac_vetopdvv = possible_sigovp/(possible_all)
                    frac_vetoodvv = possible_signon/(possible_all)
                  
                    print("Mass: %s   Ctau: %s  \n" % (mass, ctau))
                    print("1-vtx incl. Eff of total %.2f : %.2f +/- %.2f \n" % (none_signon_integral+none_sigovp_integral, 100*eff_sig, 100*err_sig))
                    print("1-vtx novp Eff of total %.2f : %.2f +/- %.2f (frac. %.2f) \n" % (none_signon_integral, 100*eff_signon, 100*err_signon, 100*frac_vetoodvv))
                    print("1-vtx ovp Eff of total %.2f : %.2f +/- %.2f (frac. %.2f) \n" % (none_sigovp_integral, 100*eff_sigovp, 100*err_sigovp, 100*frac_vetopdvv))
                    #overlap_uncerts = round (100*overlap_right_unc,2)
                    es0 = ROOT.Double(0) 
                    is0 = dat_den.IntegralAndError(0,200,es0)
                    none_tmdat_integral = round(is0,2)
                    err_none_tmdat_integral = round(es0,2)
                    err_none_tmdat_eff = assessRatioEffPropagateUncerts(pre_tmdat_dist, tmdat_dist)
                    es1 = ROOT.Double(0) 
                    is1 = sim_den.IntegralAndError(0,200,es1)
                    none_tmmc_integral = round(is1,2)
                    err_none_tmmc_integral = round(es1,2)
                    err_none_tmmc_eff = assessRatioEffPropagateUncerts(pre_tmmc_dist, tmmc_dist)

                else:
                    DiffeffArray.append(eff_psd - effArray[0])
                    DifferrArray.append(assessCorrelatedDiffEffUncerts(eff_psd, effArray[0], none_signon_integral))
                    DiffeffArray_emu.append(eff_psd_emu - effArray_emu[0])
                    DifferrArray_emu.append(assessCorrelatedDiffEffUncerts(eff_psd_emu, effArray_emu[0], none_signon_integral))

        print("Probe Data-to-MC Overall effciency difference \n")
        print("Total TM MC %.2f +/- %.2f (w/ Eff. %.2f +/- %.2f) and Total TM Data %.2f +/- %.2f (w/ Eff. %.2f +/- %.2f)\n" % (none_tmmc_integral, err_none_tmmc_integral, 100*none_tmmc_eff, 100*err_none_tmmc_eff, none_tmdat_integral, err_none_tmdat_integral, 100*none_tmdat_eff, 100*err_none_tmdat_eff))
        print(" Mass: %s GeV  Ctau: %s um  Year: %s   Eta: %s" % (mass, ctau, year, eta))
        #print(" Data/MC efficiency ratio is: %.2f +/- %.2f" % (none_tmdat_eff/none_tmmc_eff, none_tmdat_eff/none_tmmc_eff*math.sqrt( (err_none_tmdat_eff/none_tmdat_eff)**2 + (err_none_tmmc_eff/none_tmmc_eff)**2 )))
        data_MC_ratio = none_tmdat_eff/none_tmmc_eff
        data_MC_ratio_stat_unc = none_tmdat_eff/none_tmmc_eff*math.sqrt( (err_none_tmdat_eff/none_tmdat_eff)**2 + (err_none_tmmc_eff/none_tmmc_eff)**2 )
        print(" 1 - Data/MC efficiency ratio is: %.2f +/- %.2f percent" % ( 100*(1-data_MC_ratio), 100*data_MC_ratio_stat_unc))
        data_MC_ratio_eta[eta] = data_MC_ratio

        for i in range(1,len(psd_methods)):
            if (i == 1 or i==3):
               dataMC_unc +=  (-100*DiffeffArray[i-1]/effArray[0])**2
               print("%s pseudo eff %.2f +/- %.2f \t pseudo eff - incl. sig eff %.2f +/- %.2f \t 1-ratio %.2f +/- %.2f \n" % (psd_methods[i], 100*effArray[i], 100*errArray[i], 100*DiffeffArray[i-1], 100*DifferrArray[i-1], -100*DiffeffArray[i-1]/effArray[0], -100*DifferrArray[i-1]/effArray[0]))
        #print("Probe how well TM MC emulating signal MC \n")
        for i in range(1,len(psd_methods)):
            if (i == 3):
               emulate_unc += (-100*DiffeffArray_emu[i-1]/effArray_emu[0])**2
               stat_unc = (-100*DifferrArray_emu[i-1]/effArray_emu[0])**2 
               print("%s pseudo emulating eff %.2f +/- %.2f \t pseudo emulating eff - novp. sig eff %.2f +/- %.2f \t 1-ratio %.2f +/- %.2f \n" % (psd_methods[i],100*effArray_emu[i], 100*errArray_emu[i], 100*DiffeffArray_emu[i-1], 100*DifferrArray_emu[i-1], -100*DiffeffArray_emu[i-1]/effArray_emu[0], -100*DifferrArray_emu[i-1]/effArray_emu[0]))
        #print("Probe overlapped LLPs \n")

        print "New data_MC_ratio_stat_unc %.2f %%" % (100*data_MC_ratio_stat_unc)
        iso_tot_unc_new = np.sqrt( (100*data_MC_ratio_stat_unc)**2 + emulate_unc) # note emulate_unc is actually a squared quantity already

        # Old "stat_unc" appears to be related (at least in part) to the signal MC stat uncertainty, and is tiny for the 55 GeV VH samples. let's see if it matters anywhere at all, otherwise we ignore it.
        print "Old dataMC_unc %.2f %%" % math.sqrt(dataMC_unc)
        print "Old stat_unc %.2f %%" % math.sqrt(stat_unc)
        print "Old (and current) emulate_unc %.2f %%" % math.sqrt(emulate_unc)
        iso_tot_unc = np.sqrt(dataMC_unc + stat_unc + emulate_unc) 

        #print("pseudo slide dvv eff %.2f +/- %.2f \t pseudo slide dvv eff - dvv eff %.2f \t 1-ratio %.2f \n" % (100*eff_psd_dvv, 100*err_psd_dvv, 100*(eff_psd_dvv-eff_dvv), 100*(1-(eff_psd_dvv/eff_dvv))))

        #print("\n")
        print( " Isolated-LLP Unc. : %.2f Data-to-MC Unc +/- %2.f Stat. Unc +/- %.2f Emulate Unc. %% or %.2f %%" % (np.sqrt(dataMC_unc), np.sqrt(stat_unc), np.sqrt(emulate_unc), iso_tot_unc))
        print( " Mid Overlapped-LLP Unc. : %.2f %% " % np.sqrt((dvv_unc*100)**2))
        print( " Real Overlapped-LLP Unc. : %.2f %% " % np.sqrt((ovp_unc*100)**2))
        print( " Two Overlapped-LLP Unc. : %.2f %% " % np.sqrt((ovp_unc*100)**2 + (dvv_unc*100)**2))
        
        #print("\n")
    
        dvv_unc = dvv_unc*100 #FIXME
        ovp_unc = ovp_unc*100 #FIXME

        old_tot_err = np.sqrt(ovp_unc**2 + dvv_unc**2 + iso_tot_unc**2)
        new_tot_err = np.sqrt(ovp_unc**2 + dvv_unc**2 + iso_tot_unc_new**2)
        #print( " Weighted Iso. & Ovp. LLP Unc. : %.2f %%" %(old_tot_err))
        err_eta[eta] = old_tot_err 
        new_err_eta[eta] = new_tot_err 
        #print(eta, " 1-vtx err. ", old_tot_err)
        #print("\n")

    print("\n")
    tot_possible = possible_eta['Low'] + possible_eta['High']
    frac_low = possible_eta['Low']/tot_possible
    print('frac low = ', frac_low)
    print('old err low = ', err_eta['Low'])
    print('new err low = ', new_err_eta['Low'])
    frac_high = possible_eta['High']/tot_possible
    print('frac high = ', frac_high)
    print('old err high = ', err_eta['High'])
    print('new err high = ', new_err_eta['High'])
    data_MC_ratio_mass_tau = frac_low*(data_MC_ratio_eta['Low']) + frac_high*(data_MC_ratio_eta['High'])
    new_tot_err_mass_tau = frac_low*(new_err_eta['Low']**2) + frac_high*(new_err_eta['High']**2)

    tot_err_mass_tau = frac_low*(err_eta['Low']**2) + frac_high*(err_eta['High']**2)
    tot_eff_mass_tau = frac_low*(eff_eta['Low']) + frac_high*(eff_eta['High'])
    # JPR FIXME: note that the new relative uncertainty is an uncertainty on the signal eff, not the SF itself.
    # SF_abs_uncertainty = SF * (eff_signal_MC_abs_uncertainty / eff_signal_MC) = SF * eff_signal_MC_relative_uncertainty
    # oh wait, so the SF_relative_uncertainty = SF_abs_uncertainty/SF = eff_signal_MC_relative_uncertainty ?? Double check.
    #
    # okay yes:
    # SF +/- SF_err = SF +/- SF *eff_MC_err/eff_MC ==> rel_SF_err = eff_MC_err/eff_MC
    print( " Weighted #eta 1-vtx Data/MC ratio : %.2f %%" %(data_MC_ratio_mass_tau*100))
    print( " Weighted #eta 1-vtx Rel.Unc. (new) : %.2f %%" %(np.sqrt(new_tot_err_mass_tau)))
    print( " Weighted #eta 1-vtx Abs.Unc. on the Data/MC ratio (new) : %.2f %%" %(data_MC_ratio_mass_tau*np.sqrt(new_tot_err_mass_tau)))

    print( " Weighted #eta 1-vtx Eff. : %.2f %%" %(tot_eff_mass_tau*100))
    print( " Weighted #eta 1-vtx Rel.Unc. (old) : %.2f %%" %(np.sqrt(tot_err_mass_tau)))
    print( " Weighted #eta 1-vtx Abs.Unc. (old) : %.2f %%" %(tot_eff_mass_tau*np.sqrt(tot_err_mass_tau)))
    if year=='20161p2':
      list_eff.append(tot_eff_mass_tau*100)
      list_err.append(tot_eff_mass_tau*np.sqrt(tot_err_mass_tau))
      list_relerr.append(np.sqrt(tot_err_mass_tau))

      list_data_MC_ratio.append(data_MC_ratio_mass_tau*100)
      list_new_err.append(data_MC_ratio_mass_tau*np.sqrt(new_tot_err_mass_tau))
      list_new_relerr.append(np.sqrt(new_tot_err_mass_tau))
    else:
      list_eff_2.append(tot_eff_mass_tau*100)
      list_err_2.append(tot_eff_mass_tau*np.sqrt(tot_err_mass_tau))
      list_relerr_2.append(np.sqrt(tot_err_mass_tau))

      list_data_MC_ratio_2.append(data_MC_ratio_mass_tau*100)
      list_new_err_2.append(data_MC_ratio_mass_tau*np.sqrt(new_tot_err_mass_tau))
      list_new_relerr_2.append(np.sqrt(new_tot_err_mass_tau))

ps = plot_saver(plot_dir('TM_Results_June5_2026_neu_m%s' % mass), size=(700,600), pdf=True, log=False)
canvas = ps.c
canvas.SetBottomMargin(0.15)
# Create arrays for x, y, x errors, and y errors
x = array('d', np.asarray(list_ctau))
y = array('d', np.asarray(list_eff)*np.asarray(list_data_MC_ratio)/100.)
ex = array('d', [ 0.0, 0.0, 0.0, 0.0, 0.0])
ey = array('d', np.asarray(list_eff)*np.asarray(list_new_relerr)/100.)

y2 = array('d', np.asarray(list_eff_2)*np.asarray(list_data_MC_ratio_2)/100.)
ey2 = array('d', np.asarray(list_eff_2)*np.asarray(list_new_relerr_2)/100.)
# Create a TGraphErrors object
gr = ROOT.TGraphErrors(len(x), x, y, ex, ey)
gr2 = ROOT.TGraphErrors(len(x), x, y2, ex, ey2)

# Set graph attributes
gr.SetMarkerColor(ROOT.kBlue)
gr.SetMarkerStyle(20)
gr.SetLineColor(ROOT.kBlue)
gr.GetYaxis().SetRangeUser(0.0, 100.0)
gr.GetYaxis().SetTitle("1-vtx efficiency for an LLP decay, post SF")
# Draw the graph
gr.Draw("AP")
gr2.SetMarkerColor(ROOT.kRed)
gr2.SetMarkerStyle(20)
gr2.SetLineColor(ROOT.kRed)
gr2.GetYaxis().SetRangeUser(0.0, 100.0)
gr2.GetYaxis().SetTitle("1-vtx efficiency for an LLP decay, post SF")
gr2.Draw("P")
#canvas.SetLogx()

gr.SetTitle("pre(post)-VFP 2016");
gr2.SetTitle("2017+2018");
ROOT.gPad.BuildLegend(0.42,0.795,0.70,0.935,"","p");
gr.SetTitle("Neutralino/Gluino->tbs with LLP of "+str(mass)+" GeV")
xax = gr.GetXaxis()

for i in range(len(list_ctau)):
    bin_ind = xax.FindBin(list_ctau[i])
    xax.SetBinLabel(bin_ind, str(math.pow(10,list_ctau[i]))+" mm ")
    xax.ChangeLabel(bin_ind, 30.0)


p = ROOT.TPaveText(0.013, 0.080, 0.105, 0.120, "brNDC")
p.SetFillColor(ROOT.kWhite)
p.SetTextFont(42)
p.SetTextAlign(12)
p.AddText("c#tau")
p.SetTextSize(0.04)
p.SetBorderSize(0)
p.Draw()
# Update the canvas
ROOT.gPad.Modified()
ROOT.gPad.Update()
canvas.Update()
ps.save('neu_'+str(mass)+'GeV_mmCtau_eff')


canvas2 = ps.c
canvas2.SetBottomMargin(0.15)
# Create arrays for x, y, x errors, and y errors
relerr_y1 = array('d', np.asarray(list_new_relerr))
relerr_y2 = array('d', np.asarray(list_new_relerr_2))
# Create a TGraphErrors object
gr = ROOT.TGraph(len(x), x, relerr_y1)
gr2 = ROOT.TGraph(len(x), x, relerr_y2)

# Set graph attributes
gr.SetMarkerColor(ROOT.kBlue)
gr.SetMarkerStyle(20)
gr.SetLineColor(ROOT.kBlue)
gr.GetYaxis().SetRangeUser(0.0, 100.0)
gr.GetYaxis().SetTitle("1-vtx relative uncertainty for LLP-decay efficiency (based on SF)")
# Draw the graph
gr.Draw("AP")
gr2.SetMarkerColor(ROOT.kRed)
gr2.SetMarkerStyle(20)
gr2.SetLineColor(ROOT.kRed)
gr2.GetYaxis().SetRangeUser(0.0, 100.0)
gr2.GetYaxis().SetTitle("1-vtx relative uncertainty for LLP-decay efficiency (based on SF)")
gr2.Draw("P")
#canvas.SetLogx()

gr.SetTitle("pre(post)-VFP 2016");
gr2.SetTitle("2017+2018");
ROOT.gPad.BuildLegend(0.42,0.795,0.70,0.935,"","p");
gr.SetTitle("Neutalino/Gluino->tbs with LLP of "+str(mass)+" GeV")
xax = gr.GetXaxis()

for i in range(len(list_ctau)):
    bin_ind = xax.FindBin(list_ctau[i])
    xax.SetBinLabel(bin_ind, str(math.pow(10,list_ctau[i]))+" mm ")
    xax.ChangeLabel(bin_ind, 30.0)


p = ROOT.TPaveText(0.013, 0.080, 0.105, 0.120, "brNDC")
p.SetFillColor(ROOT.kWhite)
p.SetTextFont(42)
p.SetTextAlign(12)
p.AddText("c#tau")
p.SetTextSize(0.04)
p.SetBorderSize(0)
p.Draw()
# Update the canvas
ROOT.gPad.Modified()
ROOT.gPad.Update()
canvas2.Update()
ps.save('neu_'+str(mass)+'GeV_mmCtau_relerr')
