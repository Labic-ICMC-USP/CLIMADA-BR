# pip install sentence transformers and scikit-network

from climada.util import *

from sentence_transformers import SentenceTransformer
import pandas as pd
import os

import networkx as nx
from sklearn.neighbors import NearestNeighbors
import sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)

from IPython.display import SVG

from scipy import sparse

from sknetwork.data import art_philo_science
from sknetwork.classification import get_accuracy_score
from sknetwork.gnn import GNNClassifier
from sknetwork.visualization import visualize_graph

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

class HazReg():

    def graphBuild(self, df, features):
        # Use Nearest Neighbors to find connections
        neighbors = NearestNeighbors(n_neighbors=5, metric='cosine').fit(features)
        distances, indices = neighbors.kneighbors(features)

        # Build the graph
        G = nx.Graph()
        for idx, neighbors in enumerate(indices):
            for neighbor in neighbors:
                if idx != neighbor:  # avoid self-loops
                    G.add_edge(idx, neighbor)
        
        return G
    
    def labelAssignment(self, df):
        # Define thresholds for positive and negative labels (example, adjust intervals)
        high_severity_threshold = df['Severity of Event'].quantile(0.9)
        low_severity_threshold = df['Severity of Event'].quantile(0.1)

        labels = {}
        for idx, severity in enumerate(df['Severity of Event']):
            if severity >= high_severity_threshold:
                labels[idx] = 1  # Positive
            elif severity <= low_severity_threshold:
                labels[idx] = 0  # Negative
            else:
                labels[idx] = -1  # No label (labels with -1 are not used in training)
        
        return labels
    
    def GCN_Classification(self, df, G, labels, features):
        # Prepare adjacency matrix for the GCN
        adjacency = nx.adjacency_matrix(G)
        adjacency = sparse.csr_matrix(adjacency)

        # GNN classifier with a single hidden layer
        hidden_dim = 5

        # Number of labels
        n_labels = len(set(labels))

        gnn = GNNClassifier(dims=[hidden_dim, n_labels],
                            layer_types='Conv',
                            activations='ReLu',
                            verbose=True)
        
        # Training
        labels_pred = gnn.fit_predict(adjacency, features, labels, n_epochs=200, random_state=42)

        # History for each training epoch
        gnn.history_.keys()

        # Visualization
        # image = visualize_graph(adjacency, labels=labels_pred)
        # SVG(image)

        # probability distribution over labels
        probs = gnn.predict_proba()

        label = 1
        scores = probs[:, label]

        # Visualization
        # image = visualize_graph(adjacency, scores=scores)
        # SVG(image)

        # Add GCN scores to the dataframe
        df['gcn_scores'] = scores

        return df
    
    def Results_Plots(self):
        # Extract feature vectors and severity values
        features_before = np.vstack(self.new_df['features'].values)
        severity_values = self.new_df['Severity of Event'].values

        # Perform t-SNE on the data before adjustment
        tsne_before = TSNE(n_components=2, random_state=42).fit_transform(features_before)

        # Plot t-SNE results before adjustment
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(tsne_before[:, 0], tsne_before[:, 1], c=severity_values, cmap='viridis', alpha=0.7)
        plt.colorbar(scatter, label='Severity')
        plt.title("t-SNE Visualization Before Adjustment")
        plt.xlabel("t-SNE Dimension 1")
        plt.ylabel("t-SNE Dimension 2")
        plt.show()

        # Assuming `adjusted_features` contains the feature vectors after adjustment

        # Extract feature vectors and severity values
        adjusted_features = np.vstack(self.new_df['features'].values)
        adjusted_severity = self.new_df['gcn_scores'].values

        # Perform t-SNE on the data after adjustment
        tsne_after = TSNE(n_components=2, random_state=42).fit_transform(adjusted_features)

        # Plot t-SNE results after adjustment
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(tsne_after[:, 0], tsne_after[:, 1], c=adjusted_severity, cmap='viridis', alpha=0.7)
        plt.colorbar(scatter, label='Severity')
        plt.title("t-SNE Visualization After Adjustment")
        plt.xlabel("t-SNE Dimension 1")
        plt.ylabel("t-SNE Dimension 2")
        plt.show()

    def __init__(self, file_name):

        print("=====================================\nUsing GCN to better classify Severity\n=====================================")

        file_path = os.path.join(SYSTEM_DIR, file_name)

        # Load dengue data
        df = pd.read_excel(file_path)

        # Initialize SBERT model
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Generate feature vectors for each event
        df['features'] = df['Description of Hazard'].apply(lambda x: model.encode(x))

        # Convert feature vectors to numpy array
        features = np.vstack(df['features'].values)

        G = self.graphBuild(df, features)

        labels = self.labelAssignment(df)

        self.new_df = self.GCN_Classification(df, G, labels, features)

    def get_df(self):
        return self.new_df
        