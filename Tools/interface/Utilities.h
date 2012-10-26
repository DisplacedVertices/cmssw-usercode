#ifndef JMTucker_Tools_Utilities_h
#define JMTucker_Tools_Utilities_h

#include "TLorentzVector.h"
#include "DataFormats/Candidate/interface/Candidate.h"

double cos_angle(const TVector3& v1, const TVector3& v2);
double cos_angle(const TLorentzVector& v1, const TLorentzVector& v2);
double cos_angle_in_rest(const TLorentzVector& rest_frame, const TLorentzVector& v1, const TLorentzVector& v2);
void die_if_not(bool condition, const char* msg, ...);
TLorentzVector lorentz_boost(const TLorentzVector& boost_frame, const TLorentzVector& to_be_boosted);
TLorentzVector make_tlv(const reco::Candidate::LorentzVector& lv);
TLorentzVector make_tlv(const reco::Candidate& c);
TLorentzVector make_tlv(const reco::Candidate* c);
double pt_proj(const TLorentzVector& a, const TLorentzVector& b);

#endif
