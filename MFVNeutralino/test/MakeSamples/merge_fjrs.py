import xml.etree.ElementTree as ET

first = ET.parse('first_fjr.xml')
first_root = first.getroot()
last = ET.parse('last_fjr.xml')

first_files = first.findall('File')
assert len(first_files) == 1
last_files = last.findall('File')
assert len(last_files) == 1

first_root.remove(first_files[0])
first_root.append(last_files[0])
first.write('FrameworkJobReport.xml')

