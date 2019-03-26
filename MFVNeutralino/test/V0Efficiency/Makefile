SOURCES       = Ntuple.cc utils.cc
INCLUDES      = $(patsubst %.cc, %.h, $(SOURCES))
OBJECTS       = $(patsubst %.cc, bin/%.o, $(SOURCES))
ROOTCFLAGS    = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --nonew --glibs)
BOOSTCFLAGS   = -I$(shell scram tool tag boost INCLUDE)
BOOSTLIBS     = -L$(shell scram tool tag boost LIBDIR) -lboost_program_options
CFLAGS        = $(ROOTCFLAGS) $(BOOSTCFLAGS) -I$(CMSSW_BASE)/src -std=c++17 -pedantic -Werror -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -O3
LIBS          = $(ROOTLIBS) $(BOOSTLIBS)

all: hists.exe

%.exe: bin/%.o $(OBJECTS)
	@mkdir -p bin
	g++ -o $@ $(OBJECTS) $< $(LIBS) $(CFLAGS)

bin/%.o : %.cc
	@mkdir -p bin
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

.PRECIOUS: bin/%.o

clean:	
	-rm -f *.exe 
	-rm -rf bin/

setup:
	ln -sf ../../../Tools/src/Ntuple.cc
