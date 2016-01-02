// g++ -std=c++0x `root-config --cflags --glibs` prescales.cc -o prescales.exe && ./prescales.exe

#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <cassert>
#include <cmath>
#include <map>
#include <set>
#include <numeric>
#include <algorithm>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <vector>

class PRESCALES {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   UInt_t          run;
   UInt_t          lumi;
   unsigned long long          event;
   std::vector<bool>    *l1_was_seed;
   std::vector<int>     *l1_prescale;
   std::vector<int>     *l1_mask;
   std::vector<bool>    *pass_l1_premask;
   std::vector<bool>    *pass_l1;
   std::vector<bool>    *hlt_found;
   std::vector<int>     *hlt_prescale;
   std::vector<bool>    *pass_hlt;

   // List of branches
   TBranch        *b_run;   //!
   TBranch        *b_lumi;   //!
   TBranch        *b_event;   //!
   TBranch        *b_l1_was_seed;   //!
   TBranch        *b_l1_prescale;   //!
   TBranch        *b_l1_mask;   //!
   TBranch        *b_pass_l1_premask;   //!
   TBranch        *b_pass_l1;   //!
   TBranch        *b_hlt_found;   //!
   TBranch        *b_hlt_prescale;   //!
   TBranch        *b_pass_hlt;   //!

   PRESCALES(TTree *tree=0);
   virtual ~PRESCALES();
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
};

PRESCALES::PRESCALES(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("all.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("all.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("all.root:/MFVTriggerPrescales");
      dir->GetObject("t",tree);

   }
   Init(tree);
}

PRESCALES::~PRESCALES()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t PRESCALES::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t PRESCALES::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
   }
   return centry;
}

void PRESCALES::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   l1_was_seed = 0;
   l1_prescale = 0;
   l1_mask = 0;
   pass_l1_premask = 0;
   pass_l1 = 0;
   hlt_found = 0;
   hlt_prescale = 0;
   pass_hlt = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("lumi", &lumi, &b_lumi);
   fChain->SetBranchAddress("event", &event, &b_event);
   fChain->SetBranchAddress("l1_was_seed", &l1_was_seed, &b_l1_was_seed);
   fChain->SetBranchAddress("l1_prescale", &l1_prescale, &b_l1_prescale);
   fChain->SetBranchAddress("l1_mask", &l1_mask, &b_l1_mask);
   fChain->SetBranchAddress("pass_l1_premask", &pass_l1_premask, &b_pass_l1_premask);
   fChain->SetBranchAddress("pass_l1", &pass_l1, &b_pass_l1);
   fChain->SetBranchAddress("hlt_found", &hlt_found, &b_hlt_found);
   fChain->SetBranchAddress("hlt_prescale", &hlt_prescale, &b_hlt_prescale);
   fChain->SetBranchAddress("pass_hlt", &pass_hlt, &b_pass_hlt);
}

void write_json(const char* fn, const std::set<std::pair<unsigned, unsigned> >& json) {
  FILE* f = fopen("/tmp/writejson.py", "wt");
  fprintf(f, "from FWCore.PythonUtilities.LumiList import LumiList\nlumis = []\n");
  for (const auto& run_ls : json)
    fprintf(f, "lumis.append((%u, %u))\n", run_ls.first, run_ls.second);
  fprintf(f, "ll = LumiList(lumis=lumis)\nll.writeJSON('%s')\n", fn);
  fclose(f);
  system("python /tmp/writejson.py");
}

