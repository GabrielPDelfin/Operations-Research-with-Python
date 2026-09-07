# -*- coding: utf-8 -*-

import pyomo.environ as pyo, numpy as np
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.x = pyo.Var(bounds=(0, None))
model.y = pyo.Var(bounds=(0, None))

x = model.x
y = model.y

model.C1 = pyo.Constraint(expr= 2*x+y<=100)

model.obj = pyo.Objective(expr= x*y,sense=pyo.maximize)

opt = SolverFactory('ipopt', executable='C:\\ipopt\\Ipopt-3.14.19-win64-msvs2022-md\\bin\\ipopt.exe')
#opt.options['toL']=1e-6#Tolerance, maximum error
opt.solve(model)

model.pprint()

x_value = pyo.value(x)
y_value = pyo.value(y)

print('x=',np.round(x_value, 2))
print('y=',np.round(y_value, 2))
print('Area=',np.round(x_value*y_value, 2))