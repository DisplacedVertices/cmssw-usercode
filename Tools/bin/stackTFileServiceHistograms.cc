#include <algorithm>
#include <cassert>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <boost/program_options.hpp>
#include <boost/tokenizer.hpp>
#include <TFile.h>
#include <TH2.h>
#include <THStack.h>
#include <TKey.h>
#include <TROOT.h>

void make(TDirectory& out, TObject* o, bool stacking);
void fill(TDirectory& out, TObject* o, double weight);

static const char* const kHelpOpt = "help";
static const char* const kHelpCommandOpt = "help,h";
static const char* const kOutputFileOpt = "output-file";
static const char* const kOutputFileCommandOpt = "output-file,o";
static const char* const kInputFilesOpt = "input-files";
static const char* const kInputFilesCommandOpt = "input-files,i";
static const char* const kWeightsOpt = "weights";
static const char* const kWeightsCommandOpt = "weights,w";
static const char* const kStackOpt = "stack";
static const char* const kStackCommandOpt = "stack,s";

template <typename T>
std::vector<T> parse_comma_sep(const std::string& w) {
  std::vector<T> res;

  typedef boost::char_separator<char> sep_t;
  sep_t sep(",");
  boost::tokenizer<sep_t> tokens(w, sep);
  for (boost::tokenizer<sep_t>::iterator t = tokens.begin(); t != tokens.end(); ++t) {
    const char* begin = t->c_str();
    char* end;
    T w = strtod(begin, &end);

    if (size_t(end - begin) < t->size()) {
      std::cerr << "invalid token: " << begin << "\n";
      exit(-1);
    }

    res.push_back(w);
  }

  return res;
}

int main(int argc, char** argv) {
  std::string programName(argv[0]);
  std::string descString(programName);
  descString += " [options] ";
  descString += "data_file \nAllowed options";
  boost::program_options::options_description desc(descString);

  desc.add_options()
    (kHelpCommandOpt,                                                                                 "produce help message")
    (kInputFilesCommandOpt, boost::program_options::value<std::vector<std::string> >()->multitoken(), "input root files")
    (kOutputFileCommandOpt, boost::program_options::value<std::string>()->default_value("out.root"),  "output root file (default out.root)")
    (kWeightsCommandOpt,    boost::program_options::value<std::string>(),                             "comma-separated list of weights (default all 1)")
    (kStackCommandOpt,      boost::program_options::value<std::string>(),                             "comma-separated list of stack colors (default no stack)");

  boost::program_options::positional_options_description p;

  boost::program_options::variables_map vm;
  try {
    boost::program_options::store(boost::program_options::command_line_parser(argc,argv).options(desc).positional(p).run(), vm);
    boost::program_options::notify(vm);
  }
  catch (const boost::program_options::error&) {
    std::cerr << "invalid arguments. usage:\n" << desc << "\n";
    return -1;
  }

  if (vm.count(kHelpOpt)) {
    std::cout << desc << "\n";
    return 0;
  }

  std::vector<std::string> fileNames;
  std::string outputFile;
  std::vector<double> weights;
  std::vector<int> stack;
  bool stacking;

  if (vm.count(kInputFilesOpt))
    fileNames = vm[kInputFilesOpt].as<std::vector<std::string> >();

  if (fileNames.size() == 0) {
    std::cerr << "input files must be specified\n";
    return -1;
  }

  if (vm.count(kOutputFileOpt))
    outputFile = vm[kOutputFileOpt].as<std::string>();
  else {
    std::cerr << "output file must be specified" << "\n";
    return -1;
  }

  if (vm.count(kWeightsOpt))
    weights = parse_comma_sep<double>(vm[kWeightsOpt].as<std::string>());
  else
    weights = std::vector<double>(fileNames.size(), 1.0);

  if (weights.size() != fileNames.size()) {
    std::cerr << "the number of weights and the number of files must be the same\n";
    return -1;
  }

  if (vm.count(kStackOpt))
    stack = parse_comma_sep<int>(vm[kStackOpt].as<std::string>());

  stacking = stack.size();

  if (stacking && stack.size() != fileNames.size()) {
    std::cerr << "the number of stack colors and the number of files must be the same\n";
    return -1;
  }

  std::cout << "merging";
  if (stacking) std::cout << "/stacking";
  std::cout << " these files:\n";
  for (const std::string& f : fileNames)
    std::cout << "  " << f << "\n";
  std::cout << "with weights";
  if (stacking) std::cout << "/stack colors";
  std::cout << ":\n";
  for (size_t i = 0; i < fileNames.size(); ++i) {
    std::cout << "  " << weights[i];
    if (stacking) std::cout << "/" << stack[i];
    std::cout << "\n";
  }
  std::cout << "to output file " << outputFile << "\n";

  //////////////////////////////////////////////////////////////////////////////

  gROOT->SetBatch();

  TFile out(outputFile.c_str(), "RECREATE");
  if (!out.IsOpen()) { 
    std::cerr << "can't open output file: " << outputFile << "\n";
    return -1;  
  }

  bool empty = true;
  for (size_t i = 0; i < fileNames.size(); ++i) {
    const std::string& fileName = fileNames[i];
    TFile file(fileName.c_str());
    if (!file.IsOpen()) {
      std::cerr << "can't open input file: " << fileName <<"\n";
      return -1;
    }

    TIter next(file.GetListOfKeys());
    TKey* key = 0;
    while ((key = dynamic_cast<TKey*>(next()))) {
      std::string className(key->GetClassName());
      std::string name(key->GetName());

      TObject* obj = file.Get(name.c_str());

      if (obj == 0) {
	std::cerr << "error: key " << name << " not found in file " << fileName << "\n";
	return -1;
      }

      if (empty)
        make(out, obj, stacking);

      fill(out, obj, weights[i]);
    }

    empty = false;
    file.Close();
  }

  out.Write();
  out.Close();
}

