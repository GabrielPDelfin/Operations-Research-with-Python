# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 03:44:25 2025

@author: penad
"""

import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

m = pyo.ConcreteModel()

m.setI = pyo.RangeSet(1,5)

m.x = pyo.Var(m.setI, within=pyo.Integers, bounds=(0,None))
m.y = pyo.Var(bounds=(0,None))

y = m.y

XSUM = sum([m.x[i] for i in m.setI]) + m.y

m.obj = pyo.Objective(expr = XSUM, sense=pyo.minimize)

m.C1 = pyo.Constraint(expr = XSUM <= 20)
m.C2 = pyo.ConstraintList()
for i in m.setI:
    m.C2.add(m.x[i]+m.y >= 15)

XSUM2 = sum([i*m.x[i] for i in m.setI])

m.C3 = pyo.Constraint(expr = XSUM2 >= 10)
m.C4 = pyo.Constraint(expr=m.x[5] + 2*m.y>=30)

opt = SolverFactory('scip', executable='C:\\Program Files\\SCIPOptSuite 9.2.3\\bin\\scip.exe')
opt.solve(m)

m.pprint()

for i in m.setI:
    print('x%i= ' % i , pyo.value(m.x[i]))

print('y=',pyo.value(y))
print('obj= ', pyo.value(m.obj))
