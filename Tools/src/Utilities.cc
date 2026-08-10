#include <cstdarg>
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "JMTucker/Tools/interface/Utilities.h"

double cos_angle(const TVector3& v1, const TVector3& v2) {
  return v1 * v2 / v1.Mag() / v2.Mag();
}

double cos_angle(const TLorentzVector& v1, const TLorentzVector& v2) {
  return cos_angle(v1.Vect(), v2.Vect());
}

double cos_angle_in_rest(const TLorentzVector& rest_frame, const TLorentzVector& v1, const TLorentzVector& v2) {
  return cos_angle(lorentz_boost(rest_frame, v1),
		   lorentz_boost(rest_frame, v2));
}

void die_if_not(bool condition, const char* msg, ...) {
  va_list args;
  char buf[256];
  va_start(args, msg);
  vsnprintf(buf, 256, msg, args);
  va_end(args);
  if (!condition) throw cms::Exception("die_if_not", buf);
}

TLorentzVector lorentz_boost(const TLorentzVector& boost_frame, const TLorentzVector& to_be_boosted) {
  TLorentzVector v = to_be_boosted;
  v.Boost(-boost_frame.BoostVector());
  return v;
}

TLorentzVector make_tlv(const reco::Candidate::LorentzVector& lv) {
  TLorentzVector v;
  v.SetPtEtaPhiM(lv.pt(), lv.eta(), lv.phi(), lv.mass());
  return v;
}

TLorentzVector make_tlv(const reco::Candidate* c) {
  return c == 0 ? TLorentzVector() : make_tlv(c->p4());
}

TLorentzVector make_tlv(const reco::Candidate& c) {
  return make_tlv(c.p4());
}

TLorentzVector make_tlv(const reco::GenParticleRef& c) {
  return make_tlv(c->p4());
}

double pt_proj(const TLorentzVector& a, const TLorentzVector& b) {
  return (a.X()*b.X() + a.Y()*b.Y())/b.Pt();
}

void set_bin_labels(TAxis* xax, const char** labels) {
  for (int i = 0; i < xax->GetNbins(); ++i)
    xax->SetBinLabel(i+1, labels[i]);
}

void fill_by_label(TH1F* h, const std::string& label) {
  static const bool warn = true;
  int result = h->Fill(label.c_str(), 1);
  if (result < 0) {
    if (warn)
      printf("fill_by_label: TH1 with name %s has no label %s\n", h->GetName(), label.c_str());
    result = h->GetNbinsX();
    h->SetBinContent(result, h->GetBinContent(result) + 1);
  }
}

void fill_by_label(TH2F* h, const std::string& label_x, const std::string& label_y) {
  static const bool warn = true;
  int result = h->Fill(label_x.c_str(), label_y.c_str(), 1);
  if (result < 0) {
    if (warn)
      printf("fill_by_label: TH2 with name %s has no (label_x, label_y) %s %s\n", h->GetName(), label_x.c_str(), label_y.c_str());
    int binx = h->GetNbinsX();
    int biny = h->GetNbinsY();
    h->SetBinContent(binx, biny, h->GetBinContent(binx, biny) + 1);
  }
}

uchar int2uchar(int x) {
  assert(x >= 0 && x <= 255);
  return (uchar)x;
}

void inc_uchar(uchar& x) {
  assert(x < 255);
  ++x;
}

uchar int2uchar_clamp(int x) {
  if (x <= 0)
    return 0;
  else if (x >= 255)
    return 255;
  else return (uchar)x;
}

uchar uint2uchar_clamp(unsigned x) {
  if (x >= 255)
    return 255;
  else return (uchar)x;
}

void inc_uchar_clamp(uchar& x) {
  if (x < 255)
    ++x;
}

const reco::Track* jetDaughterTrack(const pat::Jet& jet, size_t idau) {
  if (idau >= jet.numberOfDaughters())
    return 0;

  const reco::Candidate* dau = jet.daughter(idau);
  if (dau->charge() == 0)
    return 0;

  const reco::Track* tk = 0;
  const reco::PFCandidate* pf = dynamic_cast<const reco::PFCandidate*>(dau);
  if (pf) {
    const reco::TrackRef& r = pf->trackRef();
    if (r.isNonnull())
      tk = &*r;
  }
  else {
    const pat::PackedCandidate* pk = dynamic_cast<const pat::PackedCandidate*>(dau);
    if (pk && pk->charge() && pk->hasTrackDetails())
      tk = &pk->pseudoTrack();
  }

  return tk;
}
