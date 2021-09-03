#ifndef DVCode_Tools_LumiList_h
#define DVCode_Tools_LumiList_h

#include <fstream>
#include <regex>
#include <string>

namespace jmt {
  class LumiList {
  public:
    LumiList(const std::string& fn) {
      std::ifstream ifs(fn);
      std::regex run_re("(\\d+)");
      std::regex range_re("\\[\\s*(\\d+)\\s*,\\s*(\\d+)\\s*\\]");
      std::smatch m;
      int run = -1;
      for (std::string line; std::getline(ifs, line, '"'); ) {
        // line = _trim(line);
        //if (debug) std::cout << "LumiList (TRIMMED) LINE: " << _trim(line) << "\n";
        if (std::regex_match(line, m, run_re)) {
          //if (debug) std::cout << "LumiList   RUN: " << m.str() << "\n";
          run = std::stoi(m.str());
          assert(!containsRun(run));
        }
        else {
          auto b = std::sregex_iterator(line.begin(), line.end(), range_re);
          auto e = std::sregex_iterator();
          //if (debug && std::distance(b,e)) std::cout << "LumiList  RANGE(s):\n";
          for (std::sregex_iterator i = b; i != e; ++i) {
            const int la = std::stoi((*i)[1]);
            const int lb = std::stoi((*i)[2]);
            //if (debug) std::cout << "LumiList     " << i->str() << " = run " << run << " ls " << la << " through " << lb << "\n";
            _map[run].push_back(std::make_pair(la,lb));
          }
        }
      }
    }

    bool containsRun(int run) const {
      return _map.find(run) != _map.end();
    }

    bool contains(int run, int ls) const {
      if (!containsRun(run)) return false;
      for (const auto& p: _map.find(run)->second)
        if (ls >= p.first && ls <= p.second)
          return true;
      return false;
    }

    template <typename T>
    bool contains(const T& t) const {
      return contains(int(t.run()), int(t.lumi()));
    }

    void dump(std::ostream& out) const {
      out << "{";
      bool firstrun = true;
      for (auto it = _map.begin(); it != _map.end(); ++it) {
        if (!firstrun)
          out << ",\n";
        firstrun = false;
        out << "\"" << it->first << "\": [";
        bool first = true;
        for (auto p : it->second) {
          if (!first)
            out << ", ";
          first = false;
          out << "[" << p.first << ", " << p.second << "]";
        }
        out << "]";
      }
      out << "}\n";
    }

  private:
    static inline std::string _trim(const std::string& sin) {
      std::string s(sin);
      s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int ch) { return !std::isspace(ch); }));
      s.erase(std::find_if(s.rbegin(), s.rend(), [](int ch) { return !std::isspace(ch); }).base(), s.end());
      return s;
    }

    std::map<int, std::vector<std::pair<int, int>>> _map;
  };
}

#endif
