#ifndef JMTucker_MFVNeutralino_One2Two_Utility_h
#define JMTucker_MFVNeutralino_One2Two_Utility_h

#include <string>

namespace jmt {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }

  bool parse_int(const char* s, int& v);
  bool parse_long(const char* s, long& v);
  bool parse_unsigned(const char* s, unsigned& v);
  bool parse_bool(const char* s, bool& v);
  bool parse_double(const char* s, double& v);
  bool parse_long_double(const char* s, long double& v);
  bool parse_float(const char* s, float& v);
  bool parse_string(const char* s, std::string& v);

  void die_if(int condition, const char* fmt, ...);
}

#endif
