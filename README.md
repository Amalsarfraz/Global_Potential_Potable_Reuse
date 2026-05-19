# Global Potential of Potable Reuse

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20262039.svg)](https://doi.org/10.5281/zenodo.20262039)

**Global Potential of Potable Reuse Across Coupled Climate and Socioeconomic Futures**

Utrecht University.
Contact: [a.sarfraz@uu.nl](mailto:a.sarfraz@uu.nl).

This repository holds the analysis code and figure notebooks behind the
paper. 

## Repository layout


| Path | What it is |
|------|------------|
| `notebooks/` | The main analysis. One notebook for each figure.|
| `src/potable_reuse/` | The importable Python package the notebooks share: plotting style, the scenario loader, and the figure writer. Notebooks add `src/` to the path and `import potable_reuse`. |
| `config/paths.yaml` | Every input and output path, resolved relative to the repo root. The one file to edit if your data sits elsewhere. |
| `data/` | Input data. Populate it from Zenodo (see below). |
| `outputs/` | Generated figures and tables. One subfolder per figure. |
| `environment.yml` | Conda environment covering both Python and R. |
| `requirements.txt` | Pip dependencies for Python notebooks only. |

## Data

Only the raw GCAM ensemble is hosted externally because of its size. The
rest of the inputs ship inside the `data/` subfolders of this
repository, so a clone already has them.

| `data/` subfolder | paths.yaml key | What it holds | Source |
|-------------------|----------------|---------------|--------|
| `data/Scenarios/` | `scenarios_dir` | The raw GCAM ensemble: 459 scenario folders, each with its query parquets. | [Zenodo](https://doi.org/10.5281/zenodo.20262039) |
| `data/cache/` | `cache_dir` | Combined per-query caches built by the preprocessing notebook from the raw ensemble. | In the repo. |
| `data/merged_parquets/` | `merged_parquets_dir` | The merged design matrix used by the attribution notebook. | In the repo. |
| `data/regional_reductions/` | `regional_reductions_dir` | The per-region reduction parquets (PR50 and PR100) used by the trajectory and map notebooks. | In the repo. |



## Setup

The maps notebook runs on an R kernel while the other four run on
Python. One conda environment carries both halves, so this is all you
need:

```bash
conda env create -f environment.yml
conda activate gcamwaterreuse
```

That installs the Python stack, the R kernel, and registers the
"R (gcamwaterreuse)" Jupyter kernel that the maps notebook expects. Pick
the Python kernel for the four Python notebooks and the R kernel for the
maps notebook.

If you only need the Python notebooks and want to skip R, a plain
virtual environment works too:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```



## Reproduce the analysis

Run the notebooks from `notebooks/`. The path block at the top of each one
finds the repo root automatically and reads `config/paths.yaml`.

1. **`figure1_global_displacement.ipynb`** global displacement boxplots
   and the sectoral reallocation of saved municipal water.
2. **`figure2_regional_trajectories.ipynb`** regional reduction
   trajectories with median and interquartile bands.
3. **`figure2_yearly_maps_individual.ipynb`** the GCAM 32-region world
   maps (R kernel).
4. **`figure3_variance_decomposition_combined.ipynb`** the inter-scenario
   variance decomposition.
5. **`figure4_cart_shap_combined.ipynb`** the CART and SHAP attribution of
   reduction drivers.

Each notebook writes its panels under `outputs/figure{n}/`.

## Citation

If you use this code or data, please cite the Zenodo record:
[10.5281/zenodo.20262039](https://doi.org/10.5281/zenodo.20262039).

## Questions

Email [a.sarfraz@uu.nl](mailto:a.sarfraz@uu.nl).
