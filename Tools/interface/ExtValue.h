#ifndef JMTucker_Tools_ExtValue
#define JMTucker_Tools_ExtValue

#include <limits>

namespace jmt {
  class ExtValue {
  private:
    bool lt_;
    double v_;
    int i_;
  public:
    ExtValue(bool lt) : lt_(lt), v_(lt ? std::numeric_limits<double>::max() : -std::numeric_limits<double>::max()), i_(-1) {}
    void operator()(const int i, const double v) { if ((lt_ && v < v_) || (!lt_ && v > v_)) { set(i, v); } }
    void operator()(             const double v) { set(-1, v); }
    void set(const int i, const double v) { i_ = i; v_ = v; }
    void set(             const double v) { set(-1, v); }
    operator double() const { return v_; }
    int i() const { return i_; }
  };

  class MinValue : public ExtValue { public: MinValue() : ExtValue(true)  {} };
  class MaxValue : public ExtValue { public: MaxValue() : ExtValue(false) {} };
}

#endif
