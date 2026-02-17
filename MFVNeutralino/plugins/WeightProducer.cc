#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Formats/interface/MergeablePOD.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Year.h"
#include "correction.h"
#include "RoccoR/RoccoR.h"
#include "RoccoR/RoccoR.cc"
#include "TRandom3.h"

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
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
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
  const bool apply_lepsf;
  const bool apply_roccor;
  const std::string pujson;
  const std::string elejson;
  const std::string mujson;
  const std::string eleSFjson;
  const std::string muSFjson;
  // const std::string roccor;
  double run(const std::unique_ptr<correction::CorrectionSet>&, const std::string&, const std::map<std::string, correction::Variable::Type>&) const;
  RoccoR rc;
  std::unique_ptr<correction::CorrectionSet> pu_cset;
  std::unique_ptr<correction::CorrectionSet> mu_cset;
  std::unique_ptr<correction::CorrectionSet> ele_cset;
  std::unique_ptr<correction::CorrectionSet> muSF_cset;
  std::unique_ptr<correction::CorrectionSet> eleSF_cset;

  TH1D* h_gensign;
  TH1D* h_npu;
  TH1D* h_npv;
  

  enum { sum_nevents_total, sum_gen_weight_total, sum_gen_weight, sum_pileup_weight, sum_npv_weight, sum_weight, yearcode_x_nfiles, sum_weight_ren_up, sum_weight_ren_dn, sum_weight_fac_up, sum_weight_fac_dn, sum_weight_ren_fac_up, sum_weight_ren_fac_dn, n_sums };
  TH1D* h_sums;

  enum { lsum_nevents_total, sum_leprecoSF, sum_lepidSF, sum_lepisoSF, sum_leptriggerSF, sum_leptotalSF, lsum_weight};
  TH1D* h_lepsums;
};

MFVWeightProducer::MFVWeightProducer(const edm::ParameterSet& cfg)
  : nevents_token(consumes<jmt::MergeableInt, edm::InLumi>(edm::InputTag("mcStat", "nEvents"))),
    sumweight_token(consumes<jmt::MergeableFloat, edm::InLumi>(edm::InputTag("mcStat", "sumWeight"))),
    throw_if_no_mcstat(cfg.getParameter<bool>("throw_if_no_mcstat")),
    mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
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
    misc_weight_indices(cfg.getParameter<std::vector<int>>("misc_weight_indices")),
    apply_lepsf(cfg.getParameter<bool>("apply_lepsf")),
    apply_roccor(cfg.getParameter<bool>("apply_roccor")),
    pujson(cfg.getParameter<std::string>("pujson")),
    elejson(cfg.getParameter<std::string>("elejson")),
    mujson(cfg.getParameter<std::string>("mujson")),
    eleSFjson(cfg.getParameter<std::string>("eleSFjson")),
    muSFjson(cfg.getParameter<std::string>("muSFjson"))
    
{

  if (weight_gen + weight_gen_sign_only > 1)
    throw cms::Exception("Configuration", "can only set one of weight_gen, weight_gen_sign_only");

  produces<double>();

  //FIXME way to turn off?
  produces<double>("lepsfup"); //syst up 
  produces<double>("lepsfdown"); //syst down 
  
  std::string year = std::to_string(int(MFVNEUTRALINO_YEAR));

  if (year == "20161") rc.init(edm::FileInPath("RoccoR/RoccoR2016aUL.txt").fullPath()); //FIXME year is hardcoded
  else if (year == "20162") rc.init(edm::FileInPath("RoccoR/RoccoR2016bUL.txt").fullPath()); //FIXME year is hardcoded
  else if (year == "2017")  { 
    rc.init(edm::FileInPath("RoccoR/RoccoR2017UL.txt").fullPath()); //FIXME year is hardcoded

  }
  else if (year == "2018")  {
    rc.init(edm::FileInPath("RoccoR/RoccoR2018UL.txt").fullPath()); //FIXME year is hardcoded
  }


  pu_cset = correction::CorrectionSet::from_file(pujson); 
  mu_cset = correction::CorrectionSet::from_file(mujson); 
  ele_cset = correction::CorrectionSet::from_file(elejson);
  muSF_cset = correction::CorrectionSet::from_file(muSFjson);
  eleSF_cset = correction::CorrectionSet::from_file(eleSFjson);

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

    h_lepsums = fs->make<TH1D>("h_lepsums", "partial_mc_stats_weight = 1", 8, 0, 8);
    int xbin = 1;
    for (const char* b : {"sum_nevents_total", "sum_leprecoSF", "sum_lepidSF", "sum_lepisoSF", "sum_leptriggerSF", "sum_leptotalSF", "sum_weight"})
      h_lepsums->GetXaxis()->SetBinLabel(xbin++, b);
  }
}

