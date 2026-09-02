# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 15:22:26 2025

@author: penad
"""

from pyscipopt import Model

model = Model('example')

x = model.addVar('x', vtype='INTEGER')
y = model.addVar('y')

z = model.addVar('z')

model.setObjective(z, sense='maximize')

model.addCons(z == x+y*x)
model.addCons(-x+2*x*y<=8)#Can solve non linear problems
model.addCons(2*x+y<=14)
model.addCons(2*x-y<=10)

model.optimize()

sol = model.getBestSol()

print('x= ', sol[x])
print('y= ', sol[y])
      