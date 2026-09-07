import pyomo.environ as pyo
from pyomo.opt import SolverFactory

m = pyo.ConcreteModel()

#sets and parameters
m.setMachine = pyo.Set(initialize=['A','B','C'])
m.Demand = 10000

#variables
m.C = pyo.Var(m.setMachine, bounds=(0,None))
m.P = pyo.Var(m.setMachine, within=pyo.Integers, bounds=(0,None))

#objective function
m.obj = pyo.Objective(expr = pyo.summation(m.C), sense=pyo.minimize)

#constraints
m.C1 = pyo.Constraint(expr = pyo.summation(m.P) == m.Demand)
m.C2 = pyo.Constraint(expr = m.C['A'] == 0.1*m.P['A']**2 + 0.5*m.P['A'] + 0.1)
m.C3 = pyo.Constraint(expr = m.C['B'] == 0.3*m.P['B'] + 0.5)
m.C4 = pyo.Constraint(expr = m.C['C'] == 0.01*m.P['C']**3)

#solve
opt = SolverFactory('couenne')
m.results = opt.solve(m)

#print
m.pprint()

print('\n\nOF:',pyo.value(m.obj))