#ifndef JMTucker_Tools_UncertTools_h
#define JMTucker_Tools_UncertTools_h

namespace jmt {
    namespace UncertTools {
        bool reject_btag_sf(float pt, float rand_x, int sf_var, int year);
        bool reject_btag_hlt(float bscore, float pt, float rand_x, int sf_var, int year);
        bool refactor_prompt_tk_eff(int nprompt, bool current_pass_status, float rand_x);
    }
}

#endif
