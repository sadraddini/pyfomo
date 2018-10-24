#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 17:58:06 2018

@author: sadra
"""
import sys
sys.path.append('..')

import numpy as np

from src.visualize_2D import visualize_2D
from src.main import fourier_motzkin_eliminate_single,project,convexhull
from src.polytope import translate

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
    G=np.array([[1,3],[-1,2]])
    Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
    p1=translate(project(G,Pi,np.ones((4,1))),np.array([2,2]).reshape(2,1))
    p1.show()
    
if True: # test 4
    print("\n\n\n Test 4: Another Projection")
    G=np.array([[4,1],[-5,-1]])
    Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
    p2=project(G,Pi,np.ones((4,1)))
    p2.show()
    
if True: # test 5
    print("\n\n\n Test 5: Another Projection")
    G=np.array([[1,0],[6,1]])
    Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
    p3=translate(project(G,Pi,np.ones((4,1))),np.array([-5,0]).reshape(2,1))
    p3.show()

if True: # test 6
    print("\n\n\n Test 5: Another Projection")
    G=np.array([[-1,-1],[6,8]])
    Pi=np.array([[ 1.,  0.],[0.,  1.],[-1., -0.],[-0., -1.]])
    p4=project(G,Pi,np.ones((4,1)))
    p4.show()
    
p=convexhull([p1,p2,p3,p4])
p.show()

visualize_2D([p,p1,p2,p3,p4])