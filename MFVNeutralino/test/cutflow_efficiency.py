#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import ROOT
from array import array

file_path = '~/crabdirs/TheoristRecipeV20'

gen_rec_cut = 20

#gen_num = 'FourJets'
#gen_num = 'HT40'
#gen_num = 'Ntracks1'
#gen_num = 'Geo2ddist'
#gen_num = 'Bsbs2ddist'
#gen_num = 'Sumpt300'
gen_num = 'Dvv400um'

rec_den = 'NoCuts'
gen_den = 'NoCuts'
iden = 0

#rec_den = 'OfflineJets'
#gen_den = 'FourJets'
#iden = 1

#rec_den = 'PreSel'
#gen_den = 'HT40'
#iden = 3

#rec_den = 'TwoVtxNtracks'
#gen_den = 'Ntracks1'
#iden = 5

#rec_den = 'TwoVtxGeo2ddist'
#gen_den = 'Geo2ddist'
#iden = 6

#rec_den = 'TwoVtxBsbs2ddist'
#gen_den = 'Bsbs2ddist'
#iden = 7

#rec_den = 'TwoVtxBs2derr'
#gen_den = 'Sumpt300'
#iden = 8

reconstructed = ['NoCuts', 'OfflineJets', 'TrigSel', 'PreSel', 'TwoVtxNoCuts', 'TwoVtxNtracks', 'TwoVtxGeo2ddist', 'TwoVtxBsbs2ddist', 'TwoVtxBs2derr', 'TwoVtxDvv400um']
generated = ['NoCuts', 'FourJets', '', 'HT40', '', 'Ntracks1', 'Geo2ddist', 'Bsbs2ddist', 'Sumpt300', 'Dvv400um']

