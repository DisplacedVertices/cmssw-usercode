SOURCES       = MiniNtuple.cc Utility.cc ProgressBar.cc VAException.cc Phi.cc Prob.cc Random.cc ROOTTools.cc ToyThrower.cc Templates.cc Templater.cc PhiShiftTemplater.cc ClearedJetsTemplater.cc SimpleClearingTemplater.cc Fitter.cc mfvo2t.cc
INCLUDES      = $(patsubst %.cc, %.h, $(SOURCES))
OBJECTS       = $(patsubst %.cc, bin/%.o, $(SOURCES))
ROOTCFLAGS    = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --nonew --glibs)
CFLAGS        = $(ROOTCFLAGS) -I$(CMSSW_BASE)/src -std=c++0x -pedantic -Werror -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -g
LIBS          = $(ROOTLIBS) -lMinuit

all: mfvo2t.exe

mfvo2t.exe: $(OBJECTS)
	g++ -o $@ $(OBJECTS) $(LIBS) $(CFLAGS)

bin/%.o : %.cc
	g++ $(CFLAGS) -c -o $@ $<

test:
	@echo SOURCES:
	@echo $(SOURCES)
	@echo INCLUDES:
	@echo $(INCLUDES)
	@echo OBJECTS:
	@echo $(OBJECTS)
	@echo CFLAGS:
	@echo $(CFLAGS)

clean:	
	-rm -f $(OBJECTS) mfvo2t.exe
