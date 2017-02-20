# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 11:30:22 2015

@author: ramaskri
"""

import numpy as np
from numpy import arange
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def readText(lines):
    nlines=len(lines)
    FMAX=[]
    for i in range(nlines):
        try:
            ind,exc1,exc2,exc3,exc4,ang1,ang2,ang3,ang4,jeu1,jeu2,jeu3,jeu4,int1,int2,int3,int4,f1,f2,f3,f4,fmax,temps=lines[i].split()
            FMAX.append(float(fmax))
        except:
#            print("erreur lecture ligne",i)
            pass
    return np.array(FMAX)

def readMinMax(fid,minMax):
    fid.seek(0)
    FIT=[]  
    for u in fid:
        try:
            pop,gen,ind,exc1,exc2,exc3,exc4,ang1,ang2,ang3,ang4,jeu1,jeu2,jeu3,jeu4,int1,int2,int3,int4,f1,f2,f3,f4,fit,temps=u.split()
            FIT.append(float(fit))
        except:
#            print('erreur')
            pass
    if minMax=='min':
        fext=np.min(FIT)
    elif minMax=='max':
        fext=np.max(FIT)
#    print(fext)        
    return fext
    
def discretization(nbins,xmin,xmax):
    XDATA=np.linspace(xmin,xmax,nbins+1)
    return XDATA
    
def hist(XDATA,FMAX,f0,w):
    YDATA=[]
    Niter=len(FMAX)
    for k in range(len(XDATA)-1):
        p=0
        for i in range(Niter):
            if ((FMAX[i]-f0)*100)/f0>XDATA[k] and ((FMAX[i]-f0)*100)/f0<=XDATA[k+1]:
                p+=1
#        print(Xdata[k],Xdata[k+1],p)
        YDATA.append(float(p)/(float(Niter)*w))        
    return YDATA

def getMu(XDATA,YDATA,w):
    ymax=np.amax(YDATA)
    for i in range(len(YDATA)):
        if YDATA[i]==ymax:
            p=i
            y1=YDATA[i-1]
            y2=YDATA[i+1]
#    print(ymax)
#    print(y1)
#    print(y2)
    ratio=(ymax-y2)/(ymax-y1)
#    print(ratio)
#    print(XDATA[p])
    mu=XDATA[p]+ratio*w
    return mu
        
def func0(x,xmin,xmax,alpha,beta):
    return ((x-xmin)**alpha)*((xmax-x)**beta)
    

def loiDistr(x,alpha,beta):

#    x0=(alpha*xmax+beta*xmin)/(alpha+beta)
#    x0=getMu(XDATA,YDATA,w)
#    ymax=np.amax(YDATA)
#    print(ysum)
#    R=(((x0-xmin)**alpha)*((xmax-x0)**beta))/ymax
    R=quad(func0,xmin,xmax,args=(xmin,xmax,alpha,beta))[0]
#    for i in range(1,n,1):
#        A=((xmax-xmin)/(float(n)))**(alpha+beta+1)
#        B=((float(i))**alpha)*((float(n)-float(i))**beta)
#        s=A*B
#        r0+=s
#        del A,B,s

#    print("r=",r)
#    print("a=",a)

#    y=(((x-xmin)**alpha)*((xmax-x)**beta))/r
#    print(R)
    y=func0(x,xmin,xmax,alpha,beta)/R
    return y



def fitFunc(x,alpha,beta):
    integ=quad(loiDistr,xmin,x,args=(alpha,beta))[0]
    return integ

def getFMC(fiab,w,XDATA,YDATA):
#    print(w*np.sum(YDATA))
    for i in range(1,len(XDATA)+1,1):
#        print("i=",i,"sum=",w*np.sum(YDATA[:i-1]))
        if w*np.sum(YDATA[:i-1])<=fiab and w*np.sum(YDATA[:i])>fiab:
            yfiab1=w*np.sum(YDATA[:i-1])
            yfiab2=w*np.sum(YDATA[:i])
            xfiab1=XDATA[i-1]
            xfiab2=XDATA[i]
    print('\n\n\n')
    print(fiab)
    print(xfiab1)
    print(xfiab2)
    print(yfiab1)
    print(yfiab2)
    print("******\n")
    xfiab=((fiab-yfiab1)/(yfiab2-yfiab1))*(xfiab2-xfiab1)+xfiab1
    return xfiab,xfiab1,xfiab2
    
def getFLoi(fiab,XDATA,alpha,beta):
    I=[]
    for x in XDATA:
        I.append(quad(loiDistr,xmin,x,args=(alpha,beta))[0])
        
    for i in range(1,len(XDATA)+1,1):
#        print("i=",i,"x=",'{0:.3f}'.format(XDATA[i-1]),"I=",'{0:.3f}'.format(I[i-1]))
        if I[i-1]<=fiab and I[i]>fiab:
            yfiab1=I[i-1]
            yfiab2=I[i]
            xfiab1=XDATA[i-1]
            xfiab2=XDATA[i]
#    print('\n\n\n')
#    print("fiab=",fiab)
#    print("xfiab1=",xfiab1)
#    print("xfiab2=",xfiab2)
#    print("yfiab1=",yfiab1)
#    print("yfiab2=",yfiab2)
    xfiab=((fiab-yfiab1)/(yfiab2-yfiab1))*(xfiab2-xfiab1)+xfiab1
#    print("xfiab=",xfiab)
    return xfiab

def getAlphaBeta(xdata,xmin,xmax):
    xmoy=np.mean(xdata)
    variance=np.var(xdata)
    alpha=xmoy*(((xmoy*(1-xmoy))/variance)-1)
    beta=(1-xmoy)*(((xmoy*(1-xmoy))/variance)-1)    
    return alpha,beta

    
def ponderation(X,B,C):
    S=[]
    xmin=X[0]
    xmax=X[-1]
    x1=X[int(len(X)*C[0])]
    x2=X[int(len(X)*C[1])]
    x3=X[int(len(X)*C[2])]
    b1=B[0]
    b2=B[1]
    b3=B[2]
    b4=B[3]
    b5=B[4]

    for x in X:
           
        if x>=xmin and x<x1:
            y=((b2-b1)*(x-xmin))/(x1-xmin)+b1
            S.append(y)
            
        elif x>=x1 and x<x2:
            y=((b3-b2)*(x-x1))/(x2-x1)+b2
            S.append(y)
            
        elif x>=x2 and x<x3:
            y=((b4-b3)*(x-x2))/(x3-x2)+b3
            S.append(y)
            
        elif x>=x3 and x<xmax:
            y=((b5-b4)*(x-x3))/(xmax-x3)+b4
            S.append(y)
        
        elif x==xmax:
            S.append(b5)                        
    return S        

    
if __name__ == "__main__":
#    fidFiabName="D:\Askri\Python\DefLoc_1\RESULTATS\Fiabilite2.txt"
#    fidFiab=open(fidFiabName,"w")
#    fidFiab.write(
#    '{0:>4s}'.format("fiab")+"\t"+
#    '{0:>2s}'.format("e")+"\t"+
#    '{0:>4s}'.format("IT")+"\t"+
#    '{0:>5s}'.format("Alpha")+"\t"+
#    '{0:>5s}'.format("Beta")+"\t"+
#    '{0:>4s}'.format("XMC")+"\t"+
#    '{0:>4s}'.format("XLOI")+"\t"+
#    '{0:>4s}'.format("XLOIF")+"\n"                
#    )
    B=[1.,1.,1.,5.,5.]
    C=[0.2,0.3,0.4]
    ITv=[0.,0.1,0.2,0.3]
    FIAB100=[0.,30.3,58.7,]
    ALPHA,BETA,FIAB=[],[],[]
    XMIN,XMAXGlob,XMAX=[],[],[]
    E=[0,1,2,3,6,8,10,12,15]
    Ratio=[1.,1.079,1.166,1.261,1.58,1.84,2.12,2.43,2.87]
#    F0=[7465.,7728.,7995.,8265.,9151.,9816.,10488.,11170.,12204.]
    F0=[7559.,7553.,7546.,7537.]
    FIABMC=[]
    XFIAB1,XFIAB2=[],[]
    FIABL=[]
    FIABLF=[]
    NFIAB=np.arange(0.90,1.1,0.01)
    NY=[]
    NZ=[]
    FIABL90=[]
    XXMAXX=[40,60,80,100]
#    ALPHA=[[1.86,1.64],[2.,1.66],[2.7,2.28],[2.94,2.66]]
#    BETA=[[4.95,5.5],[5.77,5.65],[6.9,6.99],[7.43,7.28]]
#    ALPHA=[[1.86,1.64],[2.,1.9],[3.2,2.],[3.4,3.]]
#    BETA=[[5.,5.5],[5.6,5.7],[7.2,6.],[7.8,7.4]]
#    a1,b1,c1=5.6,-8.0,-3.0
#    a2,b2,c2=1.5,6.0,2.7
    ki=0
    FF=[]
    ECART=[]
    for fiab in [0.90]:
        for e in [0]:
            if e==0:
                k=0
            elif e==1:
                k=1
            elif e==2:
                k=2
            elif e==3:
                k=3
            elif e==6:
                k=4
            elif e==8:
                k=5
            elif e==10:
                k=6
            elif e==12:
                k=7
            elif e==15:
                k=8

#            FIABMC.append(0.)
#            XFIAB1.append(0.)
#            XFIAB2.append(0.)
#            FIABL.append(0.)
#            FIABLF.append(0.)
            for IT0 in ["00","05","10","15"]:
                ki+=1
                NY.append(fiab)
                NZ.append(float(IT0)/100.)
                if IT0=="00":
                    couleur='r'
                elif IT0=="05":
                    couleur='b'
                elif IT0=="10":
                    couleur='g'
                elif IT0=="15":
                    couleur='m'
            # ************** PARAMETRES *************#
    #            e=3
    #            IT0="05"
                IT=float(IT0)/100.
                nbins=60
            # ******** OUVERTURE FICHIERS ***********#
                fidMCName="D:\\Askri\\Python\\chapitre_6\\IT"+IT0+"_MC\\IT"+IT0+"_MC_CHAPITRE6-2.txt"
                fidAGMINName="D:\\Askri\\Python\\chapitre_6\\IT"+IT0+"_AG_MIN\\IT"+IT0+"_AG_MIN_CHAPITRE6-2.txt"  
#                fidAGMAXNameGlob="D:\\Askri\\Python\\DefLoc_1\\e_"+str(e)+"\\IT"+IT0+"_AG_MAX\\Result\E"+str(e)+"-AG_MAX_IT"+IT0+"-glob.txt"
                fidAGMAXName="D:\\Askri\\Python\\chapitre_6\\IT"+IT0+"_AG_MAX\\IT"+IT0+"_AG_MAX_CHAPITRE6-2.txt"  
                fidMC=open(fidMCName,'r')
                fidAGMIN=open(fidAGMINName,'r')
#                fidAGMAXGlob=open(fidAGMAXNameGlob,'r')
                fidAGMAX=open(fidAGMAXName,'r')


                f0=F0[ki-1]
#                f0=F0[2]
                fmin=readMinMax(fidAGMIN,'min')
#                fmin=10000.
#                fmaxGlob=readMinMax(fidAGMAXGlob,'max')
                fmax=readMinMax(fidAGMAX,'max')
#                fmax=13000.
                xmin=((fmin-f0)/f0)*100.
#                xmaxGlob=((fmaxGlob-f0)/f0)*100.
                xmax=((fmax-f0)/f0)*100.
                w=(xmax-xmin)/(nbins)
#                print("e=",e," fmax=",fmax," fmaxGlob=",fmaxGlob)

            # *********** HISTOGRAMME **************#
#                XITER=range(100,4001,100)
                XITER=[2000]
                for m in XITER:
                    fidMC.seek(0)
                    Flines=fidMC.readlines()
#                    fidMC.close()

                    FMAX=readText(Flines[:m])
                    XDATA=discretization(nbins,xmin,xmax)
                    YDATA=hist(XDATA,FMAX,f0,w)
                    b=0.5
                    XFIT,YFIT=[],[]
                    XFIT.append(XDATA[0])
                    YFIT.append(0.)
                    YFIT.extend(YDATA)
#                    YFIT.append(0.)
                    for i in range(len(XDATA)-1):
                        XFIT.append((b*w)+XDATA[i])
#                    XFIT.append(XDATA[-1])
                    Sp=ponderation(XFIT,B,C)
#                    print(XDATA)
#                    print(YDATA)
#                    print(IT0,xmin)
#                    print(IT0,xmax)
                        
                
                    popt, pcov = curve_fit(loiDistr,XFIT,YFIT,sigma=Sp)
                    alpha=popt[0]
                    beta=popt[1]
#                    print(IT0,alpha,beta)
                    alphaFx=2.7
                    betaFx=26.
#                    alphaFx=3.
#                    betaFx=30.
#                    xminFx=-7.31
#                    alphaFx,betaFx=getAlphaBeta(XDATA,xmin,xmax)
    #                print("e=",e)
#                    print("IT=",IT)
#                    print("alpha=",alpha)
#                    print("beta=",beta)
                    Xplot=np.linspace(xmin,xmax,200)
                    XplotFx=np.linspace(xmin,xmax,200)
                    Yplot,YplotFx=[],[]
                    for x in Xplot:
                        Yplot.append(loiDistr(x,alpha,beta))
                    for xFx in XplotFx:
                        YplotFx.append(loiDistr(xFx,alphaFx,betaFx))
    ##                print(len(Xplot))
    ##                print(len(Yplot))
    ##                print(YDATA)print(XMAXGlob)
    ##                print(w*np.sum(YDATA))
                    xfiabMC,xfiab1,xfiab2=getFMC(fiab,w,XDATA,YDATA)
                    xfiabLoi=getFLoi(fiab,XDATA,alpha,beta)
                    xfiabLoiFx=getFLoi(fiab,XplotFx,alphaFx,betaFx)
                    ALPHA.append(alpha)
                    BETA.append(beta)
                    XMIN.append(xmin)
#                    print(xmin)
#                    XMAXGlob.append(xmaxGlob)
                    XMAX.append(xmax)
                    FIAB.append(xfiabMC)
                    FIABL.append(xfiabLoi)
                    FIABLF.append(xfiabLoiFx)
#                    print(40,xfiabLoi)

#                    if IT0=="00" or IT0=="05" or IT0=="10":
                    ecart=(xfiabMC-xfiabLoi)*100./xfiabMC
                    print(xfiabMC,xfiabLoi)
                    FF.append(xfiabLoi)
#                    elif IT0=="15":
#                        ecart=(xfiabMC-xfiabLoiFx)*100./xfiabMC
#                        print(xfiabMC,xfiabLoiFx)
#                        FF.append(xfiabLoiFx)
#                    else:
#                        print('erreur')
                    ECART.append(ecart)
#                    XFIAB1.append(xfiab1)
#                    XFIAB2.append(xfiab2)
                    
#                    print("IT=",IT0)
#                    print("xfiabLoi=",xfiabLoi)
#                    print("xfiabMC=",xfiabMC)
#                    print("xmax=",xmax)

#            print(ALPHA)
#            print(len(FIABL))
#    print(ALPHA)
#    fig = plt.figure()
#    ax = fig.gca(projection='3d')
#    
#    ax.plot_trisurf(FIABL, NY, NZ, cmap=cm.jet, linewidth=0.2)
                    
#        plt.figure(figsize=(10,10))
###            plt.plot(ITv,((np.array(FIABLF)-np.array(FIABL))/np.array(FIABL))*100,'b-s',label='fiab=0.99',linewidth=2,markersize=8)
###            plt.plot(ITv,FIABL,'r-o',label='fiab=0.99 (auto)',linewidth=2,markersize=8)
###            plt.plot(ITv,FIABLF,'r--',label='fiab=0.99 (manuel)',linewidth=2,markersize=8)
###            plt.plot(ITv,XMIN,'r-o',label='xmin',linewidth=2,markersize=8)
###            plt.plot(ITv,XMAX,'b-s',label='xmax',linewidth=2,markersize=8)
##    plt.plot(Ratio,XMAXGlob,'r-o',label='GLOB',linewidth=2,markersize=8)
#        plt.plot(FIABL,ITv,'bs',label='normale fiab=0.99',linewidth=2,markersize=8)
#        print(FIABL)
#                    a=ITv[2]/xfiabLoi
#                    FIABL.append(30.*a)
#                    plt.plot([0,0.35/a],[0,0.35],'k-',label='normale fiab=0.99'+str(e),linewidth=2,markersize=8)
#    plt.plot(Ratio,FIABL,'g-v',label='Xadm=30%',linewidth=2,markersize=8)

#    print(alpha)
#    print(beta)
#    print(xmax)
#
##    print(XMAXGlob)
#    print(XMIN)
#
##    plt.plot(R,BETA,'b-s',label='BETA',linewidth=2,markersize=8)
###            
#    plt.yticks(np.arange(0.,0.41,0.05))
#    plt.ylim(0,0.4)
#    plt.xticks(np.arange(0.,75.,10.))
#    plt.xlim(0,75)
#    plt.yticks(np.arange(0.,0.31,0.05))
#    plt.ylim(0,0.3)
#    plt.xticks(np.arange(1.,3.1,0.25))
#    plt.xlim(1,3)
#    plt.tick_params(axis='both',labelsize=18)
#    plt.legend(loc='lower right',fontsize=18)
#    plt.grid()

#    FF=[FIABL[0],FIABL[1],FIABL[2],FIABLF[3]]
#    print(FF)
#        A=np.linspace(FF[0],FF[-1],50)
##        B90=-0.0011*A**2.+0.0563*A-0.407
##        B99=-0.0004*A**2.+0.0337*A-0.3474
#        a1=0.13
#        b1=0.75
#        B=a1*np.log(A**b1-FF[0]**b1+1.)
#            
#        plt.figure(figsize=(10,10))
        plt.plot(ITv,ECART,'b-s',label='chapitre 6',linewidth=2)
#        plt.plot(A,B,'b-',label='fiab=0.99',linewidth=2)
#        plt.yticks(np.arange(0.,15.,2.))
#        plt.ylim(0,15.)
#        plt.xticks(np.arange(0,0.4,0.1))
#        plt.xlim(0,0.35)
#        plt.tick_params(axis='both',labelsize=18)
#        plt.legend(loc='lower right',fontsize=18)
#        plt.grid()
                
                
#                plt.plot(XITER,BETA,'b-s',label='BETA',linewidth=2)
#                plt.legend(loc='center right')
#                for i in range(len(XITER)):
#                    plt.annotate(str('{0:.2f}'.format(ALPHA[i])),xy=(XITER[i],ALPHA[i]),xytext=(XITER[i],ALPHA[i]+0.05),fontsize=10)
#                    plt.annotate(str('{0:.2f}'.format(BETA[i])),xy=(XITER[i],BETA[i]),xytext=(XITER[i],BETA[i]+0.05),fontsize=10)
#                print(len(XITER),len(FIABL))
#        print(FIAB)
#        print(FIABL)

#                plt.figure(figsize=(20,10))
#                plt.xlabel("Iteration number",fontsize=20)
#                plt.ylabel("Xi_90 [%]",fontsize=20)
#                plt.plot(XITER,FIABL,'r-',label='Loi beta (chapitre 6)',linewidth=2)
#                plt.plot(XITER,FIAB,'b-',label='MC (chapitre 6)',linewidth=2)
#                plt.legend(loc='upper right',fontsize=18)
#                plt.xticks(range(0,4001,500))
#                plt.yticks(np.arange(10,12.1,0.25))
#                plt.xlim(0,4000)
#                plt.ylim(10,12)
#                plt.tick_params(axis='both',labelsize=18)
#                plt.grid()

                
#                plt.figure(figsize=(20,10))
#                plt.xlabel("Iteration number",fontsize=20)
#                plt.ylabel("Xi_99 [%]",fontsize=20)
#                plt.plot(XITER,FIABL,'g-',label='run-3',linewidth=2)
#                plt.legend(loc='upper right',fontsize=18)
#                plt.xticks(range(0,4001,500))
#                plt.yticks(range(20,27,1))
#                plt.xlim(0,4000)
#                plt.ylim(21,25)
#                plt.tick_params(axis='both',labelsize=18)
#                plt.grid()
    
                
#                plt.figure(figsize=(20,10))
#                plt.xlabel("Iteration number",fontsize=20)
#                plt.ylabel("ALPHA",fontsize=20)
#                plt.plot(XITER,ALPHA,'b-',label='ALPHA',linewidth=2)
#                plt.grid()
#                plt.legend(loc='upper right',fontsize=18)
#                plt.xticks(range(0,4001,500))
#                plt.yticks(np.arange(7.5,9.1,0.25))
#                plt.xlim(0,4000)
#                plt.ylim(7.5,9.)
#                plt.tick_params(axis='both',labelsize=18)
#
##
#                plt.figure(figsize=(20,10))
#                plt.xlabel("Iteration number",fontsize=20)
#                plt.ylabel("BETA",fontsize=20)
#                plt.plot(XITER,BETA,'b-',label='BETA',linewidth=2)
#                plt.grid()
#                plt.legend(loc='upper right',fontsize=18)
#                plt.xticks(range(0,4001,500))
#                plt.yticks(np.arange(28.,36.1,1.))
#                plt.xlim(0,4000)
#                plt.ylim(28,36)
#                plt.tick_params(axis='both',labelsize=18)

                

#                for i in range(len(XITER)):
#                    plt.annotate(str('{0:.1f}'.format(FIAB[i])),xy=(XITER[i],FIAB[i]),xytext=(XITER[i],FIAB[i]+0.1),fontsize=10)


#                     
                
#
#                XLINEMC=[xfiabMC,xfiabMC]
#                XLINEL=[xfiabLoi,xfiabLoi]
#                XLINELF=[xfiabLoiFx,xfiabLoiFx]
#                YLINE=[0.,np.amax(YDATA)]
#                
#        print(len(YDATA))
#                plt.figure(figsize=(20,10))
#    plt.xlabel("CT [%]",fontsize=20)
#    plt.ylabel("Probability density\n(fraction per "+str('{0:.2f}'.format(w))+"% interval)",fontsize=20)
#                plt.bar(XDATA[:-1],YDATA,width=w,color='y',label="MC")
#                plt.plot(XLINEMC,YLINE,'k--',label=u'fiabilité='+str(int(fiab*100))+'% MC',linewidth=2)
#                plt.plot(XLINEL,YLINE,'r--',label=u'fiabilité='+str(int(fiab*100))+'% Loi (auto)',linewidth=2)
#        plt.plot(XLINELF,YLINE,'b--',label=u'fiabilité='+str(int(fiab*100))+'% Loi (manuel)',linewidth=2)
#    plt.plot(Xplot,Yplot,couleur+'-',label=r"$T=40$$\mu$$m$",markersize=8,linewidth=2)
#                plt.plot(XFIT,YFIT,'r-',label="IT=10",markersize=8,linewidth=3)
#                plt.plot(Xplot,Yplot,'b-',label="Loi beta",markersize=8,linewidth=2)

#                plt.plot(XplotFx,YplotFx,'b-',label="Manuel",markersize=8,linewidth=2)

#        plt.plot(Xplot,YplotFx,'r-',label="Loi (manuel) alpha="+str('{0:.2f}'.format(alphaFx))+" / beta="+str('{0:.2f}'.format(betaFx)),markersize=8,linewidth=2)
#                plt.legend(loc='upper right',fontsize=20)
#    plt.xticks(range(-10,91,10))
#                plt.xlim(-10,150)
#                plt.yticks(np.arange(0,0.2,0.01))
#                plt.xticks(range(-10,160,10))
#                plt.ylim(-0.0001,0.13) 
#                plt.tick_params(axis='both',labelsize=16)
#        figname="D:\Askri\Python\DefLoc_1\FIGURES\Distribution_E"+str(e)+"-IT"+str(IT)+"-FIAB"+str(int(100*fiab))+".png"
#        plt.savefig(figname)
#    plt.show()
#    print(quad(loiDistr,xmin,xmax,args=(alpha,beta))[0])

#                print("xfiabMC=",xfiabMC)
#                print("xfiabLoi=",xfiabLoi)
#                print("xfiabLoiFx=",xfiabLoiFx)

#                fidFiab.write(
#                '{0:>4s}'.format(str(fiab))+"\t"+
#                '{0:>2s}'.format(str(e))+"\t"+
#                '{0:>4s}'.format(str(IT))+"\t"+
#                '{0:>5s}'.format(str('{0:.2f}'.format(alpha)))+"\t"+
#                '{0:>5s}'.format(str('{0:.2f}'.format(beta)))+"\t"+
#                '{0:>4s}'.format(str('{0:.2f}'.format(xfiabMC)))+"\t"+
#                '{0:>4s}'.format(str('{0:.2f}'.format(xfiabLoi)))+"\t"+
#                '{0:>4s}'.format(str('{0:.2f}'.format(xfiabLoiFx)))+"\n"                
#                )
                

#            ERRORMC=[np.array(FIABMC)-np.array(XFIAB1),np.array(XFIAB2)-np.array(FIABMC)]
#            ERRORMC=[[1.,1.,1.],[2.,2.,2.]]
#            print(FIABMC)
#            print(XFIAB1)
#            print(XFIAB2)
#            print(ERRORMC)
#            print(ITv)
#            print(FIABMC)
#            plt.figure(figsize=(10,10))
#            plt.plot(ITv,FIABMC,'b-s',label="Statistical approach (Reliability="+str(int(100*fiab))+"%)",markersize=8,linewidth=2)
#            plt.plot(ITv,FIAB100,'g-v',label="Worst-case approach",markersize=8,linewidth=2)
#            plt.errorbar(ITv,FIABMC,yerr=ERRORMC,ecolor='r')
#            plt.plot(ITv,FIABL,'b-s',label="Loi (auto) alpha="+str('{0:.2f}'.format(alpha))+" / beta="+str('{0:.2f}'.format(beta)),markersize=8,linewidth=2)
#            plt.plot(ITv,FIABLF,'g-v',label="Loi (manuel) alpha="+str('{0:.2f}'.format(alphaFx))+" / beta="+str('{0:.2f}'.format(betaFx)),markersize=8,linewidth=2)
#            plt.xlabel("T [mm]",fontsize=22)
#            plt.ylabel(r"$\Delta$$F_{max}/F_{max}^{0}$ [%]",fontsize=22)
#            plt.tick_params(axis='both',labelsize=18)
#            plt.xticks([0.,0.05,0.1])
#            plt.xlim(0.,0.11)
##            plt.yticks(arange(0.,1.1*FIAB100[-1],10.))
#            plt.ylim(0.,61.)
#            plt.legend(loc='upper left',fontsize=18)
##            figname="D:\Askri\Python\DefLoc_1\FIGURES\Fmax-IT_E"+str(e)+"-FIAB"+str(int(100*fiab))+".png"
##            plt.savefig(figname)
#            plt.show()              

#    fidFiab.close()

