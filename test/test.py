#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 17:58:06 2018

@author: sadra
"""
import sys
sys.path.append('..')

import numpy as np
from src.main import fourier_motzkin_eliminate_single,project

if True: # test 1   
    print("\n Test 1: Simple 2D Polytope")
    A=np.array([[1,1],[-1,1],[-1,0],[-0.5,-1]])    
    b=np.array([[2,-1,1,0]]).T  
    var_index=1
    (A_new,b_new)=fourier_motzkin_eliminate_single(var_index,A,b,atol=10**-8)
    print("A_new=",A_new)
    print("b_new=",b_new)

if True:# test 2 
    print("\n\n\n Test 2: Randomized Matrices")
    A=np.random.random((7,4))-0.5
    b=np.random.random((7,1))
    var_index=1
    (A_new,b_new)=fourier_motzkin_eliminate_single(var_index,A,b,atol=10**-8)
    print("A_new=",A_new)
    print("b_new=",b_new)
    
if True: # test 3
    print("\n\n\n Test 3: Projection")
    G=np.array([[3,1],[9,3]])
    Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
    (H,h)=project(G,Pi,np.ones((4,1)))
    print("H=",H)
    print("h=",h)
    
if True: # test 4
    print("\n\n\n Test 4: Projection with Plane")
    G=np.array([[3,1],[9,3]])
    Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
    C=np.array([[1,1]]).reshape(1,2)
    d=np.array([[0]])
    (H,h)=project(G,Pi,np.ones((4,1)),C,d)
    print("H=",H)
    print("h=",h)