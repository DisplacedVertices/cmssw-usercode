#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class SimpleTriggerEfficiency : public edm::EDAnalyzer {
public:
  explicit SimpleTriggerEfficiency(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  edm::InputTag trigger_results_src;
  TH1F* triggers_pass_num;
  TH1F* triggers_pass_den;
};

SimpleTriggerEfficiency::SimpleTriggerEfficiency(const edm::ParameterSet& cfg) 
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    triggers_pass_num(0),
    triggers_pass_den(0)
{
}

void SimpleTriggerEfficiency::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByLabel(trigger_results_src, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  const size_t npaths = trigger_names.size();

  if (triggers_pass_num == 0) {
    // Initialize the histograms now that we have the information on
    // the paths. The bin labels will store the path names. The
    // denominator histogram will just end up being filled nevents
    // times in each bin.
    edm::Service<TFileService> fs;
    triggers_pass_num = fs->make<TH1F>("triggers_pass_num", "", npaths, 0, npaths);
    triggers_pass_den = fs->make<TH1F>("triggers_pass_den", "", npaths, 0, npaths);
    
    TH1F* hists[2] = { triggers_pass_num, triggers_pass_den };
    for (size_t ipath = 0; ipath < npaths; ++ipath)
      for (int ihist = 0; ihist < 2; ++ihist)
	hists[ihist]->GetXaxis()->SetBinLabel(ipath + 1, trigger_names.triggerName(ipath).c_str());
  }
  else {
    // Throw an exception if  we're not using the exact same paths.
    const TH1F* hist = triggers_pass_num;
    for (size_t ipath = 0; ipath < npaths; ++ipath) {
      std::string bin_label(hist->GetXaxis()->GetBinLabel(ipath + 1));
      const std::string& path_name = trigger_names.triggerName(ipath);
      if (bin_label != path_name)
	throw cms::Exception("SimpleTriggerEfficiency") << "different trigger menu? path " << ipath << " had name " << bin_label << " before, now " << path_name;
    }
  }

  for (size_t ipath = 0; ipath < npaths; ++ipath) {
    triggers_pass_den->Fill(ipath);
    if (trigger_results->accept(ipath))
      triggers_pass_num->Fill(ipath);
  }
}

DEFINE_FWK_MODULE(SimpleTriggerEfficiency);
