#!/usr/bin/env python

import xml.etree.cElementTree as ET

class fjr_reader:
    def __init__(self, filename):
        self.in_files = 0
        self.in_events = 0
        self.out_events = 0
        for event, elem in ET.iterparse(filename):
            if elem.tag == 'TotalEvents':
                assert(self.out_events == 0)
                self.out_events = int(elem.text)
            elif elem.tag == 'EventsRead':
                self.in_files += 1
                self.in_events +=  int(elem.text)

if __name__ == '__main__':
    import sys
    fjrs = [fjr_reader(fn) for fn in sys.argv if '.xml' in fn]

    
