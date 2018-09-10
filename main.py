#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 12:14:51 2018

@author: sadra
"""

import numpy as np

from redundancy_reduction import canonical_polytope

class system():
    def __init__(self):
        self.ineq=(None,None)
        self.eq=(None,None)
        
def fourier_motzkin_eliminate_single(var_index,A,b,C=None,d=None,atol=10**-8):
    if type(C)==type(np.array([1])):
        A=np.vstack((A,C,-C))
        b=np.vstack((b,d,-d))
        return fourier_motzkin_eliminate_single(var_index,A,b,None,None,atol)
    else:
        phi_positive=[i for i in range(A.shape[0]) if A[i,var_index]>=atol] # list of positive var entries
        phi_negative=[i for i in range(A.shape[0]) if A[i,var_index]<=-atol]  # list of negative var entries
        phi_core=[i for i in range(A.shape[0]) if abs(A[i,var_index])<atol]  # list of zero var entries
        s_smaller=np.diag(1/A[phi_positive,var_index]) # positive
        s_larger=np.diag(1/A[phi_negative,var_index]) # negative
        A_positive=np.dot(s_smaller,A[phi_positive,:]) # A of postives scaled by var entries
        b_positive=np.dot(s_smaller,b[phi_positive,:])
        A_negative=np.dot(s_larger,A[phi_negative,:])
        b_negative=np.dot(s_larger,b[phi_negative,:]) 
        """ We have A_positive x_other + x_r <= b_positive
        --> We have A_negative x_other + x_r >= b_negative
        --> We have b_postive - b_negative >= (A_neg - A _pos) * x_other (all combinations)
        """
        A_new=np.empty((0,A.shape[1]-1))
        b_new=np.empty((0,1))
        other=list(range(0,var_index))+list(range(var_index+1,A.shape[1]))
        for i in range(len(phi_positive)):
            for j in range(len(phi_negative)):
                alpha=(-A_negative[j,other]+A_positive[i,other]).reshape(1,len(other))
                beta=b_positive[i,:]-b_negative[j,:]
                A_new=np.vstack((A_new,alpha))
                b_new=np.vstack((b_new,beta))
        if phi_core!=[]:
            A_new=np.vstack((A_new,A[phi_core,:][:,other]))
            b_new=np.vstack((b_new,b[phi_core,:]))
        return canonical_polytope(A_new,b_new)

def project(T,A,b,C=None,d=None,atol=10**-8):
    """
    Finds the H-representation of T{Ax<=b, Cx=d}
    """
    (m,n)=T.shape # m: y, n: x, y=Tx
    if C==None and d==None:
        A=np.hstack((np.zeros((A.shape[0],m)),A))
        b=b
        C=np.hstack((-np.eye(m),T))
        d=np.zeros((m,1))
        (A,b)=fourier_motzkin_eliminate_single(n+m-1,A,b,C,d,atol)
        for j in range(n-1):
            (A,b)=fourier_motzkin_eliminate_single(A.shape[1]-1,A,b,None,None,atol)
        return (A,b)