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

#this variable is used to run particular orbit file after dividing the orb file into 10 parts
fnum=1

def sumarr(Arr):
    sm=0
    for i in Arr:
        if i>=0:
            sm=sm+i
    return sm

#center of the galaxy obtained from gal_center.py
centre=[0.030417353668885715, -0.008148101083228573, 0.0031331802865285714]

#forming the potential models
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

#Defining the orbit integration function
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

#g='model_component_disk.orb'
#f=open(g,'r')
#lines=f.readlines()
#print(len(lines))
g='orb_split'+str(fnum)+'.txt'
f=open(g,'r')
lines=f.readlines()


counter =0 

index=[]
for ar in range(len(lines)-1):
    index.append((ar+1))
lyap_x=[]
lyap_y=[]
lyap_r=[]
Final_lyap=[]

all_CellName=[]
for i in range(20):
    for j in range(20):
        CellName='cell'+str(i)+'R'+str(j)+'T'
        all_CellName.append(CellName)
Final_frac=[]
for i in all_CellName:
    Final_frac.append([])
count=0
#print(len(lines))
#print('done 2')
c=0
counter = 0

c=0
for i in lines:
    c=c+1
    if c>1 :
        #obtaining the initial conditions
        counter = counter+1
        initXYZ=[]
        x=(float(i.split()[1]))
        y=(float(i.split()[2]))
        z=(float(i.split()[3]))
        vx=(float(i.split()[4]))
        vy=(float(i.split()[5]))
        vz=(float(i.split()[6]))
        To, Xo, Yo, Zo, Vxo,Vyo,Vzo=orbit_integration(mypot3,x,y, z,vx,vy,vz) #Obtaining the trajectories
        #plt.plot(Xo,Yo)
        #plt.savefig('plot')
        rad = []
        theta=[]
        for j in range (len(Xo)):
            #calculating radius and angle
            rad.append(np.sqrt(np.square(Xo[j]-centre[0])+np.square(Yo[j]-centre[1])))
            if Yo[j]>0 and Xo[j]<0:
                theta.append(math.pi+math.atan(Yo[j]/Xo[j]))
            if Yo[j]<0 and Xo[j]<0:
                theta.append(math.pi+math.atan(Yo[j]/Xo[j]))
            if Yo[j]<0 and Xo[j]>0:
                theta.append(2*(math.pi)+math.atan(Yo[j]/Xo[j]))
            if Yo[j]>0 and Xo[j]>0:
                theta.append(math.atan(Yo[j]/Xo[j]))
        


        all_cells=[]
        all_fractimes=[]

        #print(rad)
        #print(theta)
        #plt.plot(To,theta)
        #plt.savefig('angle')

        #plt.plot(To,rad)
        #plt.savefig('rad')

        for time in range(len(To)):
            if rad[time]<4:
                for r1 in range(20):
                    if r1*0.2 < rad[time] and rad[time]<((r1+1)*0.2): #checking the radial grid number
                       r0=r1
                    if r1*((math.pi)/10)<theta[time] and (r1+1)*((math.pi)/10)>theta[time]:  #checking the angular grid number
                       th0=r1
                cell0='cell'+str(r0)+'R'+str(th0)+'T'  #assigning the grid
                cell_time=1
                #calculating the time spent in a particular cell
                if cell0 in all_cells:
                    ind=all_cells.index(cell0)
                    all_fractimes[ind]=all_fractimes[ind]+cell_time
                else:
                    all_cells.append(cell0)
                    all_fractimes.append(cell_time) 
        all_fractimes=all_fractimes/np.sum(len(To))
        for cl in all_CellName:
            ct=all_CellName.index(cl)
            if cl in all_cells:
                cind=all_cells.index(cl)
                Final_frac[ct].append(all_fractimes[cind])
            else:
                Final_frac[ct].append(0)
        if (counter%100)==0:
            print(counter,"done - frac_time-",str(fnum))



index=[]
for ar in range(len(lines)-1):
    index.append((ar+1))
#creating the file containg the fraction of time spent by each orbit in each cell
data = Table()
data['ID'] = index
for cl in all_CellName:
    ct=all_CellName.index(cl)
    data[str(cl)]=Final_frac[ct]
#data['Entropy'] = Final_lyap
ascii.write(data, ('Cell_frac_time_'+str(fnum)+'.txt'), overwrite=True,delimiter=' ')

                
        

