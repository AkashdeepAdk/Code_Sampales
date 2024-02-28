#splits the orb file in 10 equal files. This is done for using the benefit of parallel run
import numpy as np
import os, sys, re #agama
import astropy.io
from astropy.io import ascii
from astropy.table import Table
import math
import random
import matplotlib.pyplot as plt

g='model_component_disk.orb'
f=open(g,'r')
lines=f.readlines()
print(len(lines))


for m in range(10):
    fname='orb_split'+str(m+1)+'.txt'
    ID=[]
    X=[]
    Y=[]
    Z=[]
    vx=[]
    vy=[]
    vz=[]
    weight=[]
    prior=[]
    inttime=[]

    c=0
    for i in lines:
        c=c+1
        if c>(1+m*((len(lines)-1)/10)) and c<(2+(m+1)*((len(lines)-1)/10)):
            ID.append(c-1)
            X.append(float(i.split()[0]))
            Y.append(float(i.split()[1]))
            Z.append(float(i.split()[2]))
            vx.append(float(i.split()[3]))
            vy.append(float(i.split()[4]))
            vz.append(float(i.split()[5]))
            weight.append(float(i.split()[6]))
            prior.append(float(i.split()[7]))
            inttime.append(float(i.split()[8]))
            
    data = Table()
    data['ID'] = ID
    data['X'] = X
    data['Y'] = Y
    data['Z'] = Z
    data['Vx'] = vx
    data['Vy'] = vy
    data['Vz'] = vz
    data['Weight'] = weight
    data['prior'] = prior
    data['inttime'] = inttime
    ascii.write(data, fname, overwrite=True,delimiter=' ')
    print('split done', m+1)
