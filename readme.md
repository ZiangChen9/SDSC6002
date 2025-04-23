# Code for Bayesian Optimization for Noisy Black-box Functions: A Comparative Study Using BoTorch

## Project Overview
This repository contains a comprehensive benchmark study of Bayesian optimization methods applied to standard test functions. The project implements and evaluates multiple acquisition functions and Gaussian Process configurations, with complete experimental pipelines from data collection to statistical analysis.

## Repository Structure
```
.
├── DataCollection/                           # Core optimization implementations
│   ├── Ackley/                               # Complete Ackley function study
│   │   ├── qKG/                              # Knowledge Gradient
│   │   ├──── ConstantMean/                     # Constant mean variants
│   │   │   ├──── Matern(1.5).ipynb            # Matern 1.5 kernel
│   │   │   ├──── Matern(2.5).ipynb            # Matern 2.5 kernel
│   │   │   ├──── RBF.ipynb                     # Standard RBF
│   │   ├──── 3 mean functions/                 # Constant/Linear/Quadratic
│   │   ├── 7 other acquisition functions/    # qLBMVE, qPES, etc.
│   │   └── move_csv.py                   # Results management
│   ├── Bohachevsky/                          # Other benchmark functions
│   ├── Booth/
│   └── ......
│
├── results-Ackley/                           # Complete Ackley results
│   ├── final/                                # Final processed results
│   ├── plots/                                # Visualization outputs
│   ├── processed_data/                       # Intermediate processed data
│   ├── raw_data/                             # Raw experimental outputs
│   ├── statistic_show/                       # Statistical reports
│   ├── datacollection.py                     # Data collection script
│   ├── final-plot.py                         # Final plotting script
│   ├── process_data.py                       # Data processing pipeline
│   ├── result_show.py                        # Results visualization
│   ├── statistic_show_all.py                 # Comprehensive stats
│   └── statistic_show.py                     # Basic statistics
│
├── results-Bohachevsky/                      # Other functions' results
├── results-Booth/
├── results-Easom/
├── results-Hump Camel/
│
├── Appendix/                                 # Supplementary analyses
└── 6002data.pdf                              # Master statistical report
```

## Key Components

### 1. DataCollection
Core implementation of Bayesian optimization algorithms:

**Ackley Function Study:**
- 8 acquisition functions (qKG, qUCB, qPES, etc.)
- 3 mean function types (Constant, Linear, Quadratic)
- 3 kernel implementations (Matern 1.5/2.5, RBF)
- Thompson Sampling with management utilities

**Other Benchmark Functions:**
- Bohachevsky, Booth, Easom, Three Hump Camel implementations

### 2. Results Pipeline (Ackley Example)
Complete experimental workflow:
1. `datacollection.py` - Runs optimization experiments
2. `raw_data/` - Stores initial outputs
3. `process_data.py` - Processes into `processed_data/`
4. `result_show.py` - Generates `plots/`
5. `statistic_show*.py` - Produces `statistic_show/` reports
6. `final-plot.py` - Creates publication-ready `final/` outputs

### 3. Statistical Analysis
- Individual function statistics in each results directory
- Comprehensive cross-method analysis in 6002data.pdf
- Appendix with special case studies

## Usage Instructions

**Running Experiments:**
```bash
cd DataCollection/Ackley/ConstantMean/
jupyter notebook Matern(1.5).ipynb  # Run specific configuration
```

**Processing Results:**
```bash
cd results-Ackley/
python process_data.py              # Process raw data
python result_show.py              # Generate plots
python statistic_show_all.py       # Full statistical analysis
```

**Viewing Outputs:**
- Check `plots/` directory for visualizations
- Examine `statistic_show/` for numerical results
- Consult 6002data.pdf for comparative analysis

## Dependencies
- Python 3.10+
- NumPy, SciPy
- Matplotlib
- PyTorch/GPyTorch/BoTorch
- Jupyter Notebook
- Pandas for data analysis
- tqdm for progress bars
