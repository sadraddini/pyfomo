# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:35:05 2018

@author: sadra

This part is only for visualization of 2D Polytopes
"""

from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from scipy.spatial import ConvexHull

import numpy as np

from cdd import Polyhedron,Matrix

def visualize_2D(list_of_polytopes,a=1.5):
    """
    Given a polytope in its H-representation, plot it
    """ 
    p_list=[]
    x_all=np.empty((0,2))
    for polytope in list_of_polytopes:
        p_mat=Matrix(np.hstack((polytope.H,polytope.h)))
        poly=Polyhedron(p_mat)
        x=np.array(poly.get_generators())[:,0:2]
        x=x[ConvexHull(x).vertices,:]
        x_all=np.vstack((x_all,x))
        p=Polygon(x)
        p_list.append(p)
    p_patch = PatchCollection(p_list, color=[(np.random.random(),np.random.random(),np.tanh(np.random.random())) \
        for polytope in list_of_polytopes],alpha=0.6)
    fig, ax = plt.subplots()
    ax.add_collection(p_patch)
    ax.set_xlim([np.min(x_all[:,0])*a,a*np.max(x_all[:,0])])
    ax.set_ylim([np.min(x_all[:,1])*a,a*np.max(x_all[:,1])])
    ax.grid(color=(0,0,0), linestyle='--', linewidth=0.3)
