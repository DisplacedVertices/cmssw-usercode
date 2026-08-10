#include <cmath>
#include <vector>
#include <random>
#include <iostream>
#include "TLorentzVector.h"
#include "JMTucker/Tools/interface/UncertTools.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
    namespace UncertTools {

        // When applying btag SFs, if SF > 1.0, then we need info about the MC efficiencies for true b/c/l jets to get btagged
        // This function will return it.
        float mc_eff(float pt, int flav, int year) {
                                      //                       2016APV (idx = 0)                                                  2016 (idx = 1)
                                      //                         2017  (idx = 2)                                                  2018 (idx = 3)
            const float b_effs[4][9] = {{0.711, 0.797, 0.814, 0.823, 0.823, 0.830, 0.835, 0.830, 0.818}, {0.720, 0.803, 0.821, 0.827, 0.826, 0.832, 0.834, 0.825, 0.802},
                                        {0.743, 0.826, 0.844, 0.847, 0.844, 0.837, 0.824, 0.808, 0.798}, {0.731, 0.817, 0.831, 0.835, 0.827, 0.820, 0.807, 0.797, 0.787}};

            const float c_effs[4][9] = {{0.340, 0.372, 0.363, 0.368, 0.372, 0.395, 0.410, 0.432, 0.470}, {0.343, 0.376, 0.369, 0.372, 0.375, 0.391, 0.401, 0.410, 0.425},
                                        {0.342, 0.395, 0.390, 0.394, 0.396, 0.393, 0.396, 0.414, 0.425}, {0.326, 0.377, 0.372, 0.371, 0.371, 0.368, 0.373, 0.385, 0.392}};

            const float l_effs[4][9] = {{0.239, 0.154, 0.114, 0.110, 0.114, 0.138, 0.157, 0.192, 0.261}, {0.228, 0.150, 0.111, 0.106, 0.107, 0.126, 0.139, 0.160, 0.206},
                                        {0.108, 0.103, 0.086, 0.083, 0.082, 0.086, 0.097, 0.135, 0.176}, {0.095, 0.092, 0.075, 0.073, 0.071, 0.075, 0.083, 0.116, 0.146}};

            const int pt_idx = pt > 600.0 ? 8 : (pt > 300.0 ? 7 : (pt > 200.0 ? 6 : (pt > 140.0 ? 5 : (pt > 100.0 ? 4 : (pt > 70.0 ? 3 : (pt > 50 ? 2 : (pt > 30.0 ? 1 : 0)))))));
            const int yr_idx = year == 2018 ? 3 : (year == 2017 ? 2 : (year == 20162 ? 1 : 0));

            if (flav == 0) { return l_effs[yr_idx][pt_idx]; }
            if (flav == 4) { return c_effs[yr_idx][pt_idx]; }
            if (flav == 5) { return b_effs[yr_idx][pt_idx]; }

            else {
                std::cout << "Invalid flavor idx!" << std::endl;
                return 0.00000001;
            }
        }

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        // Should probably combine this with admit_btag_sf() below
        // When applying btag SFs, this function will demote a btagged jet to a non-btagged jet when SF < 1.0
        bool reject_btag_sf(float pt, float rand_x, int sf_var, int year) {
            float x = pt;
            float adjust = 0.0;
            float sf     = 0.0;

            if (year != 20161 and year != 20162 and year !=  2017 and year != 2018) return false; //FIXME

            if (year == 20161) {
                if      (x > 20.0 and x < 30.0)  { adjust = 0.014748076908290386; }
                else if              (x < 50.0)  { adjust = 0.0074093989096581936; }
                else if              (x < 70.0)  { adjust = 0.010435092262923717; }
                else if              (x < 100.0) { adjust = 0.0087881358340382576; }
                else if              (x < 140.0) { adjust = 0.0086383512243628502; }
                else if              (x < 200.0) { adjust = 0.0086802346631884575; }
                else if              (x < 300.0) { adjust = 0.014497509226202965; }
                else if              (x < 600.0) { adjust = 0.04255574569106102; }
                else                             { adjust = 0.049184385687112808; }
    
                sf = 1.0007*(1.+0.000290434*x)/(1.+0.000349262*x);
            }

            else if (year == 20162) {
                if      (x > 20.0 and x < 30.0)  { adjust = 0.023307550698518753; }
                else if              (x < 50.0)  { adjust = 0.0071532656438648701; }
                else if              (x < 70.0)  { adjust = 0.0064413133077323437; }
                else if              (x < 100.0) { adjust = 0.0082752639427781105; }
                else if              (x < 140.0) { adjust = 0.0088317524641752243; }
                else if              (x < 200.0) { adjust = 0.0082253143191337585; }
                else if              (x < 300.0) { adjust = 0.016790542751550674; }
                else if              (x < 600.0) { adjust = 0.023497793823480606; }
                else                             { adjust = 0.095938533544540405; }
    
                sf = 0.90894+0.00422186*log(x+19)*log(x+18)*(3-0.460651*log(x+18));
            }

            else if (year == 2017) {
                if      (x > 20.0 and x < 30.0)  { adjust = 0.021808577701449394;  }
                else if              (x < 50.0)  { adjust = 0.0066848257556557655; }
                else if              (x < 70.0)  { adjust = 0.0097699258476495743; }
                else if              (x < 100.0) { adjust = 0.012062436901032925;  }
                else if              (x < 140.0) { adjust = 0.0097645819187164307; }
                else if              (x < 200.0) { adjust = 0.01024820189923048;   }
                else if              (x < 300.0) { adjust = 0.053553581237792969;  }
                else if              (x < 600.0) { adjust = 0.030205903574824333;  }
                else                             { adjust = 0.079471737146377563;  }
    
                sf = 0.932707+(0.00201163*(log(x+19)*(log(x+18)*(3-(0.365970*log(x+18)))))); // Data/MC SF
            }

            else if (year == 2018) {
                if      (x > 20.0 and x < 30.0)  { adjust = 0.05439353734254837;  }
                else if              (x < 50.0)  { adjust = 0.016492579132318497; }
                else if              (x < 70.0)  { adjust = 0.017301365733146667; }
                else if              (x < 100.0) { adjust = 0.014144605025649071;  }
                else if              (x < 140.0) { adjust = 0.015795128419995308; }
                else if              (x < 200.0) { adjust = 0.016265010461211205;   }
                else if              (x < 300.0) { adjust = 0.05125650018453598;  }
                else if              (x < 600.0) { adjust = 0.08231847733259201;  }
                else                             { adjust = 0.16305074095726013;  }
    
                sf = 0.882297+(0.00426142*(log(x+19)*(log(x+18)*(3-(0.411195*log(x+18)))))); // Data/MC SF
            }

            sf += (sf_var * adjust);
            // If we're in a regime where SF > 1.0, then we don't need to kill any btags
            if (sf > 1.0) return false;

            if (rand_x > sf) return true;  // true meaning "reject the btag"
            return false;                  // false meaning "keep the btag"
        }

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        // Should probably combine this with reject_btag_sf() below
        // When applying btag SFs, this function will promote a non-btagged jet to a btagged jet when SF > 1.0
        bool admit_btag_sf(float pt, float rand_x, int flavor, int sf_var, int year) {
            float x = pt;
            float adjust = 0.0;
            float sf     = 0.0;

            if (year != 20161 and year != 20162 and year !=  2017 and year != 2018) return false; //FIXME

            if (year == 20161) {
                if      (x > 20.0 and x < 30.0)  { adjust = 0.014748076908290386; }
                else if              (x < 50.0)  { adjust = 0.0074093989096581936; }
                else if              (x < 70.0)  { adjust = 0.010435092262923717; }
                else if              (x < 100.0) { adjust = 0.0087881358340382576; }
                else if              (x < 140.0) { adjust = 0.0086383512243628502; }
                else if              (x < 200.0) { adjust = 0.0086802346631884575; }
                else if              (x < 300.0) { adjust = 0.014497509226202965; }
                else if              (x < 600.0) { adjust = 0.04255574569106102; }
                else                             { adjust = 0.049184385687112808; }
    
                sf = 1.0007*(1.+0.000290434*x)/(1.+0.000349262*x);
            }

            else if (year == 20162) {
                if      (x > 20.0 and x < 30.0)  { adjust = 0.023307550698518753; }
                else if              (x < 50.0)  { adjust = 0.0071532656438648701; }
                else if              (x < 70.0)  { adjust = 0.0064413133077323437; }
                else if              (x < 100.0) { adjust = 0.0082752639427781105; }
                else if              (x < 140.0) { adjust = 0.0088317524641752243; }
                else if              (x < 200.0) { adjust = 0.0082253143191337585; }
                else if              (x < 300.0) { adjust = 0.016790542751550674; }
                else if              (x < 600.0) { adjust = 0.023497793823480606; }
                else                             { adjust = 0.095938533544540405; }
    
                sf = 0.90894+0.00422186*log(x+19)*log(x+18)*(3-0.460651*log(x+18));
            }

            else if (year == 2017) {
                if      (x > 20.0 and x < 30.0)  { adjust = 0.021808577701449394;  }
                else if              (x < 50.0)  { adjust = 0.0066848257556557655; }
                else if              (x < 70.0)  { adjust = 0.0097699258476495743; }
                else if              (x < 100.0) { adjust = 0.012062436901032925;  }
                else if              (x < 140.0) { adjust = 0.0097645819187164307; }
                else if              (x < 200.0) { adjust = 0.01024820189923048;   }
                else if              (x < 300.0) { adjust = 0.053553581237792969;  }
                else if              (x < 600.0) { adjust = 0.030205903574824333;  }
                else                             { adjust = 0.079471737146377563;  }
    
                sf = 0.932707+(0.00201163*(log(x+19)*(log(x+18)*(3-(0.365970*log(x+18)))))); // Data/MC SF
            }

            else if (year == 2018) {
                if      (x > 20.0 and x < 30.0)  { adjust = 0.05439353734254837;  }
                else if              (x < 50.0)  { adjust = 0.016492579132318497; }
                else if              (x < 70.0)  { adjust = 0.017301365733146667; }
                else if              (x < 100.0) { adjust = 0.014144605025649071;  }
                else if              (x < 140.0) { adjust = 0.015795128419995308; }
                else if              (x < 200.0) { adjust = 0.016265010461211205;   }
                else if              (x < 300.0) { adjust = 0.05125650018453598;  }
                else if              (x < 600.0) { adjust = 0.08231847733259201;  }
                else                             { adjust = 0.16305074095726013;  }
    
                sf = 0.882297+(0.00426142*(log(x+19)*(log(x+18)*(3-(0.411195*log(x+18)))))); // Data/MC SF
            }

            sf += (sf_var * adjust);

            // If we're in a regime where sf < 1.0, we don't need to admit any new btags
            if (sf < 1.0) return false;

            // Don't compare directly against sf
            float to_check = fabs((1-sf) / (1 - (1/mc_eff(x, flavor, year))));

            if (rand_x < to_check) return true;  // true meaning "admit the btag"
            return false;                  // false meaning "reject the btag"
        }

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        // This applies the PF btag trigger-level scale factors (2017/2018 only) 
        bool refactor_btag_hlt(float bscore, bool current_pass_status, float rand_x, int year) {

            if (year != 2017 and year != 2018) {
                return false;
            }

            const float sfs_17[20] = {0.88, 0.741, 0.719, 0.729, 0.753, 0.769, 0.898, 0.835, 0.776, 0.915, 0.862, 0.877, 0.88, 0.925, 0.915, 0.888, 0.932, 0.921, 0.978, 0.985};
            const float sfs_18[20] = {1.44, 1.023, 0.929, 0.861, 0.855, 0.828, 0.914, 0.911, 0.918, 0.880, 0.853, 0.864, 0.875, 0.902, 0.89, 0.896, 0.904, 0.892, 0.896, 0.902};
            int bin = std::floor(bscore/0.05);
            float sf = 0.0;

            if (year == 2017) { sf = sfs_17[bin]; }
            if (year == 2018) { sf = sfs_18[bin]; }

            if (current_pass_status and rand_x > sf) return false;  // true meaning "reject the btag"
            return current_pass_status;                  // false meaning "keep the btag"
        }

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        // This applies the "standard" calo btag trigger-level scale factors (all 4 eras) 
        bool refactor_calo_btag_hlt(float bscore, bool current_pass_status, float rand_x, int year) {

            if (year != 20161 and year != 20162 and year != 2017 and year != 2018) {
                std::cout << " Invalid year!" << std::endl;
                return false;
            }

            const float sfs_16apv[10] = {0.467, 0.936, 0.92, 0.944, 1.012, 0.984, 1.015, 0.992, 0.984, 1.001};
            const float sfs_16[10]    = {0.559, 0.826, 1.008, 0.954, 1.014, 0.999, 1.003, 1.005, 1.009, 1.004};
            const float sfs_17[10]    = {1.077, 0.505, 0.855, 0.847, 1.064, 0.959, 0.891, 0.997, 0.968, 0.999};
            const float sfs_18[10]    = {1.239, 0.874, 0.779, 0.869, 0.900, 0.833, 0.841, 0.904, 0.895, 0.908};
            int bin = std::floor(bscore/0.10);
            float sf = 0.0;

            if      (year == 20161) { sf = sfs_16apv[bin]; }
            else if (year == 20162) { sf = sfs_16[bin]; }
            else if (year == 2017)  { sf = sfs_17[bin]; }
            else if (year == 2018)  { sf = sfs_18[bin]; }

            bool data_eff_greater = (sf > 0.0);
            sf = fabs(sf);

            if (data_eff_greater and not current_pass_status) {
                if (rand_x > sf) return true;
            }
            else if (not data_eff_greater and current_pass_status) {
                if (rand_x > sf) return false;
            }

            return current_pass_status;

        }


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        // This applies the "low-score" calo btag trigger-level scale factors (2016/2016APV only) 
        bool refactor_calo_lo_btag_hlt(float bscore, bool current_pass_status, float rand_x, int year) {

            if (year != 20161 and year != 20162) {
                std::cout << " Invalid year!" << std::endl;
                return false;
            }

            const float sfs_16apv[10] = {0.974, 1.041, 1.05, 1.058, 1.083, 1.05, 1.073, 1.014, 1.034, 1.023};
            const float sfs_16[10]    = {1.127, 1.096, 1.05, 1.024, 1.039, 1.047, 1.048, 1.047, 1.038, 1.019};
            int bin = std::floor(bscore/0.10);
            float sf = 0.0;

            if      (year == 20161) { sf = sfs_16apv[bin]; }
            else if (year == 20162) { sf = sfs_16[bin]; }

            bool data_eff_greater = (sf > 0.0);
            sf = fabs(sf);

            if (data_eff_greater and not current_pass_status) {
                if (rand_x > sf) return true;
            }
            else if (not data_eff_greater and current_pass_status) {
                if (rand_x > sf) return false;
            }

            return current_pass_status;

        }

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        bool refactor_prompt_tk_eff(int nprompt, bool current_pass_status, float rand_x, int year) {

            std::vector<float> veto_factors_16apv{-0.836569, -0.949928, -0.902909, -0.817867, -0.765398, -0.682079,
                -0.564047, -0.484947, -0.432599, -0.355292, -0.292986, -0.262913,
                -0.229325, -0.218455, -0.195844, -0.221708, -0.208107, -0.201382,
                -0.131389, -0.194032, -0.188108, -0.175973, -0.142479, -0.229830,
                -0.175159, -0.736488, -1.000000, -0.665239, -0.893206, 0.998258,
                -1.000000, 0.995138, -1.000000, -1.000000, 0.959362, 0.975041};

            // Factors derived from prescaled HT325 trigger
            std::vector<float> veto_factors_16{-0.968568, 0.900743, 0.958604, 0.973404, 0.987213, 
                0.992749, 0.996319, 0.997547, 0.998171, 0.998389, 0.999324, 
                0.999355, 0.999809, 0.999485, 0.999663, 0.999498, 0.999892, 
                0.999443, 0.999719, 0.999671, 0.999928, 0.999966, 0.999695, 
                0.999126, 0.998568, 0.999158, 0.996556, 0.994503, 0.992709};

            // Factors derived from prescaled HT425 trigger
            std::vector<float> veto_factors_17{-0.893308, 0.898857, 0.870336, 0.892738, 0.923750, 0.950358, 0.965808,
                0.975436, 0.981205, 0.985363, 0.989302, 0.990224, 0.991814, 0.993340,
                0.994583, 0.995452, 0.996463, 0.995928, 0.996308, 0.996597, 0.997387,
                0.996520, 0.998216, 0.996268, 0.998126, 0.998431, 0.999427, 0.997307,
                0.998534, 0.999582, 0.997612, 0.998354, -1.000000, 0.992482, 0.994563};

            std::vector<float> veto_factors_18{-0.976912, 0.975135, 0.977347, 0.980247, 0.981858, 0.987241, 0.993849,
                0.994006, 0.998216, 0.998661, 0.998445, 0.998627, 0.997991, 0.999475,
                0.999116, 0.999079, 0.998664, 0.999030, 0.999338, 0.998512, 0.999148,
                0.999171, 0.999489, 0.999162, -0.632905, 0.999904, -1.000000, 0.999903,
                0.999625, 0.999249, 0.995987, -1.000000, -1.000000, 0.995224, -1.000000};

            float veto_factor = 1.000;

            if (year == 20161) {
                veto_factor = nprompt < (int)(veto_factors_16apv.size()) ? veto_factors_16apv[nprompt] : 1.000;
            }
            else if (year == 20162) {
                veto_factor = nprompt < (int)(veto_factors_16.size()) ? veto_factors_16[nprompt] : 1.000;
            }
            else if (year == 2017) {
                veto_factor = nprompt < (int)(veto_factors_17.size()) ? veto_factors_17[nprompt] : 1.000;
            }
            else if (year == 2018) {
                veto_factor = nprompt < (int)(veto_factors_18.size()) ? veto_factors_18[nprompt] : 1.000;
            }

            bool data_eff_greater = (veto_factor > 0.0);
            veto_factor = fabs(veto_factor);

            if (data_eff_greater and not current_pass_status) {
                if (rand_x > veto_factor) return true;
            }
            else if (not data_eff_greater and current_pass_status) {
                if (rand_x > veto_factor) return false;
            }

            return current_pass_status;

        }


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        const float jer_pt(const float jet_gen_energy, const float jet_energy, const float jet_pt, const float aeta, const bool var_up) {     
            int ind = -1;
            double scale_up    = 1.0;
            double scale_down  = 1.0;
            if      (aeta < 0.522) ind = 0;
            else if (aeta < 0.783) ind = 1;
            else if (aeta < 1.131) ind = 2;
            else if (aeta < 1.305) ind = 3;
            else if (aeta < 1.740) ind = 4;
            else if (aeta < 1.930) ind = 5;
            else if (aeta < 2.043) ind = 6;
            else if (aeta < 2.322) ind = 7;
            else if (aeta < 2.500) ind = 8;
            else if (aeta < 2.650) ind = 9;
            else if (aeta < 2.853) ind = 10;
            else if (aeta < 2.964) ind = 11;
            else if (aeta < 3.139) ind = 12;
            else if (aeta < 5.191) ind = 13;

            // https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
#ifdef MFVNEUTRALINO_2017
            const double sf[14] = {1.1082, 1.1285, 1.0916, 1.1352, 1.2116, 1.0637, 1.0489, 1.1170, 1.1952, 1.0792, 1.3141, 1.4113, 1.2679, 1.0378};
            const double un[14] = {0.0563, 0.0252, 0.0247, 0.0617, 0.0686, 0.0812, 0.0789, 0.0871, 0.0912, 0.1314, 0.0967, 0.2315, 0.0547};
#elif defined(MFVNEUTRALINO_2018)
            const double sf[14] = {1.1436, 1.1538, 1.1481, 1.1304, 1.1590, 1.1628, 1.1423, 1.1479, 1.1360, 1.1911, 1.2919, 1.3851, 1.2670, 1.0367};
            const double un[14] = {0.0104, 0.0347, 0.0363, 0.0687, 0.0141, 0.0554, 0.0447, 0.1086, 0.0619, 0.0870, 0.0732, 0.1504, 0.0607, 0.1575};
#elif defined(MFVNEUTRALINO_20161)
            const double sf[14] = {1.0910, 1.1084, 1.0833, 1.0684, 1.0556, 1.0155, 0.9889, 1.0213, 1.0084, 1.1146, 1.1637, 1.1994, 1.2023, 1.0063};
            const double un[14] = {0.0227, 0.0176, 0.0215, 0.0347, 0.0340, 0.0249, 0.0211, 0.0393, 0.0492, 0.0987, 0.0687, 0.1063, 0.0347, 0.0458};
#elif defined(MFVNEUTRALINO_20162)
            const double sf[14] = {1.0993, 1.1228, 1.1000, 1.0881, 1.0761, 1.0452, 1.0670, 1.0352, 1.0471, 1.1365, 1.2011, 1.1662, 1.1599, 1.0672};
            const double un[14] = {0.0132, 0.0317, 0.0267, 0.0933, 0.0382, 0.0538, 0.0344, 0.0477, 0.0488, 0.0672, 0.1996, 0.1008, 0.0316, 0.0453};
#else
#error bad year
#endif

            if (jet_gen_energy > 0) {
                const double up = sf[ind] + un[ind];
                const double dn = sf[ind] - un[ind];
                scale_up   = (jet_gen_energy + up * (jet_energy - jet_gen_energy)) / jet_energy;
                scale_down = (jet_gen_energy + dn * (jet_energy - jet_gen_energy)) / jet_energy;
            }

            if (var_up) return scale_up   * jet_pt;
            else        return scale_down * jet_pt;
        }

        const float jer_pt_alt(const float jet_gen_energy, const TLorentzVector& jet_p4, const bool var_up) {
            return jer_pt(jet_gen_energy, jet_p4.E(), jet_p4.Pt(), fabs(jet_p4.Eta()), var_up);
        }
    }
}
