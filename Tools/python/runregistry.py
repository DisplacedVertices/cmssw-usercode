#!/usr/bin/env python

from datetime import datetime 
import xml.etree.cElementTree as ET

class RunRegistryHelper:
    def __init__(self, filename, require_bfield=True):
        self.runs = ET.parse(filename).findall('RUN')
        self.require_bfield = require_bfield

    def run_dict(self):
        d = {}
        for run in self.runs:
            d[self.run_number(run)] = run
        return d

    def parse_timestamp(self, timestamp):
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.0')

    def run_number(self, run):
        return int(run.find('NUMBER').text)

    def start_time(self, run):
        return self.parse_timestamp(run.find('START_TIME').text)

    def lumisections(self, run):
        return int(run.find('LUMI_SECTIONS').text)

    def group_name(self, run):
        return run.find('GROUP_NAME').text
    
    def is_good(self, cmps, subdet):
        for cmp in cmps:
            if cmp.find('NAME').text == subdet:
                v = cmp.find('VALUE').text
                if v not in ['EXCL', 'GOOD', 'BAD', 'NOTSET']:
                    raise ValueError('value for subdet %s is weird: %s' % (subdet, v))
                if v == 'NOTSET':
                    print 'warning: %s NOTSET' % subdet
                return v == 'GOOD'
        raise ValueError('subdet %s not found!' % subdet)

    def get_good_runs(self, subdets, min_time=None, group=None):
        good = []
        
        for run in self.runs:
            if self.require_bfield and float(run.find('BFIELD').text) < 3.79:
                continue

            if min_time is not None and self.parse_timestamp(run.find('START_TIME').text) < min_time:
                continue

            if group is not None and self.group_name(run) != group:
                continue

            run_number = self.run_number(run)

            datasets = run.find('DATASETS').findall('DATASET')
            if not datasets:
                raise ValueError('datasets is empty for run %i!' % run_number)

            # use the ratings in the newest created dataset
            datasets.sort(key=lambda ds: self.parse_timestamp(ds.find('CREATE_TIME').text))
            ds = datasets[-1]
            cmps = ds.find('CMPS').findall('CMP')

            if all(self.is_good(cmps, subdet) for subdet in subdets):
                good.append(run_number)

        good.sort()
        return good


if __name__ == '__main__':
    min_time = datetime(2010, 4, 1)
    rrh = RunRegistryHelper('download.xml')
    dt_st = rrh.get_good_runs(['DT', 'STRIP'], min_time)
    dt_px_st = rrh.get_good_runs(['DT', 'PIX', 'STRIP'], min_time)
