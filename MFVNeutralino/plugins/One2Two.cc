#include "TF1.h"
#include "TFitResult.h"
#include "TH2F.h"
#include "TRandom3.h"
#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

namespace {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  double svdist2d(const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return mag(v0.x - v1.x, v0.y - v1.y);
  }

  double dphi(const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return reco::deltaPhi(atan2(v0.y, v0.x),
			  atan2(v1.y, v1.x));
  }

  double dz(const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return v0.z - v1.z;
  }

  bool accept(TRandom* rand, const double f, const double g, const double M) {
    const double u = rand->Rndm();
    return u < f/(M*g);
  }
}

class MFVOne2Two : public edm::EDAnalyzer {
public:
  explicit MFVOne2Two(const edm::ParameterSet&);
  ~MFVOne2Two();

  MFVVertexAux xform_vertex(const MFVVertexAux&) const;
  bool sel_vertex(const MFVVertexAux&) const;

  typedef std::vector<std::pair<MFVVertexAux, MFVVertexAux> > MFVVertexPairCollection;

  void read_file(const std::string& filename, MFVVertexAuxCollection&, MFVVertexPairCollection&) const;

  void analyze(const edm::Event&, const edm::EventSetup&) {}
  void endJob();

  const int min_ntracks;
  const double svdist2d_cut;

  const std::string tree_path;
  const std::vector<std::string> filenames;
  const size_t nfiles;
  const std::vector<int> n1vs;
  const std::vector<double> weights;
  const bool just_print;

  const int seed;
  const bool toy_mode;
  const bool poisson_n1vs;
  const bool wrep;
  const int npairs;

  const bool find_g_dz;
  const std::string form_g_dz;
  const bool find_f_dphi;
  const std::string form_f_dphi;
  const bool find_f_dz;
  const std::string form_f_dz;

  const bool use_f_dz;
  const double max_1v_dz;
  const int max_1v_ntracks;

  TF1* f_dphi;
  TF1* f_dz;
  TF1* g_dz;
  TH1F* h_1v_dphi_env;
  TH1F* h_1v_absdphi_env;
  TH1F* h_1v_dz_env;
  TH1F* h_fcn_dphi;
  TH1F* h_fcn_abs_dphi;
  TH1F* h_fcn_dz;
  TH1F* h_fcn_g_dz;

  TRandom3* rand;

  enum { t_2v, t_2vsideband, t_1v, n_t };
  static const char* t_names[n_t];

  TH2F* h_xy[n_t];
  TH1F* h_bs2ddist[n_t];
  TH2F* h_bs2ddist_v_bsdz[n_t];
  TH1F* h_bsdz[n_t];
  TH1F* h_bs2ddist_0[n_t];
  TH2F* h_bs2ddist_v_bsdz_0[n_t];
  TH1F* h_bsdz_0[n_t];
  TH1F* h_bs2ddist_1[n_t];
  TH2F* h_bs2ddist_v_bsdz_1[n_t];
  TH1F* h_bsdz_1[n_t];
  TH2F* h_ntracks[n_t];
  TH1F* h_ntracks01[n_t];
  TH1F* h_svdist2d[n_t];
  TH1F* h_svdz[n_t];
  TH1F* h_svdz_all[n_t];
  TH1F* h_dphi[n_t];
  TH1F* h_abs_dphi[n_t];
  TH2F* h_svdz_v_dphi[n_t];

  TH1F* h_1v_svdist2d_fit_2v;
  TH1F* h_1v_svdist2d_fit_2v_ksdist;
  TH1F* h_1v_svdist2d_fit_2v_ksprob;

  TH2F* h_pred_v_real;
  TH1F* h_pred_m_real;
};

const char* MFVOne2Two::t_names[MFVOne2Two::n_t] = { "2v", "2vsideband", "1v" };

