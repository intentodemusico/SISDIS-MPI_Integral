# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:08:09 2020

@author: INTENTODEMUSICO
"""

from mpi4py import MPI
from time import sleep
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
myNode=rank

#Start nodes in sequential order
print("My node",myNode)
print("Nodes",comm.size,"rank",rank)