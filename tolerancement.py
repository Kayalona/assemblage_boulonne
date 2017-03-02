# -*- coding: mbcs -*-

###################################################
###                                             ###
### Approche fiabiliste - Assemblages boulonnés ###
###                                             ###
###################################################

# Bibliothèques :
import openturns as ot
import os as os
import numpy as np
import pylab as plb
import sys

IT = [10, 20, 30]
ITx = [0.0, 0.1, 0.2, 0.3]

point90_10 = 14.6283
point90_20 = 23.8718
point90_30 = 32.1752

point99_10 = 20.9318
point99_20 = 34.9877
point99_30 = 46.193


point90_00_ref = 9.6
point90_10_ref = 14.8922
point90_20_ref = 23.4617
point90_30_ref = 32.9011

point99_00_ref = 13.67
point99_10_ref = 20.2935
point99_20_ref = 32.7617
point99_30_ref = 46.1076

Point90 = [point90_00_ref,point90_10, point90_20, point90_30]
Point99 = [point99_00_ref,point99_10, point99_20, point99_30]
Point90_ref = [point90_00_ref,point90_10_ref, point90_20_ref, point90_30_ref]
Point99_ref = [point99_00_ref,point99_10_ref, point99_20_ref, point99_30_ref]

plb.figure(1)
plb.plot(Point90,ITx,'bo')
plb.plot(Point99,ITx, 'bo')
plb.plot(Point90_ref,ITx,'r+')
plb.plot(Point99_ref,ITx, 'r+')
# plb.show()

Yf90 = np.linspace(point90_00_ref,point90_30_ref,100)
Yf99 = np.linspace(point99_00_ref,point99_30_ref,100)
Fonction90 = 2.4081E-01*np.log(Yf90)-5.4765E-01
Fonction99 = 0.2371*np.log(Yf99)-0.6231
Fonction90_ref = 2.40e-01*np.log(Yf90)-5.47E-01
Fonction99_ref = 2.41e-01*np.log(Yf99)-6.31E-01

# plb.figure(2)
plb.plot(Yf90,Fonction90)
plb.plot(Yf90,Fonction90_ref,'r')
plb.plot(Yf99,Fonction99)
plb.plot(Yf99,Fonction99_ref,'r')
plb.xlim(0,50)
plb.ylim(0,0.35)
plb.savefig('Tolerancement.png')