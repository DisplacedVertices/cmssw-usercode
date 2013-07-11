from JMTucker.Tools.ROOTTools import ROOT
f = ROOT.TFile('gen_ntuple.root')
t = f.Get('MFVGenNtupleDumper/t')

n = 200
nx, ny, nz = n,n,n

def check_it(h):
    for i in xrange(0,nx+2):
        for j in xrange(0,ny+2):
            for k in xrange(0,nz+2):
                c = h.GetBinContent(i,j) #,k)
                if c > 1:
                    x = h.GetXaxis().GetBinLowEdge(i)
                    y = h.GetYaxis().GetBinLowEdge(j)
                    z = h.GetZaxis().GetBinLowEdge(k)
                    print '%3i %3i %3i  %10.7f %10.7f %10.7f   %i' % (i,j,k,x,y,z,c)

h = ROOT.TH3D('h','',nx,0,1000,ny,-6,6,nz,-3.1416,3.1416)
t.Draw('lsp_eta:lsp_phi:lsp_pt>>h')
print 'pt eta phi'
check_it(h)
del h

h = ROOT.TH3D('h','',nx,-5,5,ny,-5,5,nz,-5,5)
t.Draw('lsp_decay_vy:lsp_decay_vz:lsp_decay_vx>>h')
print 'vx vy vz'
check_it(h)
del h
