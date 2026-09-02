import pyomo.environ as pyo
from pyomo.opt import SolverFactory

m = pyo.ConcreteModel()

m.setL = pyo.RangeSet(0,2)

m.x = pyo.Var(m.setL)

x = m.x

costes = [0.2, 0.2, 0.5]
maxG = [20, 30]
maxL = [15]*len(m.setL)
minL = [0]*len(m.setL)

m.obj = pyo.Objective(expr = sum([x[i]*costes[i] for i in m.setL]), sense=pyo.minimize)

m.C1 = pyo.ConstraintList()
for i in m.setL:
    if i < 2:
        m.C1.add(pyo.inequality(minL[i], x[i], maxL[i]))
    else:
        m.C1.add(pyo.inequality(minL[i], x[i] + x[0], maxL[i]))
        
m.C2 = pyo.Constraint(expr = x[0] + x[1] <= 20)
m.C3 = pyo.Constraint(expr = x[2] <= 30)
m.C3 = pyo.Constraint(expr = sum([x[i] for i in m.setL]) == 25)

opt = SolverFactory('gurobi')
m.results = opt.solve(m)

for i in m.setL:
    print(pyo.value(x[i]))