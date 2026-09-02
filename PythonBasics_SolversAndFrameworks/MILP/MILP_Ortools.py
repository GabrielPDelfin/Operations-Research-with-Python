# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 03:12:31 2025

@author: penad
"""

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('cbc')

x = solver.IntVar(0,10,'x')
y = solver.NumVar(0,10,'y')

solver.Add(-x+2*y<=7)
solver.Add(2*x+y<=14)
solver.Add(2*x-y<=10)

solver.Maximize(x+y)

results = solver.Solve()

if (results==pywraplp.Solver.OPTIMAL):
    print('Optimal found')

print('x: ', x.solution_value())
print('y: ', y.solution_value())