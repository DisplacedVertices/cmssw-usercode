#include "ConfigFromEnv.h"

int main() {
  jmt::ConfigFromEnv c("c", true);

  std::cout << "1:\n";
  for (auto s : c.get_vstring("1"))
    std::cout << s << "\n";

  std::cout << "2:\n";
  for (auto s : c.get_vdouble("2"))
    std::cout << s << "\n";
}
