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
import sys

#########################
### Données d'entrées ###
#########################

# Paramètres :
IT = 0.3	#Interval de tolérance en mm
IT0 = str(int(IT*100))

# Paramètres incertains :
dim = 16

# Position du centre de chaque perçage :
mu_Dx = 0.
sigma_Dx = IT/6
mu_Dy = mu_Dx
sigma_Dy = sigma_Dx

distribution_Dx1 = ot.Normal(mu_Dx, sigma_Dx)
distribution_Dx2 = ot.Normal(mu_Dx, sigma_Dx)
distribution_Dx3 = ot.Normal(mu_Dx, sigma_Dx)
distribution_Dx4 = ot.Normal(mu_Dx, sigma_Dx)

distribution_Dy1 = ot.Normal(mu_Dy, sigma_Dy)
distribution_Dy2 = ot.Normal(mu_Dy, sigma_Dy)
distribution_Dy3 = ot.Normal(mu_Dy, sigma_Dy)
distribution_Dy4 = ot.Normal(mu_Dy, sigma_Dy)

# Jeux :
Jmin = IT/2
Delta_J = 0.06
Jmax = Jmin+Delta_J
mu_J = Jmin+Delta_J/2
sigma_J = Delta_J/6

distribution_J1 = ot.Normal(mu_J, sigma_J)
distribution_J2 = ot.Normal(mu_J, sigma_J)
distribution_J3 = ot.Normal(mu_J, sigma_J)
distribution_J4 = ot.Normal(mu_J, sigma_J)

# Précharge : 
Delta_P = 0.025
mu_P = 0.045
sigma_P = Delta_P/6

distribution_P1 = ot.Normal(mu_P, sigma_P)
distribution_P2 = ot.Normal(mu_P, sigma_P)
distribution_P3 = ot.Normal(mu_P, sigma_P)
distribution_P4 = ot.Normal(mu_P, sigma_P)


# Création de la collection des distributions d'entrées
myCollection = ot.DistributionCollection(dim)
myCollection[0] = distribution_Dx1
myCollection[1] = distribution_Dx2
myCollection[2] = distribution_Dx3
myCollection[3] = distribution_Dx4
myCollection[4] = distribution_Dy1
myCollection[5] = distribution_Dy2
myCollection[6] = distribution_Dy3
myCollection[7] = distribution_Dy4
myCollection[8] = distribution_J1
myCollection[9] = distribution_J2
myCollection[10] = distribution_J3
myCollection[11] = distribution_J4
myCollection[12] = distribution_P1
myCollection[13] = distribution_P2
myCollection[14] = distribution_P3
myCollection[15] = distribution_P4

# Création d'une distribution ? en fonction de la collection
myDistribution = ot.ComposedDistribution(myCollection)
# ???
vectX = ot.RandomVector(myDistribution)

########################
### Chaos Polynomial ###
########################

polyColl = ot.PolynomialFamilyCollection(dim)
for i in range(dim):
	polyColl[i] = ot.HermiteFactory()

enumerateFunction = ot.LinearEnumerateFunction(dim)
multivariateBasis = ot.OrthogonalProductPolynomialFactory(polyColl, enumerateFunction)

basisSequenceFactory = ot.LARS()
fittingAlgorithm = ot.CorrectedLeaveOneOut()
approximationAlgorithm = ot.LeastSquaresMetaModelSelectionFactory(basisSequenceFactory, fittingAlgorithm)

# Génération du plan d'expériences
N = 200
ot.RandomGenerator.SetSeed(77)
Liste_test = ot.LHSExperiment(myDistribution, N)
InputSample = Liste_test.generate()


# Ecriture du fichier de données d'entrées
fidResult=open('IT'+IT0+'/IT'+IT0+'_TIRAGE_200.txt',"a")
for i in range(N):
	fidResult.write(
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,0])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,1])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,2])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,3])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,4])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,5])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,6])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,7])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,8])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,9])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,10])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,11])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,12])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,13])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,14])))+"\t"+
	'{0:>8s}'.format(str('{0:.3f}'.format(InputSample[i,15])))+"\n")
fidResult.close()
