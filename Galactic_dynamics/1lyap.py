#importing required libraries
import numpy as np
import os, sys, re, agama
import astropy.io
from astropy.io import ascii
from astropy.table import Table
import math
import random
import matplotlib.pyplot as plt
import nolds
import warnings
warnings.filterwarnings("ignore")
##this variable is used to run particular orbit file after dividing the orb file into 10 parts
fnum=1
def sumarr(Arr):
    sm=0
    for i in Arr:
        if i>=0:
            sm=sm+i
    return sm
#creating potential models
mypot=agama.Potential(type='Ferrers',scaleRadius='1.36', scaleHeight='0.226', q ='0.1', p ='0.35', sersicIndex='1.0')
mypot1=agama.Potential(type= 'MiyamotoNagai',scaleRadius = 3.0, scaleHeight= 0.28)
mypot2bh=agama.Potential(type='Spheroid',
mass=20,
gamma=1,
beta=3,
scaleRadius=5,
outerCutoffRadius=55,
cutoffStrength=2.5,
)
mypot2bulge=agama.Potential(type='Sersic',
sersicIndex=2,
mass=0.25,
scaleRadius=0.215,
axisratioz=0.8,
)
mypot3=agama.Potential(mypot,mypot1,mypot2bh,mypot2bulge)


def orbit_integration(pot,x,y, z,vx,vy,vz):
    
    times,points = agama.orbit(potential=pot, ic=[x,y,z,vx,vy,vz], Omega=1, time=100, trajsize=10001)
    To=[]
    Xo=[]
    Yo=[]
    Zo=[]
    Vxo=[]
    Vyo=[]
    Vzo=[]
    for i in range(len(times)):
        p=points[i]
        To.append(times[i])
        Xo.append(p[0])
        Yo.append(p[1])
        Zo.append(p[2])
        Vxo.append(p[3])
        Vyo.append(p[4])
        Vzo.append(p[5])
    return To, Xo, Yo, Zo, Vxo,Vyo,Vzo

g='orb_split'+str(fnum)+'.txt'
f=open(g,'r')
lines=f.readlines()
print(len(lines))

counter =0 

index=[]
for ar in range(len(lines)-1):
    index.append((ar+1))
lyap_x=[]
lyap_y=[]
lyap_r=[]
Final_lyap=[]

c=0
for i in lines:
    c=c+1
    if c>1 :
        counter = counter+1
        initXYZ=[]
        x=(float(i.split()[0]))
        y=(float(i.split()[1]))
        z=(float(i.split()[2]))
        vx=(float(i.split()[3]))
        vy=(float(i.split()[4]))
        vz=(float(i.split()[5]))
        To, Xo, Yo, Zo, Vxo,Vyo,Vzo=orbit_integration(mypot3,x,y, z,vx,vy,vz)
        #plt.plot(Xo,Yo)
        #plt.savefig('plot')
        rad = []
        theta=[]
        for j in range (len(Xo)):
            # Calculating angle and radial distance
            rad.append(np.sqrt(np.square(Xo[j])+np.square(Yo[j])))
            if Yo[j]>0 and Xo[j]<0:
                theta.append(math.pi+math.atan(Yo[j]/Xo[j]))
            if Yo[j]<0 and Xo[j]<0:
                theta.append(math.pi+math.atan(Yo[j]/Xo[j]))
            if Yo[j]<0 and Xo[j]>0:
                theta.append(2*(math.pi)+math.atan(Yo[j]/Xo[j]))
            if Yo[j]>0 and Xo[j]>0:
                theta.append(math.atan(Yo[j]/Xo[j]))

        
        #calculating lyapunov exponents for subspaces
        
        Lmx=nolds.lyap_r(Xo)
        
        
        Lmy=nolds.lyap_r(Yo)
        
        Lmrad=nolds.lyap_r(rad)
        
        lyap_x.append(Lmx)
        lyap_y.append(Lmy)
        lyap_r.append(Lmrad)
        
        arr1 = [Lmx,Lmy,Lmrad]
        sm1 = sumarr(arr1)     #calculating ks entropy
        Final_lyap.append(sm1)
        fl.close()


                        
        #print(all_cells)
        #print(all_fractimes)
        if (counter%100)==0:
           print(counter,"done - lyap-",str(fnum))
#creating file containing the entropy for all trajectories     
data = Table()
data['ID'] = index
data['Entropy'] = Final_lyap
ascii.write(data, ('entropy_list_maximal'+str(fnum)+'.txt'), overwrite=True,delimiter=' ')     
