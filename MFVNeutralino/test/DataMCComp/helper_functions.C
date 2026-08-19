#include <sstream>
#include <iomanip>
#include <cmath>


// ROOT object helpers

void move_over_under_flows(TH1* h) {
  const int nb = h->GetNbinsX();

  const double b0_err = h->GetBinError(0);
  const double b1_err = h->GetBinError(1);
  h->SetBinContent(1, h->GetBinContent(1) + h->GetBinContent(0));
  h->SetBinError(1, sqrt(b1_err*b1_err + b0_err*b0_err));

  const double bN1_err = h->GetBinError(nb+1);
  const double bN_err = h->GetBinError(nb);
  h->SetBinContent(nb, h->GetBinContent(nb) + h->GetBinContent(nb+1));
  h->SetBinError(nb, sqrt(bN_err*bN_err + bN1_err*bN1_err));

  h->SetBinContent(0, 0);
  h->SetBinError(0, 0);
  h->SetBinContent(nb+1, 0);
  h->SetBinError(nb+1, 0);
}






// Non-ROOT object helpers

// Format numbers to strings, written in the context of mean/std. (Note these were all written by AI)

string format_fixed_dp(double val, int ndec) {
  ostringstream ss;
  ss << fixed << setprecision(ndec) << val;
  return ss.str();
}

string format_exp(int exp_val) {
  if (exp_val >= 0) {
    return "+" + to_string(exp_val);
  }
  return to_string(exp_val);
}

string format_mean_std(double mean, double std) {
  const int sigfigs = 3;
  const int sci_exp_threshold = 2;

  if (mean == 0) {
    return "0 +/- " + format_fixed_dp(std, 0);
  }

  const double abs_mean = fabs(mean);
  const int exp_val = floor(log10(abs_mean));

  if (exp_val >= sci_exp_threshold || exp_val <= -sci_exp_threshold) {
    const double scale = pow(10.0, exp_val);
    const double mean_mant = mean / scale;
    const double std_mant = std / scale;
    const int ndec = sigfigs - 1;

    return format_fixed_dp(mean_mant, ndec) + " +/- " + format_fixed_dp(std_mant, ndec) + " e" + format_exp(exp_val);
  }

  const int ndec = max(0, sigfigs - exp_val - 1);
  return format_fixed_dp(mean, ndec) + " +/- " + format_fixed_dp(std, ndec);
}


