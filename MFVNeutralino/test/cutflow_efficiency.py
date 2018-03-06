#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import ROOT
from array import array

file_path = '~/crabdirs/TheoristRecipeV43'

gen_rec_cut = 20

match = ''
#match = '_match'

ctau = ''
#ctau = 'tau00100um'
#ctau = 'tau00300um'
#ctau = 'tau01000um'
#ctau = 'tau10000um'
#ctau = 'tau30000um'

#gen_num = 'FourJets'
#gen_num = 'HT40'
#gen_num = 'Bsbs2ddist'
#gen_num = 'Geo2ddist'
#gen_num = 'Sumpt350'
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

#rec_den = 'TwoVtxBsbs2ddist'
#gen_den = 'Bsbs2ddist'
#iden = 5

#rec_den = 'TwoVtxGeo2ddist'
#gen_den = 'Geo2ddist'
#iden = 6

#rec_den = 'TwoVtxBs2derr'
#gen_den = 'Sumpt350'
#iden = 8

reconstructed = ['NoCuts', 'OfflineJets', 'TrigSel', 'PreSel', 'TwoVtxNoCuts', 'TwoVtxBsbs2ddist', 'TwoVtxGeo2ddist', 'TwoVtxNtracks', 'TwoVtxBs2derr', 'TwoVtxDvv400um']
generated = ['NoCuts', 'FourJets', '', 'HT40', '', 'Bsbs2ddist', 'Geo2ddist', '', 'Sumpt350', 'Dvv400um']

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
    ('mfv_stopdbardbar_tau00100um_M0300',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_stopdbardbar_tau00100um_M0400',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_stopdbardbar_tau00100um_M0500',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_stopdbardbar_tau00100um_M0600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_stopdbardbar_tau00100um_M0800',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_stopdbardbar_tau00100um_M1200',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_stopdbardbar_tau00100um_M1600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_stopdbardbar_tau00100um_M3000',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_stopdbardbar_tau00300um_M0300',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_stopdbardbar_tau00300um_M0400',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_stopdbardbar_tau00300um_M0500',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_stopdbardbar_tau00300um_M0600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_stopdbardbar_tau00300um_M0800',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_stopdbardbar_tau00300um_M1200',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_stopdbardbar_tau00300um_M1600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_stopdbardbar_tau00300um_M3000',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_stopdbardbar_tau01000um_M0300',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_stopdbardbar_tau01000um_M0400',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_stopdbardbar_tau01000um_M0500',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_stopdbardbar_tau01000um_M0600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_stopdbardbar_tau01000um_M0800',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_stopdbardbar_tau01000um_M1200',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_stopdbardbar_tau01000um_M1600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_stopdbardbar_tau01000um_M3000',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_stopdbardbar_tau10000um_M0300',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_stopdbardbar_tau10000um_M0400',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_stopdbardbar_tau10000um_M0500',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_stopdbardbar_tau10000um_M0600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_stopdbardbar_tau10000um_M0800',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_stopdbardbar_tau10000um_M1200',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_stopdbardbar_tau10000um_M1600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_stopdbardbar_tau10000um_M3000',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_stopdbardbar_tau30000um_M0300',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_stopdbardbar_tau30000um_M0400',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_stopdbardbar_tau30000um_M0500',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_stopdbardbar_tau30000um_M0600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_stopdbardbar_tau30000um_M0800',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_stopdbardbar_tau30000um_M1200',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_stopdbardbar_tau30000um_M1600',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_stopdbardbar_tau30000um_M3000',     r'$\tilde{t} \rightarrow \bar{d}\bar{d}$, $c\tau =   30\mm$, $M = 3000\GeV$'),
    ('mfv_xxddbar_tau00100um_M0300',          r'$X \rightarrow d\bar{d}$,         $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_xxddbar_tau00100um_M0400',          r'$X \rightarrow d\bar{d}$,         $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_xxddbar_tau00100um_M0500',          r'$X \rightarrow d\bar{d}$,         $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_xxddbar_tau00100um_M0600',          r'$X \rightarrow d\bar{d}$,         $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_xxddbar_tau00100um_M0800',          r'$X \rightarrow d\bar{d}$,         $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_xxddbar_tau00100um_M1200',          r'$X \rightarrow d\bar{d}$,         $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_xxddbar_tau00100um_M1600',          r'$X \rightarrow d\bar{d}$,         $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_xxddbar_tau00100um_M3000',          r'$X \rightarrow d\bar{d}$,         $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_xxddbar_tau00300um_M0300',          r'$X \rightarrow d\bar{d}$,         $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_xxddbar_tau00300um_M0400',          r'$X \rightarrow d\bar{d}$,         $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_xxddbar_tau00300um_M0500',          r'$X \rightarrow d\bar{d}$,         $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_xxddbar_tau00300um_M0600',          r'$X \rightarrow d\bar{d}$,         $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_xxddbar_tau00300um_M0800',          r'$X \rightarrow d\bar{d}$,         $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_xxddbar_tau00300um_M1200',          r'$X \rightarrow d\bar{d}$,         $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_xxddbar_tau00300um_M1600',          r'$X \rightarrow d\bar{d}$,         $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_xxddbar_tau00300um_M3000',          r'$X \rightarrow d\bar{d}$,         $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_xxddbar_tau01000um_M0300',          r'$X \rightarrow d\bar{d}$,         $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_xxddbar_tau01000um_M0400',          r'$X \rightarrow d\bar{d}$,         $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_xxddbar_tau01000um_M0500',          r'$X \rightarrow d\bar{d}$,         $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_xxddbar_tau01000um_M0600',          r'$X \rightarrow d\bar{d}$,         $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_xxddbar_tau01000um_M0800',          r'$X \rightarrow d\bar{d}$,         $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_xxddbar_tau01000um_M1200',          r'$X \rightarrow d\bar{d}$,         $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_xxddbar_tau01000um_M1600',          r'$X \rightarrow d\bar{d}$,         $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_xxddbar_tau01000um_M3000',          r'$X \rightarrow d\bar{d}$,         $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_xxddbar_tau10000um_M0300',          r'$X \rightarrow d\bar{d}$,         $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_xxddbar_tau10000um_M0400',          r'$X \rightarrow d\bar{d}$,         $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_xxddbar_tau10000um_M0500',          r'$X \rightarrow d\bar{d}$,         $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_xxddbar_tau10000um_M0600',          r'$X \rightarrow d\bar{d}$,         $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_xxddbar_tau10000um_M0800',          r'$X \rightarrow d\bar{d}$,         $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_xxddbar_tau10000um_M1200',          r'$X \rightarrow d\bar{d}$,         $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_xxddbar_tau10000um_M1600',          r'$X \rightarrow d\bar{d}$,         $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_xxddbar_tau10000um_M3000',          r'$X \rightarrow d\bar{d}$,         $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_xxddbar_tau30000um_M0300',          r'$X \rightarrow d\bar{d}$,         $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_xxddbar_tau30000um_M0400',          r'$X \rightarrow d\bar{d}$,         $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_xxddbar_tau30000um_M0500',          r'$X \rightarrow d\bar{d}$,         $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_xxddbar_tau30000um_M0600',          r'$X \rightarrow d\bar{d}$,         $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_xxddbar_tau30000um_M0800',          r'$X \rightarrow d\bar{d}$,         $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_xxddbar_tau30000um_M1200',          r'$X \rightarrow d\bar{d}$,         $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_xxddbar_tau30000um_M1600',          r'$X \rightarrow d\bar{d}$,         $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_xxddbar_tau30000um_M3000',          r'$X \rightarrow d\bar{d}$,         $c\tau =   30\mm$, $M = 3000\GeV$'),
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
    ('mfv_neuude_tau00100um_M0300',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 100\mum$, $M =  300\GeV$'),
    ('mfv_neuude_tau00100um_M0400',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 100\mum$, $M =  400\GeV$'),
    ('mfv_neuude_tau00100um_M0500',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 100\mum$, $M =  500\GeV$'),
    ('mfv_neuude_tau00100um_M0600',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 100\mum$, $M =  600\GeV$'),
    ('mfv_neuude_tau00100um_M0800',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 100\mum$, $M =  800\GeV$'),
    ('mfv_neuude_tau00100um_M1200',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 100\mum$, $M = 1200\GeV$'),
    ('mfv_neuude_tau00100um_M1600',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 100\mum$, $M = 1600\GeV$'),
    ('mfv_neuude_tau00100um_M3000',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 100\mum$, $M = 3000\GeV$'),
    ('mfv_neuude_tau00300um_M0300',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 300\mum$, $M =  300\GeV$'),
    ('mfv_neuude_tau00300um_M0400',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 300\mum$, $M =  400\GeV$'),
    ('mfv_neuude_tau00300um_M0500',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 300\mum$, $M =  500\GeV$'),
    ('mfv_neuude_tau00300um_M0600',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 300\mum$, $M =  600\GeV$'),
    ('mfv_neuude_tau00300um_M0800',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 300\mum$, $M =  800\GeV$'),
    ('mfv_neuude_tau00300um_M1200',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 300\mum$, $M = 1200\GeV$'),
    ('mfv_neuude_tau00300um_M1600',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 300\mum$, $M = 1600\GeV$'),
    ('mfv_neuude_tau00300um_M3000',           r'$\tilde{N} \rightarrow ude$,      $c\tau = 300\mum$, $M = 3000\GeV$'),
    ('mfv_neuude_tau01000um_M0300',           r'$\tilde{N} \rightarrow ude$,      $c\tau =    1\mm$, $M =  300\GeV$'),
    ('mfv_neuude_tau01000um_M0400',           r'$\tilde{N} \rightarrow ude$,      $c\tau =    1\mm$, $M =  400\GeV$'),
    ('mfv_neuude_tau01000um_M0500',           r'$\tilde{N} \rightarrow ude$,      $c\tau =    1\mm$, $M =  500\GeV$'),
    ('mfv_neuude_tau01000um_M0600',           r'$\tilde{N} \rightarrow ude$,      $c\tau =    1\mm$, $M =  600\GeV$'),
    ('mfv_neuude_tau01000um_M0800',           r'$\tilde{N} \rightarrow ude$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neuude_tau01000um_M1200',           r'$\tilde{N} \rightarrow ude$,      $c\tau =    1\mm$, $M = 1200\GeV$'),
    ('mfv_neuude_tau01000um_M1600',           r'$\tilde{N} \rightarrow ude$,      $c\tau =    1\mm$, $M = 1600\GeV$'),
    ('mfv_neuude_tau01000um_M3000',           r'$\tilde{N} \rightarrow ude$,      $c\tau =    1\mm$, $M = 3000\GeV$'),
    ('mfv_neuude_tau10000um_M0300',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   10\mm$, $M =  300\GeV$'),
    ('mfv_neuude_tau10000um_M0400',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   10\mm$, $M =  400\GeV$'),
    ('mfv_neuude_tau10000um_M0500',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   10\mm$, $M =  500\GeV$'),
    ('mfv_neuude_tau10000um_M0600',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   10\mm$, $M =  600\GeV$'),
    ('mfv_neuude_tau10000um_M0800',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   10\mm$, $M =  800\GeV$'),
    ('mfv_neuude_tau10000um_M1200',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   10\mm$, $M = 1200\GeV$'),
    ('mfv_neuude_tau10000um_M1600',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neuude_tau10000um_M3000',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   10\mm$, $M = 3000\GeV$'),
    ('mfv_neuude_tau30000um_M0300',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   30\mm$, $M =  300\GeV$'),
    ('mfv_neuude_tau30000um_M0400',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   30\mm$, $M =  400\GeV$'),
    ('mfv_neuude_tau30000um_M0500',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   30\mm$, $M =  500\GeV$'),
    ('mfv_neuude_tau30000um_M0600',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   30\mm$, $M =  600\GeV$'),
    ('mfv_neuude_tau30000um_M0800',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   30\mm$, $M =  800\GeV$'),
    ('mfv_neuude_tau30000um_M1200',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   30\mm$, $M = 1200\GeV$'),
    ('mfv_neuude_tau30000um_M1600',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   30\mm$, $M = 1600\GeV$'),
    ('mfv_neuude_tau30000um_M3000',           r'$\tilde{N} \rightarrow ude$,      $c\tau =   30\mm$, $M = 3000\GeV$'),
    ('mfv_neucdb_tau01000um_M0800',           r'$\tilde{N} \rightarrow cdb$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neucdb_tau10000um_M1600',           r'$\tilde{N} \rightarrow cdb$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neucds_tau01000um_M0800',           r'$\tilde{N} \rightarrow cds$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neucds_tau10000um_M1600',           r'$\tilde{N} \rightarrow cds$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neutbb_tau01000um_M0800',           r'$\tilde{N} \rightarrow tbb$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neutbb_tau10000um_M1600',           r'$\tilde{N} \rightarrow tbb$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neutds_tau01000um_M0800',           r'$\tilde{N} \rightarrow tds$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neutds_tau10000um_M1600',           r'$\tilde{N} \rightarrow tds$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neuubb_tau01000um_M0800',           r'$\tilde{N} \rightarrow ubb$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neuubb_tau10000um_M1600',           r'$\tilde{N} \rightarrow ubb$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neuudb_tau01000um_M0800',           r'$\tilde{N} \rightarrow udb$,      $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neuudb_tau10000um_M1600',           r'$\tilde{N} \rightarrow udb$,      $c\tau =   10\mm$, $M = 1600\GeV$'),
    ('mfv_neuudtu_tau01000um_M0800',          r'$\tilde{N} \rightarrow ud\tau$,   $c\tau =    1\mm$, $M =  800\GeV$'),
    ('mfv_neuudtu_tau10000um_M1600',          r'$\tilde{N} \rightarrow ud\tau$,   $c\tau =   10\mm$, $M = 1600\GeV$'),
    ]

def style(sample):
    model = sample.split('_tau')[0]
    for i in range(1, len(sample.split('M')[1].split('_'))):
        model += '_' + sample.split('M')[1].split('_')[i]
    if model == 'mfv_neu':
        return 20
    if model == 'mfv_stopdbardbar':
        return 22
    if model == 'mfv_xxddbar':
        return 23
    if model == 'mfv_neuuds':
        return 21
    if model == 'mfv_neuudmu':
        return 34
    if model == 'mfv_neuude':
        return 29
    if model == 'mfv_neucdb':
        return 27
    if model == 'mfv_neucds':
        return 26
    if model == 'mfv_neutbb':
        return 32
    if model == 'mfv_neutds':
        return 24
    if model == 'mfv_neuubb':
        return 25
    if model == 'mfv_neuudb':
        return 30
    if model == 'mfv_neuudtu':
        return 28

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
    if ctau not in sample:
        continue

    print sample
    f = ROOT.TFile('%s/%s.root' % (file_path, sample))
    nrec = f.Get('mfvTheoristRecipe%s/h_gen%s_dvv' % (rec_den, match)).GetEntries()
    ngen = f.Get('mfvGen%s/h_gen%s_dvv' % (gen_den, match)).GetEntries()
    print '%26s%26s%20s%20s%20s' % ('reconstructed', 'generated', 'reco eff +/- error', 'gen eff +/- error', 'gen/reco +/- error')
    for i, rec in enumerate(reconstructed):
        if i < iden:
            continue
        rec_hist = f.Get('mfvTheoristRecipe%s/h_gen%s_dvv' % (rec, match))
        rec_eff = rec_hist.GetEntries()/nrec
        rec_err = (rec_eff * (1-rec_eff) / nrec)**0.5
        if generated[i] != '':
            gen_hist = f.Get('mfvGen%s/h_gen%s_dvv' % (generated[i], match))
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
                if int(sample.split('tau')[1].split('um')[0]) == 1000 or ctau != '':
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
#c.SaveAs('plots/theorist_recipe/gen_vs_reco_eff_%s_divide_%s%s%s.pdf' % (gen_num, gen_den, '' if ctau == '' else '_%s'%ctau, match))
