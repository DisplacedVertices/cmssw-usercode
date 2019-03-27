#ifndef JMTucker_Tools_NtupleReader_h
#define JMTucker_Tools_NtupleReader_h

#include <iostream>
#include <string>
#include <boost/program_options.hpp>
#include "TFile.h"
#include "TTree.h"
#include "JMTucker/Tools/interface/LumiList.h"
#include "JMTucker/Tools/interface/PileupWeights.h"
#include "JMTucker/Tools/interface/Prob.h"
#include "JMTucker/Tools/interface/ROOTTools.h"

namespace jmt {
  template <typename Ntuple>
  class NtupleReader {
  public:
    NtupleReader()
      : desc_("Allowed options"),
        t_(nullptr),
        nt_(new Ntuple),
        puw_helper_(new jmt::PileupWeights)
    {}

    ~NtupleReader() {
      if (f_out_) {
        f_out_->Write();
        f_out_->Close();
      }
      f_->Close();
    }

    TFile& f() { return *f_.get(); }
    TTree& t() { return *t_; }
    Ntuple& nt() { return *nt_.get(); }
    TFile& f_out() { return *f_out_.get(); }

    //    jmt::PileupWeights& puw_helper() { return *puw_helper_; }
    //    jmt::LumiList& ll() { return *ll_.get(); }

    bool is_mc() const { return is_mc_; }
    bool use_weights() const { return use_weights_; }

    boost::program_options::options_description_easy_init& init_options(const std::string& tree_path) {
      namespace po = boost::program_options;
      return desc_.add_options()
        ("help,h", "this help message")
        ("input-file,i",  po::value<std::string>(&in_fn_),                                       "the input file (required)")
        ("output-file,o", po::value<std::string>(&out_fn_)        ->default_value("hists.root"), "the output file")
        ("tree-path,t",   po::value<std::string>(&tree_path_)     ->default_value(tree_path),    "the tree path")
        ("json,j",        po::value<std::string>(&json_),                                        "lumi mask json file for data")
        ("nevents-frac,n",po::value<double>     (&nevents_frac_)  ->default_value(1.),           "only run on this fraction of events in the tree")
        ("weights",       po::value<bool>       (&use_weights_)   ->default_value(true),         "whether to use any other weights, including those in the tree")
        ("pu-weights",    po::value<std::string>(&pu_weights_)    ->default_value(""),           "extra pileup weights beyond whatever's already in the tree")
        ;
    }

    bool parse_options(int argc, char** argv) {
      namespace po = boost::program_options;
      po::variables_map vm;
      po::store(po::parse_command_line(argc, argv, desc_), vm);
      po::notify(vm);

      if (vm.count("help")) {
        std::cerr << desc_ << "\n";
        return false;
      }

      if (in_fn_ == "") {
        std::cerr << "value for --input-file is required\n" << desc_ << "\n";
        return false;
      }

      if (tree_path_.find("/") == std::string::npos) {
        tree_path_ += "/t";
        std::cerr << "tree_path changed to " << tree_path_ << "\n";
      }

      std::cout << argv[0] << " with options:"
                << " in_fn: " << in_fn_
                << " out_fn: " << out_fn_
                << " tree_path: " << tree_path_
                << " json: " << (json_ != "" ? json_ : "none")
                << " nevents_frac: " << nevents_frac_
                << " weights: " << use_weights_
                << " pu_weights: " << (pu_weights_ != "" ? pu_weights_ : "none");

      return true;
    }

    bool init() {
      jmt::set_root_style();

      f_.reset(TFile::Open(in_fn_.c_str()));
      if (!f_ || !f_->IsOpen()) {
        std::cerr << "could not open " << in_fn_ << "\n";
        return false;
      }

      t_ = (TTree*)f_->Get(tree_path_.c_str());
      if (!t_) {
        std::cerr << "could not get tree " << tree_path_ << " from " << in_fn_ << "\n";
        return false;
      }

      nt_->read_from_tree(t_);

      if (out_fn_.compare(0, 3, "n/a") != 0)
        f_out_.reset(new TFile(out_fn_.c_str(), "recreate"));

      t_->GetEntry(0);

      puw_helper_->set_key(pu_weights_);

      is_mc_ = nt_->base().run() == 1;
      if (!is_mc() && json_ != "")
        ll_.reset(new jmt::LumiList(json_));

      f_out_->mkdir("mfvWeight")->cd();
      auto h_sums = (TH1D*)f_->Get("mcStat/h_sums")->Clone("h_sums");
      if (is_mc() && nevents_frac_ < 1) {
        h_sums->SetBinContent(1, h_sums->GetBinContent(1) * nevents_frac_);
        // invalidate other entries since we can't just assume equal weights in them
        for (int i = 2, ie = h_sums->GetNbinsX(); i <= ie; ++i) 
          h_sums->SetBinContent(i, -1e9);
      }
      f_out_->cd();

      auto h_norm = new TH1F("h_norm", "", 1, 0, 1);
      if (is_mc()) h_norm->Fill(0.5, h_sums->GetBinContent(1));

      h_weight = new TH1D("h_weight", ";weight;events/0.01", 100, 0, 10);
      h_npu = new TH1D("h_npu", ";# PU;events/1", 100, 0, 100);

      return true;
    }

    double weight() {
      double w = 1;
      if (use_weights_) {
        w *= nt_->base().weight();
        if (puw_helper_->valid())
          w *= puw_helper_->w(nt_->base().npu());
      }
      return w;
    }

    typedef std::pair<bool,double> fcn_ret_t;
    void loop(std::function<fcn_ret_t()> fcn) { 
      unsigned long long notskipped = 0, nnegweight = 0, jj = 0;
      const unsigned long long jje = t_->GetEntries();
      const unsigned long long jjmax = nevents_frac_ < 1 ? nevents_frac_ * jje : jje;
      for (; jj < jjmax; ++jj) {
        if (t_->LoadTree(jj) < 0) break;
        if (t_->GetEntry(jj) <= 0) continue;
        if (jj % 25000 == 0) {
          if (jjmax != jje) printf("\r%llu/%llu(/%llu)", jj, jjmax, jje);
          else              printf("\r%llu/%llu",        jj, jjmax);
          fflush(stdout);
        }

        if (!is_mc() && ll_ && !ll_->contains(nt_->base()))
          continue;

        ++notskipped;

        fcn_ret_t r = fcn();
        double w = r.second;
        if (!r.first)
          break;

        if (w < 0)
          ++nnegweight;

        h_weight->Fill(w);
        h_npu->Fill(nt_->base().npu(), w);
      }

      if (jjmax != jje) printf("\rdone with %llu events (out of %llu)\n", jjmax, jje);
      else              printf("\rdone with %llu events\n",               jjmax);
      printf("%llu/%llu events with negative weights\n", nnegweight, notskipped);
    }

  private:
    boost::program_options::options_description desc_;

    std::string in_fn_;
    std::string out_fn_;
    std::string tree_path_;
    std::string json_;
    double nevents_frac_;
    bool use_weights_;
    std::string pu_weights_;

    template <typename T> using uptr = std::unique_ptr<T>;

    uptr<TFile> f_;
    TTree* t_; // this, other bare pointers owned by root
    uptr<Ntuple> nt_;
    uptr<TFile> f_out_;

    uptr<jmt::PileupWeights> puw_helper_;
    uptr<jmt::LumiList> ll_;

    bool is_mc_;

    TH1D* h_weight;
    TH1D* h_npu;
  };
}

#endif