void PRESCALES::Loop() {
  const Long64_t nentries = fChain->GetEntriesFast();

  std::map<std::pair<unsigned, unsigned>, double> lls;
  FILE* f = fopen("prescales_intlumi.txt", "rt");
  assert(f);

  char line[1024];
  double lumtot = 0;
  while (fgets(line, 1024, f) != 0) {
    unsigned run, ls;
    double lumi;
    int res = sscanf(line, "%u %u %lf", &run, &ls, &lumi);
    assert(res == 3);
    lls[std::make_pair(run, ls)] = lumi;
    lumtot += lumi;
  }
  fclose(f);
  printf("%lu %f\n", lls.size(), lumtot/1e9);
  for (int i = 0; i < 10; ++i)
    printf("***************** should've been 40520 ***************\n");
  assert(lls.size() == 40504);
  assert(fabs(lumtot - 2630245431.953) < 1);

  std::map<std::pair<unsigned, unsigned>, bool> seen;
  std::map<std::pair<unsigned, unsigned>, bool> nolumi;

  const int NL1 = 4;
  const int NHLT = 2;
  const int NCAT = 7;

  std::set<std::pair<unsigned, unsigned> > json[NL1][NCAT];
  std::map<std::pair<int, int>, double> intlumi[NCAT];
  const char* names[NCAT] = {
    "all ls",
    "ls with tot. presc. != 0",
    "ls with tot. presc. != 0, scaled",
    "ls where bit mask == 0",
    "ls where bit mask == 0, tot. presc. != 0",
    "ls where bit mask == 0, tot. presc. != 0, scaled",
    "ls where bit mask == 0, tot. presc. == 1"
  };

  const char* l1s[NL1] = {"L1_HTT100", "L1_HTT125", "L1_HTT150", "L1_HTT175"};
  const int hlt_vers[NHLT] = {1,2};

  int check_pass_l1[NL1][2][2] = {{{0}}};
  int check_l1_mask[NL1][2][2] = {{{0}}};

  int i_run_ls = 0;

  for (Long64_t jentry = 0; jentry < nentries; ++jentry) {
    if (LoadTree(jentry) < 0) break;
    fChain->GetEntry(jentry);

    if (jentry % 500000 == 0) {
      printf("%lli/%lli (# run/ls = %i)\n",jentry, nentries, i_run_ls);
      fflush(stdout);
    }

    for (int i = 0; i < NL1; ++i) {
      ++check_pass_l1[i][pass_l1_premask->at(i)][pass_l1->at(i)];
      ++check_l1_mask[i][l1_mask->at(i)][pass_l1->at(i)];
    }

    {
      const int c = std::accumulate(l1_was_seed->begin(), l1_was_seed->end(), 0);
      assert(c == 2 || c == NL1); // only two l1 bits 150,175 were seeds for HLT_v1
    }

    std::pair<unsigned, unsigned> run_ls = {run, lumi};
    if (seen.find(run_ls) != seen.end())
      continue;
    seen[run_ls] = true;

    if (lls.find(run_ls) == lls.end()) {
      nolumi[run_ls] = true;
      continue;
    }

    for (int l1 = 0; l1 < NL1; ++l1) {
      for (int hlt = 0; hlt < NHLT; ++hlt) {
        std::pair<int, int> l1_hlt = {l1, hlt};

        double il = lls[run_ls] / 1e9;
        int l1p = l1_prescale->at(l1);
        int hltp = hlt_prescale->at(hlt);
        int p = l1p * hltp;

        intlumi[0][l1_hlt] += il;
        json[l1][0].insert(run_ls);

        if (l1_mask->at(l1) == 0) {
          intlumi[3][l1_hlt] += il;
          json[l1][3].insert(run_ls);
        }

        if (p > 0) {
          intlumi[1][l1_hlt] += il;
          json[l1][1].insert(run_ls);

          intlumi[2][l1_hlt] += il / p;
          json[l1][2].insert(run_ls);

          if (l1_mask->at(l1) == 0) {
            intlumi[4][l1_hlt] += il;
            json[l1][4].insert(run_ls);

            intlumi[5][l1_hlt] += il / p;
            json[l1][5].insert(run_ls);

            if (p == 1) {
              intlumi[6][l1_hlt] += il;
              json[l1][6].insert(run_ls);
            }
          }
        }
      }
    }

    ++i_run_ls;
    //if (i_run_ls == 5000) break;
  }

  printf("check_l1_mask:\n");
  for (int l1 = 0; l1 < NL1; ++l1)
    printf("%25s: %20i %20i %20i %20i\n", l1s[l1], check_l1_mask[l1][0][0],check_l1_mask[l1][0][1],check_l1_mask[l1][1][0],check_l1_mask[l1][1][1]);
  printf("check_pass_l1:\n");
  for (int l1 = 0; l1 < NL1; ++l1)
    printf("%25s: %20i %20i %20i %20i\n", l1s[l1], check_pass_l1[l1][0][0],check_pass_l1[l1][0][1],check_pass_l1[l1][1][0],check_pass_l1[l1][1][1]);

  system("mkdir -p jsons");

  for (int w = 0; w < NCAT; ++w) {
    printf("========================================================================\nw = %i: %s\n", w, names[w]);
    for (int l1 = 0; l1 < NL1; ++l1) {
      double sum = 0;

      for (int hlt = 0; hlt < NHLT; ++hlt) {
        std::pair<int, int> l1_hlt = {l1, hlt};
        double il = intlumi[w][l1_hlt];
        sum += il;
        printf("%25s  HLT_PFHT800_v%i   %f\n", l1s[l1], hlt_vers[hlt], il);
      }

      printf("\n%25s  HLT_PFHT800 tot  %f   %lu LS in json\n--------------------------------------------------------------------\n", l1s[l1], sum, json[l1][w].size());
      char json_fn[1024];
      snprintf(json_fn, 1024, "jsons/%s--%s.json", l1s[l1], names[w]);
      write_json(json_fn, json[l1][w]);
    }
  }
}

int main() {
  PRESCALES p;
  p.Loop();
}
