#ifndef JMTucker_Tools_NtupleReader_h
#define JMTucker_Tools_NtupleReader_h

#include <iostream>
#include <string>
#include <boost/program_options.hpp>
#include "TFile.h"
#include "TH2.h"
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
        puw_helper_(new jmt::PileupWeights),
        h_weight_(nullptr),
        h_npu_(nullptr)
    {}

    ~NtupleReader() {
      if (f_out_) {
        f_out_->Write();
        f_out_->Close();
      }
      if (f_)
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

    boost::program_options::options_description_easy_init init_options(const std::string& tree_path) {
      namespace po = boost::program_options;
      return desc_.add_options()
        ("help,h", "this help message")
        ("input-file,i",  po::value<std::string>(&in_fn_),                                       "the input file (required)")
        ("output-file,o", po::value<std::string>(&out_fn_)        ->default_value("hists.root"), "the output file")
        ("tree-path,t",   po::value<std::string>(&tree_path_)     ->default_value(tree_path),    "the tree path")
        ("json,j",        po::value<std::string>(&json_),                                        "lumi mask json file for data")
        ("num-chunks,n",  po::value<int>        (&num_chunks_)    ->default_value(1),            "split the tree entries into this many chunks")
        ("which-chunk,w", po::value<int>        (&which_chunk_)   ->default_value(0),            "chunk to run")
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

      if (num_chunks_ <= 0 || which_chunk_ < 0 || which_chunk_ >= num_chunks_) {
        std::cerr << "required: num_chunks >= 1 and 0 <= which_chunk < num_chunks\n";
        return false;
      }

      std::cout << argv[0] << " with options:"
                << " in_fn: " << in_fn_
                << " out_fn: " << out_fn_
                << " tree_path: " << tree_path_
                << " json: " << (json_ != "" ? json_ : "none")
                << " num_chunks: " << num_chunks_
                << " which_chunk: " << which_chunk_
                << " weights: " << use_weights_
                << " pu_weights: " << (pu_weights_ != "" ? pu_weights_ : "none")
                << "\n";

      return true;
    }

    bool init(bool for_copy=false) {
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

      nentries_ = t_->GetEntries();
      entry_t per = num_chunks_ > 1 ? nentries_ / double(num_chunks_) : nentries_;
      entry_start_ = which_chunk_ * per;
      entry_end_ = which_chunk_ == num_chunks_ - 1 ? nentries_ : (which_chunk_+1)*per;
      entries_run_ = entry_end_ - entry_start_;
      assert(entry_start_ < entry_end_);

      nt_->read_from_tree(t_);

      if (out_fn_.compare(0, 3, "n/a") != 0)
        f_out_.reset(new TFile(out_fn_.c_str(), "recreate"));

      t_->GetEntry(0);

      puw_helper_->set_key(pu_weights_);

      is_mc_ = nt_->base().run() == 1;
      if (!is_mc() && json_ != "")
        ll_.reset(new jmt::LumiList(json_));

      f_out_->mkdir(for_copy ? "mcStat" : "mfvWeight")->cd();
      auto h_sums = (TH1D*)f_->Get("mcStat/h_sums")->Clone("h_sums");
      if (is_mc() && num_chunks_ > 1) {
        h_sums->SetBinContent(1, h_sums->GetBinContent(1) * entries_run_ / nentries_);
        // invalidate other entries since we can't just assume equal weights in them
        for (int i = 2, ie = h_sums->GetNbinsX(); i <= ie; ++i) 
          h_sums->SetBinContent(i, -1e9);
      }
      f_out_->cd();

      if (!for_copy) {
        auto h_norm = new TH1F("h_norm", "", 1, 0, 1);
        if (is_mc()) h_norm->Fill(0.5, h_sums->GetBinContent(1));

        h_weight_ = new TH1D("h_weight", ";weight;events/0.01", 100, 0, 10);
        h_npu_ = new TH1D("h_npu", ";# PU;events/1", 100, 0, 100);
      }

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
      entry_t notskipped = 0, nnegweight = 0;
      entry_t print_per = entries_run_ / 20;
      if (print_per == 0) print_per = 1;
      printf("tree has %llu entries; running on %llu-%llu\n", nentries_, entry_start_, entry_end_-1);
      for (entry_t jj = entry_start_; jj < entry_end_; ++jj) {
        if (t_->LoadTree(jj) < 0) break;
        if (t_->GetEntry(jj) <= 0) continue;
        if (jj % print_per == 0) { printf("\r%llu", jj); fflush(stdout); }

        if (!is_mc() && ll_ && !ll_->contains(nt_->base()))
          continue;

        ++notskipped;

        fcn_ret_t r = fcn();
        double w = r.second;
        if (!r.first)
          break;

        if (w < 0)
          ++nnegweight;

        if (h_weight_) h_weight_->Fill(w);
        if (h_npu_) h_npu_->Fill(nt_->base().npu(), w);
      }

      printf("\r%llu events done, %llu not skipped, %llu with negative weights\n", entries_run_, notskipped, nnegweight);
    }

  private:
    boost::program_options::options_description desc_;

    std::string in_fn_;
    std::string out_fn_;
    std::string tree_path_;
    std::string json_;
    int num_chunks_;
    int which_chunk_;
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

    typedef unsigned long long entry_t;
    entry_t nentries_;
    entry_t entry_start_;
    entry_t entry_end_;
    entry_t entries_run_;

    TH1D* h_weight_;
    TH1D* h_npu_;
  };

  template <typename Ntuple> int copy(int argc, char** argv, const char* path) {
    jmt::NtupleReader<Ntuple> nr;
    char tpath[256];
    snprintf(tpath, 256, "%s/t", path);
    nr.init_options(path);
    if (!nr.parse_options(argc, argv) || !nr.init(true)) return 1;

    nr.f_out().mkdir(path)->cd();
    TTree* t_out = new TTree("t", "");
    nr.nt().write_to_tree(t_out);

    auto fcn = [&]() {
      nr.nt().copy_vectors();
      t_out->Fill();
      return std::make_pair(true, nr.weight());
    };

    nr.loop(fcn);
    return 1;
  }
}

#endif
