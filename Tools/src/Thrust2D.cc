#include "JMTucker/Tools/interface/Thrust2D.h"

void Thrust2D::init(const std::vector<const reco::Candidate*>& cands) {
  int i = 0;
  for (std::vector<const reco::Candidate*>::const_iterator t = cands.begin(); t != cands.end(); ++t, ++i) {
    p_[i] = (*t)->momentum();
    p_[i].SetZ(0);
    pSum_ += p_[i].r();
  }

  axis_ = axis(finalAxis(initialAxis()));
  if (axis_.phi() < 0 || axis_.phi() > M_PI) axis_ *= -1;
  thrust_ = thrust(axis_);
}

double Thrust2D::thrust(const Vector& axis) const {
  double result = 0;
  double sum = 0;
  for (unsigned int i = 0; i < n_; ++i)
    sum += fabs(axis.x()*p_[i].x() + axis.y()*p_[i].y());
  if (pSum_ > 0) result = sum / pSum_;
  return result;
}

void Thrust2D::parabola(double& a, double& b, double& c, const Vector& a1, const Vector& a2, const Vector& a3) const {
  double t1 = thrust(a1), t2 = thrust(a2), t3 = thrust(a3);
  a = (t2 - 2 * c + t3) / 2;
  b = t2 - a - c;
  c = t1;
}

Thrust2D::ThetaPhi Thrust2D::initialAxis() const {
  static const int nSegsPhi = 10;
  int j;
  double thr[nSegsPhi], max = 0;
  int indJ = 0, index = -1;
  for (j = 0; j < nSegsPhi; ++j) {
    double phi = 2*M_PI * j / nSegsPhi;
    thr[j] = thrust(Vector(cos(phi), sin(phi), 0.));
    if (thr[j] > max) {
      index = indJ = j;
      max = thr[index];
    }
  }

  // take max and one point on either size, fitting to a parabola and
  // extrapolating to the real max.  Do this separately for each dimension.
  // y = a x^2 + b x + c.  At the max, x = 0, on either side, x = +/-1.
  // do phi first
  double a, b, c = max;
  int ind1 = indJ + 1;
  if (ind1 >= nSegsPhi) ind1 -= nSegsPhi;
  int ind2 = indJ - 1;
  if (ind2 < 0) ind2 += nSegsPhi;
  a = (thr[ind1] + thr[ind2] - 2*c) / 2;
  b = thr[ind1] - a - c;
  double maxPhiInd = 0;
  if (a != 0) maxPhiInd = -b/(2*a);
  return ThetaPhi(M_PI / 2, 2 * M_PI * (maxPhiInd + indJ) / nSegsPhi);
}

Thrust2D::ThetaPhi Thrust2D::finalAxis(ThetaPhi best) const {
  static const double epsilon = 0.0001;
  double maxChange2 = 0, a = 0, b = 0, c = 0, thr = 0;
  int mandCt = 3, maxCt = 1000;
  bool done;
  do { 
    parabola(a, b, c, 
	     axis(best),
	     axis(best.theta, best.phi + epsilon),
	     axis(best.theta, best.phi - epsilon));
    maxChange2 = 10 * (b < 0 ? -1 : 1);
    if (a != 0) maxChange2 = - b / (2 * a);
    while (fabs(maxChange2 * epsilon) > M_PI/4) { maxChange2 /= 2; }
    do {
      // L.L.: fixed odd behavior adding epsilon
      thr = thrust(axis(best.theta, best.phi + maxChange2 * epsilon)) + epsilon;
      if (thr < c) maxChange2 /= 2;
    } while (thr < c);
    best.phi += maxChange2 * epsilon;
    if (best.phi > 2*M_PI) best.phi -= 2*M_PI;
    if (best.phi < 0) best.phi += 2*M_PI;
    // phi ambiguity, use convention that phi in [0,pi]
    if (best.phi > M_PI) best.phi -= M_PI;
    if (mandCt > 0) --mandCt;
    --maxCt;
    done = (fabs(maxChange2) > 1 || mandCt) && (maxCt > 0);
  } while (done);

  return best;
}
