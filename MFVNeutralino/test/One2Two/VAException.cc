#include "VAException.h"
#include <cstdarg>
#include <stdexcept>

namespace jmt {
  void vthrow(const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    const int n = 2048;
    char buf[n];
    vsnprintf(buf, n, fmt, args);
    va_end(args);
    throw std::runtime_error(buf);
  }
}
