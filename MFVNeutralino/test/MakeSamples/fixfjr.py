import xml.etree.ElementTree as ET

x = ET.parse('tempfjr.xml')

inputs = x.findall('InputFile')
assert len(inputs) == 1
x.getroot().remove(inputs[0])

for f in x.findall('File'):
    for i in f.findall('Inputs'):
        f.remove(i)

x.write('FrameworkJobReport.xml')