MFVOne2Two::MFVOne2Two(const edm::ParameterSet& cfg)
  : min_ntracks(cfg.getParameter<int>("min_ntracks")),
    svdist2d_cut(cfg.getParameter<double>("svdist2d_cut")),

    tree_path(cfg.getParameter<std::string>("tree_path")),
    filenames(cfg.getParameter<std::vector<std::string> >("filenames")),
    nfiles(filenames.size()),
    n1vs(cfg.getParameter<std::vector<int> >("n1vs")),
    weights(cfg.getParameter<std::vector<double> >("weights")),
    just_print(cfg.getParameter<bool>("just_print")),

    seed(cfg.getParameter<int>("seed")),
    toy_mode(cfg.getParameter<bool>("toy_mode")),
    poisson_n1vs(cfg.getParameter<bool>("poisson_n1vs")),
    wrep(cfg.getParameter<bool>("wrep")),
    npairs(cfg.getParameter<int>("npairs")),

    find_g_dz(cfg.getParameter<bool>("find_g_dz")),
    form_g_dz(cfg.getParameter<std::string>("form_g_dz")),

    find_f_dphi(cfg.getParameter<bool>("find_f_dphi")),
    form_f_dphi(cfg.getParameter<std::string>("form_f_dphi")),

    find_f_dz(cfg.getParameter<bool>("find_f_dz")),
    form_f_dz(cfg.getParameter<std::string>("form_f_dz")),

    use_f_dz(cfg.getParameter<bool>("use_f_dz")),
    max_1v_dz(cfg.getParameter<double>("max_1v_dz")),
    max_1v_ntracks(cfg.getParameter<int>("max_1v_ntracks")),

    //    signal_files(cfg.getParameter<std::vector<std::string> >("signal_files")),
    //    signal_weights(cfg.getParameter<std::vector<double> >("signal_weights")),

    f_dphi(0),
    f_dz(0),
    g_dz(0),
    rand(0)
{
  if (n1vs.size() != weights.size() || (toy_mode && nfiles != n1vs.size()))
    throw cms::Exception("VectorMismatch") << "inconsistent sample info";

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  f_dphi = new TF1("f_dphi", form_f_dphi.c_str(), 0, M_PI);
  f_dz = new TF1("f_dz", form_f_dz.c_str(), -40, 40);
  g_dz = new TF1("g_dz", form_g_dz.c_str(), -40, 40);
  
  h_1v_dphi_env = fs->make<TH1F>("h_1v_dphi_env", "", 8, -M_PI, M_PI);
  h_1v_absdphi_env = fs->make<TH1F>("h_1v_absdphi_env", "", 8, 0, M_PI);
  h_1v_dz_env = fs->make<TH1F>("h_1v_dz_env", "", 200, -40, 40);
  h_fcn_dphi = fs->make<TH1F>("h_fcn_dphi", "", 8, -M_PI, M_PI);
  h_fcn_abs_dphi = fs->make<TH1F>("h_fcn_abs_dphi", "", 8, 0, M_PI);
  h_fcn_dz = fs->make<TH1F>("h_fcn_dz", "", 20, -0.1, 0.1);
  h_fcn_g_dz = fs->make<TH1F>("h_fcn_g_dz", "", 200, -40, 40);

  for (int i = 0; i < n_t; ++i) {
    const char* iv = t_names[i];

    h_xy                [i] = fs->make<TH2F>(TString::Format("h_%s_xy"                , iv), "", 100, -0.05, 0.05, 100, 0.05, 0.05);
    h_bs2ddist          [i] = fs->make<TH1F>(TString::Format("h_%s_bs2ddist"          , iv), "", 100, 0, 0.1);
    h_bs2ddist_v_bsdz   [i] = fs->make<TH2F>(TString::Format("h_%s_bs2ddist_v_bsdz"   , iv), "", 200, -20, 20, 100, 0, 0.1);
    h_bsdz              [i] = fs->make<TH1F>(TString::Format("h_%s_bsdz"              , iv), "", 200, -20, 20);
    h_bs2ddist_0        [i] = fs->make<TH1F>(TString::Format("h_%s_bs2ddist_0"        , iv), "", 100, 0, 0.1);
    h_bs2ddist_v_bsdz_0 [i] = fs->make<TH2F>(TString::Format("h_%s_bs2ddist_v_bsdz_0" , iv), "", 200, -20, 20, 100, 0, 0.1);
    h_bsdz_0            [i] = fs->make<TH1F>(TString::Format("h_%s_bsdz_0"            , iv), "", 200, -20, 20);
    h_bs2ddist_1        [i] = fs->make<TH1F>(TString::Format("h_%s_bs2ddist_1"        , iv), "", 100, 0, 0.1);
    h_bs2ddist_v_bsdz_1 [i] = fs->make<TH2F>(TString::Format("h_%s_bs2ddist_v_bsdz_1" , iv), "", 200, -20, 20, 100, 0, 0.1);
    h_bsdz_1            [i] = fs->make<TH1F>(TString::Format("h_%s_bsdz_1"            , iv), "", 200, -20, 20);

    h_ntracks           [i] = fs->make<TH2F>(TString::Format("h_%s_ntracks"           , iv), "", 20, 0, 20, 20, 0, 20);
    h_ntracks01         [i] = fs->make<TH1F>(TString::Format("h_%s_ntracks01"         , iv), "", 30, 0, 30);
    h_svdist2d          [i] = fs->make<TH1F>(TString::Format("h_%s_svdist2d"          , iv), "", 100, 0, 0.1);
    h_svdz              [i] = fs->make<TH1F>(TString::Format("h_%s_svdz"              , iv), "", 20, -0.1, 0.1);
    h_svdz_all          [i] = fs->make<TH1F>(TString::Format("h_%s_svdz_all"          , iv), "", 400, -20, 20);
    h_dphi              [i] = fs->make<TH1F>(TString::Format("h_%s_dphi"              , iv), "", 8, -M_PI, M_PI);
    h_abs_dphi          [i] = fs->make<TH1F>(TString::Format("h_%s_abs_dphi"          , iv), "", 8, 0, M_PI);
    h_svdz_v_dphi       [i] = fs->make<TH2F>(TString::Format("h_%s_svdz_v_dphi"       , iv), "", 8, -M_PI, M_PI, 50, -0.1, 0.1);
  }

  h_1v_svdist2d_fit_2v = fs->make<TH1F>("h_1v_svdist2d_fit_2v", "", 100, 0, 0.1);
  h_1v_svdist2d_fit_2v_ksdist = fs->make<TH1F>("h_1v_svdist2d_fit_2v_ksdist", "", 30, 0, 30);
  h_1v_svdist2d_fit_2v_ksprob = fs->make<TH1F>("h_1v_svdist2d_fit_2v_ksprob", "", 30, 0, 30);

  h_pred_v_real = fs->make<TH2F>("h_pred_v_real", "", 100, 0, 20, 100, 0, 20);
  h_pred_m_real = fs->make<TH1F>("h_pred_m_real", "", 100, -20, 20);
}

