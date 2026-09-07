import pyomo.environ as pyo
from pyomo.opt import SolverFactory
 
#creating the model
m = pyo.ConcreteModel()
 
#parameters
C1 = 100
C2 = 300
Nmax1 = 31
Nmax2 = 100
D = 50

#variables
m.N1 = pyo.Var()
m.N2 = pyo.Var()
N1 = m.N1
N2 = m.N2

def myrule(m):
    return N1+N2 == D
 
#objective function and constraints
m.obj = pyo.Objective(expr = C1*N1+C2*N2)
#m.C1 = pyo.Constraint(expr = N1+N2 == D)
m.C1 = pyo.Constraint(rule = myrule)
m.C2 = pyo.Constraint(expr = N1 <= Nmax1)
m.C3 = pyo.Constraint(expr = N2 <= Nmax2)
 
#solving model
m.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
opt = SolverFactory('gurobi')
m.results = opt.solve(m)
 
#dual variables
print('-'*20 + ' MODEL ' + '-'*20)
m.pprint() 
 
#prints the model
print('\n\n'+'-'*20 + ' DUAL VARIABLES ' + '-'*20)
m.dual.pprint() 
 
#prints the dual variables
print('\n\n'+'-'*20 + ' Value of ObjFun ' + '-'*20)
print('Objective Function is %.2f' % (pyo.value(m.obj)))
print (pyo.value(m.N1))
print (pyo.value(m.N2))
print(m.C3.uslack())
print(m.C3.lslack())
 
#access a single dual variable
mydual = m.dual[m.C2]