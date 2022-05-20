import re
from JMTucker.Tools.general import popen

class EdmBranch(object):
    re = re.compile('(\S+) ([0-9.]+) ([0-9.]+)')

    def __init__(self, s):
        self.name, s1, s2 = s.strip().split()
        self.uncompressed_avg_size = float(s1)
        self.avg_size = float(s2)

    def __repr__(self):
        return '<EdmBranch %s %f %f>' % (self.name, self.uncompressed_avg_size, self.avg_size)

class EdmTree(object):
    re = re.compile('File .+ Events (\d+)')

    def __init__(self, name, output):
        self.name = name
        self.nevents = None
        self.branches = []

        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue

            mo = self.re.match(line)
            if mo:
                self.nevents = int(mo.group(1))
            else:
                mo = EdmBranch.re.match(line)
                if mo:
                    self.branches.append(EdmBranch(line))

        if self.nevents is None or not self.branches:
            raise ValueError('failed to parse edmEventSize output for %s:\n%s' % (name, output))

    def size(self, uncompressed=False):
        return sum((b.uncompressed_avg_size if uncompressed else b.avg_size) for b in self.branches) * self.nevents

    def __repr__(self):
        return '<EdmTree name=%s nevents=%i nbranches=%i size=%f>' % (self.name, self.nevents, len(self.branches), self.size())

class EdmFileInfo(object):
    all_trees = ('Events','Runs','LuminosityBlocks','MetaData','ParameterSets')
    non_metadata_trees = ('Events','Runs','LuminosityBlocks')
    event_tree_only = ('Events',)

    def __init__(self, fn, trees=None):
        self.fn = fn
        if (fn.startswith('/store/user') or (fn.startswith('/store/group'))):
            fn = 'root://cmseos.fnal.gov/' + fn
        elif fn.startswith('/store'):
            fn = 'root://cmsxrootd.fnal.gov/' + fn

        if not trees:
            trees = EdmFileInfo.event_tree_only
        self.trees = [EdmTree(name, popen('edmEventSize -vn %s %s' % (name,fn))) for name in trees]
        for t in self.trees:
            setattr(self, t.name, t)

    def size(self):
        return sum(t.size() for t in self.trees)

    def __repr__(self):
        return '<EdmFileInfo fn=%s parsed_trees=%s apparent_size=%f>' % (self.fn, ','.join(t.name for t in self.trees), self.size())

if __name__ == '__main__':
    x = EdmFileInfo('ntuple_1.root')
    print repr(x)