void MFVWeightProducer::endLuminosityBlock(const edm::LuminosityBlock& lumi, const edm::EventSetup&) {
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
	h_lepsums->Fill(lsum_nevents_total,     partial_mc_stats_weight * nEvents->get());
      }
    }
    else if (throw_if_no_mcstat)
      throw cms::Exception("ProductNotFound", "MCStatProducer luminosity branch products not found!");
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


double MFVWeightProducer::run (const std::unique_ptr<correction::CorrectionSet>& cset,
                               const std::string& key,
                               const std::map<std::string, correction::Variable::Type>& values) const {
  correction::Correction::Ref sf;
  try {
    sf = cset->at(key);
  }
  catch (const std::exception& e) {
    std::cerr << "FAILED cset->at(key): " << key << "  what=" << e.what() << "\n";
    throw;
  }

  std::vector<correction::Variable::Type> inputs;
  for (const correction::Variable& input: sf->inputs()) {
    const std::string& n = input.name();
    try {
      inputs.push_back(values.at(n));
    }
    catch (const std::exception& e) {
      std::cerr << "FAILED values.at(name) for key=" << key
                << " missing=" << n << " provided:";
      for (const auto& kv : values) std::cerr << " " << kv.first;
      std::cerr << "  what=" << e.what() << "\n";
      throw;
    }
  }
  return sf->evaluate(inputs);
}


