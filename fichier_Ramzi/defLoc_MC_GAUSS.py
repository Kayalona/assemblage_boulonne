# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 17:09:31 2015

@author: ramzi
"""

from __future__ import division, print_function
import numpy as np
from numpy import cos,sin,arctan,pi,arange
import copy
import os
import random
#import shutil
import time
import warnings
warnings.filterwarnings('ignore')

################################ createBatFile ################################
def createBatFile(batFileDIR,odbDIR,inpName,cpus):
    batFileName=batFileDIR+"batFile.bat"
    batFile=open(batFileName,'w')
#    batFile.write("echo off\n")
    batFile.write("cd "+odbDIR+"\n")
    batFile.write("abaqus job=MB-0 cpus="+str(cpus)+" interactive")
    return batFileName
    
################################# createNewInp ################################
def createNewInp(oldInpName,odbDIR,clr,EXC,ANG_IN):
    from defLoc_Lib import occurLine
    from defLoc_Lib import readCoord
    from defLoc_Lib import generDefLoc
    from defLoc_Lib import generVectDefLoc
    from defLoc_Lib import replaceText
    from defLoc_Lib import writeCoordText

    oldInp=open(oldInpName,"r")    
    oldInp.seek(0)
    oldInpText=oldInp.read()
    
    oldInp.seek(0)
    debutCoordPlaque2=occurLine(oldInp,
    '*Part, name=Plaque-Composite\n')+2
    finCoordPlaque2=occurLine(oldInp,
    ' 1, 129,   2, 156, 845, 136,   1, 148, 833\n')-2  
    
    oldCoordText2,n2,x2,y2,z2=readCoord(oldInp,
    debutCoordPlaque2,finCoordPlaque2)
    oldInp.close()
    
    excX2,excY2=generVectDefLoc(EXC,ANG_IN)        
    newLocalX2,newLocalY2=generDefLoc(n2,x2,y2,z2,clr,excX2,excY2)
    newCoordText2=writeCoordText(n2,newLocalX2,newLocalY2,z2) 
    newInpName="MB-0.inp"
    newInp=open(odbDIR+newInpName,'w')
    newInpText2=replaceText(oldCoordText2,newCoordText2,oldInpText)
    newInp.write(newInpText2)
    newInp.close()
    return newInpName

################################# generDefLoc #################################
def generDefLoc(n,x,y,z,J,excX,excY):                  
                   
    compteur=0
    tolLoc=0.05
    r0=3.175    
    x0=55.        
    y0=15.
    dx=30.
    dy=30.
    newLocalX,newLocalY=copy.copy(x),copy.copy(y)
    xc=np.zeros(4)
    yc=np.zeros(4)
#    i=np.array([1,2,1,2])
#    j=np.array([1,1,2,2])
    i=np.array([2,1,2,1])
    j=np.array([2,2,1,1])
    R=np.zeros(len(i))
    S=np.zeros(len(i))
    Alpha=np.zeros(len(i))
#    if max(max(excX),max(excY))<=clr or len(excX)!=4:
    for k in range (len(n)):
        for p in range(len(i)):
            xc[p]=x0+(i[p]-1)*dx
            yc[p]=y0+(j[p]-1)*dy
            R[p]='{0:.8f}'.format(((x[k]-xc[p])**2.+(y[k]-yc[p])**2.)**0.5)
            S[p]=(y[k]-yc[p])/(x[k]-xc[p])
            Alpha[p]=arctan(S[p])
            if (R[p]<=r0+tolLoc) and (x[k]<xc[p]):
                compteur+=1
                newLocalX[k]=x[k]+excX[p]-J[p]*cos(Alpha[p])
                newLocalY[k]=y[k]+excY[p]-J[p]*sin(Alpha[p])
            elif (R[p]<=r0+tolLoc) and (x[k]>=xc[p]):
                compteur+=1
                newLocalX[k]=x[k]+excX[p]+J[p]*cos(Alpha[p])
                newLocalY[k]=y[k]+excY[p]+J[p]*sin(Alpha[p])
    return newLocalX,newLocalY
      

############################### generVectDefLoc ###############################    
def generVectDefLoc(EXC,ANG_IN):
#    from defLoc_Lib import inverseVectCol
    excX,excY=[],[]
    for i in range(len(ANG_IN)):
        excx=EXC[i]*cos(ANG_IN[i]*(pi/180.))
        excy=EXC[i]*sin(ANG_IN[i]*(pi/180.))
        excX.append(excx)
        excY.append(excy)
    return np.array(excX),np.array(excY)
    
################################ getMax #######################################
def getMax(v):
    valMax=v[0]
    iMax=0
    for i in range(0,len(v)-1,1):
        if v[i+1]>valMax:
            valMax=v[i+1]
            iMax=i+1
    return iMax,valMax

############################ inverseVectCol ###################################
def inverseVectCol(v):
    nV=[]
    for i in range(len(v)):
        nV.append(v[len(v)-i-1])
    return np.array(nV)

############################### occurLine #####################################
def occurLine(oldInp,occurence):
    oldInp.seek(0)
    for j,u in enumerate(oldInp):
        if (occurence==u):
            break
    return j
############################## permuteItem ####################################
def permuteItem(A,i,j):
    for k in range(len(A)):
        if k==i:
            s=A[i]
            A[i]=A[j]
            A[j]=s
    return A            
############################## postTraitODB ###################################
def postTraitODB(odbName,resultDIR):
    print('--------------------------START POST-TRAIT ODB----------------------------')
    import warnings
    warnings.filterwarnings('ignore')
#    from sys import path
#    path.append(os.getcwd()+'/abaqus_lib/')
    from abaqus import *
    from abaqusConstants import *
    from caeModules import *
    from odbAccess import openOdb
    from viewerModules import *    
    ANGLES0,ANGLES,RCTF0,RCTF=[],[],[],[]
    try:
        o1 = session.openOdb(name=odbName)
        session.viewports['Viewport: 1'].setValues(displayedObject=o1)
        odb = session.odbs[odbName]
        session.fieldReportOptions.setValues(printTotal=OFF, printMinMax=OFF)
        session.writeFieldReport(
            fileName=resultDIR+'ODB.txt', 
            append=OFF, sortItem='Element Label', odb=odb, step=0, frame=1, 
            outputPosition=WHOLE_ELEMENT, variable=(('CTF', WHOLE_ELEMENT, ((COMPONENT, 'CTF2'), (COMPONENT, 'CTF3'), )), ))
        session.odbs[odbName].close()
#        print('ODB RESULT FILE CREATED')
    except:
#        exit('UNABLE TO EXTRACT RESULTS FROM ODB')
        pass
    try:
        fidODB=open(resultDIR+'ODB.txt',"r")
#        print('READING ODB RESULT FILE')
    except:
#        print('UNABLE TO OPEN ODB RESULT FILE')
        pass

    for i,u in enumerate(fidODB):
        if i in [19,27,35,43]:
            try:
                label,ctf2,ctf3=u.split()
                RCTF0.append((float(ctf2)**2.+float(ctf3)**2.)**0.5)
                ANGLES0.append(arctan(float(ctf2)/float(ctf3)))
            except:
                print('ERREUR CALCUL SORTIES')
                pass
    try:
        idCTFMAX,CTFMAX=getMax(RCTF0)
    except:
        print('UNABLE TO GET MAX RCTF')
        pass
    fidODB.close()
    try:
        ANGLES=permuteItem(ANGLES0,1,2)
        RCTF=permuteItem(RCTF0,1,2)
    except:
        print('UNABLE TO PERMUTE ANGLE AND RCTF')
        pass
    return idCTFMAX,CTFMAX,ANGLES,RCTF

################################ readCoord ####################################
def readCoord(oldInp,firstLine,lastLine):
    oldInp.seek(0)
    N,X,Y,Z=[],[],[],[]
    oldCoordPlaqueText=''
    for i,u in enumerate(oldInp):
        if (i>=firstLine) and (i<=lastLine):
            try:
                n,x,y,z=map(float,u.split(','))
                N.append(int(n))
                X.append(x)
                Y.append(y)
                Z.append(z)
                oldCoordPlaqueText+=u
            except:
                pass
    VN, VX, VY, VZ=np.array(N),np.array(X),np.array(Y),np.array(Z)
    return oldCoordPlaqueText,VN,VX,VY,VZ

################################ readVectCol ##################################    
def readVectCol(fid):
    VectCol=[]
    for u in fid:
        val=float(u)
        VectCol.append(val)
    return np.array(VectCol)

################################ replaceText ##################################    
def replaceText(oldText,newText,oldInpText):
    if oldText in oldInpText:
#        print('oldtext trouve !!!')
        newInpText=oldInpText.replace(oldText,newText)
    else:
#        print('tu es dans la merde')
        pass
    return newInpText

################################### Run ####################################### 
def runOs(inputFile,calculDIR):
    print("start running...")
    os.system("D:\\Askri\\Python\\chapitre_6_2\\IT30_MC\\batFile.bat")
#    import os
#    from sys import path
#    path.append(os.getcwd()+'/abaqus_lib/')
#    print('abaqus lib path')
#    from abaqus import *
#    from abaqusConstants import *
#    from caeModules import *
#    from driverUtils import executeOnCaeStartup
#    print('ok run0s 1')
#    session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=331.800506591797, 
#        height=268.111114501953)
#    session.viewports['Viewport: 1'].makeCurrent()
#    session.viewports['Viewport: 1'].maximize()
#
#    executeOnCaeStartup()
#    print('ok run0s 2')
#    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
#        referenceRepresentation=ON)
#    a = mdb.models['Model-1'].rootAssembly
#    session.viewports['Viewport: 1'].setValues(displayedObject=a)
#    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
#        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
#    mdb.JobFromInputFile(name='MB-0', 
#        inputFileName=inputFile, 
#        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
#        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
#        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, userSubroutine='', 
#        scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=4, 
#        activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=4)
#    print('ok run0s 2')
#    os.chdir(calculDIR)
#    mdb.jobs['MB-0'].submit(consistencyChecking=OFF)
#    print('ok run0s 3')
    
   
################################# sendMail ####################################
def sendMail(test):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    if test==True:
        body = "CALCUL TERMINE"
    else:
        body = "PROBLEME DE CALCUL"
    fromaddr = "boltedjoint@outlook.fr"
    toaddr = "ramzi.askri@u-bordeaux.fr"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "FIN DE CALCUL"
     
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, "Multi-ConnectedRigidSurfaces")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    messageInfo="MAIL SENT"
    return messageInfo

################################ writeCoordText ###############################
def writeCoordText(n,x,y,z):
    coordText=''
    for i in range(len(n)):
        coordText+='{0:>7}'.format(str(int(n[i])))+', {0:>12}'.format(str('{0:.6f}'.format(x[i])))+', {0:>12}'.format(str('{0:.6f}'.format(y[i])))+', {0:>12}'.format(str('{0:.6f}'.format(z[i])))+'\n'
    return coordText

def writeTeteB_lin_1_1(P,oldInpText):
#    print("TeteB_lin_1_1")
    oldText="*Instance, name=TeteB-lin-1-1, part=Vis-1"+"\n"+"         55.,          15.,        8.128"+"\n"+"         55.,          15.,        8.128,          56.,          15.,        8.128,          90."
    newText="*Instance, name=TeteB-lin-1-1, part=Vis-1"+"\n"+"         55.,          15.,        "+str(8.128-P[0])+"\n"+"         55.,          15.,        "+str(8.128-P[0])+",          56.,          15.,        "+str(8.128-P[0])+",          90."
    return oldText,newText

def writeTeteB_lin_1_2(P):
#    print("TeteB_lin_1_2")
    oldText="*Instance, name=TeteB-lin-1-2, part=Vis-1"+"\n"+"         55.,          45.,        8.128"+"\n"+"         55.,          45.,        8.128,          56.,          45.,        8.128,          90."
    newText="*Instance, name=TeteB-lin-1-2, part=Vis-1"+"\n"+"         55.,          45.,        "+str(8.128-P[1])+"\n"+"         55.,          45.,        "+str(8.128-P[1])+",          56.,          45.,        "+str(8.128-P[1])+",          90."
    return oldText,newText        

def writeTeteB_lin_2_1(P):
#    print("TeteB_lin_2_1")
    oldText="*Instance, name=TeteB-lin-2-1, part=Vis-1"+"\n"+"         85.,          15.,        8.128"+"\n"+"         85.,          15.,        8.128,          86.,          15.,        8.128,          90."
    newText="*Instance, name=TeteB-lin-2-1, part=Vis-1"+"\n"+"         85.,          15.,        "+str(8.128-P[2])+"\n"+"         85.,          15.,        "+str(8.128-P[2])+",          86.,          15.,        "+str(8.128-P[2])+",          90."
    return oldText,newText

def writeTeteB_lin_2_2(P):
#    print("TeteB_lin_2_2")
    oldText="*Instance, name=TeteB-lin-2-2, part=Vis-1"+"\n"+"         85.,          45.,        8.128"+"\n"+"         85.,          45.,        8.128,          86.,          45.,        8.128,          90."
    newText="*Instance, name=TeteB-lin-2-2, part=Vis-1"+"\n"+"         85.,          45.,        "+str(8.128-P[3])+"\n"+"         85.,          45.,        "+str(8.128-P[3])+",          86.,          45.,        "+str(8.128-P[3])+",          90."
    return oldText,newText
# *****************************************************************************#

def writeTeteA_lin_1_1(P):
#    print("TeteA_lin_1_1")
    oldText="*Instance, name=TeteA-lin-1-1, part=Vis-1"+"\n"+"         55.,          15.,  0."+"\n"+"         55.,          15.,  0.,          54.,          15.,  0.,          90."
    newText="*Instance, name=TeteA-lin-1-1, part=Vis-1"+"\n"+"         55.,          15.,  "+str(P[0])+"\n"+"         55.,          15.,  "+str(P[0])+",          54.,          15.,  "+str(P[0])+",          90."
    return oldText,newText

def writeTeteA_lin_1_2(P):
#    print("TeteA_lin_1_2")
    oldText="*Instance, name=TeteA-lin-1-2, part=Vis-1"+"\n"+"         55.,          45.,  0."+"\n"+"         55.,          45.,  0.,          54.,          45.,  0.,          90."
    newText="*Instance, name=TeteA-lin-1-2, part=Vis-1"+"\n"+"         55.,          45.,  "+str(P[1])+"\n"+"         55.,          45.,  "+str(P[1])+",          54.,          45.,  "+str(P[1])+",          90."
    return oldText,newText        

def writeTeteA_lin_2_1(P):
#    print("TeteA_lin_2_1")
    oldText="*Instance, name=TeteA-lin-2-1, part=Vis-1"+"\n"+"         85.,          15.,  0."+"\n"+"         85.,          15.,  0.,          84.,          15.,  0.,          90."
    newText="*Instance, name=TeteA-lin-2-1, part=Vis-1"+"\n"+"         85.,          15.,  "+str(P[2])+"\n"+"         85.,          15.,  "+str(P[2])+",          84.,          15.,  "+str(P[2])+",          90."
    return oldText,newText

def writeTeteA_lin_2_2(P):
#    print("TeteA_lin_2_2")
    oldText="*Instance, name=TeteA-lin-2-2, part=Vis-1"+"\n"+"         85.,          45.,  0."+"\n"+"         85.,          45.,  0.,          84.,          45.,  0.,          90."
    newText="*Instance, name=TeteA-lin-2-2, part=Vis-1"+"\n"+"         85.,          45.,  "+str(P[3])+"\n"+"         85.,          45.,  "+str(P[3])+",          84.,          45.,  "+str(P[3])+",          90."
    return oldText,newText
       
if __name__ == "__main__":
    print("START MAIN")
    IT0="30"
    IT=float(IT0)/100.
    e=2
    

    calculDIR="D:\\Askri\\Python\\chapitre_6_2\\IT30_MC\\"
    oldInpName=calculDIR+"MCRS_4_Boulons_ORIGINAL_PRECH.inp"
    odbName=calculDIR+"MB-0.odb"
    oldInp=open(oldInpName,"r")
    

    oldInp.seek(0)
    oldInpText=oldInp.read()

    
    oldInp.seek(0)
    debutCoordPlaque2=occurLine(oldInp,'*Part, name=Plaque-Composite\n')+2
    finCoordPlaque2=occurLine(oldInp,' 1, 129,   2, 156, 845, 136,   1, 148, 833\n')-2  
    
    oldCoordText2,n2,x2,y2,z2=readCoord(oldInp,debutCoordPlaque2,finCoordPlaque2)
    oldInp.close()

    try:
        os.remove(calculDIR+"MB-0.inp")
        os.remove(calculDIR+"MB-0.odb")
        os.remove(calculDIR+"MB-0.dat")
        os.remove(calculDIR+"MB-0.sta")
        os.remove(calculDIR+"MB-0.com")
        os.remove(calculDIR+"MB-0.msg")
        os.remove(calculDIR+"MB-0.prt")
        os.remove(calculDIR+"MB-0.sim")
        os.remove(calculDIR+"MB-0.lck")
        os.remove(calculDIR+"MB-0.cid")
    except:
        pass
    
    ################### DECLARATION VARIABLES ################
    ntotConfig=2000
#    batFileName="D:\\Askri\\Python\\DefLoc_1\\e_"+str(e)+"\\IT"+IT0+"_MC\\batFile\\batFile.bat"
    
    fidResultName=calculDIR+"IT30_MC_CHAPITRE6-XY.txt"
    fidResult=open(fidResultName,'w')
    fidResult.write(
    '{0:>4s}'.format("IND")+"\t"+
    '{0:>8s}'.format("DX_1")+"\t"+
    '{0:>8s}'.format("DX_2")+"\t"+
    '{0:>8s}'.format("DX_3")+"\t"+
    '{0:>8s}'.format("DX_4")+"\t"+
    '{0:>8s}'.format("DY_1")+"\t"+
    '{0:>8s}'.format("DY_2")+"\t"+
    '{0:>8s}'.format("DY_3")+"\t"+
    '{0:>8s}'.format("DY_4")+"\t"+
    '{0:>8s}'.format("JEU1")+"\t"+
    '{0:>8s}'.format("JEU2")+"\t"+
    '{0:>8s}'.format("JEU3")+"\t"+
    '{0:>8s}'.format("JEU4")+"\t"+
    '{0:>8s}'.format("INT1")+"\t"+
    '{0:>8s}'.format("INT2")+"\t"+
    '{0:>8s}'.format("INT3")+"\t"+
    '{0:>8s}'.format("INT4")+"\t"+
    '{0:>8s}'.format("F1")+"\t"+
    '{0:>8s}'.format("F2")+"\t"+
    '{0:>8s}'.format("F3")+"\t"+
    '{0:>8s}'.format("F4")+"\t"+
    '{0:>8s}'.format("FIT")+"\t"+
    '{0:>10s}'.format("TIME")+"\n"   
    )
    fidResult.close()
    
    # paramètres incertains #
    delta_J=0.06
    delta_P=0.025
    mu_X,sigma_X=0,IT/6.
    mu_Y,sigma_Y=0,IT/6.
    mu_J,sigma_J=(IT+delta_J)/2.,delta_J/6.
    mu_P,sigma_P=0.045,delta_P/6.


    
    ################################################################################################   
    ############################ CALCUL EN BOUCLE ###########################
    for i in range(1,ntotConfig+1,1):
        print('START1')
        try: 
            A=[]           
            v1=random.gauss(mu_X,sigma_X)
            A.append(v1)
            v2=random.gauss(mu_X,sigma_X)
            A.append(v2)
            v3=random.gauss(mu_X,sigma_X)
            A.append(v3)
            v4=random.gauss(mu_X,sigma_X)
            A.append(v4)
            
            T=[]
            t1=random.gauss(mu_Y,sigma_Y)
            T.append(t1)
            t2=random.gauss(mu_Y,sigma_Y)
            T.append(t2)
            t3=random.gauss(mu_Y,sigma_Y)
            T.append(t3)
            t4=random.gauss(mu_Y,sigma_Y)
            T.append(t4)
            
            J=[]
            j1=random.gauss(mu_J,sigma_J)
            J.append(j1)
            j2=random.gauss(mu_J,sigma_J)
            J.append(j2)
            j3=random.gauss(mu_J,sigma_J)
            J.append(j3)
            j4=random.gauss(mu_J,sigma_J)
            J.append(j4)

            I=[]
            i1=random.gauss(mu_P,sigma_P)
            I.append(i1)
            i2=random.gauss(mu_P,sigma_P)
            I.append(i2)
            i3=random.gauss(mu_P,sigma_P)
            I.append(i3)
            i4=random.gauss(mu_P,sigma_P)
            I.append(i4)            
            
            
            print(
            "\n\n**************************************************************************\n"
            )
            print("MONTE CARLO IT="+str(float(IT)))
            print("ITERATION: "+str(int(i))+" / "+str(ntotConfig))
            print("--------------------------------PARAMETRES--------------------------------")    
            print('D_X:   '
            '{0:>10s}'.format(str('{0:.3f}'.format(A[0])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(A[1])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(A[2])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(A[3])))    
            )
            print('D_Y:   '
            '{0:>10s}'.format(str('{0:.3f}'.format(T[0])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(T[1])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(T[2])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(T[3])))    
            )
            print('JEU:   '
            '{0:>10s}'.format(str('{0:.3f}'.format(J[0])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(J[1])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(J[2])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(J[3])))    
            )
            print('INT:   '
            '{0:>10s}'.format(str('{0:.3f}'.format(I[0])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(I[1])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(I[2])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(I[3])))    
            )
            
            #///////////////// SUPRESSION DES FICHIERS CALCULS //////////////#
            try:
                os.remove(calculDIR+"MB-0.inp")
                os.remove(calculDIR+"MB-0.odb")
                os.remove(calculDIR+"MB-0.dat")
                os.remove(calculDIR+"MB-0.sta")
                os.remove(calculDIR+"MB-0.com")
                os.remove(calculDIR+"MB-0.msg")
                os.remove(calculDIR+"MB-0.prt")
                os.remove(calculDIR+"MB-0.sim")
                os.remove(calculDIR+"MB-0.lck")
            except:
                pass
            #////////////////////// CREATION NOUVEAU INP ///////////////////#
#            print('OK1')
#            excX2,excY2=generVectDefLoc(T,A)
            excX2,excY2=np.array(T),np.array(A)

#            print('OK2')
            newLocalX2,newLocalY2=generDefLoc(n2,x2,y2,z2,J,excX2,excY2)
            newCoordText2=writeCoordText(n2,newLocalX2,newLocalY2,z2)                
            newInpName=calculDIR+"MB-0.inp"
            newInp=open(newInpName,'w')
#            print('OK3')
            newInpText2=replaceText(oldCoordText2,newCoordText2,oldInpText)
#            print('OK4')
            OTEXT1,NTEXT1=writeTeteB_lin_1_1(I,oldInpText)
#            print('OK5')
            newInpText3=replaceText(OTEXT1,NTEXT1,newInpText2)
#            print('OK6')
            OTEXT2,NTEXT2=writeTeteB_lin_1_2(I)
#            print('OK7')
            newInpText4=replaceText(OTEXT2,NTEXT2,newInpText3)
#            print('OK8')
            OTEXT3,NTEXT3=writeTeteB_lin_2_1(I)
#            print('OK9')
            newInpText5=replaceText(OTEXT3,NTEXT3,newInpText4)
#            print('OK10')
            OTEXT4,NTEXT4=writeTeteB_lin_2_2(I)
#            print('OK11')
            newInpText6=replaceText(OTEXT4,NTEXT4,newInpText5)
#            print('OK12')
            
            OTEXT5,NTEXT5=writeTeteA_lin_1_1(I)
#            print('OK12')
            newInpText7=replaceText(OTEXT5,NTEXT5,newInpText6)
#            print('OK13')
            OTEXT6,NTEXT6=writeTeteA_lin_1_2(I)
#            print('OK14')
            newInpText8=replaceText(OTEXT6,NTEXT6,newInpText7)
#            print('OK15')
            OTEXT7,NTEXT7=writeTeteA_lin_2_1(I)
#            print('OK16')
            newInpText9=replaceText(OTEXT7,NTEXT7,newInpText8)
#            print('OK17')
            OTEXT8,NTEXT8=writeTeteA_lin_2_2(I)
#            print('OK18')
            newInpText10=replaceText(OTEXT8,NTEXT8,newInpText9)
#            print('OK19')
            newInp.write(newInpText10)
#            print('OK20')
            newInp.close()
#            print(newInpName)
#            print('NEW INP CREATED')
            #////////////////////// COPIE DU INP POUR VERIF ////////////////#
#            shutil.copy(newInpName,"D:\\Askri\\Python\\DefLoc_1\\e_"+str(e)+"\\IT"+IT0+"_MC\\verifINP\\MB-"+str(i)+".inp")
            print("--------------------------------RUNNING-----------------------------------")    
            #///////////////////////////// CALCUL //////////////////////////#
            ti=time.clock()
            runOs(newInpName,calculDIR)
            tf=time.clock()
            duree=tf-ti
            TEMPS=str('%0*d'%(2,int(duree/60)))+":"+str('%0*d'%(2,int(duree%60)))                           
            #//////////////////////// POST-TRAITEMENT //////////////////////#            
            idCTFMAX,CTFMAX,ANGLES,RCTF=postTraitODB(odbName,calculDIR)
            print('POST-TRAIT FINISHED')
            print("-----------------------------RECAPITULATIF--------------------------------")    
            print('D_X:'
            '{0:>10s}'.format(str('{0:.3f}'.format(A[0])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(A[1])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(A[2])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(A[3])))    
            )
            print('D_Y:   '
            '{0:>10s}'.format(str('{0:.3f}'.format(T[0])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(T[1])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(T[2])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(T[3])))    
            )
            print('JEU:   '
            '{0:>10s}'.format(str('{0:.3f}'.format(J[0])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(J[1])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(J[2])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(J[3])))    
            )
            print('INT:   '
            '{0:>10s}'.format(str('{0:.3f}'.format(I[0])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(I[1])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(I[2])))+"\t"+
            '{0:>10s}'.format(str('{0:.3f}'.format(I[3])))    
            )
            print('FMAX:  '
            '{0:>10s}'.format(str('{0:.0f}'.format(CTFMAX)))    
            )
            print("DUREE CALCUL=\t"+TEMPS)    
            print("--------------------------------------------------------------------------")
                
            #/////////////////// ECRITURE FICHIER RESULTATS ////////////////#
            fidResult=open(fidResultName,"a")
            fidResult.write(
            '{0:>4s}'.format(str(i))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(T[0])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(T[1])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(T[2])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(T[3])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(A[0])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(A[1])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(A[2])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(A[3])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(J[0])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(J[1])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(J[2])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(J[3])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(I[0])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(I[1])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(I[2])))+"\t"+
            '{0:>8s}'.format(str('{0:.3f}'.format(I[3])))+"\t"+
            '{0:>8s}'.format(str('{0:.0f}'.format(RCTF[0])))+"\t"+
            '{0:>8s}'.format(str('{0:.0f}'.format(RCTF[1])))+"\t"+
            '{0:>8s}'.format(str('{0:.0f}'.format(RCTF[2])))+"\t"+
            '{0:>8s}'.format(str('{0:.0f}'.format(RCTF[3])))+"\t"+
            '{0:>8s}'.format(str('{0:.0f}'.format(CTFMAX)))+"\t"+
            '{0:>10s}'.format(TEMPS)+"\n"
            )
            fidResult.close()
            
        except:
            print('PROBLEME')
            pass
            
    ############################################################################################
    ############################################################################################

    #///////////////////////// SEND MAIL //////////////////////////////#
#    test=True
#    try:
#        messageInfo=sendMail(test)
#        print(messageInfo)
#    except:
#        exit('UNABLE TO SEND MAIL')
#    del i,t,k,exc,jeu,ntotConfig,JeuMIN,JeuMAX,IncJeu,vJeu,ExcMIN,IncExc,vExc
#    del fidRecapFile,fidSta,idCTFMAX_0,CTFMAX_0,ANGLES_0,RCTF_0,testJob
#    del fidStaName,calculDIR,lastLine,newLocalX1,newLocalY1,newLocalX2,newLocalY2,batFileName
