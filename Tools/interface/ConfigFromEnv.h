#ifndef JMTucker_MFVNeutralino_One2Two_ConfigFromEnv
#define JMTucker_MFVNeutralino_One2Two_ConfigFromEnv

#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include "VAException.h"

namespace jmt {
  class ConfigFromEnv {
  public:
    ConfigFromEnv() : verbose(false), prefix("") {}
    ConfigFromEnv(const std::string& prefix_) : verbose(false), prefix(prefix_ + "_") {}
    ConfigFromEnv(const std::string& prefix_, const bool verbose_) : verbose(verbose_), prefix(prefix_ + "_") {}

  private:
    const bool verbose;
    const std::string prefix;

    const char* env_get(std::string name) const {
      return getenv((prefix + name).c_str());
    }

    template <typename T>
    T _get(const char* name, bool (*__get)(const char*, T& v)) const {
      const char* s = env_get(name);
      if (s == 0)
        vthrow("bad env var %s%s\n", prefix.c_str(), name);
      T v;
      if (!__get(s, v))
        vthrow("bad conversion %s%s=%s\n", prefix.c_str(), name, s);
      if (verbose)
        std::cout << prefix << name << " = " << v << std::endl;
      return v;
    }

    template <typename T>
    T _get(const char* name, bool (*__get)(const char*, T& v), T def) const {
      T v = def;
      const char* s = env_get(name);
      if (s != 0)
        __get(s, v);
      if (verbose) {
        if (v == def)
          std::cout << prefix << name << " = " << v << " (the default)" << std::endl;
        else
          std::cout << prefix << name << " = " << v << " (default = " << def << ")" << std::endl;
      }
      return v;
    }

  public:
    int get_int(const char* name)          const { return _get(name, parse_int);      }
    int get_int(const char* name, int def) const { return _get(name, parse_int, def); }

    long get_long(const char* name)           const { return _get(name, parse_long);      }
    long get_long(const char* name, long def) const { return _get(name, parse_long, def); }

    unsigned get_unsigned(const char* name)               const { return _get(name, parse_unsigned);      }
    unsigned get_unsigned(const char* name, unsigned def) const { return _get(name, parse_unsigned, def); }

    bool get_bool(const char* name)           const { return _get(name, parse_bool);      }
    bool get_bool(const char* name, bool def) const { return _get(name, parse_bool, def); }

    double get_double(const char* name)             const { return _get(name, parse_double);      }
    double get_double(const char* name, double def) const { return _get(name, parse_double, def); }

    long double get_long_double(const char* name)                  const { return _get(name, parse_long_double);      }
    long double get_long_double(const char* name, long double def) const { return _get(name, parse_long_double, def); }

    float get_float(const char* name)             const { return _get(name, parse_float);      }
    float get_float(const char* name, float def)  const { return _get(name, parse_float, def); }

    std::string get_string(const char* name)                   const { return _get(name, parse_string);      }
    std::string get_string(const char* name, std::string def)  const { return _get(name, parse_string, def); }
    std::string get_string_lower(const char* name, std::string def) const {
      std::string s = _get(name, parse_string, def);
      std::transform(s.begin(), s.end(), s.begin(), ::tolower);
      return s;
    }

  private:
    std::vector<std::string> _tokenize(const std::string& s) const {
      const bool debug = false;
      std::vector<std::string> tokens;
      std::string token;
      if (debug) printf("s size %lu\n", s.size());
      for (size_t i = 0, ie = s.size(); i < ie; ++i) {
        char c = s[i];
        if (debug) printf("%lu: [%c]\n", i, c);

        if (c == ',' || c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '#') {
          if (debug) printf("found whitespace or comma or comment\n");
          if (token.size()) {
            tokens.push_back(token);
            if (debug) printf("had token [%s], new tokens size %lu\n", token.c_str(), tokens.size());
            token = "";
          }
          if (c == '#') {
            if (debug) printf("comment character, breaking\n");
            break;
          }
          else
            continue;
        }

        token += c;
        if (debug) printf("building up token, now [%s]\n", token.c_str());
      }

      if (token.size())
        tokens.push_back(token);

      if (debug) {
        printf("final tokens: size: %lu, \n", tokens.size());
        for (size_t i = 0, ie = tokens.size(); i < ie; ++i)
          printf("[%s] ", tokens[i].c_str());
        printf("\n");
      }

      return tokens;
    }

    template <typename T>
    std::vector<T> _get_v(const char* name, bool (*__get)(const char*, T& v)) const {
      const char* s = env_get(name);
      if (s == 0)
        vthrow("bad env var %s%s\n", prefix.c_str(), name);
      const std::vector<std::string> t = _tokenize(s);
      std::vector<T> v(t.size());
      for (size_t i = 0; i < t.size(); ++i)
        if (!__get(t[i].c_str(), v[i]))
          vthrow("bad conversion %s%s=%s\n", prefix.c_str(), name, s);
      if (verbose) {
        std::cout << prefix << name << " =";
        for (auto x : v)
          std::cout << " " << x;
        std::cout << std::endl;
      }
      return v;
    }

    template <typename T>
    std::vector<T> _get_v(const char* name, bool (*__get)(const char*, T& v), std::vector<T> def) const {
      std::vector<T> v(def);
      const char* s = env_get(name);
      if (s != 0) {
        const std::vector<std::string> t = _tokenize(s);
        v.resize(t.size());
        for (size_t i = 0; i < t.size(); ++i)
          if (!__get(t[i].c_str(), v[i]))
            vthrow("bad conversion %s%s=%s\n", prefix.c_str(), name, s);
      }
      
      if (verbose) {
        std::cout << prefix << name << " =";
        for (auto x : v)
          std::cout << " " << x;
        if (v == def)
          std::cout << " (the default)";
        else {
          std::cout << " (default =";
          for (auto x : def)
            std::cout << " " << x;
          std::cout << ")";
        }
        std::cout << std::endl;
      }

      return v;
    }

  public:
    std::vector<std::string> get_vstring(const char* name)                               const { return _get_v(name, parse_string);      }
    std::vector<std::string> get_vstring(const char* name, std::vector<std::string> def) const { return _get_v(name, parse_string, def); }

    std::vector<int> get_vint(const char* name)                       const { return _get_v(name, parse_int);      }
    std::vector<int> get_vint(const char* name, std::vector<int> def) const { return _get_v(name, parse_int, def); }

    std::vector<double> get_vdouble(const char* name)                          const { return _get_v(name, parse_double);      }
    std::vector<double> get_vdouble(const char* name, std::vector<double> def) const { return _get_v(name, parse_double, def); }

  private:
    static bool parse_int(const char* s, int& v) {
      return sscanf(s, "%i", &v) == 1;
    }

    static bool parse_long(const char* s, long& v) {
      return sscanf(s, "%li", &v) == 1;
    }

    static bool parse_unsigned(const char* s, unsigned& v) {
      return sscanf(s, "%u", &v) == 1;
    }

    static bool parse_bool(const char* s, bool& v) {
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

    static bool parse_double(const char* s, double& v) {
      return sscanf(s, "%lf", &v) == 1;
    }

    static bool parse_long_double(const char* s, long double& v) {
      return sscanf(s, "%Lf", &v) == 1;
    }

    static bool parse_float(const char* s, float& v) {
      return sscanf(s, "%f", &v) == 1;
    }

    static bool parse_string(const char* s, std::string& v) {
      bool ok = s != 0;
      if (ok)
        v = s;
      return ok;
    }
  };
}

#endif
