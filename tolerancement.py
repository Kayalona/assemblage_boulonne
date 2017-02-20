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

point90_10 = 14.6283
point90_20 = 23.757
point90_30 = 31.8952

point99_10 = 20.9318
point99_20 = 34.8625
point99_30 = 45.8833

Point90 = [point90_10, point90_20, point90_30]
Point99 = [point99_10, point99_20, point99_30]

point90_00_ref = 10
point90_10_ref = 14.8922
point90_20_ref = 23.4617
point90_30_ref = 32.9011

point99_00_ref = 14
point99_10_ref = 20.2935
point99_20_ref = 32.7617
point99_30_ref = 46.1076

Point90_ref = [point90_10_ref, point90_20_ref, point90_30_ref]
Point99_ref = [point99_10_ref, point99_20_ref, point99_30_ref]

plb.figure(1)
plb.plot(Point90,IT,'bo')
plb.plot(Point99,IT, 'go')
plb.plot(Point90_ref,IT,'r+')
plb.plot(Point99_ref,IT, 'r+')
plb.show()

Yf90 = np.linspace(point90_00_ref,point90_30_ref,100)
Fonction90 = 
Fonction95 = 
Fonction90_ref = 
Fonction95_ref = 