template <typename T>
bool make_hist(TDirectory& out, TObject* o, bool stacking) {
  T* h = dynamic_cast<T*>(o);
  if (!h)
    return false;

  if (!stacking) {
    T* h2 = (T*)h->Clone();
    h2->Reset();
    if (!h2->GetSumw2N())
      h2->Sumw2();
    h2->SetDirectory(&out);
  }
  else {
    THStack* hs = new THStack(h->GetName(), h->GetTitle());
    hs->Write();
  }
    
  return true;
}

void make(TDirectory& out, TObject* o, bool stacking) {
  TDirectory* dir;

  out.cd();

  if ((dir = dynamic_cast<TDirectory*>(o)) != 0) {
    TDirectory* outDir = out.mkdir(dir->GetName(), dir->GetTitle());
    TIter next(dir->GetListOfKeys());
    TKey* key;
    while ((key = dynamic_cast<TKey*>(next()))) {
      std::string className(key->GetClassName());
      std::string name(key->GetName());
      TObject* obj = dir->Get(name.c_str());

      if (obj == 0) {
	std::cerr << "error: key " << name << " not found in directory " << dir->GetName() << "\n";
	exit(-1);
      }

      make(*outDir, obj, stacking);
    }
  }
  else if (make_hist<TH1F>(out, o, stacking)) {}
  else if (make_hist<TH1D>(out, o, stacking)) {}
  else if (make_hist<TH2F>(out, o, false)) {}
  else if (make_hist<TH2D>(out, o, false)) {}
}

template <typename T>
bool fill_hist(TDirectory& out, TObject* o, double w, int s) {
  T* h = dynamic_cast<T*>(o);
  if (!h)
    return false;
  T* h2 = dynamic_cast<T*>(out.Get(o->GetName()));
  if (!h2) {
    std::cerr << "error: histogram " << typeid(*o).name() << " not fuond in directory " << out.GetName() << "\n";
    exit(-1);
  }
  h2->Add(h, w);
  return true;
}

void fill(TDirectory& out, TObject* o, double w, int s) {
  TDirectory* dir;

  if ((dir = dynamic_cast<TDirectory*>(o)) != 0) {
    const char* name = dir->GetName();
    TDirectory* outDir = dynamic_cast<TDirectory*>(out.Get(name));

    if (outDir == 0) {
      std::cerr << "can't find directory " << name << " in output file" << "\n";
      exit(-1);
    }

    TIter next(dir->GetListOfKeys());
    TKey* key;
    while ((key = dynamic_cast<TKey*>(next()))) {
      std::string className(key->GetClassName());
      std::string name(key->GetName());
      TObject* obj = dir->Get(name.c_str());

      if (obj == 0) {
	std::cerr <<"error: key " << name << " not found in directory " << dir->GetName() << "\n";
	exit(-1);
      }

      fill(*outDir, obj, w);
    }
  }
  else if (fill_hist<TH1F>(out, o, w)) {}
  else if (fill_hist<TH1D>(out, o, w)) {}
  else if (fill_hist<TH2F>(out, o, w)) {}
  else if (fill_hist<TH2D>(out, o, w)) {}
}
