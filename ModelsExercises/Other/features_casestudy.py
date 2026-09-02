import pyomo.environ as pyo
from pyomo.opt import SolverFactory

#Params and Sets
model = pyo.ConcreteModel()
model.T = pyo.Param(initialize=10)
T = model.T
model.M = pyo.Param(initialize=4)
M = model.M
model.LimProd = pyo.Param(initialize=10)

model.setT = pyo.RangeSet(1,T)
model.setM = pyo.RangeSet(1,M)

#variables
model.x = pyo.Var(model.setM, model.setT, within=pyo.Integers)
x = model.x

#rules
def myrule1(model,t):
    return 2*x[2,t] - 8*x[3,t] <= 0

def myrule2(model,t):
    if t <= 2:
        return pyo.Constraint.Skip
    else:
        return x[2,t] - 2*x[3,t-2] + x[4,t] >= 1
    
def myrule3(model,m,t):
    return pyo.inequality(0, x[m,t], model.LimProd)

#obj function
#model.obj = pyo.Objective(expr = sum([x[m,t] for m in range(1,M+1) for t in range(1,T+1)]), sense=pyo.maximize)
model.obj = pyo.Objective(expr = pyo.summation(x), sense=pyo.maximize)

#constraints
model.C1 = pyo.Constraint(model.setT, rule = myrule1)
'''
model.C1 = pyo.ConstraintList()
for t in model.setT:
    model.C1.add(expr = 2*x[2,t] - 8*x[3,t] <= 0)
'''

model.C2 = pyo.Constraint(model.setT, rule = myrule2)
'''   
model.C2 = pyo.ConstraintList()
for t in model.setT:
    if t>=3:    
        model.C2.add(expr = x[2,t] - 2*x[3,t-2] + x[4,t] >= 1)
'''
    
model.C3 = pyo.ConstraintList()
for t in model.setT:
    model.C3.add(expr = sum([x[m,t] for m in model.setM]) <= 50)

model.C4 = pyo.ConstraintList()
for t in model.setT:
    if t >=2:
        model.C4.add(expr = x[1,t] + x[2,t-1] + x[3,t] + x[4,t] <= model.LimProd)

model.C5 = pyo.Constraint(model.setM, model.setT, rule=myrule3)

'''
model.C5 = pyo.ConstraintList()
for m in model.setM:
    for t in model.setT:
        model.C5.add(pyo.inequality(0, x[m,t], model.LimProd))
        #model.C5.add(expr = x[m,t] <= 10)
        #model.C5.add(expr = x[m,t] >= 0)
'''

#solve
opt = SolverFactory('gurobi')
opt.options['MIPgap'] = 0.00
opt.options['TimeLimit'] = 0.1
results = opt.solve(model, tee=True)

print(pyo.value(model.obj))