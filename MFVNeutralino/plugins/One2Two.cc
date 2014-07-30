#include "Math/QuantFuncMathCore.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TH2D.h"
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

  double accept_prob(const double f, const double g, const double M) {
    return f/(M*g);
  }

  bool accept(TRandom* rand, const double f, const double g, const double M) {
    return rand->Rndm() < accept_prob(f, g, M);
  }

  double clopper_pearson(const double n_on, const double n_tot, double& lower, double& upper) {
    const double alpha=1-0.6827;
    const bool equal_tailed=true;
    const double alpha_min = equal_tailed ? alpha/2 : alpha;
    lower = 0;
    upper = 1;

    if (n_on > 0)
      lower = ROOT::Math::beta_quantile(alpha_min, n_on, n_tot - n_on + 1);
    if (n_tot - n_on > 0)
      upper = ROOT::Math::beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on);

    if (n_on == 0 and n_tot == 0)
      return 0;
    else
      return n_on/n_tot;
  }

  double clopper_pearson_poisson_means(const double x, const double y, double& lower, double& upper) {
    double rl, rh;
    clopper_pearson(x, x+y, rl, rh);

    lower = rl/(1-rl);

    if (y == 0 or fabs(rh - 1) < 1e-9) {
      upper = 0;
      return 0;
    }

    upper = rh/(1-rh);
    return x/y;
  }

  double fcn_g_dphi(const double* x, const double* par) {
    return (par[0] + par[1]*fabs(x[0] - M_PI/2.))/(par[0]*M_PI + par[1]*2.46740110);
  }

  double fcn_f_dphi(const double* x, const double* par) {
    return pow(fabs(x[0]), par[0])/(pow(M_PI, (par[0]+1))/(par[0]+1));
  }

  double fcn_fg_dz(const double* x, const double* par) {
    return exp(-x[0]*x[0]/2./par[0]/par[0])/sqrt(2.*M_PI*par[0]*par[0]);
  }
}

class MFVOne2Two : public edm::EDAnalyzer {
public:
  explicit MFVOne2Two(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&) {}
  void endJob() { run(); }
  ~MFVOne2Two();

  MFVVertexAux xform_vertex(const MFVVertexAux&) const;
  void set_sig(MFVVertexAux&) const;
  bool is_sig(const MFVVertexAux&) const;
  bool sel_vertex(const MFVVertexAux&) const;
  bool is_sideband(const MFVVertexAux&, const MFVVertexAux&) const;

  typedef std::vector<std::pair<MFVVertexAux, MFVVertexAux> > MFVVertexPairCollection;

  void read_file(const std::string& filename, const bool sig, MFVVertexAuxCollection&, MFVVertexPairCollection&) const;
  void fill_2d(const int ih, const double weight, const MFVVertexAux&, const MFVVertexAux&) const;
  void fill_1d(              const double weight, const MFVVertexAux&, const MFVVertexAux&) const;

  double prob_1v_pair(const MFVVertexAux&, const MFVVertexAux&) const;
  bool accept_1v_pair(const MFVVertexAux&, const MFVVertexAux&) const;

  void print_config() const;
  void read_signals();
  void read_vertices();
  void fill_2d_histos();
  void fit_envelopes();
  void fit_fs_with_sideband();
  void update_f_weighting_pars();
  void set_phi_exp(double);
  void choose_2v_from_1v(const bool output_usage=false);
  void fill_1d_histos();
  TH1D* shift_hist(const TH1D* h, const int shift, TH1D** hshifted) const;
  void by_means();
  void make_1v_templates();
  void load_1v_templates(const std::string& fn, const std::string& dir);
  TH1D* make_2v_toy();

  void run();

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
  const bool toy_only;
  const bool poisson_n1vs;
  const int sampling_type; // 0 = sample random pairs with replacement, 1 = sample all unique pairs and accept/reject, 2 = sample all unique pairs and fill 1v dists with weight according to accept/reject prob
  const int sample_only;
  const int npairs;

  const int max_1v_ntracks01;

  const std::vector<std::string> signal_files;
  const size_t nsignals;
  const std::vector<double> signal_weights;
  const int signal_contamination;

  const bool find_g_dphi;
  const bool use_form_g_dphi;
  const std::string form_g_dphi;

  const bool find_g_dz;
  const bool use_form_g_dz;
  const std::string form_g_dz;

  const bool find_f_dphi;
  const bool find_f_dphi_bkgonly;
  const bool use_form_f_dphi;
  const std::string form_f_dphi;

  const bool find_f_dz;
  const bool find_f_dz_bkgonly;
  const bool use_form_f_dz;
  const std::string form_f_dz;

  const bool do_by_means;

  const bool make_templates;
  const std::vector<double> template_range;
  const std::vector<double> template_binning;
  const std::string template_fn;
  const std::string template_dir;

  TF1* f_dphi;
  TF1* f_dz;
  TF1* g_dphi;
  TF1* g_dz;
  double gdpmax;
  double fdpmax;
  double Mdp;
  double gdzmax;
  double fdzmax;
  double Mdz;
  TH1D* h_1v_dphi_env;
  TH1D* h_1v_absdphi_env;
  TH1D* h_1v_dz_env;
  TH1D* h_fcn_dphi;
  TH1D* h_fcn_abs_dphi;
  TH1D* h_fcn_g_dphi;
  TH1D* h_fcn_dz;
  TH1D* h_fcn_g_dz;
  TH1D* h_dphi_env_mean;
  TH1D* h_dphi_env_mean_err;
  TH1D* h_dphi_env_rms;
  TH1D* h_dphi_env_rms_err;
  TH1D* h_dphi_env_fit_offset;
  TH1D* h_dphi_env_fit_offset_err;
  TH1D* h_dphi_env_fit_offset_pull;
  TH1D* h_dphi_env_fit_slope;
  TH1D* h_dphi_env_fit_slope_err;
  TH1D* h_dphi_env_fit_slope_pull;
  TH1D* h_dphi_env_fit_chi2;
  TH1D* h_dphi_env_fit_chi2prob;
  TH1D* h_dz_env_mean;
  TH1D* h_dz_env_mean_err;
  TH1D* h_dz_env_rms;
  TH1D* h_dz_env_rms_err;
  TH1D* h_dz_env_fit_sig;
  TH1D* h_dz_env_fit_sig_err;
  TH1D* h_dz_env_fit_sig_pull;
  TH1D* h_dz_env_fit_chi2;
  TH1D* h_dz_env_fit_chi2prob;
  TH1D* h_dphi_mean;
  TH1D* h_dphi_mean_err;
  TH1D* h_dphi_rms;
  TH1D* h_dphi_rms_err;
  TH1D* h_dphi_asym;
  TH1D* h_dphi_asym_err;
  TH1D* h_dphi_fit_exp;
  TH1D* h_dphi_fit_exp_err;
  TH1D* h_dphi_fit_exp_pull;
  TH1D* h_dphi_fit_chi2;
  TH1D* h_dphi_fit_chi2prob;
  TH1D* h_dz_mean;
  TH1D* h_dz_mean_err;
  TH1D* h_dz_rms;
  TH1D* h_dz_rms_err;
  TH1D* h_dz_fit_sig;
  TH1D* h_dz_fit_sig_err;
  TH1D* h_dz_fit_sig_pull;
  TH1D* h_dz_fit_chi2;
  TH1D* h_dz_fit_chi2prob;

  std::vector<MFVVertexAuxCollection> signal_one_vertices;
  std::vector<MFVVertexPairCollection> signal_two_vertices;
  MFVVertexAuxCollection one_vertices;
  std::vector<MFVVertexPairCollection> two_vertices;

