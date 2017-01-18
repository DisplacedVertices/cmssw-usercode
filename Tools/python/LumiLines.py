# should merge this with general.intlumi_from_brilcalc_csv

import time
from collections import defaultdict
from JMTucker.Tools.general import from_pickle, to_pickle

class LumiLine:
    beam_statuses = {
        'STABLE BEAMS': 0,
        'ADJUST': 1,
        'SQUEEZE': 2,
        }

class LumiLines:
    @classmethod
    def load_csv(cls, fn):
        header = 'Run:Fill,LS,UTCTime,Beam Status,E(GeV),Delivered(/ub),Recorded(/ub),avgPU'

        lls = []

        for line in open(fn):
            line = line.strip()
            if not line:
                continue

            try:
                ll = LumiLine()

                run_fill, ls, utctime, beam_status, energy, delivered, recorded, avg_pu = line.split(',')

                run, fill = run_fill.split(':')
                ll.run = int(run)
                ll.fill = int(fill)

                ls = ls.split(':')
                assert ls[0] == ls[1]
                ll.ls = int(ls[0])

                ll.time = time.mktime(time.strptime(utctime, '%m/%d/%y %H:%M:%S'))

                ll.beam_status = LumiLine.beam_statuses[beam_status]

                ll.energy = float(energy)
                ll.delivered = float(delivered)
                ll.recorded = float(recorded)
                ll.avg_pu = float(avg_pu)

                lls.append(ll)

            except ValueError:
                assert line == header

        return lls

    @classmethod
    def load(cls, fn, is_csv=False):
        if is_csv or fn.endswith('.csv'):
            return cls.load_csv(fn)
        return from_pickle(fn, comp=True)

    @classmethod
    def save(cls, csv_fn, fn):
        lls = cls.load_csv(csv_fn)
        to_pickle(lls, fn, comp=True)
        return lls

    def __init__(self, fn):
        self.lls = LumiLines.load(fn)
        self.by_run = defaultdict(list)
        self.by_run_ls = {}
        for ll in self.lls:
            self.by_run[ll.run].append(ll)
            self.by_run_ls[(ll.run, ll.ls)] = ll

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
    import sys
    lls = LumiLines.save(sys.argv[1], sys.argv[1].replace('.csv', '.gzpickle'))
