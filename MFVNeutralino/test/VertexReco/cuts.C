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

  printf("%s n>=2\n", nr.sample.fn);
  
  int nevents = 0;
  std::map<std::string, int> nvtxpass;
  std::map<std::string, int> nevtpass;
  
  for (Long64_t jentry = 0, nentries = nr.tree->GetEntriesFast(); jentry < nentries; ++jentry) {
    if (nr.tree->LoadTree(jentry) < 0) break;
    nr.tree->GetEntry(jentry);

    if (jentry % 25000 == 0) {
      printf("\r%12li/%12li entries processed", jentry, nentries);
      fflush(stdout);
    }

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
  //EVAL_CUT(nr.nt.njetsntks     > 1);

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

  printf("\r                                                                                \r");
  fflush(stdout);

  if (nevents != nr.sample.nevents)
    printf("nevents %i not right\n", nevents);
  assert(nevents == nr.sample.nevents);
  const double intlumi = 20000;
  const double all = nevtpass["all"];
  for (auto cut : nevtpass) {
    double eff, eff2;
    bool is_all = cut.first == "all";
    
    if (is_all)
      eff = float(cut.second)/nevents;
    else {
      if (cut.second == 0)
        eff = -1;
      else
        eff = all/cut.second;
      eff2 = float(cut.second)/nevents;
    }

    const double sigL = nr.sample.xsec * intlumi;
    const double N = eff * sigL;
    confint ci = clopper_pearson(cut.second, nevents);
    ci.lower *= sigL;
    ci.upper *= sigL;
    if (is_all)
      printf("%24s: nevtpass: %10i nevents: %10i  eff: %10.6f  N: %10.1f [%10.1f, %10.1f]\n", "eff with all cuts", cut.second, nevents, eff, N, ci.lower, ci.upper);
    else
      printf("w/o %20s: nevtpass: %10i          %7s n-1 eff: %10.6f  eff %10.6f\n", cut.first.c_str(), cut.second, "", eff, eff2);
  }
}

//const char* Sample::file_dir = "crab/VertexRecoPlay/roots/";
const char* Sample::file_dir = "dcap://cmsdca3.fnal.gov:24145/pnfs/fnal.gov/usr/cms/WAX/resilient/tucker/crabdump/VertexRecoPlay/";
const char* Sample::root_dir = "playMYQno";

int main() {
  printf("opening files from %s\n", Sample::file_dir);

  Sample samples[] = {
//    {"mfv_neutralino_tau0000um_M0200.root", 99850 , 1 },   // 888.0 },
//    {"mfv_neutralino_tau0000um_M0400.root", 100000, 1 },   // 17.4  },
//    {"mfv_neutralino_tau0000um_M0600.root", 100000, 1 },   // 1.24  },
//    {"mfv_neutralino_tau0000um_M0800.root", 99900 , 1 },   // 0.15  },
//    {"mfv_neutralino_tau0000um_M1000.root", 99996 , 1 },   // 0.0233},
//    {"mfv_neutralino_tau0010um_M0200.root", 100000, 1 },   // 888.0 },
//    {"mfv_neutralino_tau0010um_M0400.root", 100000, 1 },   // 17.4  },
//    {"mfv_neutralino_tau0010um_M0600.root", 99700 , 1 },   // 1.24  },
//    {"mfv_neutralino_tau0010um_M0800.root", 99950 , 1 },   // 0.15  },
//    {"mfv_neutralino_tau0010um_M1000.root", 99899 , 1 },   // 0.0233},
//    {"mfv_neutralino_tau0100um_M0200.root", 99700 , 1 },   // 888.0 },
//    {"mfv_neutralino_tau0100um_M0400.root", 99250 , 1 },   // 17.4  },
//    {"mfv_neutralino_tau0100um_M0600.root", 99650 , 1 },   // 1.24  },
//    {"mfv_neutralino_tau0100um_M0800.root", 100000, 1 },   // 0.15  },
//    {"mfv_neutralino_tau0100um_M1000.root", 99749 , 1 },   // 0.0233},
//    {"mfv_neutralino_tau1000um_M0200.root", 99752 , 1 },   // 888.0 },
//    {"mfv_neutralino_tau1000um_M0400.root", 99850 , 1 },   // 17.4  },
//    {"mfv_neutralino_tau1000um_M0600.root", 99851 , 1 },   // 1.24  },
//    {"mfv_neutralino_tau1000um_M0800.root", 99949 , 1 },   // 0.15  },
//    {"mfv_neutralino_tau1000um_M1000.root", 100000, 1 },   // 0.0233},
//    {"mfv_neutralino_tau9900um_M0200.root", 99950 , 1 },   // 888.0 },
//    {"mfv_neutralino_tau9900um_M0400.root", 100000, 1 },   // 17.4  },
//    {"mfv_neutralino_tau9900um_M0600.root", 99950 , 1 },   // 1.24  },
//    {"mfv_neutralino_tau9900um_M0800.root", 99900 , 1 },   // 0.15  },
//    {"mfv_neutralino_tau9900um_M1000.root", 99899 , 1 },   // 0.0233},
//    {"qcdht0100.root",         4455967, 1.04e7  },
//    {"qcdht0250.root",        11137722, 2.76e5  },
//    {"qcdht0500.root",         4991784, 8.43e3  },
//    {"qcdht1000.root",         6968522, 2.04e2  },
    {"ttbarhadronic.root",     9738903, 225.2 * 0.457},
    {"ttbarsemilep.root",      7987193, 225.2 * 0.438},
    {"ttbardilep.root",        1389075, 225.2 * 0.105},
  };

  for (const Sample& s : samples) {
    NtupleReader nr(s);
    Run(nr);
  }
}
