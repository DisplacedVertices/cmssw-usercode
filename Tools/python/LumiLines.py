# should merge this with general.intlumi_from_brilcalc_csv

import gzip, time
from collections import defaultdict
from JMTucker.Tools.general import from_pickle, to_pickle
from FWCore.PythonUtilities.LumiList import LumiList

class LumiLine:
    beam_statuses = {
        'STABLE BEAMS': 0,
        'ADJUST': 1,
        'SQUEEZE': 2,
        }
    sources = {
        'DT': 0,
        'PXL': 1,
        'PLTZERO': 2,
        'HFOC': 3,
        }

class LumiLines:
    run_boundary_15_16 = 260627

    @classmethod
    def load_csv(cls, fn):
        header = '#run:fill,ls,time,beamstatus,E(GeV),delivered(/ub),recorded(/ub),avgpu,source'
        seen_header = False

        lls = []

        open_ = gzip.open if fn.endswith('.gz') else open
            
        for line in open_(fn):
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                if line == header:
                    seen_header = True
            else:
                ll = LumiLine()

                run_fill, ls, utctime, beam_status, energy, delivered, recorded, avg_pu, source = line.split(',')

                run, fill = run_fill.split(':')
                ll.run = int(run)
                ll.fill = int(fill)

                ls = ls.split(':')
                assert ls[0] == ls[1] or ls[0] != '0' and ls[1] == '0'
                ll.ls = int(ls[0])

                ll.time = time.mktime(time.strptime(utctime, '%m/%d/%y %H:%M:%S'))

                ll.beam_status = LumiLine.beam_statuses[beam_status]

                ll.energy = float(energy)
                ll.delivered = float(delivered)
                ll.recorded = float(recorded)
                ll.avg_pu = float(avg_pu)
                ll.source = LumiLine.sources[source]

                lls.append(ll)
        assert seen_header
        return lls

    @classmethod
    def load(cls, fn, is_csv=False):
        if is_csv or fn.endswith('.csv') or fn.endswith('.csv.gz'):
            return cls.load_csv(fn)
        return from_pickle(fn, comp=True)

    @classmethod
    def save(cls, csv_fn, fn):
        lls = cls.load_csv(csv_fn)
        to_pickle(lls, fn, comp=True)
        return lls

    @classmethod
    def strip(cls, fn, new_fn):
        lls = from_pickle(fn, comp=True)
        for ll in lls:
            del ll.time
            del ll.beam_status
            del ll.energy
            del ll.delivered
        to_pickle(lls, new_fn, comp=True)

    def __init__(self, fn, mask_fn=None):
        self.mask = LumiList(mask_fn) if mask_fn else None
        self.lls = LumiLines.load(fn)
        self.by_run = defaultdict(list)
        self.by_run_ls = {}
        self.fills = defaultdict(lambda: 999999)
        for ll in self.lls:
            if not self.mask or (ll.run, ll.ls) in self.mask:
                self.by_run[ll.run].append(ll)
                self.by_run_ls[(ll.run, ll.ls)] = ll
                self.fills[ll.fill] = min(self.fills[ll.fill], ll.run)
        self.by_run = dict(self.by_run)

    def runs(self, year=None):
        runs = sorted(self.by_run.keys())
        rb = self.run_boundary_15_16
        if year == 2015:
            runs = [r for r in runs if r <= rb]
        elif year == 2016:
            runs = [r for r in runs if r > rb]
        else:
            assert year is None
        return runs

    def recorded(self, run):
        return sum(ll.recorded for ll in self.by_run[run])

    def avg_pu(self, run):
        s, sw = 0., 0.
        for ll in self.by_run[run]:
            rec = ll.recorded
            pu = ll.avg_pu
            sw += rec
            s += pu * rec
        return s/sw

if __name__ == '__main__':
    #import sys
    #lls = LumiLines.save(sys.argv[1], sys.argv[1].replace('.csv', '.gzpickle'))
    #LumiLines.strip('/uscms/home/tucker/public/mfv/2015plus2016.gzpickle', '/uscms/home/tucker/public/mfv/2015plus2016stripped.gzpickle')
    lls = LumiLines('/uscms/home/tucker/public/mfv/2015plus2016stripped.gzpickle')
