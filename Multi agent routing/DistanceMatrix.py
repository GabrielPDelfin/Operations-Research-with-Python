import pandas as pd

distance_data = {
    "A": [0,  2,  5, -1, -1],
    "B": [2,  0,  2,  4, -1],
    "C": [5,  2,  0,  1,  3],
    "D": [-1, 4,  1,  0,  2],
    "E": [-1, -1, 3,  2,  0],
}

df = pd.DataFrame(
    distance_data,
    index=["A", "B", "C", "D", "E"]
)

df.to_excel("distances.xlsx")

print(df)