#include "JMTucker/Tools/interface/Utility.h"
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>

namespace jmt {
  bool parse_int(const char* s, int& v) {
    return sscanf(s, "%i", &v) == 1;
  }

  bool parse_long(const char* s, long& v) {
    return sscanf(s, "%li", &v) == 1;
  }

  bool parse_unsigned(const char* s, unsigned& v) {
    return sscanf(s, "%u", &v) == 1;
  }

  bool parse_bool(const char* s, bool& v) {
    char buf[8];
    strncpy(buf, s, 8);
    char* p = buf;
    while (*p)
      tolower(*p++);
    bool t = strcmp(buf, "true")  == 0;
    bool f = strcmp(buf, "false") == 0;
    bool o = strcmp(buf, "1")     == 0;
    bool z = strcmp(buf, "0")     == 0;
    v = (t || o);
    return t+f+o+z == 1;
  }

  bool parse_double(const char* s, double& v) {
    return sscanf(s, "%lf", &v) == 1;
  }

  bool parse_long_double(const char* s, long double& v) {
    return sscanf(s, "%Lf", &v) == 1;
  }

  bool parse_float(const char* s, float& v) {
    return sscanf(s, "%f", &v) == 1;
  }

  bool parse_string(const char* s, std::string& v) {
    bool ok = s != 0;
    if (ok)
      v = s;
    return ok;
  }

  void die_if(int condition, const char* fmt, ...) {
    if (!condition) {
      fprintf(stderr, "died: ");
      va_list args;
      va_start(args, fmt);
      vfprintf(stderr, fmt, args);
      va_end(args);
      fprintf(stderr, "\n");
      exit(condition);
    }
  }
}
