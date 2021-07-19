#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Formats/interface/MergeablePOD.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/Tools/interface/Year.h"

class MFVWeightProducer : public edm::EDProducer {
public:
  explicit MFVWeightProducer(const edm::ParameterSet&);
  virtual void endLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&) override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

private:
  const edm::EDGetTokenT<jmt::MergeableInt> nevents_token;
  const edm::EDGetTokenT<jmt::MergeableFloat> sumweight_token;
  const bool throw_if_no_mcstat;
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const bool enable;
  const bool prints;
  const bool histos;

  const double partial_mc_stats_weight;
  const bool weight_gen;
  const bool weight_gen_sign_only;
  const bool weight_pileup;
  const std::vector<double> pileup_weights;
  double pileup_weight(int mc_npu) const;
  const bool weight_npv;
  const std::vector<double> npv_weights;
  double npv_weight(int mc_npu) const;
  const std::vector<int> misc_weight_indices;

  TH1D* h_gensign;
  TH1D* h_npu;
  TH1D* h_npv;

  enum { sum_nevents_total, sum_gen_weight_total, sum_gen_weight, sum_pileup_weight, sum_npv_weight, sum_weight, yearcode_x_nfiles, sum_weight_ren_up, sum_weight_ren_dn, sum_weight_fac_up, sum_weight_fac_dn, sum_weight_ren_fac_up, sum_weight_ren_fac_dn, n_sums };
  TH1D* h_sums;
};

MFVWeightProducer::MFVWeightProducer(const edm::ParameterSet& cfg)
  : nevents_token(consumes<jmt::MergeableInt, edm::InLumi>(edm::InputTag("mcStat", "nEvents"))),
    sumweight_token(consumes<jmt::MergeableFloat, edm::InLumi>(edm::InputTag("mcStat", "sumWeight"))),
    throw_if_no_mcstat(cfg.getParameter<bool>("throw_if_no_mcstat")),
    mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    enable(cfg.getParameter<bool>("enable")),
    prints(cfg.getUntrackedParameter<bool>("prints", false)),
    histos(cfg.getUntrackedParameter<bool>("histos", true)),
    partial_mc_stats_weight(cfg.getParameter<double>("partial_mc_stats_weight")),
    weight_gen(cfg.getParameter<bool>("weight_gen")),
    weight_gen_sign_only(cfg.getParameter<bool>("weight_gen_sign_only")),
    weight_pileup(cfg.getParameter<bool>("weight_pileup")),
    pileup_weights(cfg.getParameter<std::vector<double> >("pileup_weights")),
    weight_npv(cfg.getParameter<bool>("weight_npv")),
    npv_weights(cfg.getParameter<std::vector<double> >("npv_weights")),
    misc_weight_indices(cfg.getParameter<std::vector<int>>("misc_weight_indices"))
{
  if (weight_gen + weight_gen_sign_only > 1)
    throw cms::Exception("Configuration", "can only set one of weight_gen, weight_gen_sign_only");

  produces<double>();

  if (histos) {
    edm::Service<TFileService> fs;
    TH1::SetDefaultSumw2();

    h_gensign = fs->make<TH1D>("h_gensign", ";gen weight sign;events", 2, -1.5, 1.5);
    h_npu = fs->make<TH1D>("h_npu", ";number of pileup interactions;events", 100, 0, 100);
    h_npv = fs->make<TH1D>("h_npv", ";number of primary vertices;events", 100, 0, 100);

    h_sums = fs->make<TH1D>("h_sums", TString::Format("partial_mc_stats_weight = %.3f", partial_mc_stats_weight), n_sums+1, 0, n_sums+1);
    int ibin = 1;
    for (const char* x : { "sum_nevents_total", "sum_gen_weight_total", "sum_gen_weight", "sum_pileup_weight", "sum_npv_weight", "sum_weight", "yearcode_x_nfiles", "sum_weight_ren_up", "sum_weight_ren_dn", "sum_weight_fac_up", "sum_weight_fac_dn", "sum_weight_ren_fac_up", "sum_weight_ren_fac_dn", "n_sums" })
      h_sums->GetXaxis()->SetBinLabel(ibin++, x);
    h_sums->Fill(yearcode_x_nfiles, MFVNEUTRALINO_YEARCODE);
  }
}

