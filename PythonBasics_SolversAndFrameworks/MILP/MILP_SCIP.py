# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 03:20:07 2025

@author: penad
"""

from pyscipopt import Model

model = Model('example')

x = model.addVar('x', vtype='INTEGER')
y = model.addVar('y')

model.setObjective(x+y, sense='maximize')

model.addCons(-x+2*y<=7)#Can solve non linear problems
model.addCons(2*x+y<=14)
model.addCons(2*x-y<=10)

model.optimize()

sol = model.getBestSol()

print('x= ', sol[x])
print('y= ', sol[y])
      