# RAVEN
This repository contains the code, modified gem5 sources, simulation inputs, outputs, and analysis scripts that accompany the journal submission. RAVEN extends gem5 to support microarchitectural security experiments: custom counters (HPCS), attack/benign benchmarks, timed simulations, and an ML-based attack detection pipeline. This README explains repository layout, installation & build, how to reproduce the experiments, where to find modified gem5 sources, and how to run the detection/analysis.

## Repository layout (top level)

`RAVEN-main/` contains the following principal folders and files:

`Getting started/` — Installation and build guides for gem5, and a short “How_to_install_gem5” note. Files included: `gem5_guide1.pdf`, `gem5_guide2.pdf`, `gem5_guide3.pdf`, `How_to_install_gem5`.

`Attack Assessment/` — Simulation results and scripts used to evaluate the attacks and the benign workload. Subfolders: `attack_simulations/`, `benign_simulation/`, and `Figures/`.

`gem5_config/` — The set of modified gem5 source files and full-system script(s) used in all experiments. Files present include `base.cc`, `base.hh`, `cache.cc`, `cache.hh`, `commit.cc`, `commit.hh`, `cpu.cc`, `cpu.hh`, `isa.cc`, `isa.hh`, `riscv-fs.py`, `riscv-64bit-csr.xml`, `cpt.final8`, `HPC/` and other configuration files.

`Attack Detection/` — Scripts and directories for extracting metrics, generating ML features, training/testing ML models, and the outputs of the detection pipeline. Files and subfolders observed: `Assessment_based_output`, `attack_stats_dir`, `attack_stats_dir_test`, `benign_stats_dir`, `benign_stats_dir_test`, `extract_metrics.py`, `Feature importance/`, `ML_based_output`, `ML_stats_best.py`, `ML_stats_test.py`, `run_combo.sh`, and `readme.txt`.

`benchmark/` (reported briefly) — Directory of RISC-V benchmark applications used for attack and benign workloads (place to find the code to run on the simulated RISC-V system). (If your repo uses a different name for the benchmark folder, adapt here.)

## Getting started (install & build gem5)

Begin in `Getting started/` and follow `gem5_guide1.pdf` first (installation). The minimal summary of required packages and a build command (from guide 1) is:

```bash
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev libboost-all-dev pkg-config python3-tk

git clone https://github.com/gem5/gem5.git
cd gem5/
scons build/RISCV/gem5.opt -j8
```

The three guide PDFs and `How_to_install_gem5` contain all details, troubleshooting tips, and additional dependencies. For general gem5 documentation see [https://www.gem5.org/](https://www.gem5.org/).

## What was modified in gem5 (overview)

We extended gem5 to support High-Precision Counters for Security (HPCS) and added detection hooks that allow creating and exporting new counters and metrics. The modified gem5 files relevant to the experiments are available under `RAVEN-main/gem5_config/` and include core pipeline and cache/commit/cpu files such as `base.cc/hh`, `cache.cc/hh`, `commit.cc/hh`, `cpu.cc/hh`, `isa.cc/hh`, and the `riscv-fs.py` full-system script. The `HPC/` subfolder contains the HPC-specific changes and helper code (for example `flush-fault.c` and `test_new.c`).

The repository includes `cpt.final8`, `riscv-64bit-csr.xml` and other configuration artifacts used by riscv full-system simulation.

## Reproducing the simulations (how to run)

This section explains the minimal steps to reproduce the attack and benign simulations and the detection pipeline. The exact script names and invocation parameters are provided inside the `Getting started` guides and the `gem5_config/` folder; use those if you need exact command line flags.

1. Build gem5 (see “Getting started” above) and ensure `build/RISCV/gem5.opt` exists.

2. Place or confirm the RAVEN repo on the same machine that built gem5 (paths in examples below assume `~/Downloads/RAVEN-main`).

3. Run the timed simulations used in the paper. All attack results are in `Attack Assessment/attack_simulations/`; the benign AES run is in `Attack Assessment/benign_simulation/aes/`. Each simulation in this study was executed for **2 seconds** of simulated time with data/dumps every **10¹¹ picoseconds**. The scripts and detailed per-simulation parameters are documented in `gem5_guide3.pdf` and in the `gem5_config/` folder.

4. The `riscv-fs.py` script in `gem5_config/` is the full-system runscript used to boot the RISC-V guest and launch the workloads. The `HPC/` subfolder contains example workloads used to exercise the modified counters and the flush/fault microbenchmarks. Use those scripts as the workload inputs to `riscv-fs.py` (see the guides for example invocations).

5. After each run, simulation statistics, HPCS dumps, and any runtime traces are written into the simulation result directories located under `Attack Assessment/attack_simulations/<attack_name>/` and `Attack Assessment/benign_simulation/aes/`. The `Figures/` directory contains the aggregated visualizations used in the paper.

Note: the repo provides the precomputed gem5 results in `Attack Assessment/` so you may use those directly if you do not wish to rerun the heavy simulations.

## Attack and benign workloads

The attack set used for assessment includes five attack applications. Their results are provided under:

`Attack Assessment/attack_simulations/est/`
`Attack Assessment/attack_simulations/et/`
`Attack Assessment/attack_simulations/flushfault/`
`Attack Assessment/attack_simulations/ghosttrace/`
`Attack Assessment/attack_simulations/spectre/`

The benign baseline is an AES encryption workload whose timed simulation results are under:

`Attack Assessment/benign_simulation/aes/`

Each folder contains the gem5 outputs (stats, traces, and any dumps) generated during the 2s timed simulations. See gem5 full script in folder gem5_config.

## Attack detection & ML pipeline

All scripts and folders for detection and ML are in `Attack Detection/`. The detection workflow used in the paper consisted of two stages: (1) metric extraction and selection for the suggested assessment metrics, and (2) building ML models to suggest metrics for attack classification. The directory contains scripts and outputs necessary to run this pipeline:

`extract_metrics.py` — extracts metrics from gem5 outputs into structured feature files.
`run_combo.sh` — orchestrates the pipeline (preprocessing, feature extraction, ML training/testing combinations).
`ML_stats_best.py`, `ML_stats_test.py` — scripts used to compute and evaluate ML statistics (accuracy, precision, recall, confusion matrices).
`Feature importance/` — feature importance outputs used to select the best subset of metrics.
`Assessment_based_output` and `ML_based_output` — contain the pipeline outputs for the two detection approaches.
`attack_stats_dir`, `attack_stats_dir_test`, `benign_stats_dir`, `benign_stats_dir_test` — structured directories containing the extracted stats used for training/testing.

To reproduce the detection experiments, run `run_combo.sh` inside `Attack Detection/`. The script calls `extract_metrics.py` and subsequently runs the ML scripts to produce the comparative statistics and the model outputs (the exact model hyperparameters and the train/test split are present inside `ML_stats_*` scripts and the `readme.txt` in the same folder).

## HPCS (High-Precision Counters) and how to inspect the modifications

The HPC implementation and example microbenchmarks are in `gem5_config/HPC/`. Key files that illustrate how custom counters were added are included (for example `flush-fault.c`, `test_new.c`, and the modified C++/header files inside `gem5_config/`). Use these files as a reference for adding any counters or detection hooks in your own gem5 builds.

## Expected outputs

After running the supplied pipeline or using the provided precomputed results, you should obtain:

* Per-simulation dumps in the attack and benign simulation folders under `Attack Assessment/`.
* Aggregated CSV/feature files used for ML in `Attack Detection/` (under `attack_stats_dir*` and `benign_stats_dir*`).
* ML performance summaries (accuracy, precision, recall, F1, confusion matrices) and feature importance plots in `Attack Detection/ML_based_output/` and `Feature importance/`.
* Attack Assessment Figures used in the paper in `Attack Assessment/Figures/`.


## Contact & citation

If you need help reproducing any part of the experiments, contact:

Mahreen Khan — PhD Researcher, Télécom Paris, IP Paris
Email: mahreen.khan@telecom-paris.fr

The experiments and modified gem5 code rely on the gem5 simulator; [https://www.gem5.org/].

