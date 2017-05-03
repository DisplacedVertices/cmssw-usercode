SOURCES       = MovedTracksNtuple.cc utils.cc
INCLUDES      = $(patsubst %.cc, %.h, $(SOURCES))
OBJECTS       = $(patsubst %.cc, bin/%.o, $(SOURCES))
ROOTCFLAGS    = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --nonew --glibs)
CFLAGS        = $(ROOTCFLAGS) -I$(CMSSW_BASE)/src -std=c++0x -pedantic -Werror -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -g
LIBS          = $(ROOTLIBS)

all: hists.exe mctruth.exe

%.exe: bin/%.o $(OBJECTS)
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
	-rm -f hists.exe
	-rm -rf bin/

setup:
	ln -s ../../src/MovedTracksNtuple.cc
