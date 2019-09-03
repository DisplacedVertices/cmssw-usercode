#ifndef JMTucker_Tools_Math_h
#define JMTucker_Tools_Math_h

namespace jmt {
  template <typename T> int sgn(T x) { return x >= 0 ? 1 : -1; }

  template <typename T> T mag(T x)                { return fabs(x); }
  template <typename T> T mag(T x, T y)           { return sqrt(x*x + y*y); }
  template <typename T> T mag(T x, T y, T z)      { return sqrt(x*x + y*y + z*z); }
  template <typename T> T mag(T x, T y, T z, T w) { return sqrt(x*x + y*y + z*z + w*w); }

  template <typename T> T mag2(T x, T y)           { return x*x + y*y; }
  template <typename T> T mag2(T x, T y, T z)      { return x*x + y*y + z*z; }
  template <typename T> T mag2(T x, T y, T z, T w) { return x*x + y*y + z*z + w*w; }

  template <typename T, typename T2> T2 mag(const T& v) { return mag<T2>(v.x(), v.y(), v.z()); }

  template <typename T> T signed_mag(T x, T y) {
    T m = mag(x,y);
    if (y < 0) return -m;
    return m;
  }

  template <typename T> T dphi(T a, T b) {
    T d = a - b;
    while (d > M_PI) d -= 2*M_PI;
    while (d <= -M_PI) d += 2*M_PI;
    return d;
  }

  template <typename T> T dR2(T etaa, T phia, T etab, T phib) { return mag2(etaa - etab, dphi(phia, phib)); }
  template <typename T> T dR (T etaa, T phia, T etab, T phib) { return mag (etaa - etab, dphi(phia, phib)); }
}

#endif
