import FWCore.ParameterSet.Config as cms

myttbarBowing = cms.PSet(
    X0 = cms.double(0.246344),
    Y0 = cms.double(0.389749),
    Z0 = cms.double(0.402745),
    SigmaZ = cms.double(5.98845),
    dxdz = cms.double(1.70494e-05),
    dydz = cms.double(-2.13481e-06),
    BeamWidthX = cms.double(0.00151667),
    BeamWidthY = cms.double(0.00151464),
    covariance = cms.vdouble(1.24561e-10, 5.32196e-13, 0, 0, 0, 0, 0, 1.24935e-10, 0, 0, 0, 0, 0, 0.00445375, 0, 0, 0, 0, 0.00222686, 0, 0, 0, 3.36155e-12, 2.7567e-14, 0, 3.37374e-12, 0, 2.97592e-10),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )

myttbarCurl = cms.PSet(
    X0 = cms.double(0.246597),
    Y0 = cms.double(0.38699),
    Z0 = cms.double(0.314451),
    SigmaZ = cms.double(5.99379),
    dxdz = cms.double(-1.9081e-06),
    dydz = cms.double(-1.02914e-05),
    BeamWidthX = cms.double(0.00147516),
    BeamWidthY = cms.double(0.00150106),
    covariance = cms.vdouble(1.23255e-10, 5.60119e-13, 0, 0, 0, 0, 0, 1.22964e-10, 0, 0, 0, 0, 0, 0.0045269, 0, 0, 0, 0, 0.00226344, 0, 0, 0, 3.30386e-12, 2.14557e-14, 0, 3.3566e-12, 0, 2.93467e-10),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )

myttbarElliptical = cms.PSet(
    X0 = cms.double(0.246156),
    Y0 = cms.double(0.389613),
    Z0 = cms.double(0.288198),
    SigmaZ = cms.double(5.97317),
    dxdz = cms.double(5.21863e-06),
    dydz = cms.double(7.79036e-06),
    BeamWidthX = cms.double(0.00149346),
    BeamWidthY = cms.double(0.00148959),
    covariance = cms.vdouble(1.23521e-10, 8.78629e-13, 0, 0, 0, 0, 0, 1.22967e-10, 0, 0, 0, 0, 0, 0.00439882, 0, 0, 0, 0, 0.0021994, 0, 0, 0, 3.33981e-12, 3.81918e-14, 0, 3.32571e-12, 0, 2.91985e-10),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )

myttbarRadial = cms.PSet(
    X0 = cms.double(0.246322),
    Y0 = cms.double(0.389811),
    Z0 = cms.double(0.327943),
    SigmaZ = cms.double(6.08119),
    dxdz = cms.double(6.83738e-06),
    dydz = cms.double(1.8884e-07),
    BeamWidthX = cms.double(0.00149758),
    BeamWidthY = cms.double(0.00153033),
    covariance = cms.vdouble(1.22914e-10, 5.21468e-13, 0, 0, 0, 0, 0, 1.24135e-10, 0, 0, 0, 0, 0, 0.00459276, 0, 0, 0, 0, 0.00229637, 0, 0, 0, 3.28346e-12, 1.84415e-14, 0, 3.32401e-12, 0, 2.91313e-10),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )

myttbarSagitta = cms.PSet(
    X0 = cms.double(0.235756),
    Y0 = cms.double(0.389839),
    Z0 = cms.double(0.451828),
    SigmaZ = cms.double(5.9656),
    dxdz = cms.double(-6.12007e-06),
    dydz = cms.double(-3.34286e-06),
    BeamWidthX = cms.double(0.00142781),
    BeamWidthY = cms.double(0.00146079),
    covariance = cms.vdouble(1.21587e-10, 1.2445e-12, 0, 0, 0, 0, 0, 1.22063e-10, 0, 0, 0, 0, 0, 0.00443525, 0, 0, 0, 0, 0.00221762, 0, 0, 0, 3.24618e-12, 2.20384e-14, 0, 3.29028e-12, 0, 2.87833e-10),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )

myttbarSkew = cms.PSet(
    X0 = cms.double(0.246258),
    Y0 = cms.double(0.389962),
    Z0 = cms.double(0.386416),
    SigmaZ = cms.double(6.02712),
    dxdz = cms.double(-0.00011416),
    dydz = cms.double(-7.07232e-06),
    BeamWidthX = cms.double(0.00164608),
    BeamWidthY = cms.double(0.00151397),
    covariance = cms.vdouble(1.26645e-10, 7.7728e-14, 0, 0, 0, 0, 0, 1.25663e-10, 0, 0, 0, 0, 0, 0.00445011, 0, 0, 0, 0, 0.00222484, 0, 0, 0, 3.39247e-12, 1.9986e-14, 0, 3.34669e-12, 0, 3.14378e-10),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )

myttbarTelescope = cms.PSet(
    X0 = cms.double(0.245667),
    Y0 = cms.double(0.386495),
    Z0 = cms.double(0.425672),
    SigmaZ = cms.double(6.16219),
    dxdz = cms.double(3.75215e-06),
    dydz = cms.double(-1.91476e-06),
    BeamWidthX = cms.double(0),
    BeamWidthY = cms.double(0),
    covariance = cms.vdouble(3.44758e-10, 3.61193e-13, 0, 0, 0, 0, 0, 3.46413e-10, 0, 0, 0, 0, 0, 0.000100795, 0, 0, 0, 0, 9.63705e-05, 0, 0, 0, 9.41413e-12, 7.89166e-14, 0, 9.46686e-12, 0, 0),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )

myttbarTwist = cms.PSet(
    X0 = cms.double(0.246196),
    Y0 = cms.double(0.389666),
    Z0 = cms.double(0.293139),
    SigmaZ = cms.double(6.0066),
    dxdz = cms.double(4.09512e-06),
    dydz = cms.double(1.19775e-05),
    BeamWidthX = cms.double(0.00148173),
    BeamWidthY = cms.double(0.00149055),
    covariance = cms.vdouble(1.22449e-10, 0, 0, 0, 0, 0, 0, 1.22109e-10, 0, 0, 0, 0, 0, 0.0045879, 0, 0, 0, 0, 0.00229394, 0, 0, 0, 3.27196e-12, 7.22971e-15, 0, 3.27492e-12, 0, 2.89948e-10),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )

myttbarZexpansion = cms.PSet(
    X0 = cms.double(0.246214),
    Y0 = cms.double(0.389698),
    Z0 = cms.double(0.394112),
    SigmaZ = cms.double(6.00186),
    dxdz = cms.double(3.61695e-06),
    dydz = cms.double(1.45456e-06),
    BeamWidthX = cms.double(0.0014962),
    BeamWidthY = cms.double(0.00149599),
    covariance = cms.vdouble(1.24303e-10, 7.70197e-13, 0, 0, 0, 0, 0, 1.22716e-10, 0, 0, 0, 0, 0, 0.00449324, 0, 0, 0, 0, 0.00224661, 0, 0, 0, 3.3007e-12, 2.37285e-14, 0, 3.20966e-12, 0, 2.94185e-10),
    EmittanceX = cms.double(0),
    EmittanceY = cms.double(0),
    BetaStar = cms.double(0),
    )


'''
covs = ['myttbarbowing','myttbarcurl','myttbarelliptical','myttbarradial','myttbarsagitta','myttbarskew','myttbartelescope','myttbartwist','myttbarzexpansion']
covs = [(name, eval('%s.covariance.value()' % name)) for name in covs]
for name, cov in covs:
    assert len(cov) == 49
    covsnew = []
    for i in xrange(7):
        for j in xrange(i, 7):
            assert cov[i+j*7] == cov[j+i*7]
            covsnew.append(cov[i+j*7])
    assert len(covsnew) == 28
    covsnew = [('%.6g' % c if c > 0 else '0') for c in covsnew]
    covsnew = ', '.join(covsnew)
    print name
    print '    covariance = cms.vdouble(%s),' % covsnew
'''