  struct WeightedMFVVertexPair {
    typedef unsigned short index_t;
    static const index_t bad_index = 65535;

    WeightedMFVVertexPair()                                  : w(1.), i(bad_index), j(bad_index) {}
    WeightedMFVVertexPair(           index_t i_, index_t j_) : w(1.), i(i_), j(j_) {}
    WeightedMFVVertexPair(double w_, index_t i_, index_t j_) : w(w_), i(i_), j(j_) {}
    bool ok() const { return i != bad_index && j != bad_index; }
    double w;
    index_t i;
    index_t j;
  };

  const MFVVertexAux& v0(const WeightedMFVVertexPair& pair) const { assert(pair.ok()); return one_vertices[pair.i]; }
  const MFVVertexAux& v1(const WeightedMFVVertexPair& pair) const { assert(pair.ok()); return one_vertices[pair.j]; }

  typedef std::vector<WeightedMFVVertexPair> WeightedMFVVertexPairs;
  WeightedMFVVertexPairs two_vertices_from_1v;

  std::map<int, std::pair<double, TH1D*> > h_1v_templates;
  double curr_phi_exp;

  int n_2v_toys;

  enum { t_2v, t_2vbkg, t_2vsig, t_2vsb, t_2vsbbkg, t_2vsbsig,  n_t_2v, t_1v = n_t_2v, t_1vsb, n_t };
  static const char* t_names[n_t];

  TH2D* h_xy[n_t];
  TH1D* h_bs2ddist[n_t];
  TH2D* h_bs2ddist_v_bsdz[n_t];
  TH1D* h_bsdz[n_t];
  TH1D* h_bs2ddist_0[n_t];
  TH2D* h_bs2ddist_v_bsdz_0[n_t];
  TH1D* h_bsdz_0[n_t];
  TH1D* h_bs2ddist_1[n_t];
  TH2D* h_bs2ddist_v_bsdz_1[n_t];
  TH1D* h_bsdz_1[n_t];
  TH2D* h_ntracks[n_t];
  TH1D* h_ntracks01[n_t];
  TH1D* h_svdist2d[n_t];
  TH1D* h_svdist2d_all[n_t];
  TH1D* h_svdz[n_t];
  TH1D* h_svdz_all[n_t];
  TH1D* h_dphi[n_t];
  TH1D* h_abs_dphi[n_t];
  TH2D* h_svdz_v_dphi[n_t];

  TH1D* h_1v_svdist2d_fit_2v;

  TH1D* h_meandiff;
  TH1D* h_shift;
  TH1D* h_ksdist;
  TH1D* h_ksprob;
  TH1D* h_ksdistX;
  TH1D* h_ksprobX;

  TH2D* h_pred_v_true;
  TH1D* h_pred_m_true;

  TRandom3* rand;
  edm::Service<TFileService> fs;

  std::vector<TH1D*> h_toy_nevents_from;
  TH1D* h_toy_nevents;
  TH1D* h_toy_nevents_signal;
};

