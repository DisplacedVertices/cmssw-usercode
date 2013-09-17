#include <Math/QuantFunc.h>
#include "ntuplereader.h"

struct confint {
  double lower;
  double upper;
  confint() : lower(0), upper(1) {}
};

confint clopper_pearson(const double n_on, const double n_tot, const double alpha=1-0.6827, const bool equal_tailed=true) {
  const double alpha_min = equal_tailed ? alpha/2 : alpha;
  confint res;
  if (n_on > 0)
    res.lower = ROOT::Math::beta_quantile(alpha_min, n_on, n_tot - n_on + 1);
  if (n_tot - n_on > 0)
    res.upper = ROOT::Math::beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on);
  return res;
}

void Run(NtupleReader& nr) {
  if (nr.tree == 0)
    return;
  
  int nevents = 0;
  std::map<std::string, int> nvtxpass;
  std::map<std::string, int> nevtpass;
  
  for (Long64_t jentry = 0, nentries = nr.tree->GetEntriesFast(); jentry < nentries; ++jentry) {
    if (nr.tree->LoadTree(jentry) < 0) break;
    nr.tree->GetEntry(jentry);

    //printf("%u %i/%i\n", nr.nt.event, nr.nt.isv, nr.nt.nsv);

    if (nr.nt.isv == -1) {
      ++nevents;

      for (auto n : nvtxpass)
        if (n.second >= 2)
          ++nevtpass[n.first];

      nvtxpass.clear();
      
      continue;
    }

    if (!nr.nt.pass_trigger || nr.nt.pfjetpt4 < 60)
      continue;

    std::map<std::string, bool> cuts;

    // heh
#define EVAL_CUT(x) { std::string _x(#x); _x.replace(_x.find("nr.nt."), 6, ""); cuts[_x] = x; }

    cuts["all"] = true;
    EVAL_CUT(nr.nt.ntracks       >= 7);
  //EVAL_CUT(nr.nt.ntracksptgt10 > 0);
  //EVAL_CUT(nr.nt.sumpt2        > 200);
  //EVAL_CUT(nr.nt.p             > 15);
  //EVAL_CUT(nr.nt.mass          > 25);
    EVAL_CUT(nr.nt.maxtrackpt    > 15);
  //EVAL_CUT(nr.nt.maxm1trackpt  > 5);
  //EVAL_CUT(nr.nt.maxm2trackpt  > 3);
    EVAL_CUT(nr.nt.drmin         < 0.4);
    EVAL_CUT(nr.nt.drmax         < 4);
  //EVAL_CUT(nr.nt.dravg         < 2.5);
  //EVAL_CUT(nr.nt.bs2dcompat    > 200);
  //EVAL_CUT(nr.nt.bs2dsig       > 5);
    EVAL_CUT(nr.nt.bs2derr       < 0.005);
    EVAL_CUT(nr.nt.njetssharetks > 1);

    for (auto icut : cuts) {
      bool anded = true;
      for (auto jcut : cuts) {
        if (icut.first == jcut.first)
          continue;
        anded = anded && jcut.second;
      }

      if (anded)
        ++nvtxpass[icut.first];
    }
  }

  if (nevents != nr.sample.nevents)
    printf("nevents %i not right\n", nevents);
  assert(nevents == nr.sample.nevents);
  const double intlumi = 20000;
  printf("%s n>=2\n", nr.sample.fn);
  const double all = nevtpass["all"];
  for (auto cut : nevtpass) {
    double eff;
    bool is_all = cut.first == "all";
    
    if (is_all)
      eff = float(cut.second)/nevents;
    else {
      if (cut.second == 0)
        eff = -1;
      else
        eff = all/cut.second;
    }

    const double sigL = nr.sample.xsec * intlumi;
    const double N = eff * sigL;
    confint ci = clopper_pearson(cut.second, nevents);
    ci.lower *= sigL;
    ci.upper *= sigL;
    if (is_all)
      printf("%24s: nevtpass: %10i nevents: %10i  eff: %10.6f  N: %10.1f [%10.1f, %10.1f]\n", "eff with all cuts", cut.second, nevents, eff, N, ci.lower, ci.upper);
    else
      printf("w/o %20s: nevtpass: %10i          %7s n-1 eff: %10.6f\n", cut.first.c_str(), cut.second, "", eff);
  }
}

const char* Sample::file_dir = "crab/VertexRecoPlay/";
const char* Sample::root_dir = "playMYQno";

