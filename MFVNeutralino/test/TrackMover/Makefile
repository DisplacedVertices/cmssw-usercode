SOURCES       = BTagCalibrationStandalone.cc MovedTracksNtuple.cc utils.cc
INCLUDES      = $(patsubst %.cc, %.h, $(SOURCES))
OBJECTS       = $(patsubst %.cc, bin/%.o, $(SOURCES))
ROOTCFLAGS    = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --nonew --glibs)
CFLAGS        = $(ROOTCFLAGS) -I$(CMSSW_BASE)/src -std=c++0x -pedantic -Werror -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -O3
LIBS          = $(ROOTLIBS)

all: hists.exe mctruth.exe tests.exe

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
	ln -sf ../../src/MovedTracksNtuple.cc
	ln -sf $(CMSSW_RELEASE_BASE)/src/CondTools/BTau/test/BTagCalibrationStandalone.cpp BTagCalibrationStandalone.cc
	ln -sf $(CMSSW_RELEASE_BASE)/src/CondTools/BTau/test/BTagCalibrationStandalone.h BTagCalibrationStandalone.h