const char* MFVOne2Two::t_names[MFVOne2Two::n_t] = { "2v", "2vbkg", "2vsig", "2vsb", "2vsbbkg", "2vsbsig", "1v", "1vsb" };

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
    toy_only(cfg.getParameter<bool>("toy_only")),
    poisson_n1vs(cfg.getParameter<bool>("poisson_n1vs")),
    sampling_type(cfg.getParameter<int>("sampling_type")),
    sample_only(cfg.getParameter<int>("sample_only")),
    npairs(cfg.getParameter<int>("npairs")),

    max_1v_ntracks01(cfg.getParameter<int>("max_1v_ntracks01")),

    signal_files(cfg.getParameter<std::vector<std::string> >("signal_files")),
    nsignals(signal_files.size()),
    signal_weights(cfg.getParameter<std::vector<double> >("signal_weights")),
    signal_contamination(cfg.getParameter<int>("signal_contamination")),

    find_g_dphi(cfg.getParameter<bool>("find_g_dphi")),
    use_form_g_dphi(cfg.getParameter<bool>("use_form_g_dphi")),
    form_g_dphi(cfg.getParameter<std::string>("form_g_dphi")),

    find_g_dz(cfg.getParameter<bool>("find_g_dz")),
    use_form_g_dz(cfg.getParameter<bool>("use_form_g_dz")),
    form_g_dz(cfg.getParameter<std::string>("form_g_dz")),

    find_f_dphi(cfg.getParameter<bool>("find_f_dphi")),
    find_f_dphi_bkgonly(cfg.getParameter<bool>("find_f_dphi_bkgonly")),
    use_form_f_dphi(cfg.getParameter<bool>("use_form_f_dphi")),
    form_f_dphi(cfg.getParameter<std::string>("form_f_dphi")),

    find_f_dz(cfg.getParameter<bool>("find_f_dz")),
    find_f_dz_bkgonly(cfg.getParameter<bool>("find_f_dz_bkgonly")),
    use_form_f_dz(cfg.getParameter<bool>("use_form_f_dz")),
    form_f_dz(cfg.getParameter<std::string>("form_f_dz")),

    do_by_means(cfg.getParameter<bool>("do_by_means")),

    make_templates(cfg.getParameter<bool>("make_templates")),
    template_range(cfg.getParameter<std::vector<double> >("template_range")),
    template_binning(cfg.getParameter<std::vector<double> >("template_binning")),
    template_fn(cfg.getParameter<std::string>("template_fn")),
    template_dir(cfg.getParameter<std::string>("template_dir")),

    f_dphi(0),
    f_dz(0),
    g_dphi(0),
    g_dz(0),
    gdpmax(0),
    fdpmax(0),
    Mdp(0),
    gdzmax(0),
    fdzmax(0),
    Mdz(0),
    
    signal_one_vertices(std::vector<MFVVertexAuxCollection> (nsignals)),
    signal_two_vertices(std::vector<MFVVertexPairCollection>(nsignals)),
    two_vertices(std::vector<MFVVertexPairCollection>(nfiles)),

    curr_phi_exp(-1.),

    n_2v_toys(0),

    rand(new TRandom3(12191982 + seed))
{
  if ((weights.size() > 0 && n1vs.size() != weights.size()) || (toy_mode && nfiles != n1vs.size()))
    throw cms::Exception("Misconfiguration", "inconsistent sample info");

  if (nsignals != signal_weights.size())
    throw cms::Exception("Misconfiguration", "inconsistent signal sample info");

  if (signal_contamination >= 0 && !toy_mode)
    throw cms::Exception("Misconfiguration", "no signal contamination when not in toy mode");

  if (sampling_type < 0 || sampling_type > 2)
    throw cms::Exception("Misconfiguration", "sampling_type must be one of 0,1,2");

  if (template_range.size() < 3 || template_range[0] < 0 || template_range[1] < template_range[0])
    throw cms::Exception("Misconfiguration", "template_range messed up");

  if (template_binning.size() < 3 || template_binning[0] < 1 || template_binning[2] < template_binning[1])
    throw cms::Exception("Misconfiguration", "template_binning messed up");

  TH1::SetDefaultSumw2();

  if (use_form_g_dphi)
    g_dphi = new TF1("g_dphi", form_g_dphi.c_str(), 0, M_PI);
  else
    g_dphi = new TF1("g_dphi", fcn_g_dphi, 0, M_PI, 2);

  if (use_form_g_dz)
    g_dz = new TF1("g_dz", form_g_dz.c_str(), -40, 40);
  else
    g_dz = new TF1("g_dz", fcn_fg_dz, -40, 40, 1);

  if (use_form_f_dphi)
    f_dphi = new TF1("f_dphi", form_f_dphi.c_str(), 0, M_PI);
  else
    f_dphi = new TF1("f_dphi", fcn_f_dphi, 0, M_PI, 1);

  if (use_form_f_dz)
    f_dz = new TF1("f_dz", form_f_dz.c_str(), -40, 40);
  else
    f_dz = new TF1("f_dz", fcn_fg_dz, -40, 40, 1);
  
  h_1v_dphi_env = fs->make<TH1D>("h_1v_dphi_env", "", 8, -M_PI, M_PI);
  h_1v_absdphi_env = fs->make<TH1D>("h_1v_absdphi_env", "", 8, 0, M_PI);
  h_1v_dz_env = fs->make<TH1D>("h_1v_dz_env", "", 200, -40, 40);
  h_fcn_dphi = fs->make<TH1D>("h_fcn_dphi", "", 8, -M_PI, M_PI);
  h_fcn_abs_dphi = fs->make<TH1D>("h_fcn_abs_dphi", "", 8, 0, M_PI);
  h_fcn_g_dphi = fs->make<TH1D>("h_fcn_g_dphi", "", 8, 0, M_PI);
  h_fcn_dz = fs->make<TH1D>("h_fcn_dz", "", 20, -0.1, 0.1);
  h_fcn_g_dz = fs->make<TH1D>("h_fcn_g_dz", "", 200, -40, 40);

  h_dphi_env_mean         = fs->make<TH1D>("h_dphi_env_mean"         , "", 100, 1.54, 1.6);
  h_dphi_env_mean_err     = fs->make<TH1D>("h_dphi_env_mean_err"     , "", 100, 0, 4e-4);
  h_dphi_env_rms          = fs->make<TH1D>("h_dphi_env_rms"          , "", 100, .85, .97);
  h_dphi_env_rms_err      = fs->make<TH1D>("h_dphi_env_rms_err"      , "", 100, 0, 4e-4);
  h_dphi_env_fit_offset       = fs->make<TH1D>("h_dphi_env_fit_offset"       , "", 100, 0.15, 0.17);
  h_dphi_env_fit_offset_err   = fs->make<TH1D>("h_dphi_env_fit_offset_err"   , "", 100, 0, 1);
  h_dphi_env_fit_offset_pull  = fs->make<TH1D>("h_dphi_env_fit_offset_pull"  , "", 100, -5, 5);
  h_dphi_env_fit_slope       = fs->make<TH1D>("h_dphi_env_fit_slope"       , "", 100, 0., 1e-3);
  h_dphi_env_fit_slope_err   = fs->make<TH1D>("h_dphi_env_fit_slope_err"   , "", 100, 0, 4e-3);
  h_dphi_env_fit_slope_pull  = fs->make<TH1D>("h_dphi_env_fit_slope_pull"  , "", 100, -5, 5);
  h_dphi_env_fit_chi2     = fs->make<TH1D>("h_dphi_env_fit_chi2"     , "", 100, 0, 20);
  h_dphi_env_fit_chi2prob = fs->make<TH1D>("h_dphi_env_fit_chi2prob" , "", 100, 0, 1);
  h_dz_env_mean           = fs->make<TH1D>("h_dz_env_mean"           , "", 100, -0.1, 0.1);
  h_dz_env_mean_err       = fs->make<TH1D>("h_dz_env_mean_err"       , "", 100, 0, 0.004);
  h_dz_env_rms            = fs->make<TH1D>("h_dz_env_rms"            , "", 100, 8.8, 9.8);
  h_dz_env_rms_err        = fs->make<TH1D>("h_dz_env_rms_err"        , "", 100, 0, 0.004);
  h_dz_env_fit_sig        = fs->make<TH1D>("h_dz_env_fit_sig"        , "", 100, 8.8, 9.8);
  h_dz_env_fit_sig_err    = fs->make<TH1D>("h_dz_env_fit_sig_err"    , "", 100, 0, 0.004);
  h_dz_env_fit_sig_pull   = fs->make<TH1D>("h_dz_env_fit_sig_pull"   , "", 100, -5, 5);
  h_dz_env_fit_chi2       = fs->make<TH1D>("h_dz_env_fit_chi2"       , "", 100, 0, 20);
  h_dz_env_fit_chi2prob   = fs->make<TH1D>("h_dz_env_fit_chi2prob"   , "", 100, 0, 1);
  h_dphi_mean             = fs->make<TH1D>("h_dphi_mean"             , "", 100, 1.5, 3);
  h_dphi_mean_err         = fs->make<TH1D>("h_dphi_mean_err"         , "", 100, 0, 0.2);
  h_dphi_rms              = fs->make<TH1D>("h_dphi_rms"              , "", 100, 0, 2);
  h_dphi_rms_err          = fs->make<TH1D>("h_dphi_rms_err"          , "", 100, 0, 0.2);
  h_dphi_asym             = fs->make<TH1D>("h_dphi_asym"             , "", 100, 0, 2);
  h_dphi_asym_err         = fs->make<TH1D>("h_dphi_asym_err"         , "", 100, 0, 2);
  h_dphi_fit_exp          = fs->make<TH1D>("h_dphi_fit_exp"          , "", 100, 0, 8);
  h_dphi_fit_exp_err      = fs->make<TH1D>("h_dphi_fit_exp_err"      , "", 100, 0, 4);
  h_dphi_fit_exp_pull     = fs->make<TH1D>("h_dphi_fit_exp_pull"     , "", 100, -5, 5);
  h_dphi_fit_chi2         = fs->make<TH1D>("h_dphi_fit_chi2"         , "", 100, 0, 20);
  h_dphi_fit_chi2prob     = fs->make<TH1D>("h_dphi_fit_chi2prob"     , "", 100, 0, 1);
  h_dz_mean           = fs->make<TH1D>("h_dz_mean"           , "", 100, -0.1, 0.1);
  h_dz_mean_err       = fs->make<TH1D>("h_dz_mean_err"       , "", 100, 0, 0.004);
  h_dz_rms            = fs->make<TH1D>("h_dz_rms"            , "", 100, 0, 0.04);
  h_dz_rms_err        = fs->make<TH1D>("h_dz_rms_err"        , "", 100, 0, 0.004);
  h_dz_fit_sig        = fs->make<TH1D>("h_dz_fit_sig"        , "", 100, 0, 0.04);
  h_dz_fit_sig_err    = fs->make<TH1D>("h_dz_fit_sig_err"    , "", 100, 0, 0.004);
  h_dz_fit_sig_pull   = fs->make<TH1D>("h_dz_fit_sig_pull"   , "", 100, -5, 5);
  h_dz_fit_chi2       = fs->make<TH1D>("h_dz_fit_chi2"       , "", 100, 0, 20);
  h_dz_fit_chi2prob   = fs->make<TH1D>("h_dz_fit_chi2prob"   , "", 100, 0, 1);

  for (int i = 0; i < n_t; ++i) {
    if (!do_by_means && i == n_t_2v)
      break;

    const char* iv = t_names[i];

    h_xy                [i] = fs->make<TH2D>(TString::Format("h_%s_xy"                , iv), "", 100, -0.05, 0.05, 100, 0.05, 0.05);
    h_bs2ddist          [i] = fs->make<TH1D>(TString::Format("h_%s_bs2ddist"          , iv), "", 100, 0, 0.1);
    h_bs2ddist_v_bsdz   [i] = fs->make<TH2D>(TString::Format("h_%s_bs2ddist_v_bsdz"   , iv), "", 200, -20, 20, 100, 0, 0.1);
    h_bsdz              [i] = fs->make<TH1D>(TString::Format("h_%s_bsdz"              , iv), "", 200, -20, 20);
    h_bs2ddist_0        [i] = fs->make<TH1D>(TString::Format("h_%s_bs2ddist_0"        , iv), "", 100, 0, 0.1);
    h_bs2ddist_v_bsdz_0 [i] = fs->make<TH2D>(TString::Format("h_%s_bs2ddist_v_bsdz_0" , iv), "", 200, -20, 20, 100, 0, 0.1);
    h_bsdz_0            [i] = fs->make<TH1D>(TString::Format("h_%s_bsdz_0"            , iv), "", 200, -20, 20);
    h_bs2ddist_1        [i] = fs->make<TH1D>(TString::Format("h_%s_bs2ddist_1"        , iv), "", 100, 0, 0.1);
    h_bs2ddist_v_bsdz_1 [i] = fs->make<TH2D>(TString::Format("h_%s_bs2ddist_v_bsdz_1" , iv), "", 200, -20, 20, 100, 0, 0.1);
    h_bsdz_1            [i] = fs->make<TH1D>(TString::Format("h_%s_bsdz_1"            , iv), "", 200, -20, 20);

    h_ntracks           [i] = fs->make<TH2D>(TString::Format("h_%s_ntracks"           , iv), "", 20, 0, 20, 20, 0, 20);
    h_ntracks01         [i] = fs->make<TH1D>(TString::Format("h_%s_ntracks01"         , iv), "", 30, 0, 30);
    h_svdist2d          [i] = fs->make<TH1D>(TString::Format("h_%s_svdist2d"          , iv), "", 100, 0, 0.1);
    h_svdist2d_all      [i] = fs->make<TH1D>(TString::Format("h_%s_svdist2d_all"      , iv), "", int(template_binning[0]), template_binning[1], template_binning[2]);
    h_svdz              [i] = fs->make<TH1D>(TString::Format("h_%s_svdz"              , iv), "", 20, -0.1, 0.1);
    h_svdz_all          [i] = fs->make<TH1D>(TString::Format("h_%s_svdz_all"          , iv), "", 400, -20, 20);
    h_dphi              [i] = fs->make<TH1D>(TString::Format("h_%s_dphi"              , iv), "", 8, -M_PI, M_PI);
    h_abs_dphi          [i] = fs->make<TH1D>(TString::Format("h_%s_abs_dphi"          , iv), "", 8, 0, M_PI);
    h_svdz_v_dphi       [i] = fs->make<TH2D>(TString::Format("h_%s_svdz_v_dphi"       , iv), "", 8, -M_PI, M_PI, 50, -0.1, 0.1);
  }

  if (do_by_means) {
    h_1v_svdist2d_fit_2v = fs->make<TH1D>("h_1v_svdist2d_fit_2v", "", 100, 0, 0.1);

    h_meandiff = fs->make<TH1D>("h_meandiff", "", 100, 0, 0.05);
    h_shift = fs->make<TH1D>("h_shift", "", 100, 0, 100);
    h_ksdist  = fs->make<TH1D>("h_ksdist",  "", 101, 0, 1.01);
    h_ksprob  = fs->make<TH1D>("h_ksprob",  "", 101, 0, 1.01);
    h_ksdistX = fs->make<TH1D>("h_ksdistX", "", 101, 0, 1.01);
    h_ksprobX = fs->make<TH1D>("h_ksprobX", "", 101, 0, 1.01);

    h_pred_v_true = fs->make<TH2D>("h_pred_v_true", "", 100, 0, 20, 100, 0, 20);
    h_pred_m_true = fs->make<TH1D>("h_pred_m_true", "", 100, -20, 20);
  }

  for (std::string fn : filenames) {
    size_t pos = fn.find_last_of('/');
    if (pos != std::string::npos)
      fn.erase(0, pos + 1);
    pos = fn.find(".root");
    fn.erase(pos, std::string::npos);
    fn = "h_toy_nevents_" + fn;
    TH1D* h = fs->make<TH1D>(fn.c_str(), "", 200, 0, 200);
    h_toy_nevents_from.push_back(h);
  }
  h_toy_nevents = fs->make<TH1D>("h_toy_nevents", "", 200, 0, 200);
  h_toy_nevents_signal = fs->make<TH1D>("h_toy_nevents_signal", "", 1000, 0, 1000);
}