int main() {
  
  Sample samples[] = {
    //    {"mfv_neutralino_tau0000um_M0200.root", 99250, 888.0 },
    {"mfv_neutralino_tau0000um_M0400.root", 99250, 1  },
    //    {"mfv_neutralino_tau0000um_M0600.root", 99250, 1.24  },
    //    {"mfv_neutralino_tau0000um_M0800.root", 99250, 0.15  },
    //    {"mfv_neutralino_tau0000um_M1000.root", 99250, 0.0233},
    //    {"mfv_neutralino_tau0010um_M0200.root", 99250, 888.0 },
    //{"mfv_neutralino_tau0010um_M0400.root", 99250, 1  },
    //    {"mfv_neutralino_tau0010um_M0600.root", 99250, 1.24  },
    //    {"mfv_neutralino_tau0010um_M0800.root", 99250, 0.15  },
    //    {"mfv_neutralino_tau0010um_M1000.root", 99250, 0.0233},
    //    {"mfv_neutralino_tau0100um_M0200.root", 99250, 888.0 },
    {"mfv_neutralino_tau0100um_M0400.root", 99250, 1  },
    //    {"mfv_neutralino_tau0100um_M0600.root", 99250, 1.24  },
    //    {"mfv_neutralino_tau0100um_M0800.root", 99250, 0.15  },
    //    {"mfv_neutralino_tau0100um_M1000.root", 99250, 0.0233},
    //    {"mfv_neutralino_tau1000um_M0200.root", 99250, 888.0 },
    {"mfv_neutralino_tau1000um_M0400.root", 99250, 1  },
    //    {"mfv_neutralino_tau1000um_M0600.root", 99250, 1.24  },
    //    {"mfv_neutralino_tau1000um_M0800.root", 99250, 0.15  },
    //    {"mfv_neutralino_tau1000um_M1000.root", 99250, 0.0233},
    //    {"mfv_neutralino_tau9900um_M0200.root", 99250, 888.0 },
    {"mfv_neutralino_tau9900um_M0400.root", 99250, 1  },
    //    {"mfv_neutralino_tau9900um_M0600.root", 99250, 1.24  },
    //    {"mfv_neutralino_tau9900um_M0800.root", 99250, 0.15  },
    //                                                   0.0233
    //    {"bjetsht0100.root",       99250, 1.34e5  },
    //    {"bjetsht0250.root",       99250, 5.83e3  },
    //    {"bjetsht0500.root",       99250, 2.18e2  },
    //    {"bjetsht1000.root",       99250, 4.71e0  },
    {"qcdht0100.root",         99250, 1.04e7  },
    {"qcdht0250.root",         99250, 2.76e5  },
    {"qcdht0500.root",         99250, 8.43e3  },
    {"qcdht1000.root",         99250, 2.04e2  },
    //    {"qcdpt0000.root",         99250, 4.859e10},
    //    {"qcdpt0005.root",         99250, 4.264e10},
    //    {"qcdpt0015.root",         99250, 9.883e08},
    //    {"qcdpt0030.root",         99250, 6.629e07},
    //    {"qcdpt0050.root",         99250, 8.149e06},
    //    {"qcdpt0080.root",         99250, 1.034e06},
    //    {"qcdpt0120.root",         99250, 1.563e05},
    //    {"qcdpt0170.root",         99250, 3.414e04},
    //    {"qcdpt0300.root",         99250, 1.760e03},
    //    {"qcdpt0470.root",         99250, 1.139e02},
    //    {"qcdpt0600.root",         99250, 2.699e01},
    //    {"qcdpt0800.root",         99250, 3.550e00},
    //    {"qcdpt1000.root",         99250, 7.378e-1},
    //    {"qcdpt1400.root",         99250, 3.352e-2},
    //    {"qcdpt1800.root",         99250, 1.829e-3},
    //    {"singletop_s.root",       99250, 3.79},
    //    {"singletop_s_tbar.root",  99250, 1.76},
    //    {"singletop_t.root",       99250, 56.4},
    //    {"singletop_t_tbar.root",  99250, 30.7},
    //    {"singletop_tW.root",      99250, 11.1},
    //    {"singletop_tW_tbar.root", 99250, 11.1},
    {"ttbarhadronic.root",     99250, 225.2 * 0.457},
    {"ttbarsemilep.root",      99250, 225.2 * 0.438},
    {"ttbardilep.root",        99250, 225.2 * 0.105},
    //    {"ttbarincl.root",         99250, 225.2},
    //    {"ttzjets.root",           99250, 0.172},
    //    {"ttwjets.root",           99250, 0.215},
    //    {"ttgjets.root",           99250, 1.44},
    //    {"tttt.root",              99250, 7.16E-4},
    //    {"tthbb.root",             99250, 0.1293 * 0.577},
    //    {"wjetstolnu.root",        99250, 3.04e4},
    //    {"ww.root",                99250, 57.1},
    //    {"wz.root",                99250, 32.3},
    //    {"zz.root",                99250, 8.3},
  };

  for (const Sample& s : samples) {
    NtupleReader nr(s);
    Run(nr);
  }
}
