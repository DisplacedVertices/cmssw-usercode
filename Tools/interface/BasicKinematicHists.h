#ifndef JMTucker_Tools_BasicKinematicHists_h
#define JMTucker_Tools_BasicKinematicHists_h

#include "TH1F.h"
#include "TString.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

struct BasicKinematicHists {
  edm::Service<TFileService>* fs;
  TString name;
  TString nice;

  TH1F* E;
  TH1F* P;
  TH1F* Pt;
  TH1F* Pz;
  TH1F* M;
  TH1F* Rap;
  TH1F* Eta;
  TH1F* Phi;

  BasicKinematicHists()
    : fs(0), name(""), nice("") {}

  BasicKinematicHists(edm::Service<TFileService>& fs_, const TString& name_, const TString& nice_)
    : fs(&fs_), name(name_), nice(nice_) {}
  
  TH1F* Book(const TString& subname, const TString& subnice, const int nbins, const double min, const double max, const TString& binning) {
    if (fs == 0)
      throw cms::Exception("BasicKinematicHists") << "fs not set before call to Book(...)";
    return (*fs)->make<TH1F>(name + subname, ";" + nice + " " + subnice + ";events/" + binning, nbins, min, max);
  }
  
  void BookE(int nbins, double min, double max, const TString& binning) {
    E = Book("E", "energy (GeV)", nbins, min, max, binning + " GeV");
  }

  void BookP(int nbins, double min, double max, const TString& binning) {
    P = Book("P", "momentum (GeV)", nbins, min, max, binning + " GeV");
  }

  void BookPt(int nbins, double min, double max, const TString& binning) {
    Pt = Book("Pt", "p_{T} (GeV)", nbins, min, max, binning + " GeV");
  }

  void BookPz(int nbins, double min, double max, const TString& binning) {
    Pz = Book("Pz", "p_{z} (GeV)", nbins, min, max, binning + " GeV");
  }

  void BookM(int nbins, double min, double max, const TString& binning) {
    M = Book("M", "mass (GeV)", nbins, min, max, binning + " GeV");
  }

  void BookRap(int nbins, double min, double max, const TString& binning) {
    Rap = Book("Rap", "rapidity", nbins, min, max, binning);
  }

  void BookEta(int nbins, double min, double max, const TString& binning) {
    Eta = Book("Eta", "pseudorapidity", nbins, min, max, binning);
  }

  void BookRapEta(int nbins, const TString& binning) {
    BookRap(nbins, -10, 10, binning);
    BookEta(nbins, -10, 10, binning);
  }

  void BookPhi(int nbins, double min, double max, const TString& binning) {
    Phi = Book("Phi", "phi (rad.)", nbins, min, max, binning + " rad.");
  }

  void BookPhi(int nbins, const TString& binning) {
    BookPhi(nbins, -3.14159, 3.14159, binning);
  }

  // backwards compatibility because I am too lazy to change GenHistos
  // right now...
  void Book(edm::Service<TFileService>& fs_, const TString& name_, const TString& nice_,
	    int nbins_E, double min_E, double max_E, const TString& binning_E,
	    int nbins_Pt, double min_Pt, double max_Pt, const TString& binning_Pt,
	    int nbins_Pz, double min_Pz, double max_Pz, const TString& binning_Pz,
	    int nbins_M, double min_M, double max_M, const TString& binning_M) {
    fs = &fs_;
    name = name_;
    nice = nice_;
    BookE(nbins_E, min_E, max_E, binning_E);
    BookP(nbins_E, min_E, max_E, binning_E);
    BookPt(nbins_E, min_E, max_E, binning_E);
    BookPz(nbins_E, min_E, max_E, binning_E);
    BookM(nbins_E, min_E, max_E, binning_E);
    BookRap(120, -6, 6, "0.1");
    BookEta(120, -6, 6, "0.1");
    BookPhi(100, -3.1416, 3.1416, "0.063");
  }

  void Fill(const reco::Candidate* c) {
    if (E) E->Fill(c->energy());
    if (P) P->Fill(c->p());
    if (Pt) Pt->Fill(c->pt());
    if (Pz) Pz->Fill(c->pz());
    if (M) M->Fill(c->mass());
    if (Rap) Rap->Fill(c->rapidity());
    if (Eta) Eta->Fill(c->eta());
    if (Phi) Phi->Fill(c->phi());
  }

  void Fill(const TLorentzVector& v) {
    if (E) E->Fill(v.E());
    if (P) P->Fill(v.P());
    if (Pt) Pt->Fill(v.Pt());
    if (Pz) Pz->Fill(v.Pz());
    if (M) M->Fill(v.M());
    if (v.Pt() > 0) {
      if (Rap) Rap->Fill(v.Rapidity());
      if (Eta) Eta->Fill(v.Eta());
    }
    else {
      if (Rap) Rap->Fill(1e9);
      if (Eta) Eta->Fill(1e9);
    }
    if (Phi) Phi->Fill(v.Phi());
  }

  void Fill(const reco::Candidate* c, const double weight) {
    if (E) E->Fill(c->energy(), weight);
    if (P) P->Fill(c->p(), weight);
    if (Pt) Pt->Fill(c->pt(), weight);
    if (Pz) Pz->Fill(c->pz(), weight);
    if (M) M->Fill(c->mass(), weight);
    if (Rap) Rap->Fill(c->rapidity(), weight);
    if (Eta) Eta->Fill(c->eta(), weight);
    if (Phi) Phi->Fill(c->phi(), weight);
  }

  void Fill(const TLorentzVector& v, const double weight) {
    if (E) E->Fill(v.E(), weight);
    if (P) P->Fill(v.P(), weight);
    if (Pt) Pt->Fill(v.Pt(), weight);
    if (Pz) Pz->Fill(v.Pz(), weight);
    if (M) M->Fill(v.M(), weight);
    if (v.Pt() > 0) {
      if (Rap) Rap->Fill(v.Rapidity(), weight);
      if (Eta) Eta->Fill(v.Eta(), weight);
    }
    else {
      if (Rap) Rap->Fill(1e9, weight);
      if (Eta) Eta->Fill(1e9, weight);
    }
    if (Phi) Phi->Fill(v.Phi(), weight);
  }
};

struct BasicKinematicHistsFactory {
  edm::Service<TFileService>& fs;
  typedef std::map<std::string, BasicKinematicHists*> hists_map;
  hists_map hists;
  
  BasicKinematicHistsFactory(edm::Service<TFileService>& fs_)
    : fs(fs_) {}

  ~BasicKinematicHistsFactory() {
    del();
  }

  void del() {
    // We own the pointers to the BasicKinematicHists, but the TH1F
    // pointers in them are owned by the TFileService.
    for (hists_map::iterator it = hists.begin(), ite = hists.end(); it != ite; ++it)
      delete it->second;
    hists.clear();
  }

  BasicKinematicHists* make(const char* name, const char* nice) {
    return hists[name] = new BasicKinematicHists(fs, name, nice);
  }

  BasicKinematicHists* make(const TString& name, const TString& nice) {
    return make(name.Data(), nice.Data());
  }

  BasicKinematicHists* operator[](const std::string& name) const {
    hists_map::const_iterator it = hists.find(name);
    if (it == hists.end())
      throw cms::Exception("BasicKinematicHists") << "no hists with name " << name << "\n";
    return it->second;
  }
};

#endif
