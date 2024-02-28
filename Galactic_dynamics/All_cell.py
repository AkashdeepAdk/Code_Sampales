import numpy as np
import os, sys, re
import astropy.io
from astropy.io import ascii
from astropy.table import Table

files=[]
for i in range(1,5):
    files.append(('cell_wise_entropy_'+str(i)+'.txt'))

CellName=[]
entropy=[]
#Mergs the entropies for all four cell_wise_entropy file
for f in files:
    c=0
    g=open(f,'r')
    lines=g.readlines()
    for l in lines:
        c=c+1
        if c>1:
            CellName.append(l.split()[0])
            entropy.append(float(l.split()[1]))

data = Table()
data['CellName'] = CellName
data['entropy'] = entropy
ascii.write(data, 'All_cell_entropy.txt', overwrite=True,delimiter=' ')


import math
import random
import matplotlib.pyplot as plt

#creates the radial and angular mesh of entropy

g='All_cell_entropy.txt'
f=open(g,'r')
lines=f.readlines()
lines.pop(0)

rad=[]
theta=[]
ent_value=[]
for i in range(20):
    rad.append(i*0.2)
    theta.append(i*(math.pi/10))
    ent_value.append([])
c=0
for col in range(20):
    for row in range(20):
        val=lines[((col*20)+row)].split()[1]
        if val!= 'nan':
            ent_value[row].append(float(val))
        else:
            ent_value[row].append(0)
print(ent_value)            
data = Table()
data['rad']=rad
for cl in range(20):
    data[str(theta[cl])]=ent_value[cl]

ascii.write(data, ('entropy_mesh'+'.txt'), overwrite=True,delimiter=' ')