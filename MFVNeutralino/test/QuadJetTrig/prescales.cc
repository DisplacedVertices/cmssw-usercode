#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <cassert>
#include <cmath>
#include <map>
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
   UInt_t          event;
   std::vector<bool>    *l1_was_seed;
   std::vector<int>     *l1_prescale;
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
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("crab/QuadJetTrigPrescales/all.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("crab/QuadJetTrigPrescales/all.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("crab/QuadJetTrigPrescales/all.root:/QuadJetTrigPrescales");
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
   fChain->SetBranchAddress("pass_l1", &pass_l1, &b_pass_l1);
   fChain->SetBranchAddress("hlt_found", &hlt_found, &b_hlt_found);
   fChain->SetBranchAddress("hlt_prescale", &hlt_prescale, &b_hlt_prescale);
   fChain->SetBranchAddress("pass_hlt", &pass_hlt, &b_pass_hlt);
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
  assert(lls.size() == 199161);
  assert(fabs(lumtot - 18204593068.9) < 1);

  std::map<std::pair<unsigned, unsigned>, bool> seen;
  std::map<std::pair<unsigned, unsigned>, bool> nolumi;

  std::map<std::pair<int, int>, double> intlumi[3];

  const char* l1s[9] = {"L1_QuadJetC32", "L1_QuadJetC36", "L1_QuadJetC40", "L1_HTT125", "L1_HTT150", "L1_HTT175", "L1_DoubleJetC52", "L1_DoubleJetC56", "L1_DoubleJetC64"};
  const int hlt_vers[4] = {1,2,3,5};

  for (Long64_t jentry = 0; jentry < nentries; ++jentry) {
    if (LoadTree(jentry) < 0) break;
    fChain->GetEntry(jentry);

    if (jentry % 500000 == 0)
      printf("%lli/%lli\n",jentry, nentries);

    {
      const int c = std::accumulate(l1_was_seed->begin(), l1_was_seed->end(), 0);
      assert(c == 3 || c == 9);
    }

    std::pair<unsigned, unsigned> run_ls = {run, lumi};
    if (seen.find(run_ls) != seen.end())
      continue;
    seen[run_ls] = true;

    if (lls.find(run_ls) == lls.end()) {
      nolumi[run_ls] = true;
      continue;
    }

    
    for (int l1 = 0; l1 < 9; ++l1) {
      for (int hlt = 0; hlt < 4; ++hlt) {
        std::pair<int, int> l1_hlt = {l1, hlt};

        double il = lls[run_ls] / 1e9;
        int l1p = l1_prescale->at(l1);
        int hltp = hlt_prescale->at(hlt);
        int p = l1p * hltp;

        intlumi[0][l1_hlt] += il;
        if (p > 0) {
          intlumi[1][l1_hlt] += il;
          intlumi[2][l1_hlt] += il / p;
        }
      }
    }
  }

  for (int w = 0; w < 3 ; ++w) {
    printf("w = %i\n", w);
    for (int l1 = 0; l1 < 9; ++l1) {
      for (int hlt = 0; hlt < 4; ++hlt) {
        std::pair<int, int> l1_hlt = {l1, hlt};
        printf("%25s  HLT_QuadJet50_v%i  %f\n", l1s[l1], hlt_vers[hlt], intlumi[w][l1_hlt]);
      }
    }
  }
}

int main() {
  PRESCALES p;
  p.Loop();
}