MFVOne2Two::~MFVOne2Two() {
  delete f_dphi;
  delete f_dz;
  delete g_dz;
  delete rand;
}

MFVVertexAux MFVOne2Two::xform_vertex(const MFVVertexAux& v) const {
  return v;
}

bool MFVOne2Two::sel_vertex(const MFVVertexAux& v) const {
  return v.ntracks() >= min_ntracks;
}

void MFVOne2Two::read_file(const std::string& filename, MFVVertexAuxCollection& one_vertices, MFVVertexPairCollection& two_vertices) const {
  TFile* f = new TFile(filename.c_str());
  if (!f)
    throw cms::Exception("One2Two") << "could not read file " << filename;

  TTree* tree = (TTree*)f->Get(tree_path.c_str());
  if (!tree)
    throw cms::Exception("One2Two") << "could not get " << tree_path << " from file " << filename;

  mfv::MiniNtuple nt;
  mfv::read_from_tree(tree, nt);

  for (int j = 0, je = tree->GetEntries(); j < je; ++j) {
    if (tree->LoadTree(j) < 0) break;
    if (tree->GetEntry(j) <= 0) continue;

    if (nt.nvtx == 1) {
      MFVVertexAux v0;
      v0.x = nt.x0; v0.y = nt.y0; v0.z = nt.z0; v0.bs2ddist = mag(nt.x0, nt.y0);
      for (int i = 0; i < nt.ntk0; ++i)
	v0.insert_track();
      if (sel_vertex(v0))
	one_vertices.push_back(v0);
    }
    else if (nt.nvtx == 2) {
      MFVVertexAux v0, v1;
      v0.x = nt.x0; v0.y = nt.y0; v0.z = nt.z0; v0.bs2ddist = mag(nt.x0, nt.y0);
      v1.x = nt.x1; v1.y = nt.y1; v1.z = nt.z1; v1.bs2ddist = mag(nt.x1, nt.y1);
      for (int i = 0; i < nt.ntk0; ++i) v0.insert_track();
      for (int i = 0; i < nt.ntk1; ++i) v1.insert_track();
      bool sel0 = sel_vertex(v0);
      bool sel1 = sel_vertex(v1);
      if (sel0 && sel1)
	two_vertices.push_back(std::make_pair(v0, v1));
      else if (sel0)
	one_vertices.push_back(v0);
      else if (sel1)
	one_vertices.push_back(v1);
    }
  }

  f->Close();
  delete f;

  printf("# 1v: %i  # 2v: %i\n", int(one_vertices.size()), int(two_vertices.size())); fflush(stdout);
}

