#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

class MFVWeightProducer : public edm::EDProducer {
public:
  explicit MFVWeightProducer(const edm::ParameterSet&);
  virtual void beginLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&) override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

private:
  const edm::InputTag mevent_src;
  const bool enable;
  const bool prints;
  const bool histos;

  const bool weight_gen;
  const bool weight_pileup;
  const std::vector<double> pileup_weights;
  double pileup_weight(int mc_npu) const;

  enum { sum_nevents_total, sum_gen_weight_total, sum_gen_weight_prod_total, sum_gen_weight, sum_gen_weight_prod, sum_pileup_weight, sum_weight, n_sums };
  TH1F* h_sums;
};

MFVWeightProducer::MFVWeightProducer(const edm::ParameterSet& cfg)
  : mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
    enable(cfg.getParameter<bool>("enable")),
    prints(cfg.getUntrackedParameter<bool>("prints", false)),
    histos(cfg.getUntrackedParameter<bool>("histos", true)),
    weight_gen(cfg.getParameter<bool>("weight_gen")),
    weight_pileup(cfg.getParameter<bool>("weight_pileup")),
    pileup_weights(cfg.getParameter<std::vector<double> >("pileup_weights"))
{
  produces<double>();

  if (histos) {
    edm::Service<TFileService> fs;
    TH1::SetDefaultSumw2();
    h_sums = fs->make<TH1F>("h_sums", "", n_sums+1, 0, n_sums+1);
    int ibin = 1;
    for (const char* x : { "sum_nevents_total", "sum_gen_weight_total", "sum_gen_weight_prod_total", "sum_gen_weight", "sum_gen_weight_prod", "sum_pileup_weight", "sum_weight", "n_sums" })
      h_sums->GetXaxis()->SetBinLabel(ibin++, x);
  }
}

void MFVWeightProducer::beginLuminosityBlock(const edm::LuminosityBlock& lumi, const edm::EventSetup&) {
  edm::Handle<int> nEvents;
  edm::Handle<float> sumWeight, sumWeightProd;
  lumi.getByLabel(edm::InputTag("mcStat", "nEvents"), nEvents);
  lumi.getByLabel(edm::InputTag("mcStat", "sumWeight"), sumWeight);
  lumi.getByLabel(edm::InputTag("mcStat", "sumWeightProd"), sumWeightProd);

  if (prints)
    printf("MFVWeight::beginLuminosityBlock r: %u l: %u nEvents: %i  sumWeight: %f  sumWeightProd: %f\n", lumi.run(), lumi.luminosityBlock(), *nEvents, *sumWeight, *sumWeightProd);

  if (histos) {
    h_sums->Fill(sum_nevents_total, *nEvents);
    h_sums->Fill(sum_gen_weight_total, *sumWeight);
    h_sums->Fill(sum_gen_weight_prod_total, *sumWeightProd);
  }
}

double MFVWeightProducer::pileup_weight(int mc_npu) const {
  if (mc_npu < 0 || mc_npu >= int(pileup_weights.size()))
    return 0;
  else
    return pileup_weights[mc_npu];
}

void MFVWeightProducer::produce(edm::Event& event, const edm::EventSetup&) {
  if (histos)
    h_sums->Fill(n_sums);

  if (prints)
    printf("MFVWeight: r,l,e: %u, %u, %llu  ", event.id().run(), event.luminosityBlock(), event.id().event());

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mevent_src, mevent);

  std::auto_ptr<double> weight(new double);
  *weight = 1;

  if (enable) {
    if (!event.isRealData()) {
      if (weight_gen) {
        assert((mevent->gen_weight - mevent->gen_weightprod)/mevent->gen_weightprod < 1e-3); // JMTBAD
        if (prints)
          printf("gen_weight: %g  weightprod: %g  ", mevent->gen_weight, mevent->gen_weightprod);
        *weight *= mevent->gen_weight;
      }

      if (weight_pileup) {
        const double pu_w = pileup_weight(mevent->npu);
        if (prints)
          printf("mc_npu: %g  pu weight: %g  ", mevent->npu, pu_w);
        if (histos)
          h_sums->Fill(sum_pileup_weight, pu_w);
        *weight *= pu_w;
      }
    }
  }

  if (histos)
    h_sums->Fill(sum_weight, *weight);

  if (prints)
    printf("total weight: %g\n", *weight);

  event.put(weight);
}

DEFINE_FWK_MODULE(MFVWeightProducer);
