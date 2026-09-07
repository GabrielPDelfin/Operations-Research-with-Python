import pyomo.environ as pyo
from pyomo.opt import SolverFactory

import pandas as pd

dataNodos = pd.read_excel('route_inputs.xlsx', sheet_name='nodes', engine='openpyxl')
dataCaminos = pd.read_excel('route_inputs.xlsx', sheet_name='paths', engine='openpyxl')

m = pyo.ConcreteModel()

m.x = pyo.Var(pyo.RangeSet(0, len(dataCaminos)), within=pyo.Binary)

m.obj = pyo.Objective(expr = sum([m.x[route[0]] * route[1]['distance'] for route in dataCaminos.iterrows()]), sense=pyo.minimize)

m.C1 = pyo.Constraint(expr= sum([m.x[i] for i in dataCaminos.index[dataCaminos.node_from==int(dataNodos.node[dataNodos.description=='origin'])]])==1)
m.C2 = pyo.Constraint(expr= sum([m.x[i] for i in dataCaminos.index[dataCaminos.node_to==int(dataNodos.node[dataNodos.description=='destination'])]])==1)
m.C3 = pyo.ConstraintList()
for nodo in dataNodos.node[dataNodos.description=='middle point']:
    m.C3.add(sum([m.x[bit] for bit in dataCaminos.index[dataCaminos.node_from==int(nodo)]]) == sum([m.x[bit] for bit in dataCaminos.index[dataCaminos.node_to==int(nodo)]]))

opt = SolverFactory('gurobi')
m.results = opt.solve(m)

print(pyo.value(m.obj))


#print(dataCaminos.index[dataCaminos.node_from==dataNodos.node[dataNodos.description=='origin'][0]])
#dataCaminos.index[dataCaminos.node_to==dataNodos.node[dataNodos.description=='destination'][0]
for i in range(0,len(dataCaminos)):
    print(pyo.value(m.x[i]))