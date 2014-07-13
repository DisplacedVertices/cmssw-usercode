#include "ProgressBar.h"
#include <cassert>

namespace jmt {
  ProgressBar::ProgressBar(int n_dots_, int n_complete, bool flush_, const char* chars_)
    : n_dots(n_dots_),
      n_per_dot(n_complete / n_dots),
      flush(flush_),
      chars(chars_),
      i(0),
      idot(0)
  {
    assert(chars.size() == 4);
  }

  void ProgressBar::start() {
    printf("%c", chars[0]);
    for (int j = 0; j < n_dots; ++j)
      printf("%c", chars[1]);
    printf("%c\r%c", chars[2], chars[0]);
    if (flush)
      fflush(stdout);
  }

  ProgressBar& ProgressBar::operator++() {
    if (i++ % n_per_dot == 0) {
      ++idot;
      printf("%c", chars[3]);
      if (flush)
        fflush(stdout);
    }
    return *this;
  }
}
