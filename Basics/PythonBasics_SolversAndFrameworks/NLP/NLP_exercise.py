# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 18:46:09 2025

@author: penad
"""

import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.x = pyo.Var(initialize=0,bounds=(-5,5))
model.y = pyo.Var(initialize=0,bounds=(-5,5))

x = model.x
y = model.y

objexpr = pyo.cos(x+1)+pyo.cos(x)*pyo.cos(y)
model.obj = pyo.Objective(expr= objexpr,sense=pyo.maximize)

#opt = SolverFactory('scip', executable='C:\\Program Files\\SCIPOptSuite 9.2.3\\bin\\scip.exe')
opt = SolverFactory('ipopt', executable='C:\\ipopt\\Ipopt-3.14.19-win64-msvs2022-md\\bin\\ipopt.exe')
opt.options['toL']=1e-6#Tolerance, maximum error
opt.solve(model)

model.pprint()

x_value = pyo.value(x)
y_value = pyo.value(y)

print('x=',x_value)
print('y=',y_value)