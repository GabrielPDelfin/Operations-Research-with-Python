# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 14:04:34 2025

@author: penad
"""

import pulp as pl

model = pl.LpProblem('Ex', pl.LpMaximize)

x = pl.LpVariable('x',0.10)
y = pl.LpVariable('y',0.10)

model += -x+2*y<=8
model += 2*x+y<=14
model += 2*x-y<=10

model += x+y

status = model.solve()

x_value = pl.value(x)
y_value = pl.value(y)

print('x=',x_value)
print('y=',y_value)