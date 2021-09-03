// JMTBAD keep in sync with MFVWeight+EventProducer
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DVCode/Tools/interface/Year.h"

class JMTWeightProducer : public edm::EDProducer {
public:
  explicit JMTWeightProducer(const edm::ParameterSet&);
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

private:
  const bool enable;
  const bool prints;
  const bool histos;

  const edm::EDGetTokenT<GenEventInfoProduct> gen_info_token;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_summary_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const bool weight_gen;
  const bool weight_gen_sign_only;
  const bool weight_pileup;
  const std::vector<double> pileup_weights;
  double pileup_weight(int mc_npu) const;
  const bool weight_npv;
  const std::vector<double> npv_weights;
  double npv_weight(int mc_npu) const;

  const bool weight_misc;
  std::vector<edm::EDGetTokenT<double>> misc_tokens;

  TH1D* h_gensign;
  TH1D* h_npu;
  TH1D* h_npv;

  enum { sum_gen_weight, sum_pileup_weight, sum_npv_weight, sum_misc_weight, sum_weight, yearcode_x_nfiles, n_sums };
  TH1D* h_sums;
};

JMTWeightProducer::JMTWeightProducer(const edm::ParameterSet& cfg)
  : enable(cfg.getParameter<bool>("enable")),
    prints(cfg.getUntrackedParameter<bool>("prints", false)),
    histos(cfg.getUntrackedParameter<bool>("histos", true)),
    gen_info_token(consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("gen_info_src"))),
    pileup_summary_token(consumes<std::vector<PileupSummaryInfo> >(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    weight_gen(cfg.getParameter<bool>("weight_gen")),
    weight_gen_sign_only(cfg.getParameter<bool>("weight_gen_sign_only")),
    weight_pileup(cfg.getParameter<bool>("weight_pileup")),
    pileup_weights(cfg.getParameter<std::vector<double> >("pileup_weights")),
    weight_npv(cfg.getParameter<bool>("weight_npv")),
    npv_weights(cfg.getParameter<std::vector<double> >("npv_weights")),
    weight_misc(cfg.getParameter<bool>("weight_misc"))
{
  if (weight_gen + weight_gen_sign_only > 1)
    throw cms::Exception("Configuration", "can only set one of weight_gen, weight_gen_sign_only");

  for (const edm::InputTag& src : cfg.getParameter<std::vector<edm::InputTag> >("misc_srcs"))
    misc_tokens.push_back(consumes<double>(src));

  produces<double>();

  if (histos) {
    edm::Service<TFileService> fs;
    TH1::SetDefaultSumw2();

    h_gensign = fs->make<TH1D>("h_gensign", ";gen weight sign;events", 2, -1.5, 1.5);
    h_npu = fs->make<TH1D>("h_npu", ";number of pileup interactions;events", 100, 0, 100);
    h_npv = fs->make<TH1D>("h_npv", ";number of primary vertices;events", 100, 0, 100);

    h_sums = fs->make<TH1D>("h_sums", "", n_sums+1, 0, n_sums+1);
    int ibin = 1;
    for (const char* x : { "sum_gen_weight", "sum_pileup_weight", "sum_npv_weight", "sum_misc_weight", "sum_weight", "yearcode_x_nfiles", "n_sums" })
      h_sums->GetXaxis()->SetBinLabel(ibin++, x);
    h_sums->Fill(yearcode_x_nfiles, MFVNEUTRALINO_YEARCODE);
  }
}

double JMTWeightProducer::pileup_weight(int mc_npu) const {
  if (mc_npu < 0 || mc_npu >= int(pileup_weights.size()))
    return 0;
  else
    return pileup_weights[mc_npu];
}

double JMTWeightProducer::npv_weight(int mc_npv) const {
  if (mc_npv < 0 || mc_npv >= int(npv_weights.size()))
    return 0;
  else
    return npv_weights[mc_npv];
}

void JMTWeightProducer::produce(edm::Event& event, const edm::EventSetup&) {
  if (event.isRealData() != (event.id().run() != 1))
    throw cms::Exception("BadAssumption") << "isRealData = " << event.isRealData() << " and run = " << event.id().run();

  if (histos)
    h_sums->Fill(n_sums);

  if (prints)
    printf("JMTWeight: r,l,e: %u, %u, %llu  ", event.id().run(), event.luminosityBlock(), event.id().event());

  std::unique_ptr<double> weight(new double(1.));

  if (enable) {
    if (!event.isRealData()) {
      if (weight_gen || weight_gen_sign_only) {
        edm::Handle<GenEventInfoProduct> gen_info;
        event.getByToken(gen_info_token, gen_info);

        const double gen_weight = gen_info->weight();

        if (prints)
          printf("gen_weight: %g  ", gen_weight);
        if (histos) {
          h_gensign->Fill(gen_weight > 0 ? 1 : -1);
          h_sums->Fill(sum_gen_weight, gen_weight);
        }
        if (weight_gen_sign_only) {
          if (gen_weight < 0)
            *weight *= -1;
        }
        else
          *weight *= gen_weight;
      }

      if (weight_pileup) {
        edm::Handle<std::vector<PileupSummaryInfo> > pileup;
        event.getByToken(pileup_summary_token, pileup);

        int npu = -1;
        for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
          if (psi->getBunchCrossing() == 0)
            npu = psi->getTrueNumInteractions();

        const double pu_w = pileup_weight(npu);
        if (prints)
          printf("mc_npu: %i  pu weight: %g  ", npu, pu_w);
        if (histos) {
          h_npu->Fill(npu);
          h_sums->Fill(sum_pileup_weight, pu_w);
        }
        *weight *= pu_w;
      }

      if (weight_npv) {
        edm::Handle<reco::VertexCollection> primary_vertices;
        event.getByToken(primary_vertex_token, primary_vertices);
        const int npv = count_if(primary_vertices->begin(), primary_vertices->end(), [](const reco::Vertex& v) { return !v.isFake() && v.ndof() > 4 && fabs(v.z()) <= 24 && v.position().rho() < 2; });

        const double npv_w = npv_weight(npv);
        if (prints)
          printf("mc_npv: %i  npv weight: %g  ", npv, npv_w);
        if (histos) {
          h_npv->Fill(npv);
          h_sums->Fill(sum_npv_weight, npv_w);
        }
        *weight *= npv_w;
      }
    }

    if (weight_misc) {
      double misc_w = 1;
      for (auto t : misc_tokens) {
        edm::Handle<double> m;
        event.getByToken(t, m);
        misc_w *= *m;
      }
      h_sums->Fill(sum_misc_weight, misc_w);
      *weight *= misc_w;
    }
  }

  if (histos)
    h_sums->Fill(sum_weight, *weight);

  if (prints)
    printf("total weight: %g\n", *weight);

  event.put(std::move(weight));
}

DEFINE_FWK_MODULE(JMTWeightProducer);
