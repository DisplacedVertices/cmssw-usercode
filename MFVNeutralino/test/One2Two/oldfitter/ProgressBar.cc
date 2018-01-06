#include "ProgressBar.h"
#include <cassert>
#include <cstdio>

namespace jmt {
  ProgressBar::ProgressBar(int n_dots_, int n_complete, bool flush_, const char* chars_)
    : n_dots(n_dots_),
      n_per_dot(n_complete / n_dots > 0 ? n_complete / n_dots : 1),
      flush(flush_),
      chars(chars_),
      enabled(getenv("mfvo2t_no_progressbar") == 0),
      i(0),
      idot(0)
  {
    assert(chars.size() == 4);
  }

  void ProgressBar::start() {
    if (!enabled)
      return;
    printf("%c", chars[0]);
    for (int j = 0; j < n_dots; ++j)
      printf("%c", chars[1]);
    printf("%c\r%c", chars[2], chars[0]);
    if (flush)
      fflush(stdout);
  }

  ProgressBar& ProgressBar::operator++() {
    if (enabled && i++ % n_per_dot == 0) {
      ++idot;
      printf("%c", chars[3]);
      if (flush)
        fflush(stdout);
    }
    return *this;
  }
}