void MFVWeightProducer::produce(edm::Event& event, const edm::EventSetup&) {
  //if (event.isRealData() != (event.id().run() != 1)) // This catches data with run == 1 and MC with run !=1
  if (event.isRealData() && (event.id().run() == 1)) // This only catches data with run == 1
    throw cms::Exception("BadAssumption") << "isRealData = " << event.isRealData() << " and run = " << event.id().run();

  if (histos)
    h_sums->Fill(n_sums);

  if (prints)
    printf("MFVWeight: r,l,e: %u, %u, %llu  ", event.id().run(), event.luminosityBlock(), event.id().event());

  std::unique_ptr<double> weight(new double(1.));
  std::unique_ptr<double> weight_up(new double(1.));
  std::unique_ptr<double> weight_down(new double(1.));

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
          if (mevent->gen_weight < 0) {
            *weight *= -1;
	    *weight_up *= -1;
            *weight_down *= -1;
	  }
        }
        else {
          *weight *= mevent->gen_weight;
	  *weight_up *= mevent->gen_weight;
          *weight_down *= mevent->gen_weight;
	}
      }

      double PUsf = 1.0;
      double PUsf_up = 1.0;
      double PUsf_down = 1.0;
      //pulling from json
      if (weight_pileup) {

        //double PUsf = 1.0;
        //double PUsf_up = 1.0; 
        //double PUsf_down = 1.0;
        std::map<std::string, correction::Variable::Type> values {
          {"NumTrueInteractions", mevent->npu}, 
          {"weights", "nominal"}, 
        };

        std::map<std::string, correction::Variable::Type> values_up {
          {"NumTrueInteractions", mevent->npu}, 
          {"weights", "up"}, // variation
        };

        std::map<std::string, correction::Variable::Type> values_down {
          {"NumTrueInteractions", mevent->npu}, 
          {"weights", "down"}, // variation
        };
        // //PU UL SF from Central 
        int year = int(MFVNEUTRALINO_YEAR);

        if (year == 20161 || year == 20162) { 
          PUsf = run(pu_cset, "Collisions16_UltraLegacy_goldenJSON", values);
          PUsf_up = run(pu_cset, "Collisions16_UltraLegacy_goldenJSON", values_up);
          PUsf_down = run(pu_cset, "Collisions16_UltraLegacy_goldenJSON", values_down);
        }
        else if (year == 2017) { 
          PUsf = run(pu_cset, "Collisions17_UltraLegacy_goldenJSON", values);
          PUsf_up = run(pu_cset, "Collisions17_UltraLegacy_goldenJSON", values_up);
          PUsf_down = run(pu_cset, "Collisions17_UltraLegacy_goldenJSON", values_down);

        }
        else if (year == 2018) { 
          PUsf = run(pu_cset, "Collisions18_UltraLegacy_goldenJSON", values);
          PUsf_up = run(pu_cset, "Collisions18_UltraLegacy_goldenJSON", values_up);
          PUsf_down = run(pu_cset, "Collisions18_UltraLegacy_goldenJSON", values_down);

        }

        if (histos) {
          h_npu->Fill(mevent->npu);
          h_sums->Fill(sum_pileup_weight, PUsf);
        }
        *weight *= PUsf;
        *weight_up *= PUsf_up;
        *weight_down *= PUsf_down;
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
	*weight_up *= npv_w;
        *weight_down *= npv_w;
	
      }

      for (int mwi : misc_weight_indices) {
        const double w = mevent->misc[mwi];
        if (prints)
          printf("misc weight %i: %g  ", mwi, w);
        *weight *= w;
	*weight_up *= w;
        *weight_down *= w;
      }
      //std::cout << "Before Lepton SFs" << std::endl;
      //Lepton SF workspace
      if (apply_lepsf) {
	double total_lepsf = 1;
        double total_lepIDsf = 1; //for histos; in case there are > 1 SV with a leading lepton
        double lepIDsf = 1;
        double lepRECOsf = 1;
        double total_lepRECOsf = 1; //for histos; in case there are > 1 SV with a leading lepton
        double lepISOsf = 1;
        double total_lepISOsf = 1; //for histos; in case there are > 1 SV with a leading lepton
        double lepTRsf = 1;
        double total_lepTRsf = 1; //for histos; in case there are > 1 SV with a leading lepton

        double total_lepsf_down = 1;
        double lepIDsf_down = 1;
        double lepRECOsf_down = 1;
        double lepISOsf_down = 1;
	double lepTRsf_down = 1;

        double total_lepsf_up = 1;
        double lepIDsf_up = 1;
        double lepRECOsf_up = 1;
        double lepISOsf_up = 1;
        double lepTRsf_up = 1;

	double lepSF_nominal = 1;
	double lepSF_syst = 0;
	double lepSF_stat =0;
	double lepSF = 1;
	double lepSF_up = 1;
	double lepSF_down = 1;
	//step 1 : get the leading selected lepton (the one that passes all selections; hltmatched, ID, iso, pT, eta)
	float leading_muonpt = -1;
	float leading_muoneta = -1;
	for (int jmu = 0; jmu < mevent->nmuons(); ++jmu) {
	  if (mevent->muon_pt[jmu] > leading_muonpt) {
	    leading_muonpt = mevent->muon_pt[jmu];
	    //leading_muonid = jmu;
	    leading_muoneta = mevent->muon_eta[jmu];
	  }
	}
	float leading_electronpt = -1;
        float leading_electroneta = -1;
        for (int jele = 0; jele < mevent->nelectrons(); ++jele) {
          if (mevent->electron_pt[jele] > leading_electronpt) {
	    leading_electronpt = mevent->electron_pt[jele];
            //leading_electronid = jele;
            leading_electroneta = mevent->electron_eta[jele];
          }
        }
	//float leading_leppt = *max_element(assoc_selleppt.begin(), assoc_selleppt.end());
	//int leading_lepidx = std::max_element(assoc_selleppt.begin(), assoc_selleppt.end()) - assoc_selleppt.begin();
	float leading_leppt;
	float leading_lepeta;
	//int leading_lepid;
	int leading_leptype; //0 == mu, 1 == ele

	int year_int = int(MFVNEUTRALINO_YEAR);
	if (year_int == 2017) {
	  if (leading_muonpt > 30.) {
	    leading_leppt = leading_muonpt;
	    leading_lepeta = leading_muoneta;
	    leading_leptype = 0;
	  }
	  else { //no pt cut for electron here since otherwise the event would not have passed the trigger, will not work for dilepton trigger or similar
	    leading_leppt = leading_electronpt;
	    leading_lepeta = leading_electroneta;
	    leading_leptype = 1;
	  }
	}
	else {
	  if (leading_muonpt > 27.) {
            leading_leppt = leading_muonpt;
            leading_lepeta = leading_muoneta;
            leading_leptype = 0;
          }
          else { //no pt cut for electron here since otherwise the event would not have passed the trigger, will not work for dilepton trigger or similar
            leading_leppt = leading_electronpt;
            leading_lepeta = leading_electroneta;
            leading_leptype = 1;
          }
	}
	//std::cout << "Before get SF depending on the lepton" << std::endl;
	//step 2 : depending on the lepton, get the SFs 
	if (leading_leptype == 0) { //leading_leptype is mu;
	  //std::cout << "After defining leading leptype == 0" << std::endl;
	  
	  std::map<std::string, correction::Variable::Type> values {
	    {"pt", leading_leppt}, // muon transverse momentum
	    {"eta", leading_lepeta}, // muon absolute pseudorapidity
	    {"scale_factors", "nominal"}, // variation
	  };
	  //std::cout << "After setting value map for leading lep" << std::endl;
	  std::map<std::string, correction::Variable::Type> values_up {
            {"pt", leading_leppt}, // muon transverse momentum
            {"eta", leading_lepeta}, // muon absolute pseudorapidity
            {"scale_factors", "systup"}, // variation
	  };

	  std::map<std::string, correction::Variable::Type> values_down {
	    {"pt", leading_leppt}, // muon transverse momentum
	    {"eta", leading_lepeta}, // muon absolute pseudorapidity
	    {"scale_factors", "systdown"}, // variation
	  };
	  //std::cout << "Before TrackerMuon Reconstruction" << std::endl;
	  // TrackerMuon Reconstruction UL scale factor
	  if ( leading_leppt > 40.0) {  //lower limit is 40 for RECO SF? 
	    lepRECOsf = run(mu_cset, "NUM_TrackerMuons_DEN_genTracks", values);
	    lepRECOsf_up = run(mu_cset, "NUM_TrackerMuons_DEN_genTracks", values_up);
	    lepRECOsf_down = run(mu_cset, "NUM_TrackerMuons_DEN_genTracks", values_down);  
	  }

	  // Medium ID UL scale factor, down/up variations
	  if (leading_leppt > 15.0) {  //lower limit is 15 GeV for ID SF, ISO SF
	    lepIDsf = run(mu_cset, "NUM_MediumID_DEN_TrackerMuons", values);
	    lepIDsf_up = run(mu_cset, "NUM_MediumID_DEN_TrackerMuons", values_up);
	    lepIDsf_down = run(mu_cset, "NUM_MediumID_DEN_TrackerMuons", values_down);
	    
	    //ISO UL scale factor 
	    lepISOsf = run(mu_cset, "NUM_TightRelIso_DEN_MediumID", values);
	    lepISOsf_up = run(mu_cset, "NUM_TightRelIso_DEN_MediumID", values_up);
	    lepISOsf_down = run(mu_cset, "NUM_TightRelIso_DEN_MediumID", values_down);	    
	  }

	  //Yuqing's Lepton Scale Factors (muons)
	  float leading_leppt_fix;
	  if (leading_leppt > 199) {
	    leading_leppt_fix = 199;
	  }
	  else {
	    leading_leppt_fix = leading_leppt;
	  }
	  std::map<std::string, correction::Variable::Type> trigvalues {
	    //{"year", year}, //year
	    {"scale_factors", "nominal"}, // variation
	    {"pt", leading_leppt_fix}, // electron transverse momentum
	    {"eta", leading_lepeta}, // electron absolute pseudorapidity
	  };
	  std::map<std::string, correction::Variable::Type> trigvalues_syst {
	    //{"year", year}, //year
	    {"scale_factors", "syst"}, // variation
	    {"pt", leading_leppt_fix}, // electron transverse momentum
	    {"eta", leading_lepeta}, // electron absolute pseudorapidity
	  };
	  std::map<std::string, correction::Variable::Type> trigvalues_stat {
	    //{"year", year}, //year
	    {"scale_factors", "stat"}, // variation
	    {"pt", leading_leppt_fix}, // electron transverse momentum
	    {"eta", leading_lepeta}, // electron absolute pseudorapidity
	  };

	  //std::cout << "After Yuqing muon SF map" << std::endl;
	  int year = int(MFVNEUTRALINO_YEAR);
	  if (year == 2017) {
	    //std::cout << "Before calling from Yuqing Muon jsons with: " << std::endl;
	    //std::cout << leading_leppt << std::endl;
	    lepSF_nominal = run(muSF_cset, "NUM_IsoMu27_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues);
	    //std::cout << "After calling nominal from Yuqing Muon jsons" << std::endl;
            lepSF_syst = run(muSF_cset, "NUM_IsoMu27_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues_syst);
            lepSF_stat = run(muSF_cset, "NUM_IsoMu27_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues_stat);
	    lepSF = lepSF_nominal;
	    lepSF_up = lepSF_nominal + lepSF_syst + lepSF_stat;
	    lepSF_down = lepSF_nominal - lepSF_syst - lepSF_syst;
	  }
	  else if (year == 2018) {
	    lepSF_nominal = run(muSF_cset, "NUM_IsoMu24_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues);
	    lepSF_syst = run(muSF_cset, "NUM_IsoMu24_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues_syst);
	    lepSF_stat = run(muSF_cset, "NUM_IsoMu24_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues_stat);
	    lepSF = lepSF_nominal;
            lepSF_up = lepSF_nominal + lepSF_syst + lepSF_stat;
            lepSF_down = lepSF_nominal - lepSF_syst - lepSF_syst;
	  }
	  else {
	    lepSF_nominal = run(muSF_cset, "NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues);
            lepSF_syst = run(muSF_cset, "NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues_syst);
            lepSF_stat = run(muSF_cset, "NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdMedium_and_PFIsoMedium", trigvalues_stat);
	    lepSF = lepSF_nominal;
            lepSF_up = lepSF_nominal + lepSF_syst + lepSF_stat;
            lepSF_down = lepSF_nominal - lepSF_syst - lepSF_syst;
	  }
	  
	  // // Trigger UL systematic uncertainty only
	  // if (lepinSV_pt[ilep] > 26.0) { //lower limit is 26GeV for Trigger SF 
	  //   lepTRsf = run(mu_cset, "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight", values);
	  //   lepTRsf_up = run(mu_cset, "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight", values_up);
	  //   lepTRsf_down = run(mu_cset, "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight", values_down);
	  // } 
            
	  //placeholder trigger SF : 0.99 +- 0.05 (for leptons passing the minimum pT requirements); 
	  // also, just apply it to one lepton per event; not per SV 
	  //if (ilep < 1) { 
	  lepTRsf = 0.99;
	  lepTRsf_up = 0.995;
	  lepTRsf_down = 0.985;
	  //}
	}
	else { //lepinSV is an electron
	  //std::cout << "After defining leading leptype == 1" << std::endl;
	  // int year = 2017;
    int y = int(MFVNEUTRALINO_YEAR);

    // for electron ID SF JSON (electron162UL.json.gz)
    std::string year_id;
    if (y == 20161) year_id = "2016preVFP";
    else if (y == 20162) year_id = "2016postVFP";
    else if (y == 2017)  year_id = "2017";
    else if (y == 2018)  year_id = "2018";
    else year_id = std::to_string(y);

  // for electron trigger SF JSON (electron_trigsf_runII.json)
  std::string year_trig = std::to_string(y);

	  std::map<std::string, correction::Variable::Type> values {
	    {"year", year_id}, //year
            {"ValType", "sf"}, // variation
	    {"WorkingPoint",  "Tight"}, //working point
	    {"pt", leading_leppt}, // electron transverse momentum
	    {"eta", leading_lepeta}, // electron absolute pseudorapidity
	  };
	  //std::cout << "After setting values map" << std::endl;
	  std::map<std::string, correction::Variable::Type> values_up {
	    {"year", year_id}, //year
            {"ValType", "sfup"}, // variation
	    {"WorkingPoint",  "Tight"}, //working point
	    {"pt", leading_leppt}, // electron transverse momentum
	    {"eta", leading_lepeta}, // electron absolute pseudorapidity
	  };
	  std::map<std::string, correction::Variable::Type> values_down {
	    {"year", year_id}, //year
            {"ValType", "sfdown"}, // variation
	    {"WorkingPoint",  "Tight"}, //working point
	    {"pt", leading_leppt}, // electron transverse momentum
	    {"eta", leading_lepeta}, // electron absolute pseudorapidity
	  };
	  //std::cout << "Before calling e ID SFs" << std::endl;
	  if (leading_leppt > 10.0) { 
	    lepRECOsf = run(ele_cset, "UL-Electron-ID-SF", values);
	    lepRECOsf_up = run(ele_cset, "UL-Electron-ID-SF", values_up);
	    lepRECOsf_down = run(ele_cset, "UL-Electron-ID-SF", values_down);
  
	  }
	  //std::cout << "After calling e ID SFs" << std::endl;
	  //placeholder trigger SF : 0.99 +- 0.05 (for leptons passing the minimum pT requirements)
	  // also, just apply it to one lepton per event; not per SV 
	  //if (ilep < 1) { 
	  lepTRsf = 0.99;
	  lepTRsf_up = 0.995;
	  lepTRsf_down = 0.985;
	  //}

	  //Yuqing's Lepton Scale Factors (electron)     PROBLEM HERE!!!!!!!!!!
	  std::map<std::string, correction::Variable::Type> trigvalues {
            {"year", year_trig}, //year
            {"ValType", "nominal"}, // variation
            {"pt", leading_leppt}, // electron transverse momentum
            {"eta", leading_lepeta}, // electron absolute pseudorapidity
          };
          std::map<std::string, correction::Variable::Type> trigvalues_up {
            {"year", year_trig}, //year
            {"ValType", "systup"}, // variation
            {"pt", leading_leppt}, // electron transverse momentum
            {"eta", leading_lepeta}, // electron absolute pseudorapidity
          };
          std::map<std::string, correction::Variable::Type> trigvalues_down {
            {"year", year_trig}, //year
            {"ValType", "systdown"}, // variation
            {"pt", leading_leppt}, // electron transverse momentum
            {"eta", leading_lepeta}, // electron absolute pseudorapidity
          };
	  lepSF = run(eleSF_cset, "scale_factor", trigvalues);
	  lepSF_up = run(eleSF_cset, "scale_factor", trigvalues_up);
	  lepSF_down = run(eleSF_cset, "scale_factor", trigvalues_down);
	  //std::cout << "After calling Yuqing's lepton SFs" << std::endl;
	}
	total_lepsf *= lepRECOsf*lepISOsf*lepIDsf*lepTRsf*lepSF;
	//std::cout << "lep ID sf: " << lepIDsf << ", total_lepsf: " << total_lepsf << ", leading lep pt: " << leading_leppt << ", leading lep eta: " << leading_lepeta << ", pileup sf: " << PUsf << ", number of pileup events: " << mevent->npu << std::endl;
	total_lepsf_up *= lepRECOsf_up*lepISOsf_up*lepIDsf_up*lepTRsf_up*lepSF_up;
	total_lepsf_down *= lepRECOsf_down*lepISOsf_down*lepIDsf_down*lepTRsf_down*lepSF_down;

	//to be used in histos primarily 
	total_lepRECOsf *= lepRECOsf;
	total_lepISOsf *= lepISOsf;
	total_lepIDsf *= lepIDsf;
	total_lepTRsf *= lepTRsf;

	if (histos) {
	  h_lepsums->Fill(sum_leprecoSF, total_lepRECOsf);
	  h_lepsums->Fill(sum_lepidSF, total_lepIDsf);
	  h_lepsums->Fill(sum_lepisoSF, total_lepISOsf);
	  h_lepsums->Fill(sum_leptriggerSF, total_lepTRsf);
	  h_lepsums->Fill(sum_leptotalSF, total_lepsf);
	}
	
	*weight *= total_lepsf;
	*weight_up *= total_lepsf_up;
	*weight_down *= total_lepsf_down;
      } //end if (leading_leptype == 0)

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
    //std::cout << "Before roccor SFs" << std::endl;
    //rochester corrections have a correction to apply to data/mc so putting it here
    if (apply_roccor) {
      double roccor_sf = 1.0; //total for the event
      //these sf are applied to every muon
      if (event.isRealData()) {
        for (int imu = 0; imu < mevent->nmuons(); ++imu) {
          if (mevent->muon_pt[imu] < 10.) continue;
          double dtSF = rc.kScaleDT(mevent->muon_q[imu], mevent->muon_pt[imu], mevent->muon_eta[imu], mevent->muon_phi[imu], 0, 0); //data
          roccor_sf *= dtSF;
        }
      }
      else if (!event.isRealData()) { 
        // nl is trackerlayersWithMeasurement 
        // u is random number distributed uniformly between 0 and 1 ( gRandom->Rndm() ); 
        //double u = gRandom->Rndm();
	double u = gRandom->Rndm(event.id().event());

        for (int imu = 0; imu < mevent->nmuons(); ++imu) {
          if (mevent->muon_pt[imu] < 10.) continue;

          // get gen muon if available
          bool genmatch = false;
          float genmatch_pt = -1.0; 
          double best_dR = 9.0;
          std::vector<double> mindR;
          std::vector<double> genpT;
          for (auto genmu : mevent->gen_muons) {
            double dR = reco::deltaR(mevent->muon_eta[imu], mevent->muon_phi[imu], genmu.Eta(), genmu.Phi());
            mindR.push_back(dR);
            genpT.push_back(genmu.Pt());
	    //std::cout << "genmu works" << std::endl;
          }
          if (mindR.size() !=0) { 
            best_dR = *min_element(mindR.begin(), mindR.end());
            int best_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
            genmatch_pt = genpT[best_idx];
          }
          if (best_dR < 0.1) genmatch = true;
          if (genmatch) {
            double mcSF = rc.kSpreadMC(mevent->muon_q[imu], mevent->muon_pt[imu], mevent->muon_eta[imu], mevent->muon_phi[imu], genmatch_pt, 0, 0); //(recommended), MC scale and resolution correction when matched gen muon is available
            roccor_sf *= mcSF;
          }
          else if (!genmatch){
            double mcSF = rc.kSmearMC(mevent->muon_q[imu], mevent->muon_pt[imu], mevent->muon_eta[imu], mevent->muon_phi[imu], mevent->muon_nlayers(imu), u, 0, 0); //MC scale and extra smearing when matched gen muon is not available
            roccor_sf *= mcSF;
          }
        }
      }
      //std::cout << "roccor scale factor: " << roccor_sf << std::endl;
      *weight *= roccor_sf; 
    }
    
  }

  if (histos) {
    h_sums->Fill(sum_weight, *weight);
    h_lepsums->Fill(lsum_weight, *weight);
  }

  if (prints)
    printf("total weight: %g\n", *weight);

  
  event.put(std::move(weight));
  event.put(std::move(weight_up), "lepsfup"); //specific for leptoninSV
  event.put(std::move(weight_down), "lepsfdown"); //specific for leptoninSV

}

DEFINE_FWK_MODULE(MFVWeightProducer);
