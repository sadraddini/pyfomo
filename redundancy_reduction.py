#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:52:06 2018

@author: sadra
"""
import numpy as np
from gurobipy import Model, GRB, LinExpr

def canonical_polytope_old(H,h,atol=10**-8):
    # Given H, h, provide canonical polytope by finding and removing redundant rows
    # Also scale H such that its largest absolute element is 1
    n=H.shape[1]
    H_final=np.empty((0,n))
    H_max=np.amax(abs(H),axis=1)
    H_final=np.empty((0,n))
    h_final=np.empty((0,1))
    print("before removing redundancy",H,h)
    for ROW in range(H.shape[0]):
        if check_redundancy_row(H,h,ROW)==False:
            H_scale=np.asscalar(H_max[ROW])
            H_final=np.vstack((H_final,H[ROW,:]/H_scale))
            h_final=np.vstack((h_final,h[ROW,:]/H_scale))
        else:
            pass
    return (H_final,h_final)

def canonical_polytope(H,h,flag=None,atol=10**-8):
    """
    Given a polytope in form {H x <= h}, provide canonical polytope by finding and removing redundant rows
    Also scale H such that its largest absolute element is 1
    """
    if flag==None: # Construct flag for each row
        flag={} 
        for ROW in range(H.shape[0]):
            if check_redundancy_row(H,h,ROW)==True:
                flag[ROW]=False # It "may" be removed
            else:
                flag[ROW]=True # It must remain
        return canonical_polytope(H,h,flag) 
    elif [row for row in range(H.shape[0]) if flag[row]==False]==[]: # No row is needed to be removed
        return normalize(H,h)
    elif len([row for row in range(H.shape[0]) if flag[row]==False])==1: # Remove the only remaining false row
        a_false_row=[row for row in range(H.shape[0]) if flag[row]==False][0]
        removed_ROW=list(range(0,a_false_row))+list(range(a_false_row+1,H.shape[0]))
        H=H[removed_ROW,:]
        h=h[removed_ROW,:]
        return normalize(H,h)         
    else: # Let's remove one of the False rows
        a_false_row=[row for row in range(H.shape[0]) if flag[row]==False][0]
        rows_one_removed=list(range(0,a_false_row))+list(range(a_false_row+1,H.shape[0]))
        flag_new={}
        row=0
        for ROW in rows_one_removed:
            flag_new[row]=flag[ROW]
            row+=1
        H=H[rows_one_removed,:]
        h=h[rows_one_removed,:]
        for row in range(H.shape[0]):
            if flag_new[row]==False:
                if check_redundancy_row(H,h,row)==False:
                    flag_new[row]=True
        return canonical_polytope(H,h,flag_new,atol) 
                    

def check_redundancy_row(H,h,ROW,atol=10**-8):
    model=Model("Row Redundancy Check")
    n=H.shape[1]
    x=np.empty((n,1),dtype='object')
    for row in range(n):
        x[row,0]=model.addVar(lb=-GRB.INFINITY,ub=GRB.INFINITY)
    model.update()
    for row in [r for r in range(H.shape[0]) if r!=ROW]:
        Hx=LinExpr()
        for column in range(n):
            Hx.add(H[row,column]*x[column,0])
        model.addConstr(Hx<=h[row,0])
    J=LinExpr()
    for column in range(n):
        J.add(H[ROW,column]*x[column,0])
    model.setObjective(J, GRB.MAXIMIZE)
    model.setParam('OutputFlag',False)
    model.optimize()
    if model.Status==2:
        if J.getValue()>h[ROW,0]+atol:
            return False # It is NOT redundant
        else:
            return True # It is redudant
    else:
        return False
    
def normalize(H,h):
    H_max=np.amax(abs(H),axis=1)
    H=np.dot(np.diag(1/H_max),H)
    h=np.dot(np.diag(1/H_max),h)
    return (H,h)