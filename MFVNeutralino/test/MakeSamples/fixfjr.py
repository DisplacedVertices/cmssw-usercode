import xml.etree.ElementTree as ET

x = ET.parse('tempfjr.xml')

inputs = x.findall('InputFile')
if len(inputs) != 1:
    raise ValueError('tempfjr.xml is weird, len(inputs) is %i' % len(inputs))

x.getroot().remove(inputs[0])

for f in x.findall('File'):
    for i in f.findall('Inputs'):
        f.remove(i)

x.write('FrameworkJobReport.xml')