samples = [
    ('mfv_neu_tau00100um_M0300',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_neu_tau00100um_M0400',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_neu_tau00100um_M0500',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_neu_tau00100um_M0600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_neu_tau00100um_M0800',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_neu_tau00100um_M1200',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_neu_tau00100um_M1600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_neu_tau00100um_M3000',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_neu_tau00300um_M0300',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_neu_tau00300um_M0400',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_neu_tau00300um_M0500',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_neu_tau00300um_M0600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_neu_tau00300um_M0800',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_neu_tau00300um_M1200',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_neu_tau00300um_M1600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_neu_tau00300um_M3000',              r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_neu_tau01000um_M0300',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_neu_tau01000um_M0400',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_neu_tau01000um_M0500',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_neu_tau01000um_M0600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_neu_tau01000um_M0800',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neu_tau01000um_M1200',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_neu_tau01000um_M1600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_neu_tau01000um_M3000',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_neu_tau10000um_M0300',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_neu_tau10000um_M0400',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_neu_tau10000um_M0500',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_neu_tau10000um_M0600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_neu_tau10000um_M0800',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_neu_tau10000um_M1200',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_neu_tau10000um_M1600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neu_tau10000um_M3000',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_neu_tau30000um_M0300',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_neu_tau30000um_M0400',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_neu_tau30000um_M0500',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_neu_tau30000um_M0600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_neu_tau30000um_M0800',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_neu_tau30000um_M1200',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_neu_tau30000um_M1600',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_neu_tau30000um_M3000',              r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M = 3000\GeV$'),
    ('mfv_ddbar_tau00100um_M0300',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_ddbar_tau00100um_M0400',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_ddbar_tau00100um_M0500',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_ddbar_tau00100um_M0600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_ddbar_tau00100um_M0800',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_ddbar_tau00100um_M1200',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau00100um_M1600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau00100um_M3000',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_ddbar_tau00300um_M0300',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_ddbar_tau00300um_M0400',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_ddbar_tau00300um_M0500',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_ddbar_tau00300um_M0600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_ddbar_tau00300um_M0800',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_ddbar_tau00300um_M1200',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau00300um_M1600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau00300um_M3000',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_ddbar_tau01000um_M0300',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_ddbar_tau01000um_M0400',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_ddbar_tau01000um_M0500',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_ddbar_tau01000um_M0600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_ddbar_tau01000um_M0800',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_ddbar_tau01000um_M1200',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau01000um_M1600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau01000um_M3000',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_ddbar_tau10000um_M0300',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_ddbar_tau10000um_M0400',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_ddbar_tau10000um_M0500',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_ddbar_tau10000um_M0600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_ddbar_tau10000um_M0800',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_ddbar_tau10000um_M1200',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau10000um_M1600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau10000um_M3000',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_ddbar_tau30000um_M0300',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_ddbar_tau30000um_M0400',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_ddbar_tau30000um_M0500',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_ddbar_tau30000um_M0600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_ddbar_tau30000um_M0800',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_ddbar_tau30000um_M1200',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau30000um_M1600',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau30000um_M3000',            r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M = 3000\GeV$'),
    ('mfv_neu_tau00100um_M0300_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_neu_tau00100um_M0400_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_neu_tau00100um_M0600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_neu_tau00100um_M0800_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_neu_tau00100um_M1200_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_neu_tau00100um_M1600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_neu_tau00300um_M0300_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_neu_tau00300um_M0400_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_neu_tau00300um_M0600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_neu_tau00300um_M0800_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_neu_tau00300um_M1200_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_neu_tau00300um_M1600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_neu_tau01000um_M0300_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_neu_tau01000um_M0400_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_neu_tau01000um_M0600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_neu_tau01000um_M0800_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neu_tau01000um_M1200_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_neu_tau01000um_M1600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_neu_tau10000um_M0600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_neu_tau10000um_M0800_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_neu_tau10000um_M1200_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_neu_tau10000um_M1600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neu_tau30000um_M0300_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_neu_tau30000um_M0400_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_neu_tau30000um_M0600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_neu_tau30000um_M0800_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_neu_tau30000um_M1200_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_neu_tau30000um_M1600_hip1p0_mit',   r'$\tilde{N} \rightarrow tbs$,      $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau00100um_M0300_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_ddbar_tau00100um_M0400_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_ddbar_tau00100um_M0600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_ddbar_tau00100um_M0800_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_ddbar_tau00100um_M1200_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau00100um_M1600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau00300um_M0300_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_ddbar_tau00300um_M0400_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_ddbar_tau00300um_M0600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_ddbar_tau00300um_M0800_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_ddbar_tau00300um_M1200_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau00300um_M1600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau01000um_M0300_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_ddbar_tau01000um_M0400_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_ddbar_tau01000um_M0600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_ddbar_tau01000um_M0800_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_ddbar_tau01000um_M1200_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau01000um_M1600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau10000um_M0300_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_ddbar_tau10000um_M0400_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_ddbar_tau10000um_M0600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_ddbar_tau10000um_M0800_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_ddbar_tau10000um_M1200_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau10000um_M1600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_ddbar_tau30000um_M0300_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_ddbar_tau30000um_M0400_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_ddbar_tau30000um_M0600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_ddbar_tau30000um_M0800_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_ddbar_tau30000um_M1200_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_ddbar_tau30000um_M1600_hip1p0_mit', r'$\tilde{g} \rightarrow d\bar{d}$, $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_bbbar_tau00100um_M0300',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_bbbar_tau00100um_M0400',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_bbbar_tau00100um_M0500',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_bbbar_tau00100um_M0600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_bbbar_tau00100um_M0800',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_bbbar_tau00100um_M1200',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_bbbar_tau00100um_M1600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_bbbar_tau00100um_M3000',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_bbbar_tau00300um_M0300',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_bbbar_tau00300um_M0400',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_bbbar_tau00300um_M0500',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_bbbar_tau00300um_M0600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_bbbar_tau00300um_M0800',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_bbbar_tau00300um_M1200',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_bbbar_tau00300um_M1600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_bbbar_tau00300um_M3000',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_bbbar_tau01000um_M0300',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_bbbar_tau01000um_M0400',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_bbbar_tau01000um_M0500',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_bbbar_tau01000um_M0600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_bbbar_tau01000um_M0800',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_bbbar_tau01000um_M1200',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_bbbar_tau01000um_M1600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_bbbar_tau01000um_M3000',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_bbbar_tau10000um_M0300',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_bbbar_tau10000um_M0400',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_bbbar_tau10000um_M0500',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_bbbar_tau10000um_M0600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_bbbar_tau10000um_M0800',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_bbbar_tau10000um_M1200',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_bbbar_tau10000um_M1600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_bbbar_tau10000um_M3000',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_bbbar_tau30000um_M0300',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_bbbar_tau30000um_M0400',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_bbbar_tau30000um_M0500',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_bbbar_tau30000um_M0600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_bbbar_tau30000um_M0800',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_bbbar_tau30000um_M1200',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_bbbar_tau30000um_M1600',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_bbbar_tau30000um_M3000',            r'$\tilde{g} \rightarrow b\bar{b}$, $c\tau =   30\mm$, $M = 3000\GeV$'),
    ('mfv_uds_tau00100um_M0300',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_uds_tau00100um_M0400',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_uds_tau00100um_M0500',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_uds_tau00100um_M0600',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_uds_tau00100um_M0800',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_uds_tau00100um_M1200',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_uds_tau00100um_M1600',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_uds_tau00100um_M3000',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_uds_tau00300um_M0300',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_uds_tau00300um_M0400',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_uds_tau00300um_M0500',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_uds_tau00300um_M0600',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_uds_tau00300um_M0800',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_uds_tau00300um_M1200',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_uds_tau00300um_M1600',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_uds_tau00300um_M3000',              r'$\tilde{g} \rightarrow uds$,      $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_uds_tau01000um_M0300',              r'$\tilde{g} \rightarrow uds$,      $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_uds_tau01000um_M0400',              r'$\tilde{g} \rightarrow uds$,      $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_uds_tau01000um_M0500',              r'$\tilde{g} \rightarrow uds$,      $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_uds_tau01000um_M0600',              r'$\tilde{g} \rightarrow uds$,      $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_uds_tau01000um_M0800',              r'$\tilde{g} \rightarrow uds$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_uds_tau01000um_M1200',              r'$\tilde{g} \rightarrow uds$,      $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_uds_tau01000um_M1600',              r'$\tilde{g} \rightarrow uds$,      $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_uds_tau01000um_M3000',              r'$\tilde{g} \rightarrow uds$,      $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_uds_tau10000um_M0300',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_uds_tau10000um_M0400',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_uds_tau10000um_M0500',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_uds_tau10000um_M0600',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_uds_tau10000um_M0800',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_uds_tau10000um_M1200',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_uds_tau10000um_M1600',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_uds_tau10000um_M3000',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_uds_tau30000um_M0300',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_uds_tau30000um_M0400',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_uds_tau30000um_M0500',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_uds_tau30000um_M0600',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_uds_tau30000um_M0800',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_uds_tau30000um_M1200',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_uds_tau30000um_M1600',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_uds_tau30000um_M3000',              r'$\tilde{g} \rightarrow uds$,      $c\tau =   30\mm$, $M = 3000\GeV$'),
    ('mfv_neuuds_tau00100um_M0300',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_neuuds_tau00100um_M0400',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_neuuds_tau00100um_M0500',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_neuuds_tau00100um_M0600',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_neuuds_tau00100um_M0800',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_neuuds_tau00100um_M1200',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_neuuds_tau00100um_M1600',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_neuuds_tau00100um_M3000',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_neuuds_tau00300um_M0300',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_neuuds_tau00300um_M0400',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_neuuds_tau00300um_M0500',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_neuuds_tau00300um_M0600',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_neuuds_tau00300um_M0800',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_neuuds_tau00300um_M1200',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_neuuds_tau00300um_M1600',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_neuuds_tau00300um_M3000',           r'$\tilde{N} \rightarrow uds$,      $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_neuuds_tau01000um_M0300',           r'$\tilde{N} \rightarrow uds$,      $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_neuuds_tau01000um_M0400',           r'$\tilde{N} \rightarrow uds$,      $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_neuuds_tau01000um_M0500',           r'$\tilde{N} \rightarrow uds$,      $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_neuuds_tau01000um_M0600',           r'$\tilde{N} \rightarrow uds$,      $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_neuuds_tau01000um_M0800',           r'$\tilde{N} \rightarrow uds$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neuuds_tau01000um_M1200',           r'$\tilde{N} \rightarrow uds$,      $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_neuuds_tau01000um_M1600',           r'$\tilde{N} \rightarrow uds$,      $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_neuuds_tau01000um_M3000',           r'$\tilde{N} \rightarrow uds$,      $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_neuuds_tau10000um_M0300',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_neuuds_tau10000um_M0400',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_neuuds_tau10000um_M0500',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_neuuds_tau10000um_M0600',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_neuuds_tau10000um_M0800',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_neuuds_tau10000um_M1200',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_neuuds_tau10000um_M1600',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neuuds_tau10000um_M3000',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_neuuds_tau30000um_M0300',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_neuuds_tau30000um_M0400',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_neuuds_tau30000um_M0500',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_neuuds_tau30000um_M0600',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_neuuds_tau30000um_M0800',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_neuuds_tau30000um_M1200',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_neuuds_tau30000um_M1600',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_neuuds_tau30000um_M3000',           r'$\tilde{N} \rightarrow uds$,      $c\tau =   30\mm$, $M = 3000\GeV$'),
    ('mfv_neuudmu_tau00100um_M0300',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_neuudmu_tau00100um_M0400',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_neuudmu_tau00100um_M0500',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_neuudmu_tau00100um_M0600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_neuudmu_tau00100um_M0800',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_neuudmu_tau00100um_M1200',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_neuudmu_tau00100um_M1600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_neuudmu_tau00100um_M3000',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_neuudmu_tau00300um_M0300',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_neuudmu_tau00300um_M0400',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_neuudmu_tau00300um_M0500',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_neuudmu_tau00300um_M0600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_neuudmu_tau00300um_M0800',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_neuudmu_tau00300um_M1200',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_neuudmu_tau00300um_M1600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_neuudmu_tau00300um_M3000',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_neuudmu_tau01000um_M0300',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_neuudmu_tau01000um_M0400',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_neuudmu_tau01000um_M0500',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_neuudmu_tau01000um_M0600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_neuudmu_tau01000um_M0800',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neuudmu_tau01000um_M1200',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_neuudmu_tau01000um_M1600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_neuudmu_tau01000um_M3000',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_neuudmu_tau10000um_M0300',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_neuudmu_tau10000um_M0400',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_neuudmu_tau10000um_M0500',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_neuudmu_tau10000um_M0600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_neuudmu_tau10000um_M0800',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_neuudmu_tau10000um_M1200',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_neuudmu_tau10000um_M1600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neuudmu_tau10000um_M3000',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_neuudmu_tau30000um_M0300',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_neuudmu_tau30000um_M0400',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_neuudmu_tau30000um_M0500',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_neuudmu_tau30000um_M0600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_neuudmu_tau30000um_M0800',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_neuudmu_tau30000um_M1200',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_neuudmu_tau30000um_M1600',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_neuudmu_tau30000um_M3000',          r'$\tilde{N} \rightarrow ud\mu$,    $c\tau =   30\mm$, $M = 3000\GeV$'),
    ]

def style(sample):
    model = sample.split('_tau')[0]
    for i in range(1, len(sample.split('M')[1].split('_'))):
        model += '_' + sample.split('M')[1].split('_')[i]
    if model == 'mfv_neu':
        return 20
    if model == 'mfv_ddbar':
        return 22
    if model == 'mfv_neu_hip1p0_mit':
        return 24
    if model == 'mfv_ddbar_hip1p0_mit':
        return 26
    if model == 'mfv_bbbar':
        return 23
    if model == 'mfv_uds':
        return 21
    if model == 'mfv_neuuds':
        return 34
    if model == 'mfv_neuudmu':
        return 33

def color(sample):
    mass = sample.split('M')[1].split('_')[0]
    if mass == '0300':
        return 1
    if mass == '0400':
        return 2
    if mass == '0500':
        return 3
    if mass == '0600':
        return 4
    if mass == '0800':
        return 6
    if mass == '1200':
        return 7
    if mass == '1600':
        return 8
    if mass == '3000':
        return 9

matched = []
not_matched = []
x = []
y = []
ex = []
ey = []
gs = []
l1 = ROOT.TLegend(0.75,0.1,0.95,0.5)
l2 = ROOT.TLegend(0.75,0.5,0.95,0.9)
for sample,sampleName in samples:
    print sample
    f = ROOT.TFile('%s/%s.root' % (file_path, sample))
    nrec = f.Get('mfvTheoristRecipe%s/h_gen_dvv'%rec_den).GetEntries()
    ngen = f.Get('mfvGen%s/h_gen_dvv'%gen_den).GetEntries()
    print '%26s%26s%20s%20s%20s' % ('reconstructed', 'generated', 'reco eff +/- error', 'gen eff +/- error', 'gen/reco +/- error')
    for i, rec in enumerate(reconstructed):
        if i < iden:
            continue
        rec_hist = f.Get('mfvTheoristRecipe%s/h_gen_dvv'%rec)
        rec_eff = rec_hist.GetEntries()/nrec
        rec_err = (rec_eff * (1-rec_eff) / nrec)**0.5
        if generated[i] != '':
            gen_hist = f.Get('mfvGen%s/h_gen_dvv'%generated[i])
            gen_eff = gen_hist.GetEntries()/ngen
            gen_err = (gen_eff * (1-gen_eff) / ngen)**0.5
            gen_rec_div = gen_eff/rec_eff if rec_eff != 0 else 9999
            gen_rec_err = (gen_rec_div * ((rec_err/rec_eff)**2 + (gen_err/gen_eff)**2))**0.5 if rec_eff != 0 and gen_eff != 0 else 9999
            if generated[i] == gen_num:
                print '%20s%6d%20s%6d%10.3f%10.3f%10.3f%10.3f%10.3f%10.3f\n' % (rec, rec_hist.GetEntries(), generated[i], gen_hist.GetEntries(), rec_eff, rec_err, gen_eff, gen_err, gen_rec_div, gen_rec_err)
                print r'%s & $%4.3f \pm %4.3f$ & $%4.3f \pm %4.3f$ & $%4.3f \pm %4.3f$ \\' % (sampleName, rec_eff, rec_err, gen_eff, gen_err, gen_rec_div, gen_rec_err)
                x.append(rec_eff)
                y.append(gen_eff)
                ex.append(rec_err)
                ey.append(gen_err)
                g = ROOT.TGraphErrors(1, array('d', [rec_eff]), array('d', [gen_eff]), array('d', [rec_err]), array('d', [gen_err]))
                g.SetMarkerStyle(style(sample))
                g.SetMarkerColor(color(sample))
                gs.append(g)
                label = sampleName.split(',')[0] + sampleName.split(',')[2]
                label = label.replace('\\','#').replace('#GeV',' GeV').replace('$','').replace(' M',', M')
                if int(sample.split('tau')[1].split('um')[0]) == 1000:
                    if style(sample) == 20:
                        l1.AddEntry(g, label.split(', ')[1], 'P')
                    if color(sample) == 6:
                        l2.AddEntry(g, label.split(', ')[0], 'P')
                if gen_eff >= (1-0.01*gen_rec_cut)*rec_eff and gen_eff <= (1+0.01*gen_rec_cut)*rec_eff:
                    matched.append(sample)
                else:
                    not_matched.append(sample)
                break
            else:
                print '%20s%6d%20s%6d%10.3f%10.3f%10.3f%10.3f%10.3f%10.3f' % (rec, rec_hist.GetEntries(), generated[i], gen_hist.GetEntries(), rec_eff, rec_err, gen_eff, gen_err, gen_rec_div, gen_rec_err)
        else:
            print '%20s%6d' % (rec, rec_hist.GetEntries())

print 'samples with gen eff within %s%% of reco eff:' % gen_rec_cut
for i in matched:
    print '\t', i
print
print 'samples with gen eff NOT within %s%% of reco eff:' % gen_rec_cut
for i in not_matched:
    print '\t', i

c = ROOT.TCanvas()
c.SetTickx()
c.SetTicky()
c.SetRightMargin(0.3)
g_all = ROOT.TGraphErrors(len(x), array('d', x), array('d', y), array('d', ex), array('d', ey))
g_all.SetTitle(';reconstructed-level efficiency;generator-level efficiency')
g_all.GetXaxis().SetLimits(0,1)
g_all.GetHistogram().GetYaxis().SetRangeUser(0,1)
g_all.Draw('AP')
for g in gs:
    g.Draw('P')
l1.SetFillColor(0)
l1.Draw()
l2.SetFillColor(0)
l2.Draw()
line0 = ROOT.TLine(0,0,1,1)
line0.SetLineStyle(7)
line1 = ROOT.TLine(0,0,1,1-0.01*gen_rec_cut)
line2 = ROOT.TLine(0,0,1-0.01*gen_rec_cut,1)
line0.Draw()
line1.Draw()
line2.Draw()
#c.SaveAs('plots/theorist_recipe/gen_vs_reco_eff_%s_divide_%s.pdf' % (gen_num, gen_den))
