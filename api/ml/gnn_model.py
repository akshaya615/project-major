import os
import torch
import pandas as pd
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import numpy as np

# --------------------------------------------------
# PATH CONFIGURATION (UPDATED FOR PROJECT STRUCTURE)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "ml")

# ----------------------------
# Load node & edge data
# ----------------------------
nodes = pd.read_csv(os.path.join(DATA_DIR, "nodes.csv"))
edges = pd.read_csv(os.path.join(DATA_DIR, "graph_edges.csv"))

# ----------------------------
# Feature selection
# ----------------------------
exclude_cols = ["node_id", "Severity_Score", "Accident_ID"]
feature_cols = [
    col for col in nodes.columns
    if col not in exclude_cols and nodes[col].dtype != "object"
]

print("Using GNN feature columns:", feature_cols)

# ----------------------------
# FEATURE NORMALIZATION
# ----------------------------
scaler = StandardScaler()
nodes[feature_cols] = scaler.fit_transform(nodes[feature_cols])

X = torch.tensor(nodes[feature_cols].values, dtype=torch.float)

# ----------------------------
# TARGET ENCODING
# ----------------------------
nodes["Severity_Class"] = pd.qcut(
    nodes["Severity_Score"],
    q=13,
    labels=False,
    duplicates="drop"
)

le = LabelEncoder()
y_encoded = le.fit_transform(nodes["Severity_Class"])
y = torch.tensor(y_encoded, dtype=torch.long)

print("Severity classes:", list(le.classes_))
print("Number of classes:", len(le.classes_))

# ----------------------------
# EDGE INDEX
# ----------------------------
edge_index = torch.tensor(
    np.array([edges["src"].values, edges["dst"].values]),
    dtype=torch.long
)

# If edge weights exist
if "weight" in edges.columns:
    edge_weight = torch.tensor(edges["weight"].values, dtype=torch.float)
else:
    edge_weight = None

data = Data(x=X, edge_index=edge_index, y=y)

# ----------------------------
# Train/Test split
# ----------------------------
train_idx, test_idx = train_test_split(
    np.arange(data.num_nodes),
    test_size=0.2,
    random_state=42,
    stratify=y.numpy()
)

data.train_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
data.test_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
data.train_mask[train_idx] = True
data.test_mask[test_idx] = True

# ----------------------------
# Class-weighted loss
# ----------------------------
class_counts = np.bincount(y.numpy())
class_weights = torch.tensor(1.0 / class_counts, dtype=torch.float)

# ----------------------------
# GraphSAGE Model
# ----------------------------
class GraphSAGE(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, hidden_channels)
        self.conv3 = SAGEConv(hidden_channels, out_channels)
        self.dropout = torch.nn.Dropout(p=0.3)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.conv3(x, edge_index)
        return x


model = GraphSAGE(
    in_channels=X.shape[1],
    hidden_channels=64,
    out_channels=len(le.classes_)
)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.005,
    weight_decay=1e-4
)

criterion = torch.nn.CrossEntropyLoss(weight=class_weights)

# ----------------------------
# Training loop
# ----------------------------
epochs = 300
best_loss = float("inf")
patience = 20
trigger = 0

for epoch in range(1, epochs + 1):
    model.train()
    optimizer.zero_grad()

    out = model(data.x, data.edge_index)
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch} | Loss: {loss.item():.4f}")

    if loss.item() < best_loss:
        best_loss = loss.item()
        trigger = 0
    else:
        trigger += 1
        if trigger >= patience:
            print("Early stopping triggered")
            break

# ----------------------------
# Evaluation
# ----------------------------
model.eval()
out = model(data.x, data.edge_index)
pred = out.argmax(dim=1)

correct = int((pred[data.test_mask] == data.y[data.test_mask]).sum())
accuracy = correct / int(data.test_mask.sum())

print(f"\nGraphSAGE Test Accuracy: {accuracy:.4f}")

# ----------------------------
# Save model + encoder
# ----------------------------
torch.save(model.state_dict(), os.path.join(MODEL_DIR, "gnn_model.pt"))
torch.save(le, os.path.join(MODEL_DIR, "gnn_severity_encoder.pt"))

print("\nSaved:")
print(" - gnn_model.pt")
print(" - gnn_severity_encoder.pt")