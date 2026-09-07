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

# Number of trips
R = 2

# Maximum number of movements per trip
T = 2


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

model.R = pyo.RangeSet(1, R)

model.T = pyo.RangeSet(0, T)

model.E = pyo.Set(
    dimen=2,
    initialize=edges
)


# =========================================================
# VARIABLES
# =========================================================

# x[k,r,t,i,j] = 1 if agent k travels
#                 from i to j at time t
#                 during trip r
#
model.x = pyo.Var(
    model.K,
    model.R,
    model.T,
    model.E,
    domain=pyo.Binary
)

# visit[k,r,t,i] = 1 if agent k is at node i
#                  at time t during trip r
#
model.visit = pyo.Var(
    model.K,
    model.R,
    model.T,
    model.N,
    domain=pyo.Binary
)


# =========================================================
# INITIAL POSITION OF EACH TRIP
# =========================================================

def initial_position_rule(model, k, r, node):

    if node == start[k]:
        return model.visit[k, r, 0, node] == 1

    return model.visit[k, r, 0, node] == 0


model.initial_position = pyo.Constraint(
    model.K,
    model.R,
    model.N,
    rule=initial_position_rule
)


# =========================================================
# ONE POSITION PER TIME
# =========================================================

def one_position_rule(model, k, r, t):

    return sum(
        model.visit[k, r, t, node]
        for node in model.N
    ) == 1


model.one_position = pyo.Constraint(
    model.K,
    model.R,
    model.T,
    rule=one_position_rule
)


# =========================================================
# ONE MOVEMENT PER TIME
# =========================================================

def one_move_rule(model, k, r, t):

    if t == T:
        return pyo.Constraint.Skip

    return sum(
        model.x[k, r, t, i, j]
        for (i, j) in model.E
    ) == 1


model.one_move = pyo.Constraint(
    model.K,
    model.R,
    model.T,
    rule=one_move_rule
)


# =========================================================
# MOVEMENT MUST LEAVE CURRENT NODE
# =========================================================

def outgoing_rule(model, k, r, t, node):

    if t == T:
        return pyo.Constraint.Skip

    return sum(
        model.x[k, r, t, i, j]
        for (i, j) in model.E
        if i == node
    ) == model.visit[k, r, t, node]


model.outgoing = pyo.Constraint(
    model.K,
    model.R,
    model.T,
    model.N,
    rule=outgoing_rule
)


# =========================================================
# MOVEMENT MUST ARRIVE AT NEXT NODE
# =========================================================

def incoming_rule(model, k, r, t, node):

    if t == T:
        return pyo.Constraint.Skip

    return sum(
        model.x[k, r, t, i, j]
        for (i, j) in model.E
        if j == node
    ) == model.visit[k, r, t + 1, node]


model.incoming = pyo.Constraint(
    model.K,
    model.R,
    model.T,
    model.N,
    rule=incoming_rule
)


# =========================================================
# RETURN TO STARTING NODE AFTER EVERY TRIP
# =========================================================

def return_home_rule(model, k, r):

    return model.visit[
        k, r, T, start[k]
    ] == 1


model.return_home = pyo.Constraint(
    model.K,
    model.R,
    rule=return_home_rule
)


# =========================================================
# EVERY NODE MUST BE VISITED
# =========================================================

def coverage_rule(model, node):

    return sum(
        model.visit[k, r, t, node]
        for k in model.K
        for r in model.R
        for t in model.T
    ) >= 1


model.coverage = pyo.Constraint(
    model.N,
    rule=coverage_rule
)


# =========================================================
# MINIMIZE TOTAL TRAVEL COST
# =========================================================

def objective_rule(model):

    return sum(
        COST_PER_DISTANCE
        * df.loc[i, j]
        * model.x[k, r, t, i, j]

        for k in model.K
        for r in model.R
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
# CHECK SOLUTION
# =========================================================

print()
print("Solver status:",
      result.solver.status)

print(
    "Termination condition:",
    result.solver.termination_condition
)

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

    print(f"\n{'=' * 40}")
    print(f"{k}  (starts at {start[k]})")
    print(f"{'=' * 40}")

    agent_total_distance = 0

    for r in model.R:

        route = []
        trip_distance = 0

        # ---------------------------------------------
        # Get route
        # ---------------------------------------------

        for t in model.T:

            for node in model.N:

                if pyo.value(
                    model.visit[k, r, t, node]
                ) > 0.5:

                    route.append(node)
                    break

        # ---------------------------------------------
        # Calculate trip distance
        # ---------------------------------------------

        for t in model.T:

            if t == T:
                continue

            for (i, j) in model.E:

                if pyo.value(
                    model.x[k, r, t, i, j]
                ) > 0.5:

                    trip_distance += df.loc[i, j]
                    break

        agent_total_distance += trip_distance

        print(
            f"Trip {r}: "
            f"{' -> '.join(route)}"
        )

        print(
            f"  Distance: {trip_distance}"
        )

        print(
            f"  Cost: "
            f"${trip_distance * COST_PER_DISTANCE:.2f}"
        )

    total_distance += agent_total_distance

    print(
        f"\nTotal distance for {k}: "
        f"{agent_total_distance}"
    )

    print(
        f"Total cost for {k}: "
        f"${agent_total_distance * COST_PER_DISTANCE:.2f}"
    )


# =========================================================
# TOTAL COST
# =========================================================

print(f"\n{'=' * 40}")
print("TOTAL")
print(f"{'=' * 40}")

print(
    "Total distance:",
    total_distance
)

print(
    "Total cost: "
    f"${total_distance * COST_PER_DISTANCE:.2f}"
)