#include <cassert>
#include <iostream>
#include <boost/program_options.hpp>
#include "TH2.h"
#include "TFile.h"
#include "TTree.h"
#include "TVector2.h"
#include "TVector3.h"
#include "JMTucker/Tools/interface/LumiList.h"
#include "JMTucker/Tools/interface/PileupWeights.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "utils.h"

int main(int argc, char** argv) {
  std::string in_fn;
  std::string out_fn("hists.root");
  std::string json;
  float nevents_frac;
  bool apply_weights = true;
  std::string pu_weights;

  {
    namespace po = boost::program_options;
    po::options_description desc("Allowed options");
    desc.add_options()
      ("help,h", "this help message")
      ("input-file,i",  po::value<std::string>(&in_fn),                                             "the input file (required)")
      ("output-file,o", po::value<std::string>(&out_fn)        ->default_value("hists.root"),       "the output file")
      ("json,j",        po::value<std::string>(&json),                                              "lumi mask json file for data")
      ("nevents-frac,n",po::value<float>      (&nevents_frac)  ->default_value(1.f),                "only run on this fraction of events in the tree")
      ("weights",       po::value<bool>       (&apply_weights) ->default_value(true),               "whether to use any other weights, including those in the tree")
      ("pu-weights",    po::value<std::string>(&pu_weights)    ->default_value(""),                 "extra pileup weights beyond whatever's already in the tree")
      ;

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    if (vm.count("help")) {
      std::cout << desc << "\n";
      return 1;
    }

    if (in_fn == "") {
      std::cout << "value for --input-file is required\n" << desc << "\n";
      return 1;
    }
  }

  std::cout << argv[0] << " with options:"
            << " in_fn: " << in_fn
            << " out_fn: " << out_fn
            << " json: " << (json != "" ? json : "none")
            << " nevents_frac: " << nevents_frac
            << " weights: " << apply_weights
            << " pu_weights: " << pu_weights
            << "\n";

  ////

  jmt::PileupWeights puwhelper(pu_weights);

  root_setup();

  file_and_tree fat(in_fn.c_str(), out_fn.c_str());
  TTree* t = fat.t;
  mfv::K0Ntuple& nt = fat.nt;
  t->GetEntry(0);

  const bool is_mc = nt.base().run() == 1;
  std::unique_ptr<jmt::LumiList> good_ll;
  if (!is_mc && json != "") good_ll.reset(new jmt::LumiList(json));

  fat.f_out->mkdir("mfvWeight")->cd();
  TH1D* h_sums = (TH1D*)fat.f->Get("mcStat/h_sums")->Clone("h_sums");
  if (is_mc && nevents_frac < 1) {
    h_sums->SetBinContent(1, h_sums->GetBinContent(1) * nevents_frac);
    for (int i = 2, ie = h_sums->GetNbinsX(); i <= ie; ++i) // invalidate other entries since we can't just assume equal weights in them
      h_sums->SetBinContent(i, -1e9);
  }
  fat.f_out->cd();

  TH1F* h_norm = new TH1F("h_norm", "", 1, 0, 1);
  if (is_mc)
    h_norm->Fill(0.5, h_sums->GetBinContent(1));

  TH1D* h_weight = new TH1D("h_weight", ";weight;events/0.01", 200, 0, 2);
  TH1D* h_npu = new TH1D("h_npu", ";# PU;events/1", 100, 0, 100);

  long notskipped = 0, nnegweight = 0;

  const double mpi = 0.13957;
  TH1D* h_premass = new TH1D("h_premass", ";SV mass before refit (GeV);vertices/5 MeV", 400, 0, 2);
  TH1D* h_mass = new TH1D("h_mass", ";SV mass (GeV);vertices/5 MeV", 400, 0, 2);
  TH1D* h_costh = new TH1D("h_costh", ";costh;vertices/0.001", 2002, -1.001, 1.001);

  unsigned long long jj = 0;
  const unsigned long long jje = fat.t->GetEntries();
  const unsigned long long jjmax = nevents_frac < 1 ? nevents_frac * jje : jje;
  for (; jj < jjmax; ++jj) {
    if (fat.t->LoadTree(jj) < 0) break;
    if (fat.t->GetEntry(jj) <= 0) continue;
    if (jj % 25000 == 0) {
      if (jjmax != jje) printf("\r%llu/%llu(/%llu)", jj, jjmax, jje);
      else              printf("\r%llu/%llu",        jj, jjmax);
      fflush(stdout);
    }

    if (!is_mc && good_ll.get() && !good_ll->contains(nt.base()))
      continue;

    ++notskipped;

    double w = 1;

    if (is_mc && apply_weights) {
      if (nt.base().weight() < 0) ++nnegweight;
      w *= nt.base().weight();

      if (puwhelper.valid())
        w *= puwhelper.w(nt.base().npu());
    }

    h_weight->Fill(w);
    h_npu->Fill(nt.base().npu(), w);

    const TVector3 pv = nt.pvs().pos(0);

    for (int isv = 0, isve = nt.svs().n(); isv < isve; ++isv) {
      const TVector3 pos = nt.svs().pos(isv);
      const TVector3 flight = pos - pv;

      const int itk = nt.svs().misc(isv) & 0xFFFF;
      const int jtk = nt.svs().misc(isv) >> 16;
      const int irftk = 2*isv;
      const int jrftk = 2*isv+1;

      const TLorentzVector ip4 = nt.tracks().p4(itk, mpi);
      const TLorentzVector jp4 = nt.tracks().p4(jtk, mpi);
      const TLorentzVector irfp4 = nt.refit_tks().p4(irftk, mpi);
      const TLorentzVector jrfp4 = nt.refit_tks().p4(jrftk, mpi);

      const TLorentzVector prep4 = ip4 + jp4;
      const TLorentzVector p4 = irfp4 + jrfp4;
      const TVector3 momdir = p4.Vect().Unit();

      const double costh = momdir.Dot(flight.Unit());
      const double mass = p4.M();

      if (flight.Mag() > 1) {
        h_premass->Fill(prep4.M());
        h_mass->Fill(mass);
        h_costh->Fill(costh);
      }

    }
  }

  if (jjmax != jje) printf("\rdone with %llu events (out of %llu)\n", jjmax, jje);
  else              printf("\rdone with %llu events\n",               jjmax);
  printf("%li/%li events with negative weights\n", nnegweight, notskipped);
}
