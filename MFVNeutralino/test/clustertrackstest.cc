// ZZZ_SZ=0.4; make clustertrackstest.exe && ./clustertrackstest.exe $fxrd/store/user/tucker/mfv_neu_tau01000um_M0800/crab_MinitreeV9_wtk_mfv_mfv_neu_tau01000um_M0800/161209_191028/0000/minitree_1.root mfv1mm.root $ZZZ_SZ && ./clustertrackstest.exe $crd/MinitreeV9_ntk5/qcdht2000ext.root qcdht2000ext.root $ZZZ_SZ && comparehists.py qcdht2000ext.root mfv1mm.root / $asdf/plots/clustertracks --nice qcdht2000ext mfv1mm --scaling '-{"qcdht2000ext": 25400*36/4016332., "mfv1mm": 36/10000.}[curr]'

#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "fastjet/ClusterSequence.hh"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

fastjet::PseudoJet track_to_particle(double x, double y, double z, double mass=0.14) {
  return fastjet::PseudoJet(x,y,z, x*x + y*y + z*z + mass*mass);
}

double jet_R = 0.7;
fastjet::JetAlgorithm jet_algo = fastjet::antikt_algorithm;
fastjet::RecombinationScheme jet_recomb_scheme = fastjet::E_scheme;

TH1F* h_nclusters = 0;
TH1F* h_nconstituents = 0;
TH1F* h_nsingleclusters = 0;
TH1F* h_fsingleclusters = 0;
TH1F* h_avg_nconstituents = 0;
TH1F* h_avg_nconstituents_per_tk = 0;
TH1F* h_nsingleclusters_per_tk = 0;
TH1F* h_ndoubleclusters = 0;
TH1F* h_ndoubleclusters_per_tk = 0;
TH1F* h_ndoubleclusters_per_way = 0;

bool analyze(int j, int je, const mfv::MiniNtuple& nt) {
  const bool prints = false;

  if (prints) std::cout << "Entry " << j << "\n";

  //if (nt.nvtx == 1) {
  //if (sqrt(nt.x0*nt.x0 + nt.y0*nt.y0) > 0.02) {
  //if (sqrt(nt.x0*nt.x0 + nt.y0*nt.y0) > 0.05) {
  {

    std::vector<fastjet::PseudoJet> particles;
    for (size_t k = 0; k < nt.ntk0; ++k)  {
      fastjet::PseudoJet p = track_to_particle((*nt.p_tk0_px)[k], (*nt.p_tk0_py)[k], (*nt.p_tk0_pz)[k]);
      p.set_user_index(k);
      particles.push_back(p);
    }

    fastjet::ClusterSequence cs(particles, fastjet::JetDefinition(jet_algo, jet_R, jet_recomb_scheme));
    std::vector<fastjet::PseudoJet> jets = fastjet::sorted_by_pt(cs.inclusive_jets());

    const size_t njets = jets.size();
    h_nclusters->Fill(njets);

    double avg_nconstituents = 0;
    int nsingleclusters = 0;
    int ndoubleclusters = 0;

    for (size_t i = 0; i < njets; i++) {
      const size_t nconstituents = jets[i].constituents().size();
      h_nconstituents->Fill(nconstituents);
      avg_nconstituents += nconstituents;

      if (nconstituents == 1)
        ++nsingleclusters;
      else if (nconstituents <= 2)
        ++ndoubleclusters;
    }

    h_nsingleclusters->Fill(nsingleclusters);
    h_fsingleclusters->Fill(nsingleclusters / double(njets));
    h_nsingleclusters_per_tk->Fill(nsingleclusters / double(nt.ntk0));

    h_ndoubleclusters->Fill(ndoubleclusters);
    h_ndoubleclusters_per_tk->Fill(ndoubleclusters / double(nt.ntk0));
    h_ndoubleclusters_per_way->Fill(ndoubleclusters / (nt.ntk0 * (nt.ntk0 - 1) / 2.));

    avg_nconstituents /= njets;
    h_avg_nconstituents->Fill(avg_nconstituents);
    h_avg_nconstituents_per_tk->Fill(avg_nconstituents / nt.ntk0);

    if (prints) {
      for (size_t i = 0; i < jets.size(); i++) {
        const fastjet::PseudoJet& jet = jets[i];
        std::cout << "jet " << i << ": "<< jet.pt() << " " << jet.rap() << " " << jet.phi() << "\n";
        for (size_t j = 0; j < jet.constituents().size(); j++) {
          const fastjet::PseudoJet& c = jet.constituents()[j];
          std::cout << "    constituent " << j << " (user " << c.user_index() << ") 's pt: " << c.pt() << "\n";
        }
      }

      std::cout << std::endl;
    }
  }

  return true;
}

