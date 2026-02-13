import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

print("Loading: processed_accident_with_coords.csv")

df = pd.read_csv("processed_accident_with_coords.csv")

print(f"Loaded dataframe with {df.shape[0]} rows and {df.shape[1]} columns.\n")

# ----------------------------
# Required columns
# ----------------------------
required_cols = [
    "Accident_ID",
    "Latitude",
    "Longitude",
    "Speed_Limit",
    "Hour",
    "Month",
    "DayOfWeek",
    "Number_of_Deaths",
    "Number_of_Injuries",
    "Severity_Score"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# ----------------------------
# Drop rows with NaN in critical columns
# ----------------------------
df = df.dropna(subset=required_cols).reset_index(drop=True)

# ----------------------------
# Create nodes dataframe (WITH FEATURES)
# ----------------------------
nodes = df[required_cols].copy()
nodes["node_id"] = range(len(nodes))

# ----------------------------
# Build k-NN graph using coordinates
# ----------------------------
coords = nodes[["Latitude", "Longitude"]].values

k = 5
nbrs = NearestNeighbors(n_neighbors=k + 1, algorithm="ball_tree").fit(coords)
distances, indices = nbrs.kneighbors(coords)

edges = []
for i, neighbors in enumerate(indices):
    for j in neighbors[1:]:  # skip self
        edges.append((i, j))

edges_df = pd.DataFrame(edges, columns=["src", "dst"])

# ----------------------------
# Save outputs
# ----------------------------
nodes.to_csv("nodes.csv", index=False)
edges_df.to_csv("graph_edges.csv", index=False)

print("Graph built successfully!")
print("Saved:")
print(" - nodes.csv (with features)")
print(" - graph_edges.csv")
