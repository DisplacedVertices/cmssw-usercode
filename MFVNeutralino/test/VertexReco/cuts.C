// alias rootg++ 'g++ `root-config --cflags --libs --glibs`'
// rootg++ -I../../plugins -std=c++0x cuts.C && ./a.out

#include <assert.h>
#include <TROOT.h>
#include <TTree.h>
#include <TFile.h>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <Math/QuantFunc.h>
#include "VertexNtuple.h"

void die_if_not(bool condition, const char* msg, ...) {
  if (condition)
    return;
  va_list args;
  va_start(args, msg);
  vfprintf(stderr, msg, args);
  va_end(args);
  assert(0);
}

struct Sample {
  static const char* prefix;
  const char* fn;
  int nevents;
  double xsec;
};

//const char* Sample::prefix = "";
const char* Sample::prefix = "crab/VertexRecoPlay/";

class Analyzer {
public:
  Sample sample;
  TFile* file;
  TTree* tree;
  VertexNtuple nt;

  Analyzer(const char*, const Sample&);
  ~Analyzer();
  void Loop();
};

Analyzer::~Analyzer() {
  file->Close();
  delete file;
}

Analyzer::Analyzer(const char* dir_name, const Sample& s)
  : sample(s)
{
  file = new TFile(TString(s.prefix) + s.fn);
  die_if_not(file && file->IsOpen(), "couldn't open file %s\n", s.fn);

  TDirectory* dir = (TDirectory*)file->Get(dir_name);
  die_if_not(dir, "couldn't get dir %s from %s\n", dir_name, s.fn);
  
  dir->GetObject("tree", tree);
  die_if_not(tree, "couldn't get tree \"tree\" from %s/%s\n", s.fn, dir_name);

  tree->SetMakeClass(1);
  nt.read(tree);
}

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

void Analyzer::Loop() {
  if (tree == 0)
    return;

  int nevents = tree->GetEntries();
  die_if_not(nevents == sample.nevents, "nevents %i not right\n", nevents);

  std::map<std::string, int> nevtpass;

  for (int ievent = 0; ievent < nevents; ++ievent) {
    die_if_not(tree->LoadTree(ievent) >= 0, "problem with tree for %s\n", sample.fn);
    tree->GetEntry(ievent);

    //printf("%u %i/%i\n", nt.event, nt.isv, nt.nsv);

    if (!nt.pass_trigger || nt.pfjetpt4 < 60)
      continue;

    std::map<std::string, int> nvtxpass;
    const int nsv = int(nt.ntracks.size());

// heh
#define EVAL_CUT(x) { std::string _x(#x); _x.replace(_x.find("nt."), 3, ""); _x.replace(_x.find("[isv]"), 5, ""); cuts[_x] = x; }

    for (int isv = 0; isv < nsv; ++isv) {
      std::map<std::string, bool> cuts;
      cuts["all"] = true;
      EVAL_CUT(nt.ntracks      [isv] >= 7);
    //EVAL_CUT(nt.ntracksptgt10[isv] > 0);
    //EVAL_CUT(nt.sumpt2       [isv] > 200);
    //EVAL_CUT(nt.p            [isv] > 15);
    //EVAL_CUT(nt.mass         [isv] > 25);
      EVAL_CUT(nt.maxtrackpt   [isv] > 15);
    //EVAL_CUT(nt.maxm1trackpt [isv] > 5);
    //EVAL_CUT(nt.maxm2trackpt [isv] > 3);
      EVAL_CUT(nt.drmin        [isv] < 0.4);
      EVAL_CUT(nt.drmax        [isv] < 4);
    //EVAL_CUT(nt.dravg        [isv] < 2.5);
    //EVAL_CUT(nt.bs2dcompat   [isv] > 200);
    //EVAL_CUT(nt.bs2dsig      [isv] > 5);
      EVAL_CUT(nt.bs2derr      [isv] < 0.005);
      EVAL_CUT(nt.njetssharetks[isv] > 1);

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


    for (auto n : nvtxpass)
      if (n.second >= 2)
        ++nevtpass[n.first];
  }

  const double intlumi = 20000;
  printf("%s n>=2\n", sample.fn);
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
    const double N = eff * sample.xsec * intlumi;
    confint ci = clopper_pearson(cut.second, nevents);
    ci.lower *= sample.xsec * intlumi;
    ci.upper *= sample.xsec * intlumi;
    if (is_all)
      printf("%24s: nevtpass: %10i nevents: %10i  eff: %10.6f  N: %10.1f [%10.1f, %10.1f]\n", "eff with all cuts", cut.second, nevents, eff, N, ci.lower, ci.upper);
    else
      printf("w/o %20s: nevtpass: %10i          %7s n-1 eff: %10.6f\n", cut.first.c_str(), cut.second, "", eff);
  }
}

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
    Analyzer a("playMYQno", s);
    a.Loop();
  }
}
