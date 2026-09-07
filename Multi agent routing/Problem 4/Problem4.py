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

# Maximum distance an agent can travel during one trip
MAX_DISTANCE_PER_TRIP = 6

COST_PER_DISTANCE = 0.5

# Number of trips
R = 2

# Maximum number of movements per trip
T = 3


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

# ---------------------------------------------------------
# use_trip[k,r]
#
# 1 if agent k uses trip r
# 0 if trip r is not used
# ---------------------------------------------------------

model.use_trip = pyo.Var(
    model.K,
    model.R,
    domain=pyo.Binary
)

# =========================================================
# TRIPS MUST BE USED SEQUENTIALLY
# =========================================================
#
# If trip 2 is used, trip 1 must also be used.
#
# Therefore:
#
# use_trip[k,1] >= use_trip[k,2]
# use_trip[k,2] >= use_trip[k,3]
# etc.
#
# This prevents solutions such as:
#
# Trip 1 = unused
# Trip 2 = used
#

def sequential_trips_rule(model, k, r):

    if r == 1:
        return pyo.Constraint.Skip

    return (
        model.use_trip[k, r]
        <= model.use_trip[k, r - 1]
    )


model.sequential_trips = pyo.Constraint(
    model.K,
    model.R,
    rule=sequential_trips_rule
)


# =========================================================
# INITIAL POSITION OF EACH TRIP
# =========================================================
#
# If a trip is used, the agent starts at its home node.
#
# If the trip isn't used, all visit variables are zero.
#

def initial_position_rule(model, k, r, node):

    if node == start[k]:

        return (
            model.visit[k, r, 0, node]
            == model.use_trip[k, r]
        )

    return (
        model.visit[k, r, 0, node]
        == 0
    )


model.initial_position = pyo.Constraint(
    model.K,
    model.R,
    model.N,
    rule=initial_position_rule
)


# =========================================================
# ONE POSITION PER TIMESTEP
# =========================================================
#
# If the trip is used:
#     exactly one position.
#
# If the trip isn't used:
#     no position.
#

def one_position_rule(model, k, r, t):

    return sum(
        model.visit[k, r, t, node]
        for node in model.N
    ) == model.use_trip[k, r]


model.one_position = pyo.Constraint(
    model.K,
    model.R,
    model.T,
    rule=one_position_rule
)


# =========================================================
# ONE MOVEMENT PER TIMESTEP
# =========================================================
#
# Used trip:
#     exactly one edge per timestep.
#
# Unused trip:
#     no edges.
#

def one_move_rule(model, k, r, t):

    if t == T:
        return pyo.Constraint.Skip

    return sum(
        model.x[k, r, t, i, j]
        for (i, j) in model.E
    ) == model.use_trip[k, r]


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
# RETURN HOME AT END OF USED TRIP
# =========================================================
#
# If trip is used:
#     final position = starting node
#
# If trip is unused:
#     use_trip = 0, so this constraint becomes:
#
#     visit[...] = 0
#

def return_home_rule(model, k, r):

    return (
        model.visit[k, r, T, start[k]]
        == model.use_trip[k, r]
    )


model.return_home = pyo.Constraint(
    model.K,
    model.R,
    rule=return_home_rule
)

# =========================================================
# MAXIMUM DISTANCE PER USED TRIP
# =========================================================

def max_distance_rule(model, k, r):

    return sum(
        df.loc[i, j]
        * model.x[k, r, t, i, j]

        for t in model.T
        if t < T

        for (i, j) in model.E

    ) <= MAX_DISTANCE_PER_TRIP * model.use_trip[k, r]


model.max_distance = pyo.Constraint(
    model.K,
    model.R,
    rule=max_distance_rule
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
# PRINT SOLUTION
# =========================================================

total_distance = 0

for k in model.K:

    print("\n" + "=" * 50)
    print(f"{k}  (starts at {start[k]})")
    print("=" * 50)

    agent_total_distance = 0

    for r in model.R:

        used = pyo.value(
            model.use_trip[k, r]
        )

        if used < 0.5:
            print(f"Trip {r}: NOT USED")
            continue

        route = []
        trip_distance = 0

        # ---------------------------------------------
        # Route
        # ---------------------------------------------

        for t in model.T:

            for node in model.N:

                if pyo.value(
                    model.visit[k, r, t, node]
                ) > 0.5:

                    route.append(node)
                    break

        # ---------------------------------------------
        # Distance
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


# =========================================================
# TOTAL
# =========================================================

print("\n" + "=" * 50)
print("TOTAL")
print("=" * 50)

print(
    "Total distance:",
    total_distance
)

print(
    "Total cost: "
    f"${total_distance * COST_PER_DISTANCE:.2f}"
)