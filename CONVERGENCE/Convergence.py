# -*- coding: mbcs -*-

###################################################
###                                             ###
### Approche fiabiliste - Assemblages boulonnés ###
###                                             ###
###################################################

# Bibliothèques :
import openturns as ot
import numpy as np
from matplotlib import pyplot as plt
import sys
from openturns import viewer
from scipy.stats import beta

xmin = -7.223
xmax = 52.559
a = 5.957+1
b = 20.151+2+5.957
Beta =  ot.Beta(a,b,xmin,xmax)
Beta_PDF = Beta.drawPDF(xmin,xmax,251)


xmin_100 = -11.2559
xmax_100 = 29.6451
a_100 = 24.9179
b_100 = 51.753
Q90_MB100 = 12.0725
Q90_MS100 = 11.36857904541198
Q90_EB100 = 15.506
Q90_ES100 = 15.179398914338677
Q99_MB100 = 14.9486
Q99_MS100 = 16.824690069102072
Q99_EB100 = 19.7793
Q99_ES100 = 21.253144445915538
Beta_100 =  ot.Beta(a_100,b_100,xmin_100,xmax_100)
Beta_100_PDF = Beta_100.drawPDF(xmin,xmax,251)
Beta_100_draw = Beta_100_PDF.getDrawable(0)
Beta_PDF.add(Beta_100_draw)

xmin_150 = -13.7746
xmax_150 = 39.6043
a_150 = 18.0236
b_150 = 45.4171
Q90_MB150 = 12.4074
Q90_MS150 = 11.704872213848899
Q90_EB150 = 14.056
Q90_ES150 = 13.22785648086853
Q99_MB150 = 16.5576
Q99_MS150 = 19.663336096979311
Q99_EB150 = 19.2652
Q99_ES150 = 21.475440222428148
Beta_150 =  ot.Beta(a_150,b_150,xmin_150,xmax_150)
Beta_150_PDF = Beta_150.drawPDF(xmin,xmax,251)
Beta_150_draw = Beta_150_PDF.getDrawable(0)
Beta_PDF.add(Beta_150_draw)

xmin_200 = -5.80237
xmax_200 = 49.5384
a_200 = 5.54926
b_200 = 22.3114
Q90_MB200 = 14.6283
Q90_MS200 = 13.925604617321625
Q90_EB200 = 14.3579
Q90_ES200 = 14.101681451079042
Q99_MB200 = 20.9318
Q99_MS200 = 26.722490429751879
Q99_EB200 = 19.7976
Q99_ES200 = 19.64755726201507
Beta_200 =  ot.Beta(a_200,b_200,xmin_200,xmax_200)
Beta_200_PDF = Beta_200.drawPDF(xmin,xmax,251)
Beta_200_draw = Beta_200_PDF.getDrawable(0)
Beta_PDF.add(Beta_200_draw)

xmin_300 = 0.318117
xmax_300 = 48.501
a_300 = 2.41449
b_300 = 15.2901
Q90_MB300 = 13.9239
Q90_MS300 = 13.191956516673629
Q90_EB300 = 14.1138
Q90_ES300 = 13.666092943201379
Q99_MB300 = 20.5928
Q99_MS300 = 25.258591982633884
Q99_EB300 = 19.3625
Q99_ES300 = 20.083807758506541
Beta_300 =  ot.Beta(a_300,b_300,xmin_300,xmax_300)
Beta_300_PDF = Beta_300.drawPDF(xmin,xmax,251)
Beta_300_draw = Beta_300_PDF.getDrawable(0)
Beta_PDF.add(Beta_300_draw)

xmin_400 = -0.317802
xmax_400 = 43.9636
a_400 = 2.75796
b_400 = 14.81
Q90_MB400 = 13.89
Q90_MS400 = 13.090482550501406
Q90_EB400 = 14.1399
Q90_ES400 = 14.293658149079844
Q99_MB400 = 20.1737
Q99_MS400 = 24.337428351682156
Q99_EB400 = 19.0071
Q99_ES400 = 19.702105123791867
Beta_400 =  ot.Beta(a_400,b_400,xmin_400,xmax_400)
Beta_400_PDF = Beta_400.drawPDF(xmin,xmax,251)
Beta_400_draw = Beta_400_PDF.getDrawable(0)
Beta_PDF.add(Beta_400_draw)

xmin_500 = -1.3134
xmax_500 = 44.998
a_500 = 3.06737
b_500 = 15.3167
Q90_MB500 = 14.2516
Q90_MS500 = 13.398200412859307
Q90_EB500 = 14.6726
Q90_ES500 = 14.508142459949696
Q99_MB500 = 20.7089
Q99_MS500 = 25.184095579267844
Q99_EB500 = 19.6635
Q99_ES500 = 22.337481795313117
Beta_500 =  ot.Beta(a_500,b_500,xmin_500,xmax_500)
Beta_500_PDF = Beta_500.drawPDF(xmin,xmax,251)
Beta_500_draw = Beta_500_PDF.getDrawable(0)
Beta_PDF.add(Beta_500_draw)

xmin_600 = -1.61707
xmax_600 = 46.1333
a_600 = 3.1756
b_600 = 15.7605
Q90_MB600 = 14.4108
Q90_MS600 = 13.55280137362902
Q90_EB600 = 14.6524
Q90_ES600 = 14.65907586389514
Q99_MB600 = 20.9648
Q99_MS600 = 25.21878541662819
Q99_EB600 = 20.1068
Q99_ES600 = 23.063815702369919
Beta_600 =  ot.Beta(a_600,b_600,xmin_600,xmax_600)
Beta_600_PDF = Beta_600.drawPDF(xmin,xmax,251)
Beta_600_draw = Beta_600_PDF.getDrawable(0)
Beta_PDF.add(Beta_600_draw)

xmin_700 = -1.72697
xmax_700 = 49.7688
a_700 = 3.06282
b_700 = 16.2919
Q90_MB700 = 14.583
Q90_MS700 = 13.657649387967266
Q90_EB700 = 14.3365
Q90_ES700 = 14.580961207467231
Q99_MB700 = 21.5097
Q99_MS700 = 25.890879696038379
Q99_EB700 = 19.5364
Q99_ES700 = 20.69535283993115
Beta_700 =  ot.Beta(a_700,b_700,xmin_700,xmax_700)
Beta_700_PDF = Beta_700.drawPDF(xmin,xmax,251)
Beta_700_draw = Beta_700_PDF.getDrawable(0)
Beta_PDF.add(Beta_700_draw)

xmin_800 = -1.13858
xmax_800 = 47.1928
a_800 = 2.83707
b_800 = 15.1736
Q90_MB800 = 14.335
Q90_MS800 = 13.485323066985517
Q90_EB800 = 14.1458
Q90_ES800 = 14.024890771878724
Q99_MB800 = 21.101
Q99_MS800 = 25.550878971000301
Q99_EB800 = 19.7673
Q99_ES800 = 21.092413610485899
Beta_800 =  ot.Beta(a_800,b_800,xmin_800,xmax_800)
Beta_800_PDF = Beta_800.drawPDF(xmin,xmax,251)
Beta_800_draw = Beta_800_PDF.getDrawable(0)
Beta_PDF.add(Beta_800_draw)

xmin_900 = -2.89604
xmax_900 = 44.827
a_900 = 4.03533
b_900 = 17.8835
Q90_MB900 = 14.111
Q90_MS900 = 13.342980507614532
Q90_EB900 = 14.7199
Q90_ES900 = 14.26188269561764
Q99_MB900 = 20.2298
Q99_MS900 = 24.930674963521433
Q99_EB900 = 20.3264
Q99_ES900 = 22.772805507745264
Beta_900 =  ot.Beta(a_900,b_900,xmin_900,xmax_900)
Beta_900_PDF = Beta_900.drawPDF(xmin,xmax,251)
Beta_900_draw = Beta_900_PDF.getDrawable(0)
Beta_PDF.add(Beta_900_draw)

xmin_1000 = -1.9637
xmax_1000 = 46.132
a_1000 = 3.25008
b_1000 = 15.7917
Q90_MB1000 = 14.4287
Q90_MS1000 = 13.588915145452965
Q90_EB1000 = 14.3184
Q90_ES1000 = 14.578313253012048
Q99_MB1000 = 21.0245
Q99_MS1000 = 25.532802858033193
Q99_EB1000 = 19.5955
Q99_ES1000 = 19.992056136634449
Beta_1000 =  ot.Beta(a_1000,b_1000,xmin_1000,xmax_1000)
Beta_1000_PDF = Beta_1000.drawPDF(xmin,xmax,251)
Beta_1000_draw = Beta_1000_PDF.getDrawable(0)
Beta_PDF.add(Beta_1000_draw)


