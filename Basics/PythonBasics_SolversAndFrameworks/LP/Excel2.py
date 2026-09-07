# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 14:42:25 2025

@author: penad
"""

import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd

dataGen = pd.read_excel('inputsExcel2.xlsx', sheet_name='gen', engine='openpyxl')
dataLoad = pd.read_excel('inputsExcel2.xlsx', sheet_name='load', engine='openpyxl')
Ng = len(dataGen)

model = pyo.ConcreteModel()

model.Pg = pyo.Var(range(Ng),bounds=(0,None))
Pg = model.Pg

Pg_sum = sum([Pg[g] for g in dataGen.id])

model.balance = pyo.Constraint(expr = Pg_sum == sum(dataLoad.value))

model.cond = pyo.Constraint(expr = Pg[0]+Pg[3] >= dataLoad.value[0])

model.limits = pyo.ConstraintList()
for g in dataGen.id:
    model.limits.add(expr = Pg[g] <= dataGen.limit[g])

cost_sum = sum([Pg[g]*dataGen.cost[g] for g in dataGen.id])
model.obj = pyo.Objective(expr=cost_sum)

opt = SolverFactory('gurobi')
results = opt.solve(model)

dataGen['Pg'] = [pyo.value(Pg[g]) for g in dataGen.id]

print(dataGen)