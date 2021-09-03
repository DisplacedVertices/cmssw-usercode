#ifndef DVCode_Tools_BasicKinematicHists_h
#define DVCode_Tools_BasicKinematicHists_h

#include "TH1F.h"
#include "TString.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

struct BasicKinematicHists {
  TFileDirectory dir;
  TString nice;

  TH1F* E;
  TH1F* P;
  TH1F* Pt;
  TH1F* Pz;
  TH1F* M;
  TH1F* Rap;
  TH1F* Eta;
  TH1F* Phi;
  TH1F* Dxy;
  TH1F* Dz;
  TH1F* Q;

  BasicKinematicHists(TFileDirectory dir_, const TString& nice_)
    : dir(dir_), nice(nice_) { reset(); }

  void reset() {
    E = P = Pt = Pz = M = Rap = Eta = Phi = Dxy = Dz = Q = 0;
  }

  TH1F* Book(const TString& subname, const TString& subnice, const int nbins, const double min, const double max, const TString& binning) {
    return dir.make<TH1F>(subname, ";" + nice + " " + subnice + ";events/" + binning, nbins, min, max);
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

  void BookEta(int nbins, const TString& binning) {
    BookEta(nbins, -10, 10, binning);
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

  void BookDxy(int nbins, double min, double max, const TString& binning) {
    Dxy = Book("Dxy", "dxy (cm)", nbins, min, max, binning + " cm");
  }

  void BookDz(int nbins, double min, double max, const TString& binning) {
    Dz = Book("Dz", "dz (cm)", nbins, min, max, binning + " cm");
  }

  void BookQ() {
    Q = Book("Q", "charge", 3, -1, 2, "1");
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

  void FillEx(const double dxy, const double dz, const int q) {
    if (Dxy) Dxy->Fill(dxy);
    if (Dz)  Dz ->Fill(dz);
    if (Q)   Q  ->Fill(q);
  }

  void FillEx(const double dxy, const double dz, const int q, const double weight) {
    if (Dxy) Dxy->Fill(dxy, weight);
    if (Dz)  Dz ->Fill(dz,  weight);
    if (Q)   Q  ->Fill(q,   weight);
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

  BasicKinematicHists* make(TFileDirectory& dir, const char* nice) {
    return hists[dir.fullPath()] = new BasicKinematicHists(dir, nice);
  }

  BasicKinematicHists* make(const std::string& dir_path, const char* nice) {
    TFileDirectory dir = fs->mkdir(dir_path);
    return make(dir, nice);
  }

  BasicKinematicHists* make(const TString& dir_path, const char* nice) {
    return make(std::string(dir_path.Data()), nice);
  }

  BasicKinematicHists* make(const char* dir_path, const char* nice) {
    return make(std::string(dir_path), nice);
  }

  BasicKinematicHists* operator[](const std::string& name) const {
    hists_map::const_iterator it = hists.find(name);
    if (it == hists.end())
      throw cms::Exception("BasicKinematicHists") << "no hists with name " << name << "\n";
    return it->second;
  }
};

#endif
