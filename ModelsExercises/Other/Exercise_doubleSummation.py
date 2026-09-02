# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 15:36:35 2025

@author: penad
"""

import pyomo.environ as pyo#, numpy as np
#from pyomo.environ import *
from pyomo.opt import SolverFactory

#creation of the model and variables
model = pyo.ConcreteModel()

model.setM = pyo.RangeSet(1,4)
model.setT = pyo.RangeSet(1,10)

model.x = pyo.Var(model.setM, model.setT, within=pyo.Integers, bounds=(0,10))

x = model.x

suma = sum([x[m,t] for m in model.setM for t in model.setT])

model.obj = pyo.Objective(expr = suma, sense=pyo.maximize)

model.C1 = pyo.ConstraintList()
for t in model.setT:
    model.C1.add(2*x[2,t] - 8*x[3,t] <= 0)
    model.C1.add(sum([x[m,t] for m in model.setM]) <= 50)
    if t>=2:
        model.C1.add(x[1,t] + x[2,t-1] + x[3,t] + x[4,t] <= 10)
    if t>=3:
        model.C1.add(x[2,t] - 2*x[3,t-2] + x[4,t] >= 1)
        
#solve
opt = SolverFactory('gurobi')
model.results = opt.solve(model)

#print
model.pprint()
print('Obj: ', pyo.value(model.obj))

for m in model.setM:
    print('Machine ', m)
    for t in model.setT:
        print('Hour: %i . Prod: %i' % (t,pyo.value(x[m,t])))