# should merge this with general.intlumi_from_brilcalc_csv

import gzip, time, sys
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
        'HFET': 4,
        'BCM1F': 5,
        }

class LumiLines:
    ls_time = 2**18 / 11245.5
    # runs for each year, inclusive
    year_boundaries = {2015: (254227, 260627),
                       2016: (272760, 284044),
                       2017: (297047, 306460),
                       2018: (315252, 325175),
                       '2017p8': (297047, 325175),
                       }
    years = sorted(year_boundaries.keys())
    # starting runs of each era
    era_boundaries = [254227, 256630,                                                 # 2015 C D
                      272760, 273150, 275656, 276315, 276831, 277932, 278820, 281613, # 2016 B1 B2 C D E F G H2
                      297047, 299368, 302031, 303824, 305040,                         # 2017 B C D E F
                      315252, 317080, 319337, 325175,                                 # 2018 A B C D
                      ]

    @classmethod
    def year_from_run(cls, run):
        for year in cls.years:
            a,b = cls.year_boundaries[year]
            if a <= run <= b:
                return year

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
        self.fill_boundaries = sorted(self.fills.values())
        self.by_run = dict(self.by_run)

    def runs(self, year=None):
        runs = sorted(self.by_run.keys())
        ra,rb = self.year_boundaries[year]
        return [r for r in runs if ra <= r <= rb]

    def _sumintlumi(self, run_or_year=None, which=None):
        if run_or_year is None:
            return sum(self._sumintlumi(year, which) for year in LumiLines.years)
        elif run_or_year in LumiLines.years:
            return sum(self._sumintlumi(run, which) for run in self.runs(run_or_year))
        else:
            return sum(which(ll) for ll in self.by_run[run_or_year])

    def delivered(self, run_or_year=None):
        return self._sumintlumi(run_or_year, lambda ll: ll.delivered)
    def recorded(self, run_or_year=None):
        return self._sumintlumi(run_or_year, lambda ll: ll.recorded)

    def avg_inst(self, run):
        n, s = 0, 0.
        for ll in self.by_run[run]:
            s += ll.delivered / self.ls_time
            n += 1
        return s/n

    def max_inst(self, run):
        return max(ll.delivered for ll in self.by_run[run]) / self.ls_time

    def avg_pu(self, run):
        s, sw = 0., 0.
        for ll in self.by_run[run]:
            rec = ll.recorded
            pu = ll.avg_pu
            sw += rec
            s += pu * rec
        return s/sw

if __name__ == '__main__':
    year = '2017p8'
    LumiLines.save('/uscms/home/tucker/public/mfv/lumi/%s.byls.csv.gz' % year,
                   '/uscms/home/tucker/public/mfv/lumi/%s.gzpickle'    % year)
    LumiLines.strip('/uscms/home/tucker/public/mfv/lumi/%s.gzpickle'          % year,
                    '/uscms/home/tucker/public/mfv/lumi/%s.stripped.gzpickle' % year)

    if 0:
        lls = LumiLines('/uscms/home/tucker/public/mfv/lumi/2017stripped.gzpickle')
        eb = lls.era_boundaries[:] + [1000000]
        bins = [ [x,y,-1,0,0] for x,y in zip(eb, eb[1:]) ]
        print bins
        for run in lls.runs(2017):
            for i in xrange(len(bins)):
                x,y,r,m,s = bins[i]
                if x <= run < y:
                    recorded = lls.recorded(run)
                    s += recorded
                    if recorded > m:
                        m = recorded
                        r = run
                    bins[i] = x,y,r,m,s
        ss = 0
        for x,y,r,m,s in bins:
            ss += s
            print x,y,r,m,s
        print ss
