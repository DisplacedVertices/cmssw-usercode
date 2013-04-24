#ifndef JMTucker_Tools_Thrust2D_h
#define JMTucker_Tools_Thrust2D_h

// Utility to compute thrust value and axis from a collection of
// candidates.
//
// Ported from BaBar implementation.
//
// The thrust axis is the vector T which maximises the following
// expression:
//
//       sum_i=1...N ( | T . p_i | )
//  t = --------------------------------- 
//      sum_i=1...N ( (p_i . _p_i)^(1/2) )
//
// where p_i, i=1...N are the particle momentum vectors. The thrust
// value is the maximum value of t.
// 
// The thrust axis has a two-fold ambiguity due to taking the absolute
// value of the dot product. This computation returns by convention a
// thrust axis in the present 2D case with phi in [0,pi).
//
// The thrust measure the alignment of a collection of particles along
// a common axis.  The lower the thrust, the more spherical the event
// is. The higher the thrust, the more jet-like.
//
// Author of original 3D class in CMSSW (PhysicsTools/CandUtils): Luca Lista
// 2D-ified by Werner Sun

#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include <vector>
 
class Thrust2D  {
public:
  typedef math::XYZVector Vector;

  template<typename const_iterator>
  Thrust2D(const_iterator begin, const_iterator end) 
    : thrust_(0),
      axis_(0, 0, 0),
      pSum_(0), 
      n_(end - begin),
      p_(n_)
  {
    if (n_ == 0)
      return;
    std::vector<const reco::Candidate*> cands;
    for (const_iterator i = begin; i != end; ++i)
      cands.push_back(&*i);
    init(cands);
  } 

  /// thrust value (in the range [0.5, 1.0])
  double thrust() const { return thrust_; } 
  /// thrust axis (with magnitude = 1)
  const Vector& axis() const { return axis_; } 

private:
  double thrust_;
  Vector axis_;
  double pSum_;
  const unsigned int n_;
  std::vector<Vector> p_;

  struct ThetaPhi {
    ThetaPhi(double t, double p) : theta(t), phi(p) {}
    double theta, phi;
  };

  void init(const std::vector<const reco::Candidate*>&);

  double thrust(const Vector& theAxis) const;
  void parabola(double& a, double& b, double& c, const Vector&, const Vector&, const Vector&) const;

  Vector axis(double theta, double phi) const {
    return Vector(cos(phi), sin(phi), 0);
  }

  Vector axis(const ThetaPhi& tp) const {
    return axis(tp.theta, tp.phi);
  }

  ThetaPhi initialAxis() const;
  ThetaPhi finalAxis(ThetaPhi) const;
};

#endif
