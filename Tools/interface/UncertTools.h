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
    }
}

#endif
