#this file gives the center of the galaxy
import numpy as np
import os, sys, re, agama
import astropy.io
from astropy.io import ascii
from astropy.table import Table
import math
import random
import matplotlib.pyplot as plt

#!/usr/bin/python



g='model_component_disk.orb'
f=open(g,'r')
lines=f.readlines()
print(len(lines))


ID=[]
X=[]
Y=[]
Z=[]
    

c=0
for i in lines:
    c=c+1
    if c>1:

        ID.append(c-1)
        X.append(float(i.split()[0]))
        Y.append(float(i.split()[1]))
        Z.append(float(i.split()[2]))

centreX= np.average(X)
centreY = np.average(Y)
centreZ=  np.average(Z)
print([centreX,centreY,centreZ])
