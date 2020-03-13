# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 13:23:38 2020

@author: INTENTODEMUSICO
"""

#%% importing libraries
from mpi4py import MPI
import numpy as np
import time 
import math
global area, dx

#%% defining functions
area=0
def f(x): #f(x) function, returns result of f(x)
    return 5258*x**3+x*math.exp(5) #
def iterationLi(i): #returns li for a determined iteration
    return a+dx*i
def sumArea(obtained): #sums areas to local area
    global area
    area+=obtained
def getArea(li): #returns a rectangle area with li=$li
    return getH(li)*dx
def getH(li): #returns h (or y) for a determined li=$li
    return f(li+dx/2)

#%% communication
comm = MPI.COMM_WORLD #stablishes communication
rank = comm.Get_rank() #node rank
name = MPI.Get_processor_name() #gets processor name


print("My node",rank,"Name",name,"Nodes",comm.size,"\n")

#%% global const
n=10000000000
a=-5000 
b=5000
dx=(b-a)/n

#%% implementation
start=int(n/comm.size*rank) #defines local a (or first li)

#################################################################################################################################################################
#defines b=int(totalN/number of nodes *rank+1)+2 if this is the last node and totalN/number of nodes isn't float, else -> b=int(totalN/number of nodes*(rank+1))#
#           *rank+1 is used to select the interval according to the node rank (every node will run the inverval number rank+1)                                  #
#                       +2 is used to fix the loss of the trunk function                                                                                        #
#################################################################################################################################################################

stop=int(n/comm.size*(rank+1))+2 if(rank==comm.size-1 and int(n/comm.size*(rank+1))!=n/comm.size*(rank+1) ) else int(n/comm.size*(rank+1))
print("Node",rank,"Start",start,"Stop",stop)


#%% calculating area
t = time.time()
for i in range(start,stop):
    sumArea(getArea(iterationLi(i)))
elapsed = time.time() - t #elapsed time

#%% sending messages according to rank
if rank == 0:
    print("Master local area:",area)
    for i in range(1,3): #receive 2 messages
        print(name,rank,"waiting",i)
        req = comm.irecv(source=MPI.ANY_SOURCE, tag=1)
        data = req.wait() #wait until a message is incoming from any source with tag 1
        print(name,rank,"Received",i)
        sumArea(data["area"]) #updates master local area and elapsed time
        elapsed+=data["time"]
    print("\n\nTotal area:",area)
    print("\nTotal time:",elapsed)
else:
    data = {"area":area,"time":elapsed} #dictionary containing time and area
    comm.isend(data, dest=0, tag=1)#sending dictionary
    print(name,rank,"sent",area,"local time:",elapsed)    


                                    #%%conclusions%%#
#############################################################################################
#It is important to use good programming practices due to the needing of a recoding task.   #
#The best way to measure higher times and obtaining best precision is using lower dx.       #
#It is necesary to understand synchronus programming for using blocking methods.            #
#############################################################################################


#
