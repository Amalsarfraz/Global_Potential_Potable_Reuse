# Global Potential of Potable Reuse

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20262039.svg)](https://doi.org/10.5281/zenodo.20262039)

**Global Potential of Potable Reuse **

Utrecht University.
Contact: [a.sarfraz@uu.nl](mailto:a.sarfraz@uu.nl).

This repository holds the analysis code and figure notebooks behind the
paper. The GCAM model code and the scenario setup are in a separate
repository.

## Repository layout

| Path | What it is |
|------|------------|
| `notebooks/` | One preprocessing notebook and one notebook for each figure. |
| `src/potable_reuse/` | Python package shared by the notebooks: plotting style, scenario loader and figure writer. |
| `config/paths.yaml` | Every input and output path, relative to the repo root. Edit this file if your data sits elsewhere. |
| `data/` | Input data (see below). |
| `outputs/` | Generated figures and tables, one subfolder per figure. |
| `environment.yml` | Conda environment for Python and R. |
| `requirements.txt` | Pip dependencies for the Python notebooks only. |

## Data

Only the processed GCAM ensemble is hosted externally because of its size.
Everything else is already in `data/`.

| Folder | paths.yaml key | Contents | Source |
|--------|----------------|----------|--------|
| `data/Scenarios/` | `scenarios_dir` | Raw GCAM ensemble: 459 scenario folders with their query parquets. | [Zenodo](https://doi.org/10.5281/zenodo.20262039) |
| `data/cache/` | `cache_dir` | Combined query caches used by Figures 1 and 3. | In the repo, or rebuilt by notebook 00. |
| `data/regional_reductions/` | `regional_reductions_dir` | Regional municipal withdrawal with and without reuse, for PR50 and PR100. Used by Figures 2 and 4. | In the repo. |
| `data/merged_parquets/` | `merged_parquets_dir` | Regional municipal withdrawal, groundwater, GDP per capita and population. Used by Figure 5. | In the repo. |

The Zenodo download is only needed to rebuild `data/cache/` with
notebook 00. All figures run from the files already in the repo.

## Setup

Figures 2 and 3 run on an R kernel and the other notebooks on Python.
One conda environment covers both:

```bash
conda env create -f environment.yml
conda activate gcamwaterreuse
```

This also registers the "R (gcamwaterreuse)" Jupyter kernel.

For the Python notebooks alone, a plain virtual environment is enough:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Reproduce the analysis

Run the notebooks from `notebooks/`. Each one finds the repo root and
reads `config/paths.yaml` on its own.

| Notebook | Kernel | Output |
|----------|--------|--------|
| `00_preprocess_scenario_caches.ipynb` | Python | Builds the combined query caches in `data/cache/`. Optional. |
| `figure1_global_displacement.ipynb` | Python | Global municipal reduction and where the saved water goes. |
| `figure2_yearly_maps_individual.ipynb` | R | Yearly regional reduction maps for PR50 and PR100. |
| `figure3_composite_maps_panels_20260929.ipynb` | R | Variance decomposition: dominant driver map and regional panels. |
| `figure4_regional_trajectories_cost.ipynb` | Python | Exemplar region trajectories by reuse cost tier. |
| `figure5_shap_rc_tiers.ipynb` | Python | SHAP attribution of regional reduction drivers. |

Each notebook writes to its own folder, `outputs/figure1/` through
`outputs/figure5/`. 


## Citation

Please cite the Zenodo record:
[10.5281/zenodo.20262039](https://doi.org/10.5281/zenodo.20262039).

## Questions

Email [a.sarfraz@uu.nl](mailto:a.sarfraz@uu.nl).
