#include <cmath>
#include <vector>
#include "JMTucker/Tools/interface/UncertTools.h"

namespace jmt {
    namespace UncertTools {
        bool reject_btag_sf(float pt, float rand_x, int sf_var, int year) {
            float x = pt;
            float adjust = 0.0;

            if      (x > 20.0 and x < 30.0)  { adjust = 0.021808577701449394;  }
            else if              (x < 50.0)  { adjust = 0.0066848257556557655; }
            else if              (x < 70.0)  { adjust = 0.0097699258476495743; }
            else if              (x < 100.0) { adjust = 0.012062436901032925;  }
            else if              (x < 140.0) { adjust = 0.0097645819187164307; }
            else if              (x < 200.0) { adjust = 0.01024820189923048;   }
            else if              (x < 300.0) { adjust = 0.053553581237792969;  }
            else if              (x < 600.0) { adjust = 0.030205903574824333;  }
            else                             { adjust = 0.079471737146377563;  }

            float sf = 0.932707+(0.00201163*(log(x+19)*(log(x+18)*(3-(0.36597*log(x+18)))))); // Data/MC SF
            sf += (sf_var * adjust);

            if (year != 2017) return false; //FIXME
            if (rand_x > sf) return true;  // true meaning "reject the btag"
            return false;                  // false meaning "keep the btag"
        }

        bool reject_btag_hlt(float bscore, float pt, float rand_x, int sf_var, int year) {
            float x = pt;

            // This is a do-nothing conditional, which will just be a placeholder in case we need pT-dependent corrections later
            // FIXME
            if (x > 90 and false) {
                return false;
            }

            const float sfs[20] = {0.871, 0.733, 0.735, 0.738, 0.744, 0.787, 0.902, 0.826, 0.805, 0.895, 0.871, 0.864, 0.902, 0.897, 0.92, 0.904, 0.937, 0.923, 0.97, 0.982};
            int bin = std::floor(bscore/0.05);

            float sf = sfs[bin];

            if (year != 2017 || sf_var != 0) return false; //FIXME
            if (rand_x > sf) return true;  // true meaning "reject the btag"
            return false;                  // false meaning "keep the btag"
        }

        bool refactor_prompt_tk_eff(int nprompt, bool current_pass_status, float rand_x) {

            // FIXME need a better way for this, but here are the survival factors for now

            // Factors derived from prescaled HT425 trigger
            std::vector<float> veto_factors{-0.893308, 0.898857, 0.870336, 0.892738, 0.923750, 0.950358, 0.965808,
                                             0.975436, 0.981205, 0.985363, 0.989302, 0.990224, 0.991814, 0.993340,
                                             0.994583, 0.995452, 0.996463, 0.995928, 0.996308, 0.996597, 0.997387,
                                             0.996520, 0.998216, 0.996268, 0.998126, 0.998431, 0.999427, 0.997307,
                                             0.998534, 0.999582, 0.997612, 0.998354, -1.000000, 0.992482, 0.994563};

            float veto_factor = nprompt < (int)(veto_factors.size()) ? veto_factors[nprompt] : 1.000;
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
    }
}
