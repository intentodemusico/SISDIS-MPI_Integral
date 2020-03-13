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
    

#%Const
#n=100000000
n=100000000
a=-5000
b=5000
dx=(b-a)/n


#n= n/nodos*miNodo,n/nodos*(miNodo+1)       ->[miNodo] starts with 0
for i in range(n):
    sumArea(getArea(iterationLi(i)))
print(area)
