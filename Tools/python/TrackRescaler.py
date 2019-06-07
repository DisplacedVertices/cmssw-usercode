from JMTucker.Tools.CMSSWTools import cmssw_base
from JMTucker.Tools.ROOTTools import ROOT

class TrackRescalerFcnsHelper(object):
    lines = []
    fcns = {}
    eras = ['2017B','2017C','2017DE','2017F','2018A','2018B','2018C','2018D']
    etas = ['lt1p5','gt1p5']
    def __init__(self):
        if not self.lines:
            self.lines = [x for x in file(cmssw_base('src/JMTucker/Tools/src/TrackRescaler.cc')) if ('p_dxy' in x or 'dxyerr' in x) and ' = ' in x and 'dsz' not in x]
            assert len(self.lines) == 32
    def __call__(self, era, eta):
        if era == '2017D' or era == '2017E':
            era = '2017DE'
        name = era + eta
        if self.fcns.has_key(name):
            return self.fcns[name]
        offset = self.eras.index(era) * 2 + self.etas.index(eta)
        pars = [float(x) for x in self.lines[offset].split('{')[1].split('}')[0].split(',')]
        fcn = self.lines[offset+1].split(' = ')[1].replace(';','').replace('p_dxy[', '[p')
        assert '[p%i]' % (len(pars)-1) in fcn        
        fcn = self.fcns[name] = ROOT.TF1('fcn_' + name, fcn, 1, 200)
        fcn.SetParameters(*pars)
        #print self.lines[offset], self.lines[offset+1], len(pars), pars
        return fcn

fcns = TrackRescalerFcnsHelper()

__all__ = ['fcns']