MFVOne2Two::~MFVOne2Two() {
  delete f_dphi;
  delete f_dz;
  delete g_dphi;
  delete g_dz;
  delete rand;
}

MFVVertexAux MFVOne2Two::xform_vertex(const MFVVertexAux& v) const {
  return v;
}

void MFVOne2Two::set_sig(MFVVertexAux& v) const {
  v.which = 255;
}

bool MFVOne2Two::is_sig(const MFVVertexAux& v) const {
  return v.which == 255;
}

bool MFVOne2Two::sel_vertex(const MFVVertexAux& v) const {
  return v.ntracks() >= min_ntracks;
}

bool MFVOne2Two::is_sideband(const MFVVertexAux& v0, const MFVVertexAux& v1) const {
  return svdist2d(v0, v1) < svdist2d_cut;
}

void MFVOne2Two::read_file(const std::string& filename, const bool sig, MFVVertexAuxCollection& one_vertices, MFVVertexPairCollection& two_vertices) const {
  TFile* f = TFile::Open(filename.c_str());
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
      if (sig) set_sig(v0);
      for (int i = 0; i < nt.ntk0; ++i)
	v0.insert_track();
      if (sel_vertex(v0))
	one_vertices.push_back(v0);
    }
    else if (nt.nvtx == 2) {
      MFVVertexAux v0, v1;
      if (sig) { 
        set_sig(v0);
        set_sig(v1);
      }
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

void MFVOne2Two::fill_2d(const int ih, const double w, const MFVVertexAux& v0, const MFVVertexAux& v1) const {
  if ((ih == t_2vsb || ih == t_2vsbbkg || ih == t_2vsbsig || ih == t_1vsb) && !is_sideband(v0, v1))
    return;

  if ((ih == t_2vsig || ih == t_2vsbsig) && (!is_sig(v0) || !is_sig(v1)))
    return;

  if ((ih == t_2vbkg || ih == t_2vsbbkg) && (is_sig(v0) || is_sig(v1)))
    return;

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
  h_svdist2d_all[ih]->Fill(svdist2d(v0, v1), w);
  h_svdz[ih]->Fill(dz(v0, v1), w);
  h_svdz_all[ih]->Fill(dz(v0, v1), w);
  h_dphi[ih]->Fill(dphi(v0, v1), w);
  h_abs_dphi[ih]->Fill(fabs(dphi(v0, v1)), w);
  h_svdz_v_dphi[ih]->Fill(dphi(v0, v1), dz(v0, v1), w);
}

void MFVOne2Two::fill_1d(const double w, const MFVVertexAux& v0, const MFVVertexAux& v1) const {
  // The 2v pairs are ordered with ntk0 > ntk1, so fill here the same way.
  const int ntk0 = v0.ntracks(); 
  const int ntk1 = v1.ntracks();
  if (ntk1 > ntk0) {
    fill_2d(t_1v,   w, v1, v0);
    fill_2d(t_1vsb, w, v1, v0);
  }
  else {
    fill_2d(t_1v,   w, v0, v1);
    fill_2d(t_1vsb, w, v0, v1);
  }
}

double MFVOne2Two::prob_1v_pair(const MFVVertexAux& v0, const MFVVertexAux& v1) const {
  const double dp = fabs(dphi(v0, v1));
  const double dz = v0.z - v1.z;

  return
    accept_prob(f_dphi->Eval(dp), g_dphi->Eval(dp), Mdp) *
    accept_prob(f_dz  ->Eval(dz), g_dz  ->Eval(dz), Mdz);
}

bool MFVOne2Two::accept_1v_pair(const MFVVertexAux& v0, const MFVVertexAux& v1) const {
  const double dp = fabs(dphi(v0, v1));
  const double dz = v0.z - v1.z;

  return
    v0.ntracks() + v1.ntracks() < max_1v_ntracks01 &&
    accept(rand, f_dphi->Eval(dp), g_dphi->Eval(dp), Mdp) &&
    accept(rand, f_dz  ->Eval(dz), g_dz  ->Eval(dz), Mdz);
}

void MFVOne2Two::print_config() const {
  printf("\n\n==================================================================\n\nconfig: ntracks >= %i  svdist2d sideband <= %f\n", min_ntracks, svdist2d_cut);
}

void MFVOne2Two::read_signals() {
  // When in all-sample mode (i.e. when we're scaling numbers to data
  // luminosity), read all signal samples to print signal
  // contamination in sideband and signal strength in signal region.

  if (nfiles > 1) { // i.e. only in all-sample mode
    printf("reading %lu signals\n", nsignals);
    for (size_t isig = 0; isig < nsignals; ++isig) {
      printf("%s ", signal_files[isig].c_str());
      read_file(signal_files[isig], true, signal_one_vertices[isig], signal_two_vertices[isig]);

      int nside = 0, nsig = 0;
      for (const auto& pair : signal_two_vertices[isig])
        if (is_sideband(pair.first, pair.second))
          ++nside;
        else
          ++nsig;

      const double w = signal_weights[isig];
      printf("  scaled: # 1v: %f  # 2v: %f = (%f sideband + %f signal region)\n", signal_one_vertices[isig].size()*w, signal_two_vertices[isig].size()*w, nside*w, nsig*w);
    }
  }
}

void MFVOne2Two::read_vertices() {
  // Read all vertices from the input files. Two modes: unweighted,
  // single sample, or combine multiple samples, reading a random
  // subset of events. The latter can include signal contamination.

  if (!toy_mode) {
    // In regular mode, take all events from the file (with weight 1).
    printf("\n==============================\n\nsingle sample mode, filename: %s\n", filenames[0].c_str());
    read_file(filenames[0], false, one_vertices, two_vertices[0]);
  }
  else {
    // Config file specifies how many to take (or the Poisson-mean
    // number) from each sample. Directly keep the 2vs; they will be
    // histogrammed with config-specified weights below.
    printf("\n==============================\n\nmultiple sample mode, #filenames: %i\n", int(filenames.size()));

    TTree* t_sample_use = fs->make<TTree>("t_sample_use", "");
    unsigned char b;
    unsigned short s;
    t_sample_use->Branch("ifile", &b, "ifile/b");
    t_sample_use->Branch("evuse", &s, "evuse/s");

    for (size_t ifile = 0; ifile < nfiles; ++ifile) {
      printf("file: %s\n", filenames[ifile].c_str());
      MFVVertexAuxCollection v1v;
      read_file(filenames[ifile], false, v1v, two_vertices[ifile]);

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
          b = ifile;
          s = t;
          t_sample_use->Fill();
          one_vertices.push_back(v1v[t++]);
        }
      }
    }

    if (signal_contamination >= 0) {
      const size_t isig(signal_contamination);
      const MFVVertexAuxCollection& v1v = signal_one_vertices[isig];
      const double w = signal_weights[isig];
      const double n1v_d = v1v.size() * w;
      const int n1v = poisson_n1vs ? rand->Poisson(n1v_d) : int(n1v_d) + 1;
      const int N1v = int(v1v.size());

      printf("including signal contamination from %s: %i/%i 1v events", signal_files[isig].c_str(), n1v, N1v);
      int t = 0, m = 0;
      while (m < n1v) {
        if ((N1v - t) * rand->Rndm() >= n1v - m)
          ++t;
        else {
          ++m;
          b = 100 + isig;
          s = t;
          t_sample_use->Fill();
          one_vertices.push_back(v1v[t++]);
        }
      }

      const int N2v(signal_two_vertices[isig].size());
      printf(" and %f (%i unweighted) 2v events\n", w*N2v, N2v);
    }
  }

  assert(one_vertices.size() <= WeightedMFVVertexPair::bad_index); // storing pairs later by index of type ushort, and index 65535 is reserved for uninitialized pair 
}

