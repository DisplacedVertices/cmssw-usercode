import numpy as np
from bigsigscan import *
from DVCode.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

class costheta_helper:
    def __init__(self):
        self.cache = {}

        self.masses = range(200, 1001, 200)
        self.masses.insert(1, 300)
        assert all(mb - ma > 0 for ma, mb in zip(self.masses, self.masses[1:]))

        self.files = [ROOT.TFile('crab/CorrelationsForGeomEff/mfv_neutralino_tau1000um_M%04i.root' % m) for m in self.masses]
        self.hists = [f.Get('h_costheta') for f in self.files]

        self.mh = zip(self.masses, self.hists)
        self.mh = zip(self.mh, self.mh[1:])

        for h in self.hists:
            h.Rebin2D(5,5)
            for ix in xrange(1, h.GetNbinsX()+1):
                for iy in xrange(1, h.GetNbinsY()+1):
                    assert h.GetBinContent(ix, iy)
            h.Scale(1./h.Integral())

    def sample(self, mass, N):
        #print mass, self.cache
        if self.cache.has_key(mass):
            h = self.cache[mass]
        else:
            for (ma,ha), (mb,hb) in self.mh:
                if mass <= ma:
                    h = ha
                elif mass >= mb:
                    h = hb
                elif ma <= mass <= mb:
                    h = ha.Clone('h%i' % mass)
                    h.SetDirectory(0)
                    self.cache[mass] = h

                    t = (mass - ma) / (mb - ma)
                    h.Add(ha, hb, 1-t, t)

        a, p = [], []
        xax = h.GetXaxis()
        yax = h.GetYaxis()
        for ix in xrange(1, h.GetNbinsX()+1):
            x = xax.GetBinCenter(ix)
            for iy in xrange(1, h.GetNbinsY()+1):
                y = yax.GetBinCenter(iy)

                a.append((x,y))
                p.append(h.GetBinContent(ix, iy))

        #return np.random.choice(a, size=N, replace=True, p)
        a = np.asarray(a)
        p = np.asarray(p)
        cdf = np.cumsum(p)

        unif = np.random.random_sample(N)
        idx = cdf.searchsorted(unif, side='right')
        return a[idx]

ch = costheta_helper()

def guess(tau, mass, N=10000):
    dbv_cut = 25000
    dvv_cut = 800

    betagamma = 16.7*mass**-0.46
    betagamma = np.random.normal(betagamma, betagamma*0.1, (N,2))
    r = betagamma * np.random.exponential(tau, (N,2))
    costheta = ch.sample(mass, N)
    sintheta = (1 - costheta**2)**0.5
    phi = np.random.uniform(-np.pi, np.pi, N)
    phi = np.column_stack((phi, np.pi + phi))

    l = r * sintheta
    x = l * np.cos(phi)
    y = l * np.sin(phi)

    dbv = (x**2 + y**2)**0.5
    dvv = ((x[...,0] - x[...,1])**2 + (y[...,0] - y[...,1])**2)**0.5

    And = np.logical_and
    passes = And(And(dbv[...,0] < dbv_cut, dbv[...,1] < dbv_cut), dvv > dvv_cut)
    n = np.count_nonzero(passes)
    return float(n)/N

def parse_gluglu():
    gluglu = [eval(x.strip()) for x in open('/afs/fnal.gov/files/home/room3/tucker/gluglu.csv').readlines() if x.strip()]
    gluglu = [(z[0], z[1]*1000, z[2]/100*z[1]*1000) for z in gluglu] # convert pb to fb and percent to absolute
    return gluglu

def guess_exclusion():
    h = ROOT.TH2F('h_guess_exclusion', '', 12, 400, 1600, 1990, 50000, 1e7)
    gluglu = parse_gluglu()
    gluglu = dict((m, (s, es)) for m, s, es in gluglu)
    for (imass, itau0), (mass, tau0), c in bin_iterator(h, bin_values=True):
        g = guess(tau0, mass)
        if g:
            eff = g/1.5
            lim = 0.3/eff
            s, es = gluglu[mass]
            h.SetBinContent(imass, itau0, 1 if lim < s-es else 0)
    return h

def ratio():
    h = book('h', '')
    for num, tau0, mass in all_points():
        guess_eff = guess(tau0, mass)
        real_eff = num2eff(num, 800)
        bin = h.FindBin(mass, tau0)
        print num, tau0, mass, guess_eff, real_eff
        h.SetBinContent(bin, guess_eff / real_eff)
    return h

def extrap():
    ts = array('d', tau0s[:] + range(44000, 1000001, 2000))
    nts = len(ts)-1
    h = ROOT.TH1F('hextrap', '', nts, ts)
    h.SetStats(0)
    for i, tau0 in enumerate(ts):
        h.SetBinContent(i+1, guess(tau0, 800))
    return h
    
def go():
    set_style()
    rainbow_palette()
    ps = plot_saver('/uscms/home/tucker/asdf/plots/mfvlimits_guess', log=False, size=(600,600))

    h = ratio()
    h.Draw('colz')
    ps.save('ratio')
    h.GetYaxis().SetRangeUser(5000, 44000)
    ps.save('ratioz1')
    h.GetXaxis().SetRangeUser(400,  1600)
    ps.save('ratioz2')

    h = extrap()
    h.Draw()
    ps.save('extrap')

    h = guess_exclusion()
    h.Draw('colz')
    ps.save('guess_exclusion')

if __name__ == '__main__':
    go()