void MFVWeightProducer::endLuminosityBlock(const edm::LuminosityBlock& lumi, const edm::EventSetup&) {
  if (lumi.run() == 1) { // no lumi.isRealData()
    edm::Handle<jmt::MergeableInt> nEvents;
    edm::Handle<jmt::MergeableFloat> sumWeight;
    lumi.getByToken(nevents_token, nEvents);
    lumi.getByToken(sumweight_token, sumWeight);

    if (nEvents.isValid() && sumWeight.isValid()) {
      if (prints)
        printf("MFVWeight::beginLuminosityBlock r: %u l: %u nEvents: %i  sumWeight: %f\n", lumi.run(), lumi.luminosityBlock(), nEvents->get(), sumWeight->get());
      
      if (histos) {
        h_sums->Fill(sum_nevents_total,        partial_mc_stats_weight * nEvents->get());
        h_sums->Fill(sum_gen_weight_total,     partial_mc_stats_weight * sumWeight->get());
      }
    }
    else if (throw_if_no_mcstat)
      throw cms::Exception("ProductNotFound", "MCStatProducer luminosity branch products not found!");
  }
}

double MFVWeightProducer::pileup_weight(int mc_npu) const {
  if (mc_npu < 0 || mc_npu >= int(pileup_weights.size()))
    return 0;
  else
    return pileup_weights[mc_npu];
}

double MFVWeightProducer::npv_weight(int mc_npv) const {
  if (mc_npv < 0 || mc_npv >= int(npv_weights.size()))
    return 0;
  else
    return npv_weights[mc_npv];
}

void MFVWeightProducer::produce(edm::Event& event, const edm::EventSetup&) {
  if (event.isRealData() != (event.id().run() != 1))
    throw cms::Exception("BadAssumption") << "isRealData = " << event.isRealData() << " and run = " << event.id().run();

  if (histos)
    h_sums->Fill(n_sums);

  if (prints)
    printf("MFVWeight: r,l,e: %u, %u, %llu  ", event.id().run(), event.luminosityBlock(), event.id().event());

  std::unique_ptr<double> weight(new double(1.));

  if (enable) {
    edm::Handle<MFVEvent> mevent;
    event.getByToken(mevent_token, mevent);

    if (!event.isRealData()) {
      if (weight_gen || weight_gen_sign_only) {
        if (prints)
          printf("gen_weight: %g  ", mevent->gen_weight);
        if (histos) {
          h_gensign->Fill(mevent->gen_weight > 0 ? 1 : -1);
          h_sums->Fill(sum_gen_weight, mevent->gen_weight);
        }
        if (weight_gen_sign_only) {
          if (mevent->gen_weight < 0)
            *weight *= -1;
        }
        else
          *weight *= mevent->gen_weight;
      }

      if (weight_pileup) {
        const double pu_w = pileup_weight(mevent->npu);
        if (prints)
          printf("mc_npu: %g  pu weight: %g  ", mevent->npu, pu_w);
        if (histos) {
          h_npu->Fill(mevent->npu);
          h_sums->Fill(sum_pileup_weight, pu_w);
        }
        *weight *= pu_w;
      }

      if (weight_npv) {
        const double npv_w = npv_weight(mevent->npv);
        if (prints)
          printf("mc_npv: %i  npv weight: %g  ", mevent->npv, npv_w);
        if (histos) {
          h_npv->Fill(mevent->npv);
          h_sums->Fill(sum_npv_weight, npv_w);
        }
        *weight *= npv_w;
      }

      for (int mwi : misc_weight_indices) {
        const double w = mevent->misc[mwi];
        if (prints)
          printf("misc weight %i: %g  ", mwi, w);
        *weight *= w;
      }
      
      // Fill in sumw entries for renormalization / factorization scale uncertainty
      if (histos) {

        double weight_ren_up = mevent->ren_weight_up;
        double weight_ren_dn = mevent->ren_weight_dn;
        double weight_fac_up = mevent->fac_weight_up;
        double weight_fac_dn = mevent->fac_weight_dn;

        h_sums->Fill(sum_weight_ren_up, *weight*weight_ren_up);
        h_sums->Fill(sum_weight_ren_dn, *weight*weight_ren_dn);
        h_sums->Fill(sum_weight_fac_up, *weight*weight_fac_up);
        h_sums->Fill(sum_weight_fac_dn, *weight*weight_fac_dn);
        h_sums->Fill(sum_weight_ren_fac_up, *weight*weight_ren_up*weight_fac_up);
        h_sums->Fill(sum_weight_ren_fac_dn, *weight*weight_ren_dn*weight_fac_dn);
      }

    }
  }

  if (histos)
    h_sums->Fill(sum_weight, *weight);

  if (prints)
    printf("total weight: %g\n", *weight);

  event.put(std::move(weight));
}

DEFINE_FWK_MODULE(MFVWeightProducer);