void MFVOne2Two::fill_2d_histos() {
  // Fill all the 2v histograms. In toy_mode we add together many
  // samples with appropriate weights. 

  for (size_t ifile = 0; ifile < nfiles; ++ifile) {
    const double w = toy_mode ? weights[ifile] : 1;

    for (const auto& pair : two_vertices[ifile])
      for (int ih = 0; ih < n_t_2v; ++ih)
        fill_2d(ih, w, pair.first, pair.second);
  }

  if (signal_contamination >= 0) {
    const size_t isig = signal_contamination;
    for (const auto& pair : signal_two_vertices[isig])
      for (int ih = 0; ih < n_t_2v; ++ih)
        if (ih != t_1v)
          fill_2d(ih, signal_weights[isig], pair.first, pair.second);
  }
}

void MFVOne2Two::fit_envelopes() {
  // Find the envelope functions for dphi and dz.

  printf("\n==============================\n\nfitting envelopes\n"); fflush(stdout);

  const int N1v = sample_only > 0 ? sample_only : int(one_vertices.size());

  // Fill the envelope histos to be fit with all unique 1v pairs.
  for (int iv = 0; iv < N1v; ++iv) {
    const MFVVertexAux& v0 = one_vertices[iv];
    for (int jv = iv+1; jv < N1v; ++jv) {
      const MFVVertexAux& v1 = one_vertices[jv];
      h_1v_dphi_env->Fill(dphi(v0, v1));
      h_1v_absdphi_env->Fill(fabs(dphi(v0, v1)));
      h_1v_dz_env->Fill(dz(v0, v1));
    }
  }

  if (find_g_dphi) {
    h_1v_absdphi_env->Scale(1./h_1v_absdphi_env->Integral());
    const double integxwidth = h_1v_absdphi_env->Integral()*h_1v_absdphi_env->GetXaxis()->GetBinWidth(1);
    TF1* g_dphi_temp = new TF1("g_dphi_temp", TString::Format("%f*(%s)", integxwidth, form_g_dphi.c_str()), g_dphi->GetXmin(), g_dphi->GetXmax());
    g_dphi_temp->SetParameter(0, 0.125);
    g_dphi_temp->SetParameter(1, 5e-4);
    TFitResultPtr res = h_1v_absdphi_env->Fit("g_dphi_temp", "RQS");
    printf("h_dphi_env mean %.3f +- %.3f  rms %.3f +- %.3f   g_dphi fit offset %.4f +- %.4f  slope %.4f +- %.4f  chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n", h_1v_absdphi_env->GetMean(), h_1v_absdphi_env->GetMeanError(), h_1v_absdphi_env->GetRMS(), h_1v_absdphi_env->GetRMSError(), res->Parameter(0), res->ParError(0), res->Parameter(1), res->ParError(1), res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
    g_dphi->FixParameter(0, res->Parameter(0));
    g_dphi->FixParameter(1, res->Parameter(1));

    h_dphi_env_mean    ->Fill(h_1v_absdphi_env->GetMean());
    h_dphi_env_mean_err->Fill(h_1v_absdphi_env->GetMeanError());
    h_dphi_env_rms     ->Fill(h_1v_absdphi_env->GetRMS());
    h_dphi_env_rms_err ->Fill(h_1v_absdphi_env->GetRMSError());
    h_dphi_env_fit_offset     ->Fill(res->Parameter(0));
    h_dphi_env_fit_offset_err ->Fill(res->ParError(0));
    h_dphi_env_fit_offset_pull->Fill((res->Parameter(0) - 0.1587) / res->ParError(0));
    h_dphi_env_fit_slope      ->Fill(res->Parameter(1));
    h_dphi_env_fit_slope_err  ->Fill(res->ParError(1));
    h_dphi_env_fit_slope_pull ->Fill((res->Parameter(1) - 5e-4) / res->ParError(0));
    h_dphi_env_fit_chi2    ->Fill(res->Chi2() / res->Ndf());
    h_dphi_env_fit_chi2prob->Fill(res->Prob());

    delete g_dphi_temp;
  }
  else {
    g_dphi->FixParameter(0, 1/M_PI);
    g_dphi->FixParameter(1, 0);
  }

  if (find_g_dz) {
    h_1v_dz_env->Scale(1./h_1v_dz_env->Integral());
    TF1* g_dz_temp = new TF1("g_dz_temp", TString::Format("%f*(%s)", h_1v_dz_env->Integral()*h_1v_dz_env->GetXaxis()->GetBinWidth(1), form_g_dz.c_str()), g_dz->GetXmin(), g_dz->GetXmax());
    g_dz_temp->SetParameter(0, 10);
    TFitResultPtr res = h_1v_dz_env->Fit(g_dz_temp, "RQS");
    printf("g_dz fit to gaus sigma %6.3f +- %6.3f   chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n", res->Parameter(0), res->ParError(0), res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
    g_dz->FixParameter(0, res->Parameter(0));

    h_dz_env_mean    ->Fill(h_1v_dz_env->GetMean());
    h_dz_env_mean_err->Fill(h_1v_dz_env->GetMeanError());
    h_dz_env_rms     ->Fill(h_1v_dz_env->GetRMS());
    h_dz_env_rms_err ->Fill(h_1v_dz_env->GetRMSError());
    h_dz_env_fit_sig     ->Fill(res->Parameter(0));
    h_dz_env_fit_sig_err ->Fill(res->Parameter(0));
    h_dz_env_fit_sig_pull->Fill((res->Parameter(0) - h_1v_dz_env->GetRMS()) / res->ParError(0));
    h_dz_env_fit_chi2    ->Fill(res->Chi2() / res->Ndf());
    h_dz_env_fit_chi2prob->Fill(res->Prob());

    delete g_dz_temp;
  }
  else
    g_dz->FixParameter(0, 9.25);

  // Fill histos with 1e5 samples of each to check things went OK.
  h_fcn_g_dphi->FillRandom("g_dphi", 100000);
  h_fcn_g_dz  ->FillRandom("g_dz",   100000);
}

void MFVOne2Two::fit_fs_with_sideband() {
  // Fit f_dphi and f_dz from the 2v events in the sideband.

  printf("\n==============================\n\nfitting fs\n"); fflush(stdout);

  TString opt = "LIRQS";
  if (toy_mode)
    opt = "W" + opt;

  if (find_f_dphi) {
    const int t_which = find_f_dphi_bkgonly ? t_2vsbbkg : t_2vsb;

    TF1* f_dphi_temp = new TF1("f_dphi_temp", TString::Format("%f*(%s)", h_abs_dphi[t_which]->Integral()*h_abs_dphi[t_which]->GetXaxis()->GetBinWidth(1), form_f_dphi.c_str()), 0, M_PI);
    TFitResultPtr res = h_abs_dphi[t_which]->Fit(f_dphi_temp, opt);
    printf("f_dphi fit exp = %6.3f +- %6.3f   chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n", res->Parameter(0), res->ParError(0), res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
    f_dphi->FixParameter(0, res->Parameter(0));

    h_dphi_mean    ->Fill(h_abs_dphi[t_which]->GetMean());
    h_dphi_mean_err->Fill(h_abs_dphi[t_which]->GetMeanError());
    h_dphi_rms     ->Fill(h_abs_dphi[t_which]->GetRMS());
    h_dphi_rms_err ->Fill(h_abs_dphi[t_which]->GetRMSError());
    double integ1, err1, integ2, err2;
    integ1 = h_abs_dphi[t_which]->IntegralAndError(1,5, err1);
    integ2 = h_abs_dphi[t_which]->IntegralAndError(6,8, err2);
    double N1 = pow(integ1/err1, 2);
    double N2 = pow(integ2/err2, 2);
    double asym, asymlo, asymhi;
    asym = clopper_pearson_poisson_means(N1, N2, asymlo, asymhi);
    h_dphi_asym      ->Fill(asym);
    h_dphi_asym_err  ->Fill((asymhi - asymlo)/2);
    h_dphi_fit_exp     ->Fill(res->Parameter(0));
    h_dphi_fit_exp_err ->Fill(res->ParError(0));
    h_dphi_fit_exp_pull->Fill((res->Parameter(0) - 2) / res->ParError(0)); // JMTBAD
    h_dphi_fit_chi2    ->Fill(res->Chi2() / res->Ndf());
    h_dphi_fit_chi2prob->Fill(res->Prob());

    delete f_dphi_temp;
  }
  else
    f_dphi->FixParameter(0, 1.5);

  if (find_f_dz) {
    const int t_which = find_f_dz_bkgonly ? t_2vsbbkg : t_2vsb;

    TF1* f_dz_temp = new TF1("f_dz_temp", TString::Format("%f*(%s)", h_svdz[t_which]->Integral()*h_svdz[t_which]->GetXaxis()->GetBinWidth(1), form_f_dz.c_str()), f_dz->GetXmin(), f_dz->GetXmax());
    TFitResultPtr res = h_svdz[t_which]->Fit(f_dz_temp, opt);
    printf("f_dz fit gaus sigma = %6.3f +- %6.3f   chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n", res->Parameter(0), res->ParError(0), res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
    f_dz->FixParameter(0, res->Parameter(0));

    h_dz_mean    ->Fill(h_svdz[t_which]->GetMean());
    h_dz_mean_err->Fill(h_svdz[t_which]->GetMeanError());
    h_dz_rms     ->Fill(h_svdz[t_which]->GetRMS());
    h_dz_rms_err ->Fill(h_svdz[t_which]->GetRMSError());
    h_dz_fit_sig     ->Fill(res->Parameter(0));
    h_dz_fit_sig_err ->Fill(res->ParError(0));
    h_dz_fit_sig_pull->Fill((res->Parameter(0) - h_svdz[t_which]->GetRMS()) / res->ParError(0));
    h_dz_fit_chi2    ->Fill(res->Chi2() / res->Ndf());
    h_dz_fit_chi2prob->Fill(res->Prob());

    delete f_dz_temp;
  }
  else
    f_dz->FixParameter(0, 0.02);

  update_f_weighting_pars();

  h_fcn_dphi->FillRandom("f_dphi", 100000);
  h_fcn_abs_dphi->FillRandom("f_dphi", 100000);
  h_fcn_dz->FillRandom("f_dz", 100000);
}

void MFVOne2Two::update_f_weighting_pars() {
  gdpmax = g_dphi->GetMaximum();
  fdpmax = f_dphi->GetMaximum();
  Mdp = fdpmax/gdpmax;

  gdzmax = g_dz->GetMaximum();
  fdzmax = f_dz->GetMaximum();
  Mdz = fdzmax/gdzmax;
}

void MFVOne2Two::set_phi_exp(double p) {
  f_dphi->FixParameter(0, p);
  update_f_weighting_pars();
}

void MFVOne2Two::choose_2v_from_1v(const bool output_usage) {
  // Sample npairs from the one_vertices sample.
  // - sampling_type = 0: sample npairs randomly with replacement,
  // accepting according to the f_dphi/dz functions.
  // - sampling_type = 1: for every unique pair, accept according to
  // f_dphi/dz.
  // - sampling_type = 2: for every unique pair, use pair with weight
  // = prob according to f_dphi/dz.

  printf("\n==============================\n\nsampling 1v pairs with phi_exp = %f\n", curr_phi_exp); fflush(stdout);

  two_vertices_from_1v.clear();
  const int N1v = sample_only > 0 ? sample_only : int(one_vertices.size());

  if (sampling_type == 0) {
    std::vector<int> used(N1v, 0);
    const int giveup = 10*N1v; // After choosing one vertex, may be so far out in e.g. dz tail that you can't find another one. Give up after trying this many times.
    const int npairsuse = npairs > 0 ? npairs : N1v/2;

    for (int ipair = 0; ipair < npairsuse; ++ipair) {
      int iv = rand->Integer(N1v);
      ++used[iv];
      const MFVVertexAux& v0 = one_vertices[iv];
      int tries = 0;
      int jv = -1;
      while (jv == -1) {
        int x = rand->Integer(N1v);
        if (x != iv) {
          const MFVVertexAux& v1 = one_vertices[x];
          if (accept_1v_pair(v0, v1)) {
            jv = x;
            ++used[jv];
            two_vertices_from_1v.push_back(WeightedMFVVertexPair(iv, x));
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
        --ipair;
      }
    }

    if (output_usage) {
      // Output 1v usage counts (versus z).
      TTree* t_use = fs->make<TTree>("t_use", "");
      unsigned char b;
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
        t_use->Branch("nuse", &b, "nuse/b");
      for (int i = 0; i < N1v; ++i) {
        z = one_vertices[i].z;
        if (use_short)
          s = used[i];
        else
          b = used[i];
        t_use->Fill();
      }
    }
  }
  else if (sampling_type == 1) {
    for (int iv = 0; iv < N1v; ++iv) {
      for (int jv = iv+1; jv < N1v; ++jv) {
        const MFVVertexAux& v0 = one_vertices[iv];
        const MFVVertexAux& v1 = one_vertices[jv];
        if (accept_1v_pair(v0, v1))
          two_vertices_from_1v.push_back(WeightedMFVVertexPair(iv, jv));
      }
    }
  }
  else if (sampling_type == 2) {
    for (int iv = 0; iv < N1v; ++iv) {
      for (int jv = iv+1; jv < N1v; ++jv) {
        const MFVVertexAux& v0 = one_vertices[iv];
        const MFVVertexAux& v1 = one_vertices[jv];
        const double w = prob_1v_pair(v0, v1);
        two_vertices_from_1v.push_back(WeightedMFVVertexPair(w, iv, jv));
      }
    }
  }
}

void MFVOne2Two::fill_1d_histos() {
  for (const auto& pair : two_vertices_from_1v)
    fill_1d(pair.w, v0(pair), v1(pair));
}

TH1D* MFVOne2Two::shift_hist(const TH1D* h, const int shift, TH1D** hshifted) const {
  const int nbins = h->GetNbinsX();
  if (*hshifted == 0)
    *hshifted = fs->make<TH1D>(TString::Format("%s_shift%i", h->GetName(), shift), "", nbins, h->GetXaxis()->GetXmin(), h->GetXaxis()->GetXmax());

  for (int ibin = 1; ibin <= nbins+1; ++ibin) {
    const int ifrom = ibin - shift;
    double val = 0, err = 0;
    if (ifrom >= 1) { // don't shift in from underflow, shouldn't be any with svdist = positive quantity anyway
      val = h->GetBinContent(ifrom);
      err = h->GetBinError  (ifrom);
    }
    if (ibin == nbins+1) {
      double var = err*err;
      for (int irest = ifrom+1; irest <= nbins+1; ++irest) {
        val += h->GetBinContent(irest);
        var += pow(h->GetBinError(irest), 2);
      }
      err = sqrt(var);
    }
    (*hshifted)->SetBinContent(ibin, val);
    (*hshifted)->SetBinError  (ibin, err);
  }

  return *hshifted;
}

void MFVOne2Two::by_means() {
  // Fit the 1v distribution to the 2v one by shifting it over and
  // scaling in the sideband.
  printf("\n==============================\n\nfitting 1v shape to 2v dist\n"); fflush(stdout);

  const double meandiff = h_svdist2d[t_2v]->GetMean() - h_svdist2d[t_1v]->GetMean();
  const int nbins = h_svdist2d[t_1v]->GetNbinsX();
  assert(h_svdist2d[t_2v]->GetNbinsX() == nbins);
  assert(fabs(h_svdist2d[t_2v]->GetBinWidth(1) - h_svdist2d[t_1v]->GetBinWidth(1)) < 1e-5);

  const int shift = int(round(meandiff/h_svdist2d[t_1v]->GetBinWidth(1)));
  printf("shift by %i bins (mean diff %f)\n", shift, meandiff); fflush(stdout);

  h_meandiff->Fill(meandiff);
  h_shift->Fill(shift);

  shift_hist(h_svdist2d[t_1v], shift, &h_1v_svdist2d_fit_2v);

  const int last_sideband_bin = h_1v_svdist2d_fit_2v->FindBin(svdist2d_cut) - 1;
  h_1v_svdist2d_fit_2v->Scale(h_svdist2d[t_2v]    ->Integral(1, last_sideband_bin) / 
                              h_1v_svdist2d_fit_2v->Integral(1, last_sideband_bin));

  printf("KStest(h_1v_svdist2d_fit_2v, h_2v_svdist2d): "); fflush(stdout);
  const double ksdist = h_1v_svdist2d_fit_2v->KolmogorovTest(h_svdist2d[t_2v], "MO");
  const double ksprob = h_1v_svdist2d_fit_2v->KolmogorovTest(h_svdist2d[t_2v], "O");
  const double ksdistX = h_1v_svdist2d_fit_2v->KolmogorovTest(h_svdist2d[t_2v], "MOX");
  const double ksprobX = h_1v_svdist2d_fit_2v->KolmogorovTest(h_svdist2d[t_2v], "OX");
  printf(" dist = %f (X: %f)  pval = %g (X: %g)\n", ksdist, ksprob, ksdistX, ksprobX); fflush(stdout);

  h_ksdist->Fill(ksdist);
  h_ksprob->Fill(ksprob);
  h_ksdistX->Fill(ksdistX);
  h_ksprobX->Fill(ksprobX);
  
  const double pred_sidereg_bkg = h_1v_svdist2d_fit_2v->Integral(1, last_sideband_bin);
  const double true_sidereg     = h_svdist2d[t_2v]    ->Integral(1, last_sideband_bin);
  const double true_sidereg_sig = h_svdist2d[t_2vsig] ->Integral(1, last_sideband_bin);
  const double pred_signreg_bkg = h_1v_svdist2d_fit_2v->Integral(last_sideband_bin+1, nbins+1);
  const double true_signreg     = h_svdist2d[t_2v]    ->Integral(last_sideband_bin+1, nbins+1);
  const double true_signreg_sig = h_svdist2d[t_2vsig] ->Integral(last_sideband_bin+1, nbins+1);

  const double true_sidereg_bkg = true_sidereg - true_sidereg_sig;
  const double true_signreg_bkg = true_signreg - true_signreg_sig;

  printf("h_1v_svdist2d_fit_2v integral in sideband    : %f\n", pred_sidereg_bkg);
  printf("h_1v_svdist2d_fit_2v integral in signal      : %f\n", pred_signreg_bkg);
  printf("h_2v_svdist2d integral in sideband           : %f\n", true_sidereg);
  printf("h_2v_svdist2d integral in sideband, sig cont.: %f\n", true_sidereg_sig);
  printf("h_2v_svdist2d integral in sideband, bkg only : %f\n", true_sidereg_bkg);
  printf("h_2v_svdist2d integral in sig.reg.           : %f\n", true_signreg);
  printf("h_2v_svdist2d integral in sig.reg., signal   : %f\n", true_signreg_sig);
  printf("h_2v_svdist2d integral in sig.reg., bkg only : %f\n", true_signreg_bkg);

  h_pred_v_true->Fill(true_signreg_bkg, pred_signreg_bkg);
  h_pred_m_true->Fill(pred_signreg_bkg - true_signreg_bkg);
}

void MFVOne2Two::make_1v_templates() {
  const double phi_exp_min = template_range[0];
  const double phi_exp_max = template_range[1];
  const double d_phi_exp = template_range[2];

  printf("\n==============================\n\nsaving 1v templates: phi = range(%f, %f, %f)\n", phi_exp_min, phi_exp_max, d_phi_exp); fflush(stdout);

  for (int i_phi = 0; curr_phi_exp + d_phi_exp < phi_exp_max; ++i_phi) {
    curr_phi_exp = phi_exp_min + i_phi * d_phi_exp;
    set_phi_exp(curr_phi_exp);

    TH1D* h_1v_template = fs->make<TH1D>(TString::Format("h_1v_template_phi%i", i_phi), TString::Format("phi_exp = %f\n", curr_phi_exp), int(template_binning[0]), template_binning[1], template_binning[2]);

    if (sampling_type != 2) {
      choose_2v_from_1v();

      for (const auto& pair : two_vertices_from_1v)
        h_1v_template->Fill(svdist2d(v0(pair), v1(pair)), pair.w);
    }
    else {
      printf("\n==============================\n\nsampling 1v pairs with phi_exp = %f\n", curr_phi_exp); fflush(stdout);

      two_vertices_from_1v.clear();
      const int N1v = sample_only > 0 ? sample_only : int(one_vertices.size());

      for (int iv = 0; iv < N1v; ++iv) {
        for (int jv = iv+1; jv < N1v; ++jv) {
          const MFVVertexAux& v0 = one_vertices[iv];
          const MFVVertexAux& v1 = one_vertices[jv];
          const double w = prob_1v_pair(v0, v1);
          h_1v_template->Fill(svdist2d(v0, v1), w);
        }
      }
    }

    h_1v_templates[i_phi] = std::make_pair(curr_phi_exp, h_1v_template);
  }
}

void MFVOne2Two::load_1v_templates(const std::string& fn, const std::string& dir) {
  printf("\n==============================\n\nloading 1v templates from %s/%s\n", fn.c_str(), dir.c_str()); fflush(stdout);

  TFile* f = TFile::Open(fn.c_str());
  if (!f)
    throw cms::Exception("ReadError", "could not read template file");

  TDirectory* d = (TDirectory*)f->Get(dir.c_str());
  if (!d)
    throw cms::Exception("ReadError", "could not read template file");

  int i_phi = 0;
  for (; i_phi < 1000; ++i_phi) {
    TH1D* h = (TH1D*)d->Get(TString::Format("h_1v_template_phi%i", i_phi));
    if (!h)
      break;

    const char* title = h->GetTitle();
    double p;
    const int r = sscanf(title, "phi_exp = %lf", &p);
    if (!r)
      throw cms::Exception("ReadError", "could not read template file");

    h_1v_templates[i_phi] = std::make_pair(p, h);
    printf("iphi: %i  phiexp: %f  rms: %f\n", i_phi, p, h->GetRMS());
  }

  if (i_phi == 0)
    throw cms::Exception("ReadError", "could not read template file");

  printf("\n==============================\n\nread %i 1v templates\n", i_phi);
}

TH1D* MFVOne2Two::make_2v_toy() {
  printf("\n==============================\n\nthrowing a 2v toy\n"); fflush(stdout);

  TH1D* h_2v_toy = fs->make<TH1D>(TString::Format("h_2v_toy_%i_%i", seed, n_2v_toys++), "", int(template_binning[0]), template_binning[1], template_binning[2]);

  int sum_n2v = 0;
  for (size_t ifile = 0; ifile < nfiles; ++ifile) {
    const double w = weights[ifile];
    const int N2v = int(two_vertices[ifile].size());
    const double n2v_d = w * N2v;
    const int n2v = rand->Poisson(n2v_d);
    sum_n2v += n2v;
    h_toy_nevents_from[ifile]->Fill(n2v);

    int t = 0, m = 0;
    while (m < n2v) {
      if ((N2v - t) * rand->Rndm() >= n2v - m)
        ++t;
      else {
        ++m;
        const auto& pair = two_vertices[ifile][t++];
        h_2v_toy->Fill(svdist2d(pair.first, pair.second));
      }
    }

    printf("events used from file #%lu:%s: %i wanted, %i actual / %i, hist integral now %.2f\n", ifile, filenames[ifile].c_str(), n2v, m, N2v, h_2v_toy->Integral());
  }

  h_toy_nevents->Fill(sum_n2v);

  if (signal_contamination >= 0) {
    const size_t isig(signal_contamination);
    const double w = signal_weights[isig];
    const int N2v = int(signal_two_vertices[isig].size());
    const double n2v_d = w * N2v;
    const int n2v = rand->Poisson(n2v_d);
    h_toy_nevents_signal->Fill(n2v);

    int t = 0, m = 0;
    while (m < n2v) {
      if ((N2v - t) * rand->Rndm() >= n2v - m)
        ++t;
      else {
        ++m;
        const auto& pair = signal_two_vertices[isig][t++];
        h_2v_toy->Fill(svdist2d(pair.first, pair.second));
      }
    }

    printf("including signal contamination from %s: %i wanted, %i actual / %i, hist integral now %.2f\n", signal_files[isig].c_str(), n2v, m, N2v, h_2v_toy->Integral());
  }
  
  return h_2v_toy;
}

void MFVOne2Two::run() {
  print_config();

  read_signals();
  read_vertices();

  fill_2d_histos();

  if (just_print)
    return;

  if (!toy_only) {
    fit_envelopes();
    fit_fs_with_sideband();

    if (do_by_means) {
      choose_2v_from_1v(true);
      fill_1d_histos();
      by_means();
    }
  }

  ////////////////////////////////////////

  if (make_templates) {
    if (template_fn.size() == 0)
      make_1v_templates();
    else
      load_1v_templates(template_fn, template_dir);
  }

  if (toy_mode) {
    make_2v_toy();
  }
}

DEFINE_FWK_MODULE(MFVOne2Two);
