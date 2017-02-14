ROOTCFLAGS    = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --libs)
CFLAGS        = $(ROOTCFLAGS) -std=c++11 -pedantic -Werror -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -g
LIBS          = $(ROOTLIBS)

all: common.exe dups.exe

%.exe: %.cc EventIdsReader.h
	g++ $(CFLAGS) $(LIBS) $< -o $@

clean:
	rm *.exe
