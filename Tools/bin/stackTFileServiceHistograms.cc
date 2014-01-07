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
#include <TKey.h>
#include <TROOT.h>

void make(TDirectory& out, TObject* o);
void fill(TDirectory& out, TObject* o, double weight);

static const char* const kHelpOpt = "help";
static const char* const kHelpCommandOpt = "help,h";
static const char* const kOutputFileOpt = "output-file";
static const char* const kOutputFileCommandOpt = "output-file,o";
static const char* const kInputFilesOpt = "input-files";
static const char* const kInputFilesCommandOpt = "input-files,i";
static const char* const kWeightsOpt = "weights";
static const char* const kWeightsCommandOpt = "weights,w";

int main(int argc, char** argv) {
  std::string programName(argv[0]);
  std::string descString(programName);
  descString += " [options] ";
  descString += "data_file \nAllowed options";
  boost::program_options::options_description desc(descString);

  desc.add_options()
    (kOutputFileCommandOpt, boost::program_options::value<std::string>()->default_value("out.root"),  "output root file (default out.root)")
    (kWeightsCommandOpt,    boost::program_options::value<std::string>(),                             "comma-separated list of weights (default all 1)")
    (kHelpCommandOpt,                                                                                 "produce help message")
    (kInputFilesCommandOpt, boost::program_options::value<std::vector<std::string> >()->multitoken(), "input root files");

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

  if (vm.count(kWeightsOpt)) {
    std::string w = vm[kWeightsOpt].as<std::string>();
    typedef boost::char_separator<char> sep_t;
    sep_t sep(",");
    boost::tokenizer<sep_t> tokens(w, sep);
    for (boost::tokenizer<sep_t>::iterator t = tokens.begin(); t != tokens.end(); ++t) {
      const char* begin = t->c_str();
      char* end;
      double w = strtod(begin, &end);

      if (size_t(end - begin) < t->size()) {
	std::cerr << "invalid weight: " << begin << "\n";
        return -1;
      }

      weights.push_back(w);
    }
  }
  else
    weights = std::vector<double>(fileNames.size(), 1.0);

  if (weights.size() != fileNames.size()) {
    std::cerr << "the number of weights and the number of files must be the same\n";
    return -1;
  }

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
        make(out, obj);

      fill(out, obj, weights[i]);
    }

    empty = false;
    file.Close();
  }

  out.Write();
  out.Close();
}

void make(TDirectory& out, TObject* o) {
  TDirectory* dir;
  TH1F* th1f;
  TH1D* th1d;
  TH2F* th2f;
  TH2D* th2d;

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

      make(*outDir, obj);
    }
  }
  else if ((th1f = dynamic_cast<TH1F*>(o)) != 0) {
    TH1F *h = (TH1F*) th1f->Clone();
    h->Reset();
    h->Sumw2();
    h->SetDirectory(&out);
  }
  else if ((th1d = dynamic_cast<TH1D*>(o)) != 0) {
    TH1D *h = (TH1D*) th1d->Clone();
    h->Reset();
    h->Sumw2();
    h->SetDirectory(&out);
  }
  else if ((th2f = dynamic_cast<TH2F*>(o)) != 0) {
    TH2F *h = (TH2F*) th2f->Clone();
    h->Reset();   
    h->Sumw2();
    h->SetDirectory(&out);
  }
  else if ((th2d = dynamic_cast<TH2D*>(o)) != 0) {
    TH2D *h = (TH2D*) th2d->Clone();
    h->Reset();   
    h->Sumw2();
    h->SetDirectory(&out);
  }
}

void fill(TDirectory& out, TObject* o, double w) {
  TDirectory* dir;
  TH1F* th1f;
  TH1D* th1d;
  TH2F* th2f;
  TH2D* th2d;

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
  else if ((th1f = dynamic_cast<TH1F*>(o)) != 0) {
    const char* name = th1f->GetName();
    TH1F* outTh1f = dynamic_cast<TH1F*>(out.Get(name));
    if (outTh1f == 0) {
      std::cerr << "error: histogram TH1F" << name << " not found in directory " << out.GetName() << "\n";
      exit(-1);	
    }
    outTh1f->Add(th1f, w);
  }
  else if ((th1d = dynamic_cast<TH1D*>(o)) != 0) {
    const char* name = th1d->GetName();
    TH1D* outTh1d = dynamic_cast<TH1D*>(out.Get(name));
    if (outTh1d == 0) {
      std::cerr << "error: histogram TH1D" << name << " not found in directory " << out.GetName() << "\n";
      exit(-1);	
    } 
    outTh1d->Add(th1d, w);
  }
  else if ((th2f = dynamic_cast<TH2F*>(o)) != 0) {
    const char* name = th2f->GetName();
    TH2F* outTh2f = dynamic_cast<TH2F*>(out.Get(name));
    if (outTh2f == 0) {
      std::cerr << "error: histogram TH2F" << name << " not found in directory " << out.GetName() << "\n";
      exit(-1);	
    }
    outTh2f->Add(th2f, w);
  }
  else if ((th2d = dynamic_cast<TH2D*>(o)) != 0) {
    const char* name = th2d->GetName();
    TH2D* outTh2d = dynamic_cast<TH2D*>(out.Get(name));
    if (outTh2d == 0) {
      std::cerr << "error: histogram TH2D" << name << " not found in directory " << out.GetName() << "\n";
      exit(-1);	
    }
    outTh2d->Add(th2d, w);
  }
}
