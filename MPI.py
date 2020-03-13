from mpi4py import MPI
global area, dx
area=0
def f(x):
    return 52*x**3+532*x**2-431*x-35228
def iterationLi(i):
    return a+dx*i
def sumArea(obtained):
    global area
    area+=obtained
def getArea(li):
    return getH(li)*dx
def getH(li):
    return f(li+dx/2)
    
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nodes=comm.size()

#Start nodes in sequential order
myNode=nodes-1
#print(comm, rank)

#%Const
n=1000000
#n=10000000000
a=-5000
b=5000
dx=(b-a)/n


#n= n/nodos*miNodo,n/nodos*(miNodo+1)       ->[miNodo] starts with 0
start=int(n/comm.size*myNode)
stop=int(n/comm.size*(myNode+1))+2 if(myNode==comm.size()-1) else int(n/comm.size*(myNode+1))
for i in range(start,stop):
    sumArea(getArea(iterationLi(i)))
#print(area)

if rank == 0:
    data1 = 0.0
    comm.Recv(data1, source=1, tag=1)
    sumArea(data1)
    data2 = 0.0
    comm.Recv(data2, source=1, tag=2)
    sumArea(data2)
    
elif rank == 1:
    data = area
    comm.Send(data, dest=0, tag=myNode)
