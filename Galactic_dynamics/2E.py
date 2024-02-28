import numpy as np
import os, sys, re #agama
import astropy.io
from astropy.io import ascii
from astropy.table import Table
import math
import random
import matplotlib.pyplot as plt

all_CellName=[]
for i in range(20):
    for j in range(20):
        CellName='cell'+str(i)+'R'+str(j)+'T'
        all_CellName.append(CellName)
cell_ent=[]
orb_ent=[]
weights=[]
g='model_component_disk.orb'
f=open(g,'r')
lines=f.readlines()
c=0
for i in lines:
    c=c+1
    if c>1:
        weights.append(float(i.split()[6]))
print('weights',len(weights))
for fnum in range(1,11):
    g2='entropy_list_maximal'+str(fnum)+'.txt'
    f2=open(g2,'r')
    lines2=f2.readlines()
    c1=0
    for i in lines2:
        c1=c1+1
        if c1>1:
            orb_ent.append(float(i.split()[1]))
print('orb_ent-',len(orb_ent))
for cl in range(100,200):
    cell_frac=[]
    
    cell= all_CellName[cl]
    
    for fnum in range(1,11):
        g1='Cell_frac_time_'+str(fnum)+'.txt'
        f1=open(g1,'r')
        lines1=f1.readlines()
        c2=0
        for i in lines1:
            c2=c2+1
            if c2>1:
                
                cell_frac.append(float(i.split()[(cl+1)]))
    
    Cell_Weight=np.array(cell_frac)*np.array(weights)
    print('cell_wt-',len(Cell_Weight),'-',cl)
    total_ent=np.array(cell_frac)*np.array(weights)*np.array(orb_ent)
    avg_ent= np.sum(total_ent)/np.sum(Cell_Weight)
    cell_ent.append(avg_ent)

all_CellName = all_CellName[100:200]
data = Table()
data['CellName'] = all_CellName
data['entropy'] = cell_ent
ascii.write(data, 'cell_wise_entropy_2.txt', overwrite=True,delimiter=' ')