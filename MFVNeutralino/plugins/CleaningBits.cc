#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DVCode/MFVNeutralinoFormats/interface/Event.h"
#include "DVCode/Tools/interface/TriggerHelper.h"

class MFVCleaningBits : public edm::EDProducer {
public:
  explicit MFVCleaningBits(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);

private:
  const edm::EDGetTokenT<edm::TriggerResults> cleaning_results_token;
  typedef unsigned char cleaning_word_t;
};

MFVCleaningBits::MFVCleaningBits(const edm::ParameterSet& cfg)
  : cleaning_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("cleaning_results_src")))
{
  assert(sizeof(cleaning_word_t)*8 >= mfv::n_clean_paths);
  produces<cleaning_word_t>();
}

void MFVCleaningBits::produce(edm::Event& event, const edm::EventSetup& setup) {
  static const bool debug = false;

  std::unique_ptr<cleaning_word_t> cleaning_word(new cleaning_word_t(0));

  TriggerHelper trig_helper_cleaning(event, cleaning_results_token);
  for (size_t i = 0; i < mfv::n_clean_paths; ++i) {
    const auto& paf = trig_helper_cleaning.pass_and_found_any_version(mfv::clean_paths[i]);
    if (!paf.second)
      assert(i>=5); // the 2016/2015 versions come after that
    bool pass = !paf.second || paf.first; // if not found, pass
    *cleaning_word |= (pass << i);
    if (debug) printf("clean path: %40s found? %i pass? %i   word -> %x \n", mfv::clean_paths[i], paf.second, paf.first, *cleaning_word);
  }

  event.put(std::move(cleaning_word));
}

DEFINE_FWK_MODULE(MFVCleaningBits);
