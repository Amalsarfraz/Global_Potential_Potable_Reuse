# Global Potential of Potable Reuse

[![DOI](https://zenodo.org/badge/DOI/10.xxxx/zenodo.xxxxxxx.svg)](https://doi.org/10.xxxx/zenodo.xxxxxxx)

**Global Potential of Potable Reuse Across Coupled Climate and Socioeconomic Futures**

Utrecht University.
Contact: [a.sarfraz@uu.nl](mailto:a.sarfraz@uu.nl).

This repository holds the analysis code and figure notebooks behind the
paper. 

## Repository layout

| Path | What it is |
|------|------------|
| `notebooks/` | The analysis. One preprocessing notebook plus one notebook per main figure. |
| `src/potable_reuse/` | The importable Python package the notebooks share: plotting style, the scenario loader, and the figure writer. Notebooks add `src/` to the path and `import potable_reuse`. |
| `config/paths.yaml` | Every input and output path, resolved relative to the repo root. The one file to edit if your data sits elsewhere. |
| `data/` |  |
| `outputs/` |  |
| `environment.yml` | Conda environment covering both the Python and the R halves. |
| `requirements.txt` | Pip dependencies for the Python notebooks only. |



## Setup

The recommended path is one conda environment, because the maps notebook
uses R while the other four use Python.

```bash
conda env create -f environment.yml
conda activate gcamwaterreuse
```



Python only:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```


## Reproduce the analysis

Run the notebooks from `notebooks/`. The path block at the top of each one
finds the repo root automatically and reads `config/paths.yaml`.

1. **`00_preprocess_scenario_caches.ipynb`** builds the combined per-query
   caches in `data/cache/`. Skip this if you downloaded tier 1, which
   already contains the caches.
2. **`figure1_global_displacement.ipynb`** global displacement boxplots
   and the sectoral reallocation of saved municipal water.
3. **`figure2_regional_trajectories.ipynb`** regional reduction
   trajectories with median and interquartile bands.
4. **`figure2_yearly_maps_individual.ipynb`** the GCAM 32-region world
   maps (R kernel).
5. **`figure3_variance_decomposition_combined.ipynb`** the inter-scenario
   variance decomposition.
6. **`figure4_cart_shap_combined.ipynb`** the CART and SHAP attribution of
   reduction drivers.

Each notebook writes its panels under `outputs/figure{n}/`.

## Citation


## Questions

Email [a.sarfraz@uu.nl](mailto:a.sarfraz@uu.nl).