double frac_above(TH1* h, double x) {
  const int n = h->GetNbinsX()+1;
  return h->Integral(h->FindBin(x),n) / h->Integral(0,n); 
}

int main(int argc, char** argv) {
  assert(argc > 3);

  const char* fn = argv[1];
  const char* out_fn = argv[2];
  jet_R = atof(argv[3]);

  TFile out_f(out_fn, "recreate");

  h_nclusters                = new TH1F("h_nclusters",                ";# clusters;events",                                           50, 0, 10);
  h_nconstituents            = new TH1F("h_nconstituents",            ";# constituents;clusters",                                     50, 0, 10);
  h_nsingleclusters          = new TH1F("h_nsingleclusters",          ";# clusters w. 1 constituent",                                 50, 0, 10);
  h_fsingleclusters          = new TH1F("h_fsingleclusters",          ";frac. clusters w. 1 constituent",                             51, 0,  1.02);
  h_avg_nconstituents        = new TH1F("h_avg_nconstituents",        ";avg # constituents / cluster;events",                         50, 0, 10);
  h_avg_nconstituents_per_tk = new TH1F("h_avg_nconstituents_per_tk", ";avg # constituents / cluster / # tracks in vertex;events",    51, 0, 1.02);
  h_nsingleclusters_per_tk   = new TH1F("h_nsingleclusters_per_tk",   ";# clusters w. 1 constituent / # tracks in vertex",            51, 0, 1.02);
  h_ndoubleclusters          = new TH1F("h_ndoubleclusters",          ";# clusters w. <= 2 constituents",                             50, 0, 10);
  h_ndoubleclusters_per_tk   = new TH1F("h_ndoubleclusters_per_tk",   ";# clusters w. <= 2 constituents / # tracks in vertex",        51, 0, 1.02);
  h_ndoubleclusters_per_way  = new TH1F("h_ndoubleclusters_per_way",  ";# clusters w. <= 2 constituents / (# tracks choose 2)",       51, 0, 1.02);

  mfv::loop(fn, "mfvMiniTree/t", analyze);

  const double denom = h_nclusters->Integral(0,h_nclusters->GetNbinsX()+1);
  std::cout << out_fn << "\n";
  std::cout << "frac nclusters >= 2: " << frac_above(h_nclusters, 2) << "\n";
  std::cout << "frac nclusters >= 3: " << frac_above(h_nclusters, 3) << "\n";
  std::cout << "frac fsingle < 0.5: " << 1-frac_above(h_fsingleclusters, 0.5) << "\n";
  std::cout << "frac avgnconst >= 2: " << frac_above(h_avg_nconstituents, 2) << "\n";
  std::cout << "frac avgnconst >= 3: " << frac_above(h_avg_nconstituents, 3) << "\n";
  std::cout << "frac avgnconst / ntk < 0.3: " << 1-frac_above(h_avg_nconstituents_per_tk, 0.3) << "\n";
  std::cout << "frac avgnconst / ntk < 0.4: " << 1-frac_above(h_avg_nconstituents_per_tk, 0.4) << "\n";
  std::cout << "frac nsingle / ntk < 0.16: " << 1-frac_above(h_nsingleclusters_per_tk, 0.16) << "\n";
  std::cout << "frac nsingle / ntk < 0.2: " << 1-frac_above(h_nsingleclusters_per_tk, 0.2) << "\n";
  std::cout << "frac ndouble / ntk < 0.2: " << 1-frac_above(h_ndoubleclusters_per_tk, 0.2) << "\n";
  std::cout << "frac ndouble / ntk < 0.25: " << 1-frac_above(h_ndoubleclusters_per_tk, 0.25) << "\n";
  std::cout << "frac ndouble / way < 0.1: " << 1-frac_above(h_ndoubleclusters_per_way, 0.1) << "\n";
  std::cout << "frac ndouble / way < 0.15: " << 1-frac_above(h_ndoubleclusters_per_way, 0.15) << "\n";
  out_f.Write();
  out_f.Close();
}
