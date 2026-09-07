# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 18:20:26 2026

@author: penad
"""

import pyomo.environ as pyo, numpy as np
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.p = pyo.Var(bounds=(50, 200))

p = model.p

numCars = 1001-5*p

model.obj = pyo.Objective(expr= p*numCars,sense=pyo.maximize)

opt = SolverFactory('ipopt', executable='C:\\ipopt\\Ipopt-3.14.19-win64-msvs2022-md\\bin\\ipopt.exe')
#opt.options['toL']=1e-6#Tolerance, maximum error
opt.solve(model)

model.pprint()

p_value = pyo.value(p)

print('p=',np.round(p_value, 2))
print('Num cars=',np.round(1001-5*p_value, 0))
print('Revenue',np.round((1001-5*p_value)*p_value, 0))