import pyomo.environ as pyo
from pyomo.opt import SolverFactory

m = pyo.ConcreteModel()

#sets 
m.setJ = pyo.Set(initialize=['A','B','C','D','E','F'])
m.setD = pyo.Set(initialize=[1,2,3])
m.D = {'A':2, 'B':3, 'C':5, 'D':2, 'E':6, 'F':4}
m.P = {'A':200, 'B':500, 'C':300, 'D':100, 'E':1000, 'F':300}
m.maxHours = 6

#variables
m.x = pyo.Var(m.setJ, m.setD, within=pyo.Binary)

#objective function
m.obj = pyo.Objective(expr = sum([m.x[j,d]*m.P[j] for j in m.setJ for d in m.setD]), sense=pyo.maximize)

#constraints
m.C1 = pyo.ConstraintList()
m.C2 = pyo.ConstraintList()
m.C3 = pyo.ConstraintList()

for d in m.setD:
    m.C1.add(sum([m.x[j,d]*m.D[j] for j in m.setJ]) <= m.maxHours)
    m.C3.add(sum([m.x[j,d] for j in m.setJ]) <= 1)
for j in m.setJ:
    m.C2.add(sum([m.x[j,d] for d in m.setD]) <= 1)


#solve
opt = SolverFactory('gurobi')
m.results = opt.solve(m)

#print
m.pprint()

print('\n\n')
print('Total Profit:', pyo.value(m.obj))
for d in m.setD:
    for j in m.setJ:
        if pyo.value(m.x[j,d])>0.9:
            print('Job %s in day %d (duration %i, profit %i)' % (j,d,m.D[j],m.P[j]))