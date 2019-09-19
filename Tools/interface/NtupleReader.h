#ifndef JMTucker_Tools_NtupleReader_h
#define JMTucker_Tools_NtupleReader_h

#include <cmath>
#include <cstdlib>
#include <experimental/filesystem>
#include <iostream>
#include <string>
#include <boost/program_options.hpp>
#include "TFile.h"
#include "TH2.h"
#include "TStopwatch.h"
#include "TTree.h"
#define JMT_STANDALONE
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/LumiList.h"
#include "JMTucker/Tools/interface/PileupWeights.h"
#include "JMTucker/Tools/interface/Prob.h"
#include "JMTucker/Tools/interface/ROOTTools.h"
#include "JMTucker/Tools/interface/Year.h"

#define NR_loop_continue return std::make_pair(true, nr.weight())
#define NR_loop_break return std::make_pair(false, nr.weight())
#define NR_loop_only(r,l,e) if (nr.nt().base().run() != (r) || nr.nt().base().lumi() != (l) || nr.nt().base().event() != (e)) NR_loop_continue

namespace jmt {
  template <typename Ntuple>
  class NtupleReader {
  public:
    NtupleReader()
      : desc_("Allowed options"),
        t_(nullptr),
        nt_(new Ntuple),
        puw_helper_(new jmt::PileupWeights),
        norm_(-1),
        year_(-1),
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
    double norm() const { return norm_; }
    int year() const { return year_; }
    bool use_weights() const { return use_weights_; }

    boost::program_options::options_description_easy_init init_options(const std::string& tree_path,
                                                                       const std::string& batch_name="", const std::string& batch_dataset="", const std::string& batch_samples="") {
      namespace po = boost::program_options;
      return desc_.add_options()
        ("help,h", "this help message")
        ("input-file,i",   po::value<std::string>(&in_fn_),                                       "the input file (required)")
        ("output-file,o",  po::value<std::string>(&out_fn_)        ->default_value("hists.root"), "the output file")
        ("same-name,f",    po::bool_switch       (&same_fn_)       ->default_value(false),        "override output filename with basename of input filename")
        ("tree-path,t",    po::value<std::string>(&tree_path_)     ->default_value(tree_path),    "the tree path")
        ("json,j",         po::value<std::string>(&json_),                                        "lumi mask json file for data")
        ("every,e",        po::bool_switch       (&every_)         ->default_value(false),        "print a message every event")
        ("quiet,q",        po::bool_switch       (&quiet_)         ->default_value(false),        "whether to be quiet (suppresses progress and timing prints)")
        ("silent,l",       po::bool_switch       (&silent_)        ->default_value(false),        "whether to be silent (absolutely no prints from us)")
        ("num-chunks,n",   po::value<int>        (&num_chunks_)    ->default_value(1),            "split the tree entries into this many chunks")
        ("which-chunk,w",  po::value<int>        (&which_chunk_)   ->default_value(0),            "chunk to run")
        ("weights",        po::bool_switch       (&use_weights_)   ->default_value(true),         "whether to use any other weights, including those in the tree")
        ("pu-weights",     po::value<std::string>(&pu_weights_)    ->default_value(""),           "extra pileup weights beyond whatever's already in the tree")

        ("submit,s",       po::bool_switch       (&submit_)        ->default_value(false),         "submit batch via CondorSubmitter")
        ("submit-batch",   po::value<std::string>(&submit_batch_)  ->default_value(batch_name),    "batch name")
        ("submit-dataset", po::value<std::string>(&submit_dataset_)->default_value(batch_dataset), "batch dataset")
        ("submit-samples", po::value<std::string>(&submit_samples_)->default_value(batch_samples), "batch code for pick_samples")
        ;
    }

    bool parse_options(int argc, char** argv) {
      namespace po = boost::program_options;
      po::variables_map vm;
      po::store(po::parse_command_line(argc, argv, desc_), vm);
      po::notify(vm);

      if (silent_)
        quiet_ = true;
      if (quiet_)
        every_ = false;

      if (vm.count("help")) {
        std::cerr << desc_ << "\n";
        return false;
      }

      if (submit_) {
        if (submit_batch_ == "" || submit_dataset_ == "") {
          std::cerr << "value for --submit-batch and --submit-dataset required, defaults not set\n";
          return false;
        }

        submit_exe_ = argv[0];
      }
      else {
        if (in_fn_ == "") {
          std::cerr << "in interactive mode, value for --input-file is required\n" << desc_ << "\n";
          return false;
        }

        if (same_fn_) {
          if (out_fn_ != "hists.root")
            std::cerr << "warning, overriding --output-file value since --same-name is set\n";
          namespace fs = std::experimental::filesystem;
          // JMTBAD gcc6 version doesn't have append
          auto dn = fs::path(out_fn_).parent_path().string();
          auto bn = fs::path(in_fn_).filename().string();
          if (dn != "")
            out_fn_ = dn + "/" + bn;
          else
            out_fn_ = bn;
        }

        if (tree_path_.find("/") == std::string::npos) {
          tree_path_ += "/t";
          std::cerr << "tree_path changed to " << tree_path_ << "\n";
        }

        if (num_chunks_ <= 0 || which_chunk_ < 0 || which_chunk_ >= num_chunks_) {
          std::cerr << "required: num_chunks >= 1 and 0 <= which_chunk < num_chunks\n";
          return false;
        }

        if (!silent_)
          std::cout << argv[0] << " with options:"
                    << " in_fn: " << in_fn_
                    << " out_fn: " << out_fn_
                    << " tree_path: " << tree_path_
                    << " json: " << (json_ != "" ? json_ : "none")
                    << " every/quiet/silent: " << every_ << "/" << quiet_ << "/" << silent_
                    << " num_chunks: " << num_chunks_
                    << " which_chunk: " << which_chunk_
                    << " weights: " << use_weights_
                    << " pu_weights: " << (pu_weights_ != "" ? pu_weights_ : "none")
                    << "\n";
      }

      return true;
    }

