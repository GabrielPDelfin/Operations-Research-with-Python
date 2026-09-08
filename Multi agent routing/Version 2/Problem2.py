import pandas as pd
import pyomo.environ as pyo


# =========================================================
# DATA
# =========================================================

df = pd.read_excel(
    "../distances.xlsx",
    index_col=0
)

nodes = df.index.tolist()

people = ["P1", "P2"]

start = {
    "P1": "A",
    "P2": "E",
}

COST_PER_DISTANCE = 0.5

T = 6


# =========================================================
# VALID EDGES
# =========================================================

# Includes zero-distance edges such as A -> A
edges = [
    (i, j)
    for i in nodes
    for j in nodes
    if df.loc[i, j] >= 0
]


# =========================================================
# MODEL
# =========================================================

model = pyo.ConcreteModel()

model.N = pyo.Set(initialize=nodes)
model.K = pyo.Set(initialize=people)
model.T = pyo.RangeSet(0, T)

model.E = pyo.Set(
    dimen=2,
    initialize=edges
)


# =========================================================
# VARIABLES
# =========================================================

# Person k travels from i to j at time t
model.x = pyo.Var(
    model.K,
    model.T,
    model.E,
    domain=pyo.Binary
)

# Person k is at node i at time t
model.visit = pyo.Var(
    model.K,
    model.T,
    model.N,
    domain=pyo.Binary
)


# =========================================================
# INITIAL POSITION
# =========================================================

def initial_position_rule(model, k, node):

    if node == start[k]:
        return model.visit[k, 0, node] == 1

    return model.visit[k, 0, node] == 0


model.initial_position = pyo.Constraint(
    model.K,
    model.N,
    rule=initial_position_rule
)


# =========================================================
# ONE POSITION PER PERSON PER TIME
# =========================================================

def one_position_rule(model, k, t):

    return sum(
        model.visit[k, t, node]
        for node in model.N
    ) == 1


model.one_position = pyo.Constraint(
    model.K,
    model.T,
    rule=one_position_rule
)


# =========================================================
# ONE EDGE PER PERSON PER TIME
# =========================================================

def one_move_rule(model, k, t):

    if t == T:
        return pyo.Constraint.Skip

    return sum(
        model.x[k, t, i, j]
        for (i, j) in model.E
    ) == 1


model.one_move = pyo.Constraint(
    model.K,
    model.T,
    rule=one_move_rule
)


# =========================================================
# EDGE MUST LEAVE CURRENT NODE
# =========================================================

def outgoing_rule(model, k, t, node):

    if t == T:
        return pyo.Constraint.Skip

    return sum(
        model.x[k, t, i, j]
        for (i, j) in model.E
        if i == node
    ) == model.visit[k, t, node]


model.outgoing = pyo.Constraint(
    model.K,
    model.T,
    model.N,
    rule=outgoing_rule
)


# =========================================================
# EDGE MUST ARRIVE AT NEXT NODE
# =========================================================

def incoming_rule(model, k, t, node):

    if t == T:
        return pyo.Constraint.Skip

    return sum(
        model.x[k, t, i, j]
        for (i, j) in model.E
        if j == node
    ) == model.visit[k, t + 1, node]


model.incoming = pyo.Constraint(
    model.K,
    model.T,
    model.N,
    rule=incoming_rule
)


# =========================================================
# EVERY NODE MUST BE VISITED
# =========================================================

def coverage_rule(model, node):

    return sum(
        model.visit[k, t, node]
        for k in model.K
        for t in model.T
    ) >= 1


model.coverage = pyo.Constraint(
    model.N,
    rule=coverage_rule
)

# =========================================================
# EVERY AGENT MUST RETURN TO THEIR STARTING NODE
# =========================================================

def final_position_rule(model, k):
    return model.visit[k, T, start[k]] == 1

model.final_position = pyo.Constraint(
    model.K,
    rule=final_position_rule
)


# =========================================================
# OBJECTIVE
# =========================================================

def objective_rule(model):

    return sum(
        COST_PER_DISTANCE
        * df.loc[i, j]
        * model.x[k, t, i, j]

        for k in model.K
        for t in model.T
        if t < T

        for (i, j) in model.E
    )


model.objective = pyo.Objective(
    rule=objective_rule,
    sense=pyo.minimize
)


# =========================================================
# SOLVE
# =========================================================

solver = pyo.SolverFactory("glpk")

result = solver.solve(
    model,
    tee=True
)


# =========================================================
# CHECK SOLUTION BEFORE READING VARIABLES
# =========================================================

print()
print("Solver status:", result.solver.status)
print("Termination condition:",
      result.solver.termination_condition)

if result.solver.termination_condition not in [
    pyo.TerminationCondition.optimal,
    pyo.TerminationCondition.feasible
]:
    raise RuntimeError(
        "The solver did not find a feasible solution."
    )


# =========================================================
# PRINT ROUTES
# =========================================================

total_distance = 0

for k in model.K:

    route = []
    person_distance = 0

    for t in model.T:

        # Current node
        for node in model.N:

            if pyo.value(model.visit[k, t, node]) > 0.5:
                route.append(node)
                break

        # Movement
        if t < T:

            for (i, j) in model.E:

                if pyo.value(
                    model.x[k, t, i, j]
                ) > 0.5:

                    person_distance += df.loc[i, j]
                    break

    total_distance += person_distance

    print(f"\n{k}")
    print("Route:", " -> ".join(route))
    print("Distance:", person_distance)
    print(
        "Cost: $",
        person_distance * COST_PER_DISTANCE
    )


print("\n==========================")
print("Total distance:", total_distance)
print(
    "Total cost: $",
    total_distance * COST_PER_DISTANCE
)