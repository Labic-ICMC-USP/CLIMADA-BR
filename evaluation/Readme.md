# Unsupervised Learning of Risk Matrix using LLMs and GNNs.

This repository provides a **self‑contained notebook** to reproduce the experimental evaluation that combines **LLM‑derived signals** (e.g., severity labels and document‑level evidence) with **graph‑based learning** (link prediction and node classification). The workflow assumes the required datasets are provided as **zipped archives** (potentially split in 20 MB volumes) and extracted locally before execution.

---

## 1) What you will reproduce

We evaluate whether the **graph structure plus node embeddings** can recover information originally produced by an LLM. Concretely:

- **Link Prediction**: we **remove a random subset of edges** (e.g., 20%) and train a GNN (GraphSAGE) to predict the missing links using the provided node embeddings. Metrics include **ROC‑AUC** and **Average Precision**, and we select a decision threshold (e.g., Youden or F1) to report calibrated performance. A PDF report with ROC/PR curves and summary tables is produced.
- **Node Severity Classification**: we treat LLM‑assigned **severity** as a 3‑class label (`low`, `medium`, `high`). Using the graph plus embeddings, a GNN classifier predicts severity; we report **macro‑F1**, **balanced accuracy**, and the **confusion matrix**. A PDF report is produced.

**Why this matters (validation idea)**: this is an **unsupervised/weakly‑supervised validation** of LLM outputs. If the graph can **reconstruct hidden edges** and **recover severity labels** that originated from the LLM, then those LLM signals are **topologically consistent**—i.e., they are encoded in the structure/embeddings and can be rediscovered without directly accessing the original text. This provides an orthogonal sanity‑check for the LLM‑based analysis.

---

## 2) Repository layout

- `evaluation.ipynb` — the main notebook that runs **both** tasks (link prediction and node severity classification) and generates PDF reports.
- Expected data artifacts (placed in the repo root or a `data/` folder):
  - `graph.pkl` — pickled **NetworkX** graph (undirected; the notebook will automatically keep the largest connected component if needed).
  - `embeddings.npy` — `N × d` **NumPy** array with node embeddings.
  - `labels.npy` — array of string labels (`low`, `medium`, `high`) for node severity.
  - `df_data.pkl` — optional **Pandas** DataFrame with auxiliary metadata (used for summaries/plots if present).
- Generated outputs (by default in the working directory):
  - `linkpred_report.pdf` — link prediction plots & metrics.
  - `severity_nodecls_report.pdf` — node classification plots & metrics.

> If you prefer a clean layout, create a `data/` directory, move all input files there, and adjust the file paths in the first parameter cell of the notebook.

---

## 3) Getting the data ready (zipped and split archives)

Place **all ZIP volumes** in the same directory (e.g., `data/`). For split ZIPs you should see files like:
```
dataset.z01
dataset.z02
...
dataset.zip
```

Then extract **directly from the `.zip` index** (no manual concatenation needed):
```bash
unzip dataset.zip -d data/
```
> Ensure the `.z01`, `.z02`, … files are in the same folder as `dataset.zip`. On Linux/macOS, `unzip` handles split archives automatically. On Windows, 7‑Zip also works.

If your files are not split, a standard unzip is enough:
```bash
unzip data.zip -d data/
```

---

## 4) Environment setup

We recommend **Python 3.10+** in a virtual environment.

### Option A — `venv` (CPU‑only PyTorch)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip

# Core scientific stack
pip install numpy pandas matplotlib scikit-learn networkx

# PyTorch (CPU wheels)
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio

# PyTorch Geometric (meta‑package)
pip install torch-geometric
```
> If `torch-geometric` requires extra wheels (`torch_scatter`, `torch_sparse`, etc.), follow the official instructions for your exact PyTorch/CUDA version at: https://pytorch-geometric.readthedocs.io/

### Option B — Conda (CPU‑only)
```bash
conda create -n llm-gnn python=3.10 -y
conda activate llm-gnn
pip install numpy pandas matplotlib scikit-learn networkx
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio
pip install torch-geometric
```

---

## 5) Running the experiments

### A) Interactive (Jupyter)
```bash
# from the repo root
jupyter lab   # or: jupyter notebook
```
Open `evaluation.ipynb` and run **all cells**. The notebook expects the following default paths (adjust if you moved files):
```python
graph_path="graph.pkl"
embeddings="embeddings.npy"
labels_path="labels.npy"  # strings: 'low'/'medium'/'high'
```
Key hyper‑parameters (as used in the notebook examples):
- **Link Prediction**: `pct_remove=0.2`, `hidden=64`, `out_dim=64`, `epochs=1000`, `lr=1e-3`, `optimize_threshold="youden"`
- **Node Classification**: `hidden=64`, `out_dim_embed=64`, `dropout=0.2`, `epochs=1000`, `lr=1e-3`, `class_weight=True`, `es_metric="val_macro_f1"`, `es_patience=150`

Outputs saved:
- `linkpred_report.pdf`
- `severity_nodecls_report.pdf`

### B) Headless execution (fully reproducible run)
You can execute the notebook without opening Jupyter and capture a timestamped copy:
```bash
pip install jupyter nbconvert
jupyter nbconvert --to notebook --execute evaluation.ipynb   --ExecutePreprocessor.timeout=0   --output "runs/evaluation_run.ipynb"
```
The PDF reports will be written as in the interactive mode.

> **Determinism**: the notebook sets `seed=42` for NumPy/PyTorch; hardware/cuDNN may still introduce minor nondeterminism on GPU. For strict CPU reproducibility, keep CPU‑only wheels.

---

## 6) Quick description of the evaluation proposal

- We **do not assume ground‑truth labels from manual annotation**. Instead, we **validate** the coherence of **LLM‑derived information** using **graph learning**:
  1. **Remove edges**, then **predict them** from the remaining graph + embeddings (link prediction). High ROC‑AUC/AP indicates that the topology embeds enough structure to recover LLM‑consistent relations.
  2. **Hide severity labels** on a validation/test split, then **predict them** using a GNN classifier (node classification). Strong macro‑F1/balanced accuracy and a compact confusion matrix indicate that the severity signal is structurally consistent.
- Together, these tests check whether the **LLM signals are recoverable from structure**. If they are, we gain confidence that the LLM outputs are **internally consistent** and **not artifacts of spurious text patterns**.

---
