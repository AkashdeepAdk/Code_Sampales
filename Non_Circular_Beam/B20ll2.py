#This code calculates beam independennt parts of the beam BipoSH coefficients
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from sympy.physics.quantum.cg import CG, cg_simp
from sympy import S
from sympy import *
import matplotlib 
from scipy.special import legendre
import math
from decimal import Decimal

#through out this code l2=l+2 and l_2=l-2
#m=m_1 and m2=m_2

#l_iso=6
l_iso=[i for i in range(2,2100)]

from scipy.special import iv


def I_ll_02(l): #required wigner d_function integration
    val=np.sqrt((math.factorial(l-2))/math.factorial(l+2))*(((4*l)/(2*l+1))-(2*l*(l+1))/(2*l+1))
    return val


def I_l_2l_02(l): #required wigner d_function integration
    val=np.sqrt((math.factorial(l-2))/math.factorial(l+2))*4
    return val


def I_ll_m2_2(l,l2,m2): #required wigner d_function integration
    m=np.abs(m2)
    if l==l2:
        
        k=np.sqrt((l-1)*l*(l+1)*(l+2))
        k0=(np.square(m2)/(np.square(l)*np.square((l+1))))-((np.square(l)-np.square(m2))/(np.square(l)*(4*np.square(l)-1)))-((np.square((l+1))-np.square(m2))/(np.square((l+1))*(2*l+1)*(2*l+3)))
    #    k1=(2*m2)*((np.sqrt((np.square(l+1)-np.square(m2))))/(l*(l+1)*(l+2)*(2*l+1)))
    #    k_1=-((2*m2)*((np.sqrt(np.square(l)-np.square(m2))/(l*(np.square(l)-1)*(2*l+1)))))
        k2=(np.sqrt(((np.square(l+1)-np.square(m2))*(np.square(l+2)-np.square(m2)))))/((l+1)*(l+2)*(2*l+1)*(2*l+3))
        k_2=(np.sqrt((np.square(l)-np.square(m2))*(np.square(l-1)-np.square(m2))))/(l*(l-1)*(4*np.square(l)-1))
        
        val=(((k*k0)+(k*k2)*np.sqrt((((l-m+2)*(l-m+1))/((l+m+2)*(l+m+1))))
                 +(k*k_2)*np.sqrt(((l-m)*(l-m-1))/((l+m)*(l+m-1))))/m)
    if l2==(l-2):
        p=l-2
        k=np.sqrt((p-1)*p*(p+1)*(p+2))
        k0=(np.square(m2)/(np.square(p)*np.square((p+1))))-((np.square(p)-np.square(m2))/(np.square(p)*(4*np.square(p)-1)))-((np.square((p+1))-np.square(m2))/(np.square((p+1))*(p*2+1)*(p*2+3)))
    #    k1=(2*m2)*((np.sqrt((np.square(l+1)-np.square(m2))))/(l*(l+1)*(l+2)*(2*l+1)))
    #    k_1=-((2*m2)*((np.sqrt(np.square(l)-np.square(m2))/(l*(np.square(l)-1)*(2*l+1)))))
        k2=(np.sqrt(((np.square(p+1)-np.square(m2))*(np.square(p+2)-np.square(m2)))))/((p+1)*(p+2)*(2*p+1)*(2*p+3))
        k_2=(np.sqrt((np.square(p)-np.square(m2))*(np.square(p-1)-np.square(m2))))/(p*(p-1)*(4*np.square(p)-1))
        val=((k*k0)*np.sqrt(((l-m)*(l-m-1))/((l+m)*(l+m-1)))
          +(k*k2)
         +(k*k_2)*np.sqrt(((l-m)*(l-m-1)*(l-m-2)*(l-m-3))/((l+m)*(l+m-1)*(l+m-2)*(l+m-3))))
    if l==l2-2:
        k=np.sqrt((l-1)*l*(l+1)*(l+2))
        k0=(np.square(m2)/(np.square(l)*np.square((l+1))))-((np.square(l)-np.square(m2))/(np.square(l)*(4*np.square(l)-1)))-((np.square((l+1))-np.square(m2))/(np.square((l+1))*(2*l+1)*(2*l+3)))
    #    k1=(2*m2)*((np.sqrt((np.square(l+1)-np.square(m2))))/(l*(l+1)*(l+2)*(2*l+1)))
    #    k_1=-((2*m2)*((np.sqrt(np.square(l)-np.square(m2))/(l*(np.square(l)-1)*(2*l+1)))))
        k2=(np.sqrt(((np.square(l+1)-np.square(m2))*(np.square(l+2)-np.square(m2)))))/((l+1)*(l+2)*(2*l+1)*(2*l+3))
        k_2=(np.sqrt((np.square(l)-np.square(m2))*(np.square(l-1)-np.square(m2))))/(l*(l-1)*(4*np.square(l)-1))
        
        val=(((k*k0)*np.sqrt(((l-m)*(l-m-1))/((l+m)*(l+m-1)))
              +(k*k2)*np.sqrt((((l-m+2)*(l-m+1)*(l-m)*(l-m-1))/((l+m+2)*(l+m+1)*(l+m)*(l+m-1)))))
             +(k*k_2))/m
    return val
    
    

def B_L0_ll(L,l,l2)#,e,s): #beam independent BipoSH coefficients
    b=1#2*bl2(l2,e,s)
    constant=np.sqrt((2*l+1)*math.pi)
    if l==l2:
        m2=[j for j in range(1,(l+1))]
        cg1=(((CG(l,0,l,0,L,0).doit()).doit()*I_ll_02(l)))
        cg1=cg1.evalf()
        circ=((-1)**l)*bl0(l,e,s)*(2/(np.sqrt(2*l+1)))

    elif l<l2:
        m2=[j for j in range(1,(l+1))]
        cg1=(((CG(l,0,l,0,L,0).doit()).doit()*I_l_2l_02(l)))
        cg1=cg1.evalf()
        circ=0

    else:
        m2=[j for j in range(1,(l-2))]
        cg1=0
        circ=0
    sum=0
    
    if L==0:
            
        for i in m2:
            cg2=((-1)**(i))*(CG(l,(-i),l2,i,L,0).doit()).doit()*I_ll_m2_2(l,l2,i)
            sum=sum+cg2
            sum=sum.evalf()
        val=(constant)*(b*(cg1+2*sum)+circ)
        
    else:    
            
        
        for i in m2:
            cg2=((-1)**(i))*(CG(l,(-i),l2,i,L,0).doit()).doit()*I_ll_m2_2(l,l2,i)
            sum=sum+cg2
            sum=sum.evalf()
        val=(constant)*b*(cg1+2*sum)
        
        
    return val



Bl=[]
for l in l_iso:
    Bl.append(B_L0_ll(2,l,l+2))
    if l%100==0:
        print(l,'done')


fname='B20ll2.txt'        
np.savetxt(fname,Bl)
