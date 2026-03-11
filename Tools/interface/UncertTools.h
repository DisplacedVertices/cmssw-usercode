#ifndef JMTucker_Tools_UncertTools_h
#define JMTucker_Tools_UncertTools_h

namespace jmt {
    namespace UncertTools {
        float mc_eff(float pt, int flavor, int year);
        bool reject_btag_sf(float pt, float rand_x, int sf_var, int year);
        bool admit_btag_sf(float pt, float rand_x, int flavor, int sf_var, int year);
        bool refactor_btag_hlt(float bscore, bool current_pass_status, float rand_x, int year);
        bool refactor_calo_btag_hlt(float bscore, bool current_pass_status, float rand_x, int year);
        bool refactor_calo_lo_btag_hlt(float bscore, bool current_pass_status, float rand_x, int year);
        bool refactor_prompt_tk_eff(int nprompt, bool current_pass_status, float rand_x, int year);
        const float jer_pt(const float jet_gen_energy, const float jet_energy, const float jet_pt, const float aeta, const bool var_up);
        const float jer_pt_alt(const float jet_gen_energy, const TLorentzVector& jet_p4, const bool var_up);

        // https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
        const double sf2017[14] = {1.1082, 1.1285, 1.0916, 1.1352, 1.2116, 1.0637, 1.0489, 1.1170, 1.1952, 1.0792, 1.3141, 1.4113, 1.2679, 1.0378};
        const double un2017[14] = {0.0563, 0.0252, 0.0247, 0.0617, 0.0686, 0.0812, 0.0789, 0.0871, 0.0912, 0.1314, 0.0967, 0.2315, 0.0547, 0.0668};

        const double sf2018[14] = {1.1436, 1.1538, 1.1481, 1.1304, 1.1590, 1.1628, 1.1423, 1.1479, 1.1360, 1.1911, 1.2919, 1.3851, 1.2670, 1.0367};
        const double un2018[14] = {0.0104, 0.0347, 0.0363, 0.0687, 0.0141, 0.0554, 0.0447, 0.1086, 0.0619, 0.0870, 0.0732, 0.1504, 0.0607, 0.1575};

        const double sf20161[14] = {1.0910, 1.1084, 1.0833, 1.0684, 1.0556, 1.0155, 0.9889, 1.0213, 1.0084, 1.1146, 1.1637, 1.1994, 1.2023, 1.0063};
        const double un20161[14] = {0.0227, 0.0176, 0.0215, 0.0347, 0.0340, 0.0249, 0.0211, 0.0393, 0.0492, 0.0987, 0.0687, 0.1063, 0.0347, 0.0458};

        const double sf20162[14] = {1.0993, 1.1228, 1.1000, 1.0881, 1.0761, 1.0452, 1.0670, 1.0352, 1.0471, 1.1365, 1.2011, 1.1662, 1.1599, 1.0672};
        const double un20162[14] = {0.0132, 0.0317, 0.0267, 0.0933, 0.0382, 0.0538, 0.0344, 0.0477, 0.0488, 0.0672, 0.1996, 0.1008, 0.0316, 0.0453};

        double get_sf(int index, int year);
        double get_un(int index, int year);
    }
}

#endif
