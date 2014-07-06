SOURCES       = Utility.cc VAException.cc Prob.cc Random.cc ROOTTools.cc ToyThrower.cc Templates.cc One2TwoPhiShift.cc Fitter.cc mfvo2t.cc
INCLUDES      = $(patsubst %.cc, %.h, $(SOURCES))
OBJECTS       = $(patsubst %.cc, %.o, $(SOURCES))
ROOTCFLAGS   := $(shell root-config --cflags)
ROOTLIBS     := $(shell root-config --nonew --glibs)
CFLAGS       += $(ROOTCFLAGS) -I $(CMSSW_BASE)/src -std=c++0x -pedantic -Werror -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -g
LIBS         += $(ROOTLIBS) -lMinuit
LDFLAGS       = -O

all: $(OBJECTS)

%.o : %.cc $(INCLUDES)
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
	-rm -f $(OBJECTS)
