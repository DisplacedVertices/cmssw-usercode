import sys
import xml.etree.ElementTree as ET

x = ET.parse('tempfjr.xml')

inputs = x.findall('InputFile')
if len(inputs) != 1:
    sys.exit("fixfjr.py: tempfjr.xml is weird, len(inputs) is %i--this may be OK if we're not at the last step" % len(inputs))

x.getroot().remove(inputs[0])

for f in x.findall('File'):
    for i in f.findall('Inputs'):
        f.remove(i)

x.write('FrameworkJobReport.xml')
