import os
import torch
import numpy as np
import joblib
from torch_geometric.nn import SAGEConv

# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "ml")

# ===============================
# GNN MODEL DEFINITION
# ===============================
class GraphSAGE(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, hidden_channels)
        self.conv3 = SAGEConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        x = torch.relu(x)
        x = self.conv3(x, edge_index)
        return x


# ===============================
# MODEL DIMENSIONS
# ===============================
GNN_INPUT_DIM = 8
GNN_HIDDEN_DIM = 64
GNN_OUTPUT_DIM = 8
XGB_INPUT_DIM = 13

# ===============================
# LOAD MODELS
# ===============================
print("Loading GNN model...")
gnn_model = GraphSAGE(GNN_INPUT_DIM, GNN_HIDDEN_DIM, GNN_OUTPUT_DIM)
gnn_model.load_state_dict(
    torch.load(os.path.join(MODEL_DIR, "gnn_model.pt"), map_location="cpu")
)
gnn_model.eval()
print("GNN model loaded successfully")

print("Loading XGBoost model...")
xgb_model = joblib.load(os.path.join(MODEL_DIR, "xgb_model.pkl"))
print("XGBoost model loaded successfully")


# ===============================
# HYBRID PREDICTION FUNCTION
# ===============================
def hybrid_predict(all_features, edge_index):
    """
    all_features: numpy array of shape [N, 13]
    edge_index: torch tensor [2, E]
    """
    gnn_features = torch.tensor(all_features[:, :8], dtype=torch.float)

    with torch.no_grad():
        gnn_logits = gnn_model(gnn_features, edge_index)
        gnn_probs = torch.softmax(gnn_logits, dim=1).numpy()

    xgb_probs = xgb_model.predict_proba(all_features)

    min_classes = min(gnn_probs.shape[1], xgb_probs.shape[1])
    final_probs = (gnn_probs[:, :min_classes] + xgb_probs[:, :min_classes]) / 2

    final_preds = np.argmax(final_probs, axis=1)

    return final_preds, final_probs


# ===============================
# TEST RUN
# ===============================
if __name__ == "__main__":
    print("Running hybrid predictor test...")

    num_nodes = 5
    dummy_features = np.random.rand(num_nodes, 13)

    dummy_edge_index = torch.tensor([
        [0, 1, 2, 3],
        [1, 2, 3, 4]
    ], dtype=torch.long)

    preds, probs = hybrid_predict(dummy_features, dummy_edge_index)

    print("Predictions:", preds)
    print("Probabilities shape:", probs.shape)