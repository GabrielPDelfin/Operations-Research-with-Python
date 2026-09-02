# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 15:37:28 2025

@author: penad
"""

import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import time

model = pyo.ConcreteModel()

model.x = pyo.Var(bounds=(None,3))
model.y = pyo.Var(bounds=(0,None))

x = model.x
y = model.y

model.C1 = pyo.Constraint(expr= x+y<=8)
model.C2 = pyo.Constraint(expr= 8*x+3*y>=-24)
model.C3 = pyo.Constraint(expr= -6*x+8*y<=48)
model.C4 = pyo.Constraint(expr= 3*x+5*y<=15)

model.obj = pyo.Objective(expr= -4*x-2*y,sense=pyo.minimize)

opt = SolverFactory('gurobi')
#Comenzar cronómetro
initial_time = time.time()
opt.solve(model)
#Parar
final_time = time.time()-initial_time
x_value = pyo.value(x)
y_value = pyo.value(y)

print('time= ', final_time)
print('x=',x_value)
print('y=',y_value)
print('obj= ', pyo.value(model.obj))