Beta_PDF.setColors(['red','green','blue','yellow','black','grey','purple','orange','cyan','darkred','darkblue','darkcyan'])
Beta_PDF.setLegends(['MC : 2000 realisations','PC meta-modele : 100 realisations','PC meta-modele : 150 realisations','PC meta-modele : 200 realisations','PC meta-modele : 300 realisations','PC meta-modele : 400 realisations','PC meta-modele : 500 realisations','PC meta-modele : 600 realisations','PC meta-modele : 700 realisations','PC meta-modele : 800 realisations','PC meta-modele : 900 realisations','PC meta-modele : 1000 realisations'])
Beta_PDF.setTitle('Convergence de la loi Beta')
Beta_PDF.setXTitle('Yf[%]')
Beta_PDF.setYTitle('Densite de probabilite')
viewer.View(Beta_PDF)

plt.figure(1)
plt.xlim( -10, 60)
plt.ylim( -0.01, 0.1)
plt.savefig('Loi_Beta.png')

nb = [ 100, 150, 200, 300, 400,  500, 600, 700, 800, 900, 1000]
y_alpha = [a_100, a_150, a_200, a_300, a_400, a_500, a_600, a_700, a_800, a_900, a_1000]
y_beta = [b_100, b_150, b_200, b_300, b_400, b_500, b_600, b_700, b_800, b_900, b_1000]
err = [0.0080976, 0.00537392, 0.00318212, 0.00161066, 0.00110808, 0.000693121, 0.000405553, 0.000343159, 0.000327746, 0.000262136, 0.000234597]

Q90_MB = [Q90_MB100, Q90_MB150, Q90_MB200, Q90_MB300, Q90_MB400, Q90_MB500, Q90_MB600, Q90_MB700, Q90_MB800, Q90_MB900, Q90_MB1000]
Q90_MS = [Q90_MS100, Q90_MS150, Q90_MS200, Q90_MS300, Q90_MS400, Q90_MS500, Q90_MS600, Q90_MS700, Q90_MS800, Q90_MS900, Q90_MS1000]
Q90_EB = [Q90_EB100, Q90_EB150, Q90_EB200, Q90_EB300, Q90_EB400, Q90_EB500, Q90_EB600, Q90_EB700, Q90_EB800, Q90_EB900, Q90_EB1000]
Q90_ES = [Q90_ES100, Q90_ES150, Q90_ES200, Q90_ES300, Q90_ES400, Q90_ES500, Q90_ES600, Q90_ES700, Q90_ES800, Q90_ES900, Q90_ES1000]
Q99_MB = [Q99_MB100, Q99_MB150, Q99_MB200, Q99_MB300, Q99_MB400, Q99_MB500, Q99_MB600, Q99_MB700, Q99_MB800, Q99_MB900, Q99_MB1000]
Q99_MS = [Q99_MS100, Q99_MS150, Q99_MS200, Q99_MS300, Q99_MS400, Q99_MS500, Q99_MS600, Q99_MS700, Q99_MS800, Q99_MS900, Q99_MS1000]
Q99_EB = [Q99_EB100, Q99_EB150, Q99_EB200, Q99_EB300, Q99_EB400, Q99_EB500, Q99_EB600, Q99_EB700, Q99_EB800, Q99_EB900, Q99_EB1000]
Q99_ES = [Q99_ES100, Q99_ES150, Q99_ES200, Q99_ES300, Q99_ES400, Q99_ES500, Q99_ES600, Q99_ES700, Q99_ES800, Q99_ES900, Q99_ES1000]


plt.figure(2)
plt.subplot(321)
plt.plot(nb, y_alpha, label='Alpha')
plt.title('Alpha')
plt.subplot(322)
plt.plot(nb, y_beta, label='Beta')
plt.title('Beta')
plt.subplot(323)
plt.plot(nb, err, label='Erreur meta-modele')
plt.title('Erreur meta-modele')
plt.subplot(324)
plt.plot(nb, Q90_MB, label='Q90_MB')
plt.plot(nb, Q90_MS, label='Q90_MS')
plt.plot(nb, Q90_EB, label='Q90_EB')
plt.plot(nb, Q90_ES, label='Q90_ES')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title('Q90')
plt.subplot(325)
plt.plot(nb, Q99_MB, label='Q99_MB')
plt.plot(nb, Q99_MS, label='Q99_MS')
plt.plot(nb, Q99_EB, label='Q99_EB')
plt.plot(nb, Q99_ES, label='Q99_ES')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title('Q99')
plt.savefig('Convergence.png')
plt.show()