    bool init(bool for_copy=false) {
      if (submit_) {
        std::ostringstream o;
        o << "from JMTucker.Tools.MetaSubmitter import *\n"
          << "dataset = '" << submit_dataset_ << "'\n"
          << "samples = pick_samples(dataset, " << submit_samples_ << ")\n"
          << "NtupleReader_submit('" << submit_batch_ << "', dataset, samples, exe_fn='" << submit_exe_ << "', output_fn='" << out_fn_ << "')\n";

        std::cout << o.str();

        char tmpnam[] = "/tmp/tmpnrsubmitXXXXXX";
        mkstemp(tmpnam);
        std::ofstream of(tmpnam);
        of << o.str();
        of.close();

        std::string cmd("python ");
        cmd += tmpnam;
        system(cmd.c_str());

        remove(tmpnam);

        return false;
      }

      if (!quiet_) time_.Start();

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
      const entry_t per = num_chunks_ > 1 ? nentries_ / double(num_chunks_) : nentries_;
      entry_start_ = which_chunk_ * per;
      entry_end_ = which_chunk_ == num_chunks_ - 1 ? nentries_ : (which_chunk_+1)*per;
      entries_run_ = entry_end_ - entry_start_;
      const double chunk_factor = double(entries_run_) / nentries_;
      const bool chunking_mc = is_mc() && num_chunks_ > 1;
      assert(entry_start_ < entry_end_);

      nt_->read_from_tree(t_);

      if (out_fn_.compare(0, 3, "n/a") != 0)
        f_out_.reset(new TFile(out_fn_.c_str(), "recreate"));

      t_->GetEntry(0);

      puw_helper_->set_key(pu_weights_);

      is_mc_ = nt_->base().run() == 1;
      jmt::AnalysisEras::set_current(nt_->base().run(), nt_->base().lumi(), nt_->base().event());
      if (!is_mc() && json_ != "")
        ll_.reset(new jmt::LumiList(json_));

      f_out_->mkdir(for_copy ? "mcStat" : "mfvWeight")->cd();
      auto h_sums = (TH1D*)f_->Get("mcStat/h_sums")->Clone("h_sums");
      f_out_->cd();

      if (!for_copy) {
        auto h_norm = new TH1F("h_norm", "", 1, 0, 1);
        auto xax = h_sums->GetXaxis();
        for (int ibin = 1; ibin <= h_sums->GetNbinsX(); ++ibin) {
          double c = h_sums->GetBinContent(ibin);
          const std::string l = xax->GetBinLabel(ibin);
          if (is_mc() && l == "sum_nevents_total") {
            if (chunking_mc) {
              c *= chunk_factor;
              h_sums->SetBinContent(ibin, c);
            }
            h_norm->Fill(0.5, norm_ = c);
          }
          else if (l == "yearcode_x_nfiles")
            year_ = jmt::yearcode(c).year(); // sets the Year global
          else if (chunking_mc)
            h_sums->SetBinContent(ibin, -1e9); // invalidate other entries since we can't just assume equal weights in them
        }

        assert(year_ > 0);
      }

      if (!for_copy) {
        h_weight_ = new TH1D("h_weight", ";weight;events/0.01", 100, 0, 10);
        h_npu_ = new TH1D("h_npu", ";# PU;events/1", 100, 0, 100);
      }

      if (!quiet_) {
        std::cout << "init time: ";
        time_.Print();
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

    void fill(TH1* h, double x) {
      h->Fill(x, weight());
    }

    void fill(TH2* h, double x, double y) {
      h->Fill(x, y, weight());
    }

    void print_event(bool newline=true) {
      printf("NtupleReader loop: r: %u l: %u e: %llu", nt_->base().run(), nt_->base().lumi(), nt_->base().event());
      if (newline) printf("\n");
    }

    typedef std::pair<bool,double> fcn_ret_t;
    void loop(std::function<fcn_ret_t()> fcn) { 
      if (!quiet_) time_.Start();
      entry_t notskipped = 0, nnegweight = 0;
      entry_t print_per = entries_run_ / 20;
      if (print_per == 0) print_per = 1;
      if (!quiet_) printf("tree has %llu entries; running on %llu-%llu\n", nentries_, entry_start_, entry_end_-1);
      for (entry_t jj = entry_start_; jj < entry_end_; ++jj) {
        if (t_->LoadTree(jj) < 0) break;
        if (t_->GetEntry(jj) <= 0) continue;
        if (every_) print_event();
        else if (!quiet_ && jj % print_per == 0) { printf("\r%llu", jj); fflush(stdout); }

        if (!is_mc() && ll_ && !ll_->contains(nt_->base()))
          continue;

        jmt::AnalysisEras::set_current(nt_->base().run(), nt_->base().lumi(), nt_->base().event());

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

      if (!silent_) printf("\rfinished %s, %llu events done, %llu not skipped, %llu with negative weights\n", in_fn_.c_str(), entries_run_, notskipped, nnegweight);
      if (!quiet_) {
        printf("cpu time per not-skipped event: %.3g, loop time:", time_.CpuTime() / notskipped);
        time_.Print();
      }
    }

  private:
    boost::program_options::options_description desc_;

    std::string in_fn_;
    std::string out_fn_;
    bool same_fn_;
    std::string tree_path_;
    std::string json_;
    bool every_;
    bool quiet_;
    bool silent_;
    int num_chunks_;
    int which_chunk_;
    bool use_weights_;
    std::string pu_weights_;

    bool submit_;
    std::string submit_exe_;
    std::string submit_batch_;
    std::string submit_dataset_;
    std::string submit_samples_;

    template <typename T> using uptr = std::unique_ptr<T>;

    uptr<TFile> f_;
    TTree* t_; // this, other bare pointers owned by root
    uptr<Ntuple> nt_;
    uptr<TFile> f_out_;

    uptr<jmt::PileupWeights> puw_helper_;
    uptr<jmt::LumiList> ll_;

    bool is_mc_;
    double norm_;
    int year_;

    typedef unsigned long long entry_t;
    entry_t nentries_;
    entry_t entry_start_;
    entry_t entry_end_;
    entry_t entries_run_;

    TH1D* h_weight_;
    TH1D* h_npu_;

    TStopwatch time_;
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
