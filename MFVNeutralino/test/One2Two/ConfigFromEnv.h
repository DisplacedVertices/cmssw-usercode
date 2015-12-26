#ifndef JMTucker_MFVNeutralino_One2Two_ConfigFromEnv
#define JMTucker_MFVNeutralino_One2Two_ConfigFromEnv

#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include "Utility.h"
#include "VAException.h"

namespace jmt {
  class ConfigFromEnv {
  public:
    ConfigFromEnv() : verbose(false), prefix("") {}
    ConfigFromEnv(const bool verbose_) : verbose(verbose_), prefix("") {}
    ConfigFromEnv(const std::string& prefix_) : verbose(false), prefix(prefix_ + "_") {}
    ConfigFromEnv(const std::string& prefix_, const bool verbose_) : verbose(verbose_), prefix(prefix_ + "_") {}

  private:
    const bool verbose;
    const std::string prefix;

    std::vector<std::string> tokenize(const std::string& s) const {
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

    float get_float(const char* name)             const { return _get(name, parse_float);      }
    float get_float(const char* name, float def)  const { return _get(name, parse_float, def); }

    std::string get_string(const char* name)                   const { return _get(name, parse_string);      }
    std::string get_string(const char* name, std::string def)  const { return _get(name, parse_string, def); }
    std::string get_string_lower(const char* name, std::string def) const {
      std::string s = _get(name, parse_string, def);
      std::transform(s.begin(), s.end(), s.begin(), ::tolower);
      return s;
    }

    /*
      std::vector<std::string> env_get_vstring(const char* name) {
      return tokenize(env_get(name));
      }

      std::vector<int> env_get_vint(const char* name) {
      std::vector<std::string> vars = tokenize(env_get(name));
      const size_t nv = vars.size();
      std::vector<int> vx(nv);
      for (size_t i = 0; i < nv; ++i)
      vx[i] = atoi(vars[i].c_str());
      return vx;
      }

      std::vector<double> env_get_vdouble(const char* name) {
      std::vector<std::string> vars = tokenize(env_get(name));
      const size_t nv = vars.size();
      std::vector<double> vx(nv);
      for (size_t i = 0; i < nv; ++i)
      vx[i] = atof(vars[i].c_str());
      return vx;
      }
      }
    */
  };
}

#endif
