import pyomo.environ as pyo
from pyomo.opt import SolverFactory

m = pyo.ConcreteModel()

#sets and parameters

#variables

m.B = pyo.Var(pyo.RangeSet(1,10), within=pyo.Binary)

#objective function
m.obj = pyo.Objective(expr = pyo.summation(m.B), sense=pyo.maximize)

def consecutivos(m):
    count=0
    for i in pyo.RangeSet(1,10):
        if pyo.value(m.B[i])==0:
            count+=1
        if count >=2:
            break
    return count

#constraints
#m.C1 = pyo.Constraint(expr= abs(pyo.summation(m.B))<=1)

m.C1 = pyo.ConstraintList()
for t in pyo.RangeSet(2,10):
    m.C1.add(expr = (m.B[t] - m.B[t-1]) <= 1)
    
m.C2 = pyo.Constraint(expr= pyo.summation(m.B)==5)
    
'''m.C2 = pyo.ConstraintList()
for t in pyo.RangeSet(2,5):
        m.C2.add(expr = (m.B[t] - m.B[t-1]) == 0)'''

#solve
#opt = SolverFactory('couenne')
opt = SolverFactory('couenne', executable='C:\\couenne\\bin\\couenne.exe')
m.results = opt.solve(m)

#print
m.pprint()

print('\n\nOF:',pyo.value(m.obj))
for i in pyo.RangeSet(1,10):
    print(pyo.value(m.B[i]))