#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/Tools/interface/Geometry.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

class MFVCutFlowHistos : public edm::EDAnalyzer {
 public:
  explicit MFVCutFlowHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
   
 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_aux_token;
  const edm::EDGetTokenT<double> weight_token;

  bool jet_hlt_match(edm::Handle<MFVEvent> mevent, int i, float min_jet_pt=20.) const {
    // an offline jet with a successful HLT match will have a nonzero jet_hlt_pt;
    // all others have the default value of 0
    return mevent->jet_hlt_pt.at(i) > min_jet_pt;
  }

  // enum { pass_trigger, pass_jetsel, pass_ID, pass_pt, pass_eta, pass_iso, pass_displept_50um, pass_dispsellept_50um };
  // TH1D* h_event_cutflow;
  TH1F* h_w;

  TH1F* h_nsv;

  // enum { any_sv, bs2derr_60, bs2derr_50, bs2derr_45, bs2derr_40, bs2derr_35, bs2derr_30, bs2derr_25 };
  // TH1D* h_bs2derr_cutflow;
    
  enum { any_electron, full5x5sigmaIetaIeta, delta_eta_seed, delta_phi, HoverE, ooEmooP, expected_missing_inner_hits, pass_conversion_veto };
  TH1D* h_tight_ele_cutflow;

  enum { isMedMuon, muiso_vl, muiso_l, muiso_med, muiso_tight, muiso_vt };
  TH1D* h_muiso_cutflow;

  enum { isTightEl, eliso_vl, eliso_l, eliso_med, eliso_tight, eliso_vt };
  TH1D* h_eleiso_cutflow;

  // enum { Apass_trigger, Apass_jetsel, Apass_lepsel, Apass_displept_50um, Ansv_goe_1, Aexclude_beampipe, Amintks_4, Amin_bs2ddist, Amax_rescale_bs2derr };
  // TH1D* h_selA_cutflow;

  // enum { Bpass_trigger, Bpass_jetsel, Bpass_lepsel, Bpass_dispsellept_50um, Bnsv_goe_1, Bexclude_beampipe, Bmintks_4, Bmin_bs2ddist, Bmax_rescale_bs2derr };
  // TH1D* h_selB_cutflow;

  //lepton cutflows
  enum {l_pass_trig, pass_leppt, pass_lepID, pass_lepeta, pass_lepiso};
  TH1D* h_lepton_cutflow;

  enum {dil_pass_trig, pass_dileppt, pass_dilepID, pass_dilepeta, pass_dilepiso};
  TH1D* h_dilepton_cutflow;
  
  enum {e_pass_trig, pass_ept, pass_eID, pass_eeta, pass_eiso};
  TH1D* h_electron_cutflow;

  enum {m_pass_trig, pass_mpt, pass_mID, pass_meta, pass_miso};
  TH1D* h_muon_cutflow;

  enum {pass_alltrig, pass_muONLY, pass_elONLY, pass_dilepONLY, pass_singlelepONLY, pass_eldilep, pass_mudilep};
  TH1D* h_trig_cutflow;
  
  enum {pass_allsel, pass_mufullsel, pass_elfullsel, pass_dilepfullsel, pass_singlelepfullsel, pass_eldilepfullsel, pass_mudilepfullsel};
  TH1D* h_fullsel_cutflow;

  enum {pass_mumut, pass_muelt, pass_eet, pass_mumuANDmuelt, pass_mumuANDeet, pass_muelANDeet, pass_alldilept};
  TH1D* h_dileptrig_cutflow;

  enum {pass_mumu_sel, pass_muel_sel, pass_ee_sel, pass_mumuANDmuel_sel, pass_mumuANDee_sel, pass_muelANDee_sel, pass_alldilep_sel};
  TH1D* h_dilep_sel_cutflow;

  enum {pass_el32t, pass_el115t, pass_el50t, pass_el32115t, pass_el3250t, pass_el11550t, pass_allelt};
  TH1D* h_eltrig_cutflow;

  enum {pass_el32sel, pass_el115sel, pass_el50sel, pass_el32115sel, pass_el3250sel, pass_el11550sel, pass_allel_sel};
  TH1D* h_el_sel_cutflow;
  
  enum {pass_mu24t, pass_mu50t, pass_allmut};
  TH1D* h_mutrig_cutflow;

  enum {pass_mu24sel, pass_mu50sel, pass_allmu_sel};
  TH1D* h_mu_sel_cutflow;

  //for vertex cutflow : first four are for atleast 1 vtx; second four are for atleast 2 vtx;
  // this should be filled AFTER full selection 
  enum {pass_presel, atleast_1vtx, pass_mintrack, pass_inbeampipe, pass_mindbv, pass_maxdbv_unc, atleast_2vtx, pass_2mintrack, pass_2inbeampipe, pass_2mindbv, pass_2maxdbv_unc};
  TH1D* h_vertex_cutflow;
};


MFVCutFlowHistos::MFVCutFlowHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    vertex_aux_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_aux_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src")))
{
  edm::Service<TFileService> fs;


  //make the histograms
  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices; arb.units", 15, 0, 15);

  // h_bs2derr_cutflow = fs->make<TH1D>("h_bs2derr_cuflow", ";events", 8, 0, 8);
  // int bsbin = 1;
  // for (const char* bs : {"any_vertex", "pass_bs2derr_60","pass_bs2derr_50", "pass_bs2derr_45", "pass_bs2derr_40", "pass_bs2derr_35", "pass_bs2derr_30", "pass_bs2derr_25"})
  //   h_tight_ele_cutflow->GetXaxis()->SetBinLabel(bsbin++, bs);
  
  
  // electron cutflow for criteria related to cutbased; filled after trigger is satisfied 
  h_tight_ele_cutflow = fs->make<TH1D>("h_tight_ele_cuflow", ";events", 8, 0, 8);
  int elbin = 1;
  for (const char* a : {"any_electron", "full5x5sigmaIetaIeta", "delta_eta_seed", "delta_phi", "HoverE", "ooEmooP", "expected_missing_inner_hits", "pass_conversion_veto"})
    h_tight_ele_cutflow->GetXaxis()->SetBinLabel(elbin++, a);

  // electron and muon cutflow to look at different isolation cuts 
  h_eleiso_cutflow = fs->make<TH1D>("h_eleiso_cutflow", ";events", 6, 0, 6);
  int elibin = 1;
  for (const char* b : {"isTightEl", "eliso_vl","eliso_l", "eliso_med", "eliso_tight", "eliso_vt"})
    h_eleiso_cutflow->GetXaxis()->SetBinLabel(elibin++, b);
  
  h_muiso_cutflow = fs->make<TH1D>("h_muiso_cutflow", ";events", 6, 0, 6);
  int mubin = 1;
  for (const char* c : {"isMedMuon", "muiso_vl","muiso_l", "muiso_med", "muiso_tight", "muiso_vt"})
    h_muiso_cutflow->GetXaxis()->SetBinLabel(mubin++, c);

  // different full selection cutflows : 1 with displaced lepton cut, the other with a displaced selected lepton 
  // h_selA_cutflow = fs->make<TH1D>("h_selA_cutflow", ";events", 9, 0, 9);
  // int sbin = 1;
  // for (const char* d : {"pass_trigger", "pass_jetsel", "pass_lepsel", "pass_displept_50um", "nsv_goe_1", "exclude_beampipe", "mintks_4", "min_bs2ddist", "max_rescale_bs2derr"})
  //   h_selA_cutflow->GetXaxis()->SetBinLabel(sbin++, d);

  // h_selB_cutflow = fs->make<TH1D>("h_selB_cutflow", ";events", 9, 0, 9);
  // int tbin = 1;
  // for (const char* f : {"pass_trigger", "pass_jetsel", "pass_lepsel", "pass_dispsellept_50um", "nsv_goe_1", "exclude_beampipe", "mintks_4", "min_bs2ddist", "max_rescale_bs2derr"})
  //   h_selB_cutflow->GetXaxis()->SetBinLabel(tbin++, f);

  // h_event_cutflow = fs->make<TH1D>("h_event_cutflow", ";events", 8, 0, 8);
  // int vbin = 1;
  // for (const char* v : {"pass_trigger", "pass_jetsel", "pass_ID", "pass_pt", "pass_eta", "pass_iso", "pass_displept_50um", "pass_dispsellept_50um" })
  //   h_event_cutflow->GetXaxis()->SetBinLabel(vbin++, v);

  h_lepton_cutflow = fs->make<TH1D>("h_lepton_cutflow", ";events", 5, 0, 5);
  int lepbin = 1;
  for (const char* d : {"pass_trigger", "pass_pt", "pass_ID", "pass_eta",  "pass_iso"})
    h_lepton_cutflow->GetXaxis()->SetBinLabel(lepbin++, d);

  h_dilepton_cutflow = fs->make<TH1D>("h_dilepton_cutflow", ";events", 5, 0, 5);
  int dilepbin = 1;
  for (const char* h : {"pass_trigger", "pass_pt", "pass_ID", "pass_eta", "pass_iso"})
    h_dilepton_cutflow->GetXaxis()->SetBinLabel(dilepbin++, h);
  
  h_electron_cutflow = fs->make<TH1D>("h_electron_cutflow", ";events", 5, 0, 5);
  int ebin = 1;
  for (const char* f : {"pass_trigger", "pass_pt", "pass_ID","pass_eta", "pass_iso"})
    h_electron_cutflow->GetXaxis()->SetBinLabel(ebin++, f);

  h_muon_cutflow = fs->make<TH1D>("h_muon_cutflow", ";events", 5, 0, 5);
  int mbin = 1;
  for (const char* g : {"pass_trigger",  "pass_pt", "pass_ID", "pass_eta", "pass_iso"})
    h_muon_cutflow->GetXaxis()->SetBinLabel(mbin++, g);

  h_trig_cutflow = fs->make<TH1D>("h_trig_cutflow", ";events", 7, 0, 7);
  int tbin = 1;
  for (const char* j : {"pass_alltrig", "pass_onlymu", "pass_onlyel", "pass_onlydilep", "pass_singlelep", "pass_elORdilep", "pass_muORdilep"})
    h_trig_cutflow->GetXaxis()->SetBinLabel(tbin++, j);

  h_fullsel_cutflow = fs->make<TH1D>("h_fullsel_cutflow", ";events", 7, 0, 7);
  int sbin = 1;
  for (const char* k : {"pass_allsel", "pass_only_musel", "pass_only_elsel", "pass_only_dilepsel", "pass_elORmusel", "pass_elORdilepsel", "pass_muORdilepsel"})
    h_fullsel_cutflow->GetXaxis()->SetBinLabel(sbin++, k);

  h_dileptrig_cutflow = fs->make<TH1D>("h_dileptrig_cutflow", ";events", 7, 0, 7);
  int lbin = 1;
  for (const char* l : {"pass_mumu", "pass_muel", "pass_ee", "pass_mumuANDmuel", "pass_mumuANDee", "pass_muelANDee", "pass_alldilep"})
    h_dileptrig_cutflow->GetXaxis()->SetBinLabel(lbin++, l);

  h_dilep_sel_cutflow = fs->make<TH1D>("h_dilepsel_cutflow", ";events", 7, 0, 7);
  int obin = 1;
  for (const char* o : {"pass_mumu_sel", "pass_muel_sel", "pass_ee_sel", "pass_mumuANDmuel_sel", "pass_mumuANDee_sel", "pass_muelANDee_sel", "pass_alldilep_sel"})
    h_dilep_sel_cutflow->GetXaxis()->SetBinLabel(obin++, o);
  
  h_vertex_cutflow = fs->make<TH1D>("h_vtx_sel_cutflow", ";events", 11, 0, 11);
  int nbin = 1;
  for (const char* n : {"pass_presel", "atleast_1vtx", "pass_min4trk", "pass_inbeampipe", "pass_mindbv", "pass_maxdbv_unc", "atleast_2vtx", "pass_2min4trk", "pass_2inbeampipe", "pass_2mindbv", "pass_2maxdbv_unc"})
    h_vertex_cutflow->GetXaxis()->SetBinLabel(nbin++, n);

  
  h_eltrig_cutflow = fs->make<TH1D>("h_eltrig_cutflow", ";events", 7, 0, 7);
  int pbin = 1;
  for (const char* p : {"pass_el32", "pass_el115", "pass_el50", "pass_el32ANDel115", "pass_el32AND50", "pass_el115AND50", "pass_allel"})
    h_eltrig_cutflow->GetXaxis()->SetBinLabel(pbin++, p);

  h_el_sel_cutflow = fs->make<TH1D>("h_el_sel_cutflow", ";events", 7, 0, 7);
  int qbin = 1;
  for (const char* q : {"pass_el32_sel", "pass_el115_sel", "pass_el50_sel", "pass_el32AND115_sel", "pass_el32AND50_sel", "pass_115AND50_sel", "pass_allel_sel"})
    h_el_sel_cutflow->GetXaxis()->SetBinLabel(qbin++, q);

  h_mutrig_cutflow = fs->make<TH1D>("h_mutrig_cutflow", ";events", 3, 0, 3);
  int rbin = 1;
  for (const char* r : {"pass_mu24", "pass_mu50", "pass_allmu"})
    h_mutrig_cutflow->GetXaxis()->SetBinLabel(rbin++, r);

  h_mu_sel_cutflow = fs->make<TH1D>("h_mu_sel_cutflow", ";events", 3, 0, 3);
  int wbin = 1;
  for (const char* w : {"pass_mu24_sel", "pass_mu50_sel", "pass_allmu_sel"})
    h_mu_sel_cutflow->GetXaxis()->SetBinLabel(wbin++, w);
}

void MFVCutFlowHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(vertex_aux_token, auxes);
  
  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);

  const int nsv = int(auxes->size());

  bool at_least_one_trigger_passed = false;
  // bool pass_trigger = false;
  //for ease; switch to array 0: ele32, 1: ele115, 2: ele50
  // mu 0: mu24, 1: mu50
  //but also keep original
  bool pass_etrig = false;
  bool pass_mtrig = false;
  std::vector<bool> pass_eltrig {false, false, false};
  std::vector<bool> pass_elsel {false, false, false};
  std::vector<bool> pass_mutrig {false, false};
  std::vector<bool> pass_musel {false, false};
  bool pass_ditrig = false;
  bool pass_mumutrig = false;
  bool pass_mueltrig = false;
  bool pass_eetrig = false;
  // bool  pass_el_goe = false;

  std::vector<bool> pass_el {false, false, false, false};
  // bool  pass_el_ID = false;
  // bool  pass_el_pt = false;
  // bool  pass_el_eta = false;
  // bool  pass_el_iso = false;

  // bool  pass_mu_goe = false;
  std::vector<bool> pass_mu {false, false, false, false};
  // bool  pass_mu_ID = false;
  // bool  pass_mu_pt = false;
  // bool  pass_mu_eta = false;
  // bool  pass_mu_iso = false ;

  std::vector<bool> pass_2el {false, false, false, false};
  // bool pass_2el_pt = false;
  // bool pass_2el_ID = false;
  // bool pass_2el_eta = false;
  // bool pass_2el_iso = false;

  std::vector<bool> pass_2mu {false, false, false, false};
  // bool pass_2mu_pt = false;
  // bool pass_2mu_ID = false;
  // bool pass_2mu_eta = false;
  // bool pass_2mu_iso = false;

  std::vector<bool> pass_muel {false, false, false, false};
  // bool pass_muel_pt = false;
  // bool pass_muel_ID = false;
  // bool pass_muel_eta = false;
  // bool pass_muel_iso = false;
  
  // bool mevent_pass_displep = false;
  // bool mevent_pass_dispsellep = false;

  bool nsv_goe1 = false;
  bool nsv_goe2 = false;
  std::vector<bool> pass_mintks {false, false};
  std::vector<bool> pass_inbp {false, false};
  std::vector<bool> pass_dbv {false, false};
  std::vector<bool> pass_bs2derr {false, false};
  //the first one corresponds to a vertex that passes all other selections
  // std::vector<int> new_pass_bs2derr {0, 0, 0, 0, 0, 0, 0, 0};
  

  // switching to complete matching with trigger :
  for(size_t trig : mfv::LeptonOrDisplacedLeptonTriggers) {
    
    if(!mevent->pass_hlt(trig)) continue;

    int nmuons = mevent->nmuons();
    int nelectrons= mevent->nelectrons();
    int njets = mevent->njets(20);
    
    switch(trig){
    case mfv::b_HLT_Ele32_WPTight_Gsf :
    {
      pass_eltrig[0] = true;
      pass_etrig = true;
      for(int ie =0; ie < nelectrons; ++ie){
	if (mevent->electron_pt[ie] < 35) continue;
	pass_el[0]= true;
	if (mevent->electron_ID[ie][3] == 1) {
	  pass_el[1] = true;
	 if (abs(mevent->electron_eta[ie]) < 2.4) {
	   pass_el[2] = true;
	   if (mevent->electron_iso[ie] < 0.10) {
	     pass_el[3] = true;
	     pass_elsel[0] = true;
	   }
	 }
	}
      }
      // return pass_el;
    }
  case mfv::b_HLT_IsoMu24 :
    {
      pass_mutrig[0] = true;
      pass_mtrig = true;
      for(int im =0; im < nmuons; ++im) {
	if (mevent->muon_pt[im] < 26) continue;
	pass_mu[0] = true;
	if (mevent->muon_ID[im][1] == 1) {
	  pass_mu[1] = true;
	  if (abs(mevent->muon_eta[im]) < 2.4) {
	    pass_mu[2] = true;
	    if (mevent->muon_iso[im] < 0.15) {
	      pass_mu[3] = true;
	      pass_musel[0] = true;
	    }
	  }
	}
      }
      // return pass_mu;
    }
  case mfv::b_HLT_Mu50 :
    {
      pass_mutrig[1] = true;
      pass_mtrig = true;
      for(int im=0; im < nmuons; ++im) {
	if (mevent->muon_pt[im] < 53) continue;
	pass_mu[0] = true;
	if (mevent->muon_ID[im][1] == 1) {
	  pass_mu[1] = true;
	  if (abs(mevent->muon_eta[im]) < 2.4) {
	    pass_mu[2] = true;
	    if (mevent->muon_iso[im] < 0.15) {
	      pass_mu[3] = true;
	      pass_musel[1] = true;
	    }
	  }
	}
      }
      // return pass_mu;
    }
  case mfv::b_HLT_Ele115_CaloIdVT_GsfTrkIdT :
    {
      pass_eltrig[1] = true;
      pass_etrig = true;
      for(int ie =0; ie < nelectrons; ++ie){
	if (mevent->electron_pt[ie] < 120) continue;
	pass_el[0] = true;
	if (mevent->electron_ID[ie][3] == 1) {
	  pass_el[1] = true;
	  if (abs(mevent->electron_eta[ie]) < 2.4) {
	    pass_el[2] = true;
	    if (mevent->electron_iso[ie] < 0.10) {
	      pass_el[3] = true;
	      pass_elsel[1] = true;
	    }
	  }
	}
      }
      //  return pass_el;
    }
  case mfv::b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165 :
    {
      pass_eltrig[2] = true;
      pass_etrig = true;
      for(int ie =0; ie < nelectrons; ++ie){
	if (mevent->electron_pt[ie] < 55) continue;
	for(int j0=0; j0 < njets; ++j0){
	  if (!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 170) continue;
	  pass_el[0] = true;
	  if (mevent->electron_ID[ie][3] == 1) {
	    pass_el[1] = true;
	    if (abs(mevent->electron_eta[ie]) < 2.4) {
	      pass_el[2] = true;
	      if (mevent->electron_iso[ie] < 0.10) {
		pass_el[3] = true;
		pass_elsel[2] = true;
	      }
	    }
	  }
	}
      }
      //  return pass_el;
    }
  case mfv::b_HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL :
    {
      pass_ditrig = true;
      pass_mueltrig = true;
      for(int ie =0; ie < nelectrons; ++ie){
	for(int im =0; im < nmuons; ++im) {
	  if (mevent->electron_pt[ie] < 45) continue;
	  if (mevent->muon_pt[im] < 45) continue;
	  pass_muel[0] = true;

	  if (mevent->electron_ID[ie][3] == 1) {
	    if (mevent->muon_ID[im][1] == 1) {
	      pass_muel[1] = true;
	  
	      if (abs(mevent->electron_eta[ie]) < 2.4) {
		if (abs(mevent->muon_eta[im]) < 2.4) {
		  pass_muel[2] = true;
	      
		  if (mevent->electron_iso[ie] < 0.10) {
		    if (mevent->muon_iso[im] < 0.15) {
		      pass_muel[3] = true; 
		    }
		  }
		}
	      }
	    }
	  }
	}
      }
      // return pass_muel;
    }
  case mfv::b_HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90 :
    {
      pass_ditrig = true;
      pass_eetrig = true;
      int pass_pt = 0;
      int pass_eta = 0;
      int pass_ID = 0;
      int pass_iso = 0;
      for(int ie=0; ie < nelectrons; ++ie){
	if (mevent->electron_pt[ie] < 75) continue;
	pass_pt +=1;
	if (mevent->electron_ID[ie][3] == 1) {
	  pass_ID +=1;
	  if (abs(mevent->electron_eta[ie]) < 2.4) {
	    pass_eta +=1;
	    if (mevent->electron_iso[ie] < 0.10) {
	      pass_iso +=1;
	    }
	  }
	}
      }
      if (pass_pt > 1) pass_2el[0] = true;
      if (pass_eta > 1) pass_2el[1] = true;
      if (pass_ID > 1) pass_2el[2] = true;
      if (pass_iso > 1) pass_2el[3] = true;
      // return pass_2el;
    }
  case mfv::b_HLT_DoublePhoton70 :
    {
      pass_ditrig = true;
      pass_eetrig = true;
      int pass_pt = 0;
      int pass_eta = 0;
      int pass_ID = 0;
      int pass_iso = 0;
      for(int ie=0; ie < nelectrons; ++ie){
	if (mevent->electron_pt[ie] < 75) continue;
	pass_pt +=1;
	if (mevent->electron_ID[ie][3] == 1) {
	  pass_ID +=1;
	  if (abs(mevent->electron_eta[ie]) < 2.4) {
	    pass_eta +=1;
	    if (mevent->electron_iso[ie] < 0.10) {
	      pass_iso +=1;
	    }
	  }
	}
      }
      if (pass_pt > 1) pass_2el[0] = true;
      if (pass_eta > 1) pass_2el[1] = true;
      if (pass_ID > 1) pass_2el[2] = true;
      if (pass_iso > 1) pass_2el[3] = true;
      // return pass_2el;
    }
  case mfv::b_HLT_DoubleMu43NoFiltersNoVtx :
    {
      pass_ditrig = true;
      pass_mumutrig = true;
      int pass_pt = 0;
      int pass_eta = 0;
      int pass_ID = 0;
      int pass_iso = 0;
      for(int im=0; im < nmuons; ++im){
	if (mevent->muon_pt[im] < 45) continue;
	pass_pt +=1;
	if (mevent->muon_ID[im][1] == 1) {
	  pass_ID +=1;
	  if (abs(mevent->muon_eta[im]) < 2.4) {
	    pass_eta +=1;
	    if (mevent->muon_iso[im] < 0.15) {
	      pass_iso +=1;
      	    }
	  }
	}
      }
      if (pass_pt > 1) pass_2mu[0] = true;
      if (pass_eta > 1) pass_2mu[1] = true;
      if (pass_ID > 1) pass_2mu[2] = true;
      if (pass_iso > 1) pass_2mu[3] = true;
      // return pass_2mu;
    }
    default :
      {
	continue;
	//throw std::invalid_argument(std::string(mfv::hlt_paths[trig]) + " not implemented in satisfiesTrigger");
      }
    }
  }
    

  
  for(size_t trig : mfv::LeptonOrDisplacedLeptonTriggers) {
    if (mevent->pass_hlt(trig)) {
      at_least_one_trigger_passed = true;
      break;
    }
  }


  // separate if loop to determine if event pass lepton cuts & fill separate muon, electron cutflows
  if (at_least_one_trigger_passed) {
    
    if (mevent->nelectrons() > 0) {
      // pass_el_goe = true;
    
      for (int iel = 0; iel < mevent->nelectrons(); ++iel) {
      
      // // if (abs(mevent->electron_dxybs[iel]) >= 0.005)
      // // 	mevent_pass_displep = true;
      // 	if (mevent->electron_pt[iel] > 35) {
      // 	  pass_el_pt = true;
      // 	  if (abs(mevent->electron_eta[iel]) < 2.4) {
      // 	    pass_el_eta = true;
      // 	    if (mevent->electron_ID[iel][3]) {
      // 	      pass_el_ID = true;
      // 	      if (mevent->electron_iso[iel] < 0.10) {
      // 		pass_el_iso = true;
        
      // 	      // if (abs(mevent->electron_dxybs[iel]) >= 0.005)
      // 	      //   mevent_pass_dispsellep = true;
      // 	      }
      // 	    }
      // 	  }
      // 	}
      

      // cutflows
	if (mevent->electron_ID[iel][3] == 1) {
	  h_eleiso_cutflow->Fill(isTightEl, w);
	  if (mevent->electron_iso[iel] < 0.25 )
	    h_eleiso_cutflow->Fill(eliso_vl, w);
	  if (mevent->electron_iso[iel] < 0.20 )
	    h_eleiso_cutflow->Fill(eliso_l, 1);
	  if (mevent->electron_iso[iel] < 0.15 )
	    h_eleiso_cutflow->Fill(eliso_med, w);
	  if (mevent->electron_iso[iel] < 0.10 )
	    h_eleiso_cutflow->Fill(eliso_tight, w);
	  if (mevent->electron_iso[iel] < 0.05 )
	    h_eleiso_cutflow->Fill(eliso_vt, w);
	}
	
	bool isEB = mevent->electron_isEB[iel] == 1;
	bool isEE = mevent->electron_isEE[iel] == 1;
	if ( !isEB && !isEE ) break;
	
	h_tight_ele_cutflow->Fill(any_electron, 1);
	if ( mevent->electron_sigmaIetaIeta5x5[iel] < (isEB ? 0.0104 : 0.0353) ) {
	  h_tight_ele_cutflow->Fill(full5x5sigmaIetaIeta, w);
	  
	  if ( mevent->electron_dEtaAtVtx[iel] < (isEB ? 0.00255 : 0.00501) ) {
	    h_tight_ele_cutflow->Fill(delta_eta_seed, w);
	    
	    if ( mevent->electron_dPhiAtVtx[iel] < (isEB ? 0.022 : 0.0236) ) {
	      h_tight_ele_cutflow->Fill(delta_phi, w);
	      
	      if ( mevent->electron_HE[iel] == 1 ) {
		h_tight_ele_cutflow->Fill(HoverE, w);
		
		if ( mevent->electron_ooEmooP[iel] < (isEB ? 0.159 : 0.0197) ) {
		  h_tight_ele_cutflow->Fill(ooEmooP, w);
		  
		  if ( mevent->electron_expectedMissingInnerHits[iel] < 1 ) {
		    h_tight_ele_cutflow->Fill(expected_missing_inner_hits, 1);
		    if ( mevent->electron_passveto[iel] == 1) {
		      h_tight_ele_cutflow->Fill(pass_conversion_veto, w);
		    }
		  }
		}
	      }
	    }	  
	  }
	}	
      }
    }
    if (mevent->nmuons() > 0) {
      // pass_mu_goe = true;
      for (int imu = 0; imu < mevent->nmuons(); ++imu) {

      // if (abs(mevent->muon_dxybs[imu]) > 0.005) 
      //   mevent_pass_displep = true;
      
	// if (mevent->muon_pt[imu] > 26) {
	//   pass_mu_pt = true;
	//   if (abs(mevent->muon_eta[imu]) < 2.4) {
	//     pass_mu_eta = true;
	//     if (mevent->muon_ID[imu][1] == 1) {
	//       pass_mu_ID = true;
	//       if (mevent->muon_iso[imu] < 0.15) {
	//         pass_mu_iso = true;
	   
	//       // if (abs(mevent->muon_dxybs[imu]) > 0.005) 
	//       // 	mevent_pass_dispsellep = true;
	//       }
	//     }
	//   }
	// }    
      
	if (mevent->muon_ID[imu][1] == 1) {
	  h_muiso_cutflow->Fill(isMedMuon, w);
	  
	  if (mevent->muon_iso[imu] < 0.4 )
	    h_muiso_cutflow->Fill(muiso_vl, w);
	  if (mevent->muon_iso[imu] < 0.25 )
	    h_muiso_cutflow->Fill(muiso_l, w);
	  if (mevent->muon_iso[imu] < 0.20 )
	    h_muiso_cutflow->Fill(muiso_med, w);
	  if (mevent->muon_iso[imu] < 0.15 )
	    h_muiso_cutflow->Fill(muiso_tight, w);
	  if (mevent->muon_iso[imu] < 0.10 )
	    h_muiso_cutflow->Fill(muiso_vt, w);
	}
      }
    }
  }

  //separate section to determine if vertex passes cuts; this is done after full preselection
  if (pass_etrig || pass_mtrig || pass_ditrig) {
    if (pass_mu[3] || pass_el[3] || pass_2el[3] || pass_2mu[3] || pass_muel[3]) {
    
      if (nsv >= 1) nsv_goe1 = true;
      // this nsv_goe2 when applied in the loop will represent 1 vtx passing all selection & the presence of another vtx. 
      if (nsv > 1) nsv_goe2 = true;
      int n_selsv = 0;
      int iv_mintk = 0;
      int iv_inbp = 0;
      int iv_dbv = 0;
      int iv_dbverr = 0;
      // for (const MFVVertexAux& vtx : *auxes) {
      for (int isv = 0; isv < nsv; ++isv) {
	const MFVVertexAux& aux = auxes->at(isv);
	if (aux.ntracks() >= 4) {
	  iv_mintk +=1;
	  if (jmt::Geometry::inside_beampipe(true, aux.x, aux.y)) {
	    iv_inbp +=1;
	    if (aux.bs2ddist > 0.01) {
	      iv_dbv +=1;
	    //   new_pass_bs2derr[0] += 1;
	    //   if (aux.bs2derr < 0.0060)
	    // 	new_pass_bs2derr[1] +=1;
	    //   if (aux.bs2derr < 0.0050)
	    // 	new_pass_bs2derr[2] +=1;
	    //   if (aux.bs2derr < 0.0045)
	    // 	new_pass_bs2derr[3] +=1;
	    //   if (aux.bs2derr < 0.0040)
	    // 	new_pass_bs2derr[4] +=1;
	    //   if (aux.bs2derr < 0.0035)
	    // 	new_pass_bs2derr[5] +=1;
	    //   if (aux.bs2derr < 0.0030)
	    // 	new_pass_bs2derr[6] +=1;
	      
	      if (aux.bs2derr < 0.0050) {
		//	new_pass_bs2derr[7] +=1;
		iv_dbverr +=1;
		n_selsv +=1;
	      }
	    }
	  }
	}
      }
    
      if (iv_mintk >= 1) pass_mintks[0] = true;
      if (iv_mintk > 1) pass_mintks[1] = true;
      if (iv_inbp >= 1) pass_inbp[0] = true;
      if (iv_inbp > 1) pass_inbp[1] = true;
      if (iv_dbv >= 1) pass_dbv[0] = true;
      if (iv_dbv > 1) pass_dbv[1] = true;
      if (iv_dbverr >= 1) pass_bs2derr[0] = true;
      if (iv_dbverr > 1) pass_bs2derr[1] = true;
    
      h_nsv->Fill(n_selsv, w);
    }
  }
  

  // now to fill the event & sel cutflows 
  // if (at_least_one_trigger_passed) {

    // h_event_cutflow->Fill(pass_trigger, 1);
    // h_selA_cutflow->Fill(Apass_trigger, 1);
    // h_selB_cutflow->Fill(Bpass_trigger, 1);
    
    // if (mevent->njets(20) > 1) {
      
    //   h_event_cutflow->Fill(pass_jetsel, 1);
    //   h_selA_cutflow->Fill(Apass_jetsel, 1);
    //   h_selB_cutflow->Fill(Bpass_jetsel, 1);
      
  //     if (mevent_pass_ID) {
  // 	h_event_cutflow->Fill(pass_ID, 1);
  // 	if (mevent_pass_pt) {
  // 	  h_event_cutflow->Fill(pass_pt, 1);
  // 	  if (mevent_pass_eta) {
  // 	    h_event_cutflow->Fill(pass_eta, 1);
  // 	    if (mevent_pass_iso) {
  // 	      h_event_cutflow->Fill(pass_iso, 1);
  // 	      if (mevent_pass_displep) {
  // 		h_event_cutflow->Fill(pass_displept_50um, 1);
  // 		if (mevent_pass_dispsellep) {
  // 		  h_event_cutflow->Fill(pass_dispsellept_50um, 1);
  // 		}
  // 	      }
  // 	    }
  // 	  }
  // 	}
  //     }
      
  //     if (mevent_pass_lepsel) {
  // 	h_selA_cutflow->Fill(Apass_lepsel, 1);
  // 	h_selB_cutflow->Fill(Bpass_lepsel, 1);

  // 	if (mevent_pass_displep) {
  // 	  h_selA_cutflow->Fill(Apass_displept_50um, 1);
  // 	  if (at_least_one_vertex) {
  // 	    h_selA_cutflow->Fill(Ansv_goe_1, 1);
  // 	    if (vertex_in_beampipe) {
  // 	      h_selA_cutflow->Fill(Aexclude_beampipe, 1);
  // 	      if(vertex_has_min4tks) {
  // 		h_selA_cutflow->Fill(Amintks_4, 1);
   // 		if(vertex_pass_bs2ddist) {
  // 		  h_selA_cutflow->Fill(Amin_bs2ddist, 1);
  // 		  if(vertex_pass_bs2derr) {
  // 		    h_selA_cutflow->Fill(Amax_rescale_bs2derr, 1);
  // 		  }
  // 		}
  // 	      }
  // 	    }
  // 	  }
  // 	}
	 
  // 	if (mevent_pass_dispsellep) {
  // 	  h_selB_cutflow->Fill(Bpass_dispsellept_50um, 1);
  // 	  if (at_least_one_vertex) {
  // 	    h_selB_cutflow->Fill(Bnsv_goe_1, 1);
  // 	    if (vertex_in_beampipe) {
  // 	      h_selB_cutflow->Fill(Bexclude_beampipe, 1);
  // 	      if(vertex_has_min4tks) {
  // 		h_selB_cutflow->Fill(Bmintks_4, 1);
  // 		if(vertex_pass_bs2ddist) {
  // 		  h_selB_cutflow->Fill(Bmin_bs2ddist, 1);		    
  // 		  if(vertex_pass_bs2derr) {
  // 		    h_selB_cutflow->Fill(Bmax_rescale_bs2derr, 1);

  // 		  }
  // 		}
  // 	      }
  // 	    }
  // 	  }
  // 	}
  //     }
  //   }
  // }

  //new way
  if (pass_etrig) {
    h_electron_cutflow->Fill(e_pass_trig, w);
    if (pass_el[0]) {
      h_electron_cutflow->Fill(pass_ept, w);
      if (pass_el[1]) {
	h_electron_cutflow->Fill(pass_eID, w);
	if (pass_el[2]) {
	  h_electron_cutflow->Fill(pass_eeta, w);
	  if (pass_el[3]) {
	    h_electron_cutflow->Fill(pass_eiso, w);
	  }
	}
      }
    }
  }
  if (pass_mtrig) {
    h_muon_cutflow->Fill(m_pass_trig, w);
    if (pass_mu[0]) {
      h_muon_cutflow->Fill(pass_mpt, w);
      if (pass_mu[1]) {
	h_muon_cutflow->Fill(pass_mID, w);
	if (pass_mu[2]) {
	  h_muon_cutflow->Fill(pass_meta, w);
	  if (pass_mu[3]) {
	    h_muon_cutflow->Fill(pass_miso, w);
	  }
	}
      }
    }
  }
  if (pass_ditrig) {
    h_dilepton_cutflow->Fill(dil_pass_trig, w);
    if (pass_2mu[0] || pass_2el[0] || pass_muel[0]) {
      h_dilepton_cutflow->Fill(pass_dileppt, w);
      if (pass_2mu[1] || pass_2el[1] || pass_muel[1]) {
	h_dilepton_cutflow->Fill(pass_dilepID, w);
	if (pass_2mu[2] || pass_2el[2] || pass_muel[2]) {
	  h_dilepton_cutflow->Fill(pass_dilepeta, w);
	  if (pass_2el[3] || pass_2mu[3] || pass_muel[3]) {
	    h_dilepton_cutflow->Fill(pass_dilepiso, w);
	  }
	}
      }
    }
  }
  if (pass_etrig || pass_mtrig || pass_ditrig) {
    h_lepton_cutflow->Fill(l_pass_trig, w);
    if (pass_mu[0] || pass_el[0] || pass_2mu[0] || pass_2el[0] || pass_muel[0]) {
      h_lepton_cutflow->Fill(pass_leppt, w);
      if (pass_mu[1] || pass_el[1] || pass_2mu[1] || pass_2el[1] || pass_muel[1]) {
	h_lepton_cutflow->Fill(pass_lepID, w);
	if (pass_mu[2] || pass_el[2] || pass_2mu[2] || pass_2el[2] || pass_muel[2]) {
	  h_lepton_cutflow->Fill(pass_lepeta, w);
	  if (pass_mu[3] || pass_el[3] || pass_2el[3] || pass_2mu[3] || pass_muel[3]) {
	    h_lepton_cutflow->Fill(pass_lepiso, w);
	    // now after passing all preselection, it is time to fill the vertex cutflow
	    h_vertex_cutflow->Fill(pass_presel, w);
	    if (nsv_goe1) {
	      h_vertex_cutflow->Fill(atleast_1vtx, w);
	      if (pass_mintks[0]) {
		h_vertex_cutflow->Fill(pass_mintrack, w);
		if (pass_inbp[0]) {
		  h_vertex_cutflow->Fill(pass_inbeampipe, w);
		  if (pass_dbv[0]) {
		    h_vertex_cutflow->Fill(pass_mindbv, w);
		    if (pass_bs2derr[0]) {
		      h_vertex_cutflow->Fill(pass_maxdbv_unc, w);
		      if (nsv_goe2) {
			h_vertex_cutflow->Fill(atleast_2vtx, w);
			if (pass_mintks[1]) {
			  h_vertex_cutflow->Fill(pass_2mintrack, w);
			  if (pass_inbp[1]) {
			    h_vertex_cutflow->Fill(pass_2inbeampipe, w);
			    if (pass_dbv[1]) {
			      h_vertex_cutflow->Fill(pass_2mindbv, w);
			      if (pass_bs2derr[1]) {
				h_vertex_cutflow->Fill(pass_2maxdbv_unc, w);
			      }
			    }
			  }
			}
		      }
		    }
		  }
		}
	      }
	    }
	  }
	}
      }
    }
  }

  // h_bs2derr_cutflow->Fill(any_sv, new_pass_bs2derr[0]);
  // h_bs2derr_cutflow->Fill(bs2derr_60, new_pass_bs2derr[1]);
  // h_bs2derr_cutflow->Fill(bs2derr_50, new_pass_bs2derr[2]);
  // h_bs2derr_cutflow->Fill(bs2derr_45, new_pass_bs2derr[3]);
  // h_bs2derr_cutflow->Fill(bs2derr_40, new_pass_bs2derr[4]);
  // h_bs2derr_cutflow->Fill(bs2derr_35, new_pass_bs2derr[5]);
  // h_bs2derr_cutflow->Fill(bs2derr_30, new_pass_bs2derr[6]);
  // h_bs2derr_cutflow->Fill(bs2derr_25, new_pass_bs2derr[7]);
  
  //electron
  if (pass_etrig && (!pass_mtrig && !pass_ditrig) ) {
    h_trig_cutflow->Fill(pass_elONLY, w);
  }
  if (pass_el[3] && (!pass_mu[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_fullsel_cutflow->Fill(pass_elfullsel, w);
  }

  //electron separated
  if (pass_eltrig[0] && (!pass_eltrig[1] && !pass_eltrig[2] && !pass_mtrig && !pass_ditrig) ) {
    h_eltrig_cutflow->Fill(pass_el32t, w);
  }
  if (pass_elsel[0] && (!pass_elsel[1] && !pass_elsel[2] && !pass_mu[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_el_sel_cutflow->Fill(pass_el32sel, w);
  }

  if (!pass_eltrig[0] && (pass_eltrig[1] && !pass_eltrig[2] && !pass_mtrig && !pass_ditrig) ) {
    h_eltrig_cutflow->Fill(pass_el115t, w);
  }
  if (!pass_elsel[0] && (pass_elsel[1] && !pass_elsel[2] && !pass_mu[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_el_sel_cutflow->Fill(pass_el115sel, w);
  }

  if (!pass_eltrig[0] && (!pass_eltrig[1] && pass_eltrig[2] && !pass_mtrig && !pass_ditrig) ) {
    h_eltrig_cutflow->Fill(pass_el50t, w);
  }
  if (!pass_elsel[0] && (!pass_elsel[1] && pass_elsel[2] && !pass_mu[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_el_sel_cutflow->Fill(pass_el50sel, w);
  }

  //now the cross contributions
  if (pass_eltrig[0] && (pass_eltrig[1] && !pass_eltrig[2] && !pass_mtrig && !pass_ditrig) ) {
    h_eltrig_cutflow->Fill(pass_el32115t, w);
  }
  if (pass_elsel[0] && (pass_elsel[1] && !pass_elsel[2] && !pass_mu[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_el_sel_cutflow->Fill(pass_el32115sel, w);
  }

  if (pass_eltrig[0] && (!pass_eltrig[1] && pass_eltrig[2] && !pass_mtrig && !pass_ditrig) ) {
    h_eltrig_cutflow->Fill(pass_el3250t, w);
  }
  if (pass_elsel[0] && (!pass_elsel[1] && pass_elsel[2] && !pass_mu[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_el_sel_cutflow->Fill(pass_el3250sel, w);
  }

  if (!pass_eltrig[0] && (pass_eltrig[1] && pass_eltrig[2] && !pass_mtrig && !pass_ditrig) ) {
    h_eltrig_cutflow->Fill(pass_el11550t, w);
  }
  if (!pass_elsel[0] && (pass_elsel[1] && pass_elsel[2] && !pass_mu[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_el_sel_cutflow->Fill(pass_el11550sel, w);
  }

  if (pass_eltrig[0] && (pass_eltrig[1] && pass_eltrig[2] && !pass_mtrig && !pass_ditrig) ) {
    h_eltrig_cutflow->Fill(pass_allelt, w);
  }
  if (pass_elsel[0] && (pass_elsel[1] && pass_elsel[2] && !pass_mu[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_el_sel_cutflow->Fill(pass_allel_sel, w);
  }

  //total 

  //muon
  if (pass_mtrig && (!pass_etrig && !pass_ditrig) ) {
    h_trig_cutflow->Fill(pass_muONLY, w);
  }
  if (pass_mu[3] && (!pass_el[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_fullsel_cutflow->Fill(pass_mufullsel, w);
  }

  //now individually 
  if (pass_mutrig[0] && (!pass_mutrig[1] && !pass_etrig && !pass_ditrig) ) {
    h_mutrig_cutflow->Fill(pass_mu24t, w);
  }
  if (pass_musel[0] && (!pass_musel[1] && !pass_el[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_mu_sel_cutflow->Fill(pass_mu24sel, w);
  }

  if (pass_mutrig[1] && (!pass_mutrig[0] && !pass_etrig && !pass_ditrig) ) {
    h_mutrig_cutflow->Fill(pass_mu50t, w);
  }
  if (pass_musel[1] && (!pass_musel[0] && !pass_el[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_mu_sel_cutflow->Fill(pass_mu50sel, w);
  }

  if (pass_mutrig[1] && (pass_mutrig[0] && !pass_etrig && !pass_ditrig) ) {
    h_mutrig_cutflow->Fill(pass_allmut, w);
  }
  if (pass_musel[1] && (pass_musel[0] && !pass_el[3] && !pass_2mu[3]) && (!pass_2el[3] && !pass_muel[3]) ) {
    h_mu_sel_cutflow->Fill(pass_allmu_sel, w);
  }
    
  //dilep
  if (pass_ditrig && (!pass_etrig && !pass_mtrig) ) {
    h_trig_cutflow->Fill(pass_dilepONLY, w);
  }
  if ( (!pass_mu[3] && !pass_el[3]) && (pass_2mu[3] || pass_2el[3] || pass_muel[3]) ) {
    h_fullsel_cutflow->Fill(pass_dilepfullsel, w);
  }

  //single lep
  if ( (pass_etrig && pass_mtrig) && !pass_ditrig ) {
    h_trig_cutflow->Fill(pass_singlelepONLY, w);
  }
  if ( (pass_mu[3] && pass_el[3]) && !pass_2mu[3] && (!pass_2el[3] && !pass_muel[3]) ) {
    h_fullsel_cutflow->Fill(pass_singlelepfullsel, w);
  }


  //ele or dilep
  if (pass_ditrig && pass_etrig && !pass_mtrig ) {
    h_trig_cutflow->Fill(pass_eldilep, w);
  }
  if ( (!pass_mu[3] && pass_el[3]) && (pass_2mu[3] || pass_2el[3] || pass_muel[3]) ) {
    h_fullsel_cutflow->Fill(pass_eldilepfullsel, w);
  }

  
  //mu or dilep
  if (pass_ditrig && (!pass_etrig && pass_mtrig) ) {
    h_trig_cutflow->Fill(pass_mudilep, w);
  }
  if ( (pass_mu[3] && !pass_el[3]) && (pass_2mu[3] || pass_2el[3] || pass_muel[3]) ) {
    h_fullsel_cutflow->Fill(pass_mudilepfullsel, w);
  }

  //all
  if (pass_ditrig && pass_etrig && pass_mtrig ) {
    h_trig_cutflow->Fill(pass_alltrig, w);
  }
  if ( pass_mu[3] && pass_el[3] && (pass_2mu[3] ||  pass_2el[3] || pass_muel[3]) ) {
    h_fullsel_cutflow->Fill(pass_allsel, w);
  }


  //dilep separated : mumu, muel, ee, mumuANDmuel, mumuANDee, muelANDee
  //get rid of cases in which other triggers fired : this is purely dilepton contributions
  if (pass_mumutrig && !pass_etrig && !pass_mtrig && !pass_eetrig && !pass_mueltrig) {
    h_dileptrig_cutflow->Fill(pass_mumut, w);
  }
  if (!pass_mu[3] && !pass_el[3] && (pass_2mu[3] &&  !pass_2el[3] && !pass_muel[3]) ) {
    h_dilep_sel_cutflow->Fill(pass_mumu_sel, w);
  }

  if (!pass_mumutrig && !pass_etrig && !pass_mtrig && !pass_eetrig && pass_mueltrig) {
    h_dileptrig_cutflow->Fill(pass_muelt, w);
  }
  if (!pass_mu[3] && !pass_el[3] && (!pass_2mu[3] &&  !pass_2el[3] && pass_muel[3]) ) {
    h_dilep_sel_cutflow->Fill(pass_muel_sel, w);
  }

  if (!pass_mumutrig && !pass_etrig && !pass_mtrig && pass_eetrig && !pass_mueltrig) {
    h_dileptrig_cutflow->Fill(pass_eet, w);
  }
  if (!pass_mu[3] && !pass_el[3] && (!pass_2mu[3] &&  pass_2el[3] && !pass_muel[3]) ) {
    h_dilep_sel_cutflow->Fill(pass_ee_sel, w);
  }


  // cross contributions (should actually be zero but just check?)
  if (pass_mumutrig && !pass_etrig && !pass_mtrig && !pass_eetrig && pass_mueltrig) {
    h_dileptrig_cutflow->Fill(pass_mumuANDmuelt, w);
  }
  if (!pass_mu[3] && !pass_el[3] && (pass_2mu[3] &&  !pass_2el[3] && pass_muel[3]) ) {
    h_dilep_sel_cutflow->Fill(pass_mumuANDmuel_sel, w);
  }

  if (pass_mumutrig && !pass_etrig && !pass_mtrig && pass_eetrig && !pass_mueltrig) {
    h_dileptrig_cutflow->Fill(pass_mumuANDeet, w);
  }
  if (!pass_mu[3] && !pass_el[3] && (pass_2mu[3] &&  pass_2el[3] && !pass_muel[3]) ) {
    h_dilep_sel_cutflow->Fill(pass_mumuANDee_sel, w);
  }

  if (!pass_mumutrig && !pass_etrig && !pass_mtrig && pass_eetrig && pass_mueltrig) {
    h_dileptrig_cutflow->Fill(pass_muelANDeet, w);
  }
  if (!pass_mu[3] && !pass_el[3] && (!pass_2mu[3] &&  pass_2el[3] && pass_muel[3]) ) {
    h_dilep_sel_cutflow->Fill(pass_muelANDee_sel, w);
  }

  if (pass_mumutrig && !pass_etrig && !pass_mtrig && pass_eetrig && pass_mueltrig) {
    h_dileptrig_cutflow->Fill(pass_alldilept, w);
  }
  if (!pass_mu[3] && !pass_el[3] && (pass_2mu[3] &&  pass_2el[3] && pass_muel[3]) ) {
    h_dilep_sel_cutflow->Fill(pass_alldilep_sel, w);
  }

  

  
  
}
  

  
  //fill the lepton cutflows; old way
  // if (at_least_one_trigger_passes) {
  //   h_lepton_cutflow->Fill(l_pass_trig, 1);
  //   h_electron_cutflow->Fill(e_pass_trig, 1);
  //   h_muon_cutflow->Fill(m_pass_trig, 1);

  //   if (pass_el_goe) {
  //     h_electron_cutflow->Fill(pass_egoe, 1);
  //     if (pass_el[0]) {
  // 	h_electron_cutflow->Fill(pass_ept, 1);
  // 	if (pass_el_eta) {
  // 	  h_electron_cutflow->Fill(pass_eeta, 1);
  // 	  if (pass_el_ID) {
  // 	    h_electron_cutflow->Fill(pass_eID, 1);
  // 	    if (pass_el_iso) {
  // 	      h_electron_cutflow->Fill(pass_eiso, 1);
  // 	    }
  // 	  }
  // 	}
  //     }
  //   }
  //   if (pass_mu_goe) {
  //     h_muon_cutflow->Fill(pass_mgoe, 1);
  //     if (pass_mu_pt) {
  // 	h_muon_cutflow->Fill(pass_mpt, 1);
  // 	if (pass_mu_eta) {
  // 	  h_muon_cutflow->Fill(pass_meta, 1);
  // 	  if (pass_mu_ID) {
  // 	    h_muon_cutflow->Fill(pass_mID, 1);
  // 	    if (pass_mu_iso) {
  // 	      h_muon_cutflow->Fill(pass_miso, 1);
  // 	    }
  // 	  }
  // 	}
  //     }
  //   }
  //   if (pass_mu_goe || pass_el_goe) {
  //     h_lepton_cutflow->Fill(pass_lepgoe, 1);
  //     if (pass_mu_pt || pass_el_pt) {
  // 	h_lepton_cutflow->Fill(pass_leppt, 1);
  // 	if (pass_mu_eta || pass_el_eta) {
  // 	  h_lepton_cutflow->Fill(pass_lepeta, 1);
  // 	  if (pass_mu_ID || pass_el_ID) {
  // 	    h_lepton_cutflow->Fill(pass_lepID, 1);
  // 	    if (pass_mu_iso || pass_el_iso) {
  // 	      h_lepton_cutflow->Fill(pass_lepiso, 1);
  // 	    }
  // 	  }
  // 	}
  //     }
  //   }
  // }

  
DEFINE_FWK_MODULE(MFVCutFlowHistos);
