import openturns as ot
import numpy as np
from matplotlib import pyplot as plt
import sys
from openturns import viewer
from scipy.stats import beta, betaprime

Beta =  ot.Beta(5.957+1,20.151+2+5.957,-7.223,52.559)
Beta_PDF = Beta.drawPDF()
Beta_draw = Beta_PDF.getDrawable(0)
Beta_draw.setColor('blue')
viewer.View(Beta_draw)

# Beta2 =  ot.Beta(2.61339,7.55733,-2.50357,27.9764)
# Beta2_PDF = Beta2.drawPDF()
# Beta2_PDF.add(Beta_draw)
# viewer.View(Beta2_PDF)

x = np.linspace(-8, 60, 1002)


plt.figure(1)
plt.plot(x, beta.pdf(x,5.957+1,20.151+1, loc = -7.223, scale = 59.782), c='black')
plt.show()