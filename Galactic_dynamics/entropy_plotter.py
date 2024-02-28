#This file plots the entropy as a function of radius
import numpy as np
import os, sys, re #agama
import astropy.io
from astropy.io import ascii
from astropy.table import Table
import math
import random
import matplotlib.pyplot as plt

f=open('entropy_mesh.txt','r')
lines=f.readlines()
lines.pop(0) #removes the header
rad=[]
avg_entropy=[]
for l in lines:

    k=l.split()
    rad.append(float(k[0]))
    k.pop(0)
    p=[]
    for q in k:
        p.append(float(q))
    avg_entropy.append(np.average(p))


fig = plt.figure()
ax = fig.gca()
ax.set_xticks(np.arange(0, 4, 0.2))
plt.plot(rad,avg_entropy)
plt.xlabel('Radius(kpc)')
plt.ylabel('Entropy')
plt.grid()
plt.savefig('rad_vs_entropy_plot')
