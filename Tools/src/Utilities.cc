#include <cstdarg>
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

double pt_proj(const TLorentzVector& a, const TLorentzVector& b) {
  return (a.X()*b.X() + a.Y()*b.Y())/b.Pt();
}