void MFVOne2Two::endJob() {
  edm::Service<TFileService> fs;
  rand = new TRandom3(121982 + seed);

  // Read all signal samples to print signal contamination in sideband
  // and signal strength in signal region. 
  //  for (int i = 0, ie = int(signal_samples.size()); i < ie; ++i) {
    
  //  }

  // Read all vertices from the input files. Two modes: unweighted,
  // single sample, or combine multiple samples, reading a random
  // subset of events.

  MFVVertexAuxCollection one_vertices;
  std::vector<MFVVertexPairCollection> two_vertices(nfiles);

  if (!toy_mode) {
    // In regular mode, take all events from the file (with weight 1).
    printf("\n\n==================================================================\n\nsingle sample mode, filename: %s  ntracks >= %i  svdist2d sideband <= %f\n", filenames[0].c_str(), min_ntracks, svdist2d_cut);
    read_file(filenames[0], one_vertices, two_vertices[0]);
  }
  else {
    // Config file specifies how many to take (or the Poisson-mean
    // number) from each sample. Directly keep the 2vs; they will be
    // histogrammed with config-specified weights below.
    printf("\n\n==================================================================\n\nmultiple sample mode, #filenames: %i  ntracks >= %i  svdist2d sideband <= %f\n", int(filenames.size()), min_ntracks, svdist2d_cut);
    for (size_t ifile = 0; ifile < nfiles; ++ifile) {
      printf("file: %s\n", filenames[ifile].c_str());
      MFVVertexAuxCollection v1v;
      read_file(filenames[ifile], v1v, two_vertices[ifile]);

      const int n1v = poisson_n1vs ? rand->Poisson(n1vs[ifile]) : n1vs[ifile];
      const int N1v = int(v1v.size());
      if (n1v > N1v)
        throw cms::Exception("NotEnough") << "not enough v1vs (" << N1v << " to sample " << n1v << " of them";
      
      printf("sampling %i/%i events from %s\n", n1v, N1v, filenames[ifile].c_str()); fflush(stdout);

      // Knuth sample-without-replacement.
      int t = 0, m = 0;
      while (m < n1v) {
        if ((N1v - t) * rand->Rndm() >= n1v - m)
          ++t;
        else {
          ++m;
          one_vertices.push_back(v1v[t++]);
        }
      }
    }
  }

  if (just_print)
    return;

  const int N1v = int(one_vertices.size());

  // Find the envelope functions for dphi (just check that it is flat)
  // and dz.

  for (int iv = 0; iv < N1v; ++iv) {
    const MFVVertexAux& v0 = one_vertices[iv];
    for (int jv = iv+1; jv < N1v; ++jv) {
      const MFVVertexAux& v1 = one_vertices[jv];
      h_1v_dphi_env->Fill(dphi(v0, v1));
      h_1v_absdphi_env->Fill(fabs(dphi(v0, v1)));
      h_1v_dz_env->Fill(dz(v0, v1));
    }
  }

  h_1v_absdphi_env->Scale(1./h_1v_absdphi_env->Integral());
  h_1v_dz_env     ->Scale(1./h_1v_dz_env     ->Integral());

  if (1) { // no find_g_dphi, just assuming it's flat and checking that assumption here.
    TFitResultPtr res = h_1v_absdphi_env->Fit("pol0", "QS");
    printf("g_dphi fit to pol0 chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n", res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
  }

  if (find_g_dz) { 
    TFitResultPtr res = h_1v_dz_env->Fit(g_dz, "LRQS");
    printf("g_dz fit to gaus sigma %6.3f +- %6.3f   chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n", res->Parameter(0), res->ParError(0), res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
    g_dz->FixParameter(0, res->Parameter(0));
  }

  h_fcn_g_dz->FillRandom("g_dz", 100000);


  // Fill all the 2v histograms. In toy_mode we add together many
  // samples with appropriate weights. Also fit f_dphi and f_dz from
  // the 2v events in the sideband.
  for (size_t ifile = 0; ifile < nfiles; ++ifile) {
    const double w = toy_mode ? weights[ifile] : 1;

    for (const auto& pair : two_vertices[ifile]) {
      const MFVVertexAux& v0 = pair.first;
      const MFVVertexAux& v1 = pair.second;
      const bool sideband = svdist2d(v0, v1) < svdist2d_cut;

      for (int ih = 0; ih < 2; ++ih) {
        if (ih == t_2vsideband && !sideband)
          continue;

        h_xy[ih]->Fill(v0.x, v0.y, w);
        h_xy[ih]->Fill(v1.x, v1.y, w);
        h_bs2ddist[ih]->Fill(v0.bs2ddist, w);
        h_bs2ddist[ih]->Fill(v1.bs2ddist, w);
        h_bs2ddist_0[ih]->Fill(v0.bs2ddist, w);
        h_bs2ddist_1[ih]->Fill(v1.bs2ddist, w);
        h_bs2ddist_v_bsdz[ih]->Fill(v0.z, v0.bs2ddist, w);
        h_bs2ddist_v_bsdz[ih]->Fill(v1.z, v1.bs2ddist, w);
        h_bs2ddist_v_bsdz_0[ih]->Fill(v0.z, v0.bs2ddist, w);
        h_bs2ddist_v_bsdz_1[ih]->Fill(v1.z, v1.bs2ddist, w);
        h_bsdz[ih]->Fill(v0.z, w);
        h_bsdz[ih]->Fill(v1.z, w);
        h_bsdz_0[ih]->Fill(v0.z, w);
        h_bsdz_1[ih]->Fill(v1.z, w);

        h_ntracks[ih]->Fill(v0.ntracks(), v1.ntracks(), w);
        h_ntracks01[ih]->Fill(v0.ntracks() + v1.ntracks(), w);
        h_svdist2d[ih]->Fill(svdist2d(v0, v1), w);
        h_svdz[ih]->Fill(dz(v0, v1), w);
        h_dphi[ih]->Fill(dphi(v0, v1), w);
        h_abs_dphi[ih]->Fill(fabs(dphi(v0, v1)), w);
        h_svdz_v_dphi[ih]->Fill(dphi(v0, v1), dz(v0, v1), w);
      }
    }
  }

  {
    TString opt = "LIRQS";
    if (toy_mode)
      opt = "W" + opt;

    if (find_f_dphi) {
      TF1* f_dphi_temp = new TF1("f_dphi_temp", TString::Format("%f*(%s)", h_abs_dphi[t_2vsideband]->Integral()*h_abs_dphi[t_2vsideband]->GetXaxis()->GetBinWidth(1), form_f_dphi.c_str()), 0, M_PI);
      TFitResultPtr res = h_abs_dphi[t_2vsideband]->Fit(f_dphi_temp, opt);
      printf("f_dphi fit exp = %6.3f +- %6.3f   chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n", res->Parameter(0), res->ParError(0), res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
      f_dphi->FixParameter(0, res->Parameter(0));
      delete f_dphi_temp;
    }

    if (find_f_dz) {
      TF1* f_dz_temp = new TF1("f_dz_temp", TString::Format("%f*(%s)", h_svdz[t_2vsideband]->Integral()*h_svdz[t_2vsideband]->GetXaxis()->GetBinWidth(1), form_f_dz.c_str()), -40, 40);
      TFitResultPtr res = h_svdz[t_2vsideband]->Fit(f_dz_temp, opt);
      printf("f_dz fit gaus sigma = %6.3f +- %6.3f   chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n", res->Parameter(0), res->ParError(0), res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
      f_dz->FixParameter(0, res->Parameter(0));
      delete f_dz_temp;
    }
  }

  h_fcn_dphi->FillRandom("f_dphi", 100000);
  h_fcn_abs_dphi->FillRandom("f_dphi", 100000);
  h_fcn_dz->FillRandom("f_dz", 100000);


  // Now try to sample npairs from the one_vertices
  // sample. With/without replacement is controlled by the config
  // flag.

  std::vector<int> used(N1v, 0);
  const int giveup = 10*N1v; // After choosing one vertex, may be so far out in e.g. dz tail that you can't find another one. Give up after trying this many times.
  const int npairsuse = npairs > 0 ? npairs : N1v/2;

  const double gdpmax = 1./2/M_PI;
  const double fdpmax = f_dphi->GetMaximum();
  const double Mdp = fdpmax/gdpmax;

  const double gdzmax = g_dz->GetMaximum();
  const double fdzmax = f_dz->GetMaximum();
  const double Mdz = fdzmax/gdzmax;

  for (int ipair = 0; ipair < npairsuse; ++ipair) {
    int iv = -1;
    while (iv == -1) {
      int x = rand->Integer(N1v);
      if (wrep || !used[x]) {
	iv = x;
	break;
      }
    }

    const MFVVertexAux& v0 = one_vertices[iv];
    int tries = 0;

    int jv = -1;
    while (jv == -1) {
      int x = rand->Integer(N1v);
      if (x != iv && (wrep || !used[x])) {
	const MFVVertexAux& vx = one_vertices[x];

        const double dp = dphi(v0, vx);
        const double dz = v0.z - vx.z;

        const bool ok =
          v0.ntracks() + vx.ntracks() < max_1v_ntracks &&
          accept(rand, f_dphi->Eval(dp), gdpmax, Mdp) &&
          (use_f_dz ? accept(rand, f_dz->Eval(dz), g_dz->Eval(dz), Mdz) : fabs(dz) < max_1v_dz);

        if (ok) {
	  jv = x;
          //if (tries >= 50000) printf("\r%200s\r", "");
	  break;
	}

        if (++tries % 50000 == 0)
          ; //printf("\ripair %10i try %10i with v0 = %2i (%12f, %12f, %12f) and v1 = %2i (%12f, %12f, %12f)", ipair, tries, v0.ntracks(), v0.x, v0.y, v0.z, vx.ntracks(), vx.x, vx.y, vx.z); fflush(stdout);

	if (tries == giveup)
	  break;
      }
    }

    if (jv == -1) {
      assert(tries == giveup);
      used[iv] = -1;
      --ipair;
      continue;
    }

    ++used[iv];
    ++used[jv];

    const MFVVertexAux& v1 = one_vertices[jv];

    // We've got the pair -- fill histos.

    h_xy[t_1v]->Fill(v0.x, v0.y);
    h_xy[t_1v]->Fill(v1.x, v1.y);
    h_bs2ddist[t_1v]->Fill(v0.bs2ddist);
    h_bs2ddist[t_1v]->Fill(v1.bs2ddist);
    h_bs2ddist_0[t_1v]->Fill(v0.bs2ddist);
    h_bs2ddist_1[t_1v]->Fill(v1.bs2ddist);
    h_bs2ddist_v_bsdz[t_1v]->Fill(v0.z, v0.bs2ddist);
    h_bs2ddist_v_bsdz[t_1v]->Fill(v1.z, v1.bs2ddist);
    h_bs2ddist_v_bsdz_0[t_1v]->Fill(v0.z, v0.bs2ddist);
    h_bs2ddist_v_bsdz_1[t_1v]->Fill(v1.z, v1.bs2ddist);
    h_bsdz[t_1v]->Fill(v0.z);
    h_bsdz[t_1v]->Fill(v1.z);
    h_bsdz_0[t_1v]->Fill(v0.z);
    h_bsdz_1[t_1v]->Fill(v1.z);
    const int ntk0 = v0.ntracks(); // The 2v pairs are ordered with ntk0 > ntk1,
    const int ntk1 = v1.ntracks(); //  so fill here the same way.
    if (ntk1 > ntk0)
      h_ntracks[t_1v]->Fill(ntk1, ntk0);
    else
      h_ntracks[t_1v]->Fill(ntk0, ntk1);
    h_ntracks01[t_1v]->Fill(ntk0 + ntk1);
    h_svdist2d[t_1v]->Fill(svdist2d(v0, v1));
    h_svdz[t_1v]->Fill(dz(v0, v1));
    h_dphi[t_1v]->Fill(dphi(v0, v1));
    h_abs_dphi[t_1v]->Fill(fabs(dphi(v0, v1)));
    h_svdz_v_dphi[t_1v]->Fill(dphi(v0, v1), dz(v0, v1));
  }


  // Output 1v usage counts (versus z).
  {
    TTree* t_use = fs->make<TTree>("t_use", "");
    unsigned char c;
    unsigned short s;
    float z;
    bool use_short = false;
    for (int i = 0; i < N1v; ++i) {
      if (used[i] >= 65536)
        throw cms::Exception("problemo");
      else if (used[i] >= 256) {
        use_short = true;
        break;
      }
    }
    t_use->Branch("z", &z, "z/F");
    if (use_short)
      t_use->Branch("nuse", &s, "nuse/s");
    else
      t_use->Branch("nuse", &c, "nuse/c");
    for (int i = 0; i < N1v; ++i) {
      z = one_vertices[i].z;
      if (use_short)
        s = used[i];
      else
        c = used[i];
      t_use->Fill();
    }
  }


  // Fit the 1v distribution to the 2v one by shifting it over and
  // scaling in the sideband.
  const int nbins = h_svdist2d[t_1v]->GetNbinsX();
  int best_shift = 0;
  double best_ksdist = 1e99;
  std::vector<TH1F*> h1vs;
  for (int shift = 0; shift < 30; ++shift) {
    TH1F* h1v = (TH1F*)h_svdist2d[t_1v]->Clone("h1v");
    h1vs.push_back(h1v);
    h1v->Scale(1./h1v->Integral());

    for (int ibin = 1; ibin <= nbins; ++ibin) {
      const int ifrom = ibin - shift;
      h1v->SetBinContent(ibin, ifrom >= 0 ? h_svdist2d[t_1v]->GetBinContent(ifrom) : 0.);
      h1v->SetBinError(ibin, 0);
    }

    const double ksdist = h1v->KolmogorovTest(h_svdist2d[t_2vsideband], "M");
    const double ksprob = h1v->KolmogorovTest(h_svdist2d[t_2vsideband]);
    if (ksdist < best_ksdist) {
      best_shift = shift;
      best_ksdist = ksdist;
    }

    h_1v_svdist2d_fit_2v_ksdist->SetBinContent(shift+1, ksdist);
    h_1v_svdist2d_fit_2v_ksprob->SetBinContent(shift+1, ksprob);
  }

  if (best_shift == 29)
    printf("WARNING SHIFT AT LIMIT\n");

  TH1F* h1v = h1vs[best_shift];
  for (int ibin = 1; ibin <= nbins; ++ibin) {
    h_1v_svdist2d_fit_2v->SetBinContent(ibin, h1v->GetBinContent(ibin));
    h_1v_svdist2d_fit_2v->SetBinError(ibin, 0);
  }

  for (TH1F* h : h1vs)
    delete h;

  const int last_sideband_bin = h_1v_svdist2d_fit_2v->FindBin(svdist2d_cut)-1;
  h_1v_svdist2d_fit_2v->Scale(h_svdist2d[t_2vsideband]->Integral()/h_1v_svdist2d_fit_2v->Integral(1, last_sideband_bin));
  
  const double pred_bkg = h_1v_svdist2d_fit_2v->Integral(last_sideband_bin+1, nbins);
  const double real_bkg = h_svdist2d[t_2v]->Integral(last_sideband_bin+1, nbins);
  printf("h_1v_svdist2d_fit_2v integral in sideband: %f\n", h_1v_svdist2d_fit_2v->Integral(1, last_sideband_bin));
  printf("h_1v_svdist2d_fit_2v integral in signal  : %f\n", pred_bkg);
  printf("h_2v_svdist2d integral in sideband: %f\n", h_svdist2d[t_2v]->Integral(1, last_sideband_bin));
  printf("h_2v_svdist2d integral in signal  : %f\n", real_bkg);

  h_pred_v_real->Fill(real_bkg, pred_bkg);
  h_pred_m_real->Fill(pred_bkg - real_bkg);
}

DEFINE_FWK_MODULE(MFVOne2Two);
