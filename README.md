# Q5-primes

**Prime values and consecutive-prime clusters of Q(n) = n⁵ − (n−1)⁵**

[![DOI](https://img.shields.io/badge/arXiv-2026.xxxxx-b31b1b.svg)](https://arxiv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository contains the source code, data, and analysis scripts accompanying the paper:

> R. Chen, *Prime values and consecutive-prime clusters of n⁵−(n−1)⁵: Computation, heuristics, and large probable prime generation*, 2026.

## Key Results

| Result | Value |
|--------|-------|
| Primes Q(n) for n ≤ 10⁸ | 5,179,467 |
| Bateman–Horn constant C_Q | 3.678113109 ± 3×10⁻⁹ |
| BH prediction error at N = 5×10⁷ | 0.009% |
| Maximum tuplet length | **6** (7-tuplets impossible) |
| Sextuplets found (n ≤ 1.9×10⁹) | 25 |
| 10,000-digit PRPs | 175 |
| 50,000-digit PRPs | 2 |
| 100,000-digit PRPs | 1 |
| **Proven prime (ECPP)** | **Q(10²⁴⁹⁹ + 3469), 9,997 digits** |

## Repository Structure

```
Q5-primes/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── .gitignore
│
├── paper/
│   ├── Q5_primes_paper.tex   # LaTeX source
│   └── Q5_primes_paper.pdf   # Compiled paper
│
├── src/
│   └── fast_sieve.cpp        # C++ modular sieve (Stage 1)
│
├── scripts/
│   ├── build_targets.py      # Python target constructor (Stage 2)
│   ├── compile.sh            # Linux build script
│   ├── compile.bat           # Windows build script
│   ├── run_pipeline.sh       # Linux pipeline runner
│   └── run_pipeline.bat      # Windows pipeline runner
│
├── data/
│   ├── README.md             # Data file descriptions
│   ├── pfgw/
│   │   ├── pfgw_10k_expressions.log  # 175 PRPs in expression form
│   │   ├── pfgw_10k_raw_values.log   # 42 PRPs as raw 9997-digit numbers
│   │   ├── pfgw_50k.log              # 2 PRPs (~50,000 digits)
│   │   └── pfgw_100k.log             # 1 PRP (~100,000 digits)
│   ├── tuplets/
│   │   └── 5-tuplets_6-tuplets.txt   # All 458 quintuplets and 25 sextuplets
│   └── ecpp/
│       └── primo-Q5_3469.cert        # ECPP certificate (Primo 4.3.3)
│
└── analysis/
    ├── analyze_primes.py     # Full statistical analysis pipeline
    └── requirements.txt      # Python dependencies
```

## The Polynomial

The quintic difference polynomial

$$Q(n) = n^5 - (n-1)^5 = 5n^4 - 10n^3 + 10n^2 - 5n + 1$$

has a remarkable arithmetic property: every prime factor of Q(n) satisfies p ≡ 1 (mod 5). This follows from its connection to the 5th cyclotomic polynomial Φ₅.

## Three-Stage Pipeline

### Stage 1: Modular Sieve (C++)

The sieve eliminates offsets i where Q(n₀ + i) has a small prime factor p ≡ 1 (mod 5).

**Build:**
```bash
# Linux/macOS
g++ -O3 -o fast_sieve src/fast_sieve.cpp -lm

# Windows
cl /O2 /EHsc src/fast_sieve.cpp
```

**Run:**
```bash
./fast_sieve    # Outputs survivor_offsets.txt
```

The sieve uses 128-bit arithmetic, runs to depth B = 10⁹ over R = 1,200,000 offsets, and completes in ~1 hour on a single core (AMD Ryzen 9 5950X).

### Stage 2: Target Construction (Python)

```bash
python scripts/build_targets.py    # Reads survivor_offsets.txt, writes pfgw_targets.txt
```

### Stage 3: PRP Testing (PFGW)

```bash
pfgw64 -t -h3 pfgw_targets.txt    # Fermat base-3 PRP test
```

## ECPP Certification

The smallest 10,000-digit PRP, Q(10²⁴⁹⁹ + 3469), has been rigorously certified prime using [Primo 4.3.3](https://www.ellipsa.eu/):

- **Wall-clock time:** 286,269 seconds (~3.3 days)
- **CPU time:** 3,753,821 seconds (~43.4 CPU-days)  
- **Certificate chain:** 887 steps
- **Certificate file:** [`data/ecpp/primo-Q5_3469.cert`](data/ecpp/primo-Q5_3469.cert)

The certificate can be independently verified using Primo's built-in verifier.

## Prime Data (Large Files)

The exhaustive prime tables for n ≤ 10⁸ (~200 MB compressed) are available separately:

- **Zenodo:** [DOI: 10.5281/zenodo.xxxxxxx](https://zenodo.org/) (4 CSV files, ~50 MB each)
- Each CSV contains columns `n, Q(n)` for all n where Q(n) is prime

To reproduce the analysis from the paper using the full dataset:
```bash
# Download from Zenodo and place in data/primes/
python analysis/analyze_primes.py --data-dir data/primes/
```

## Running the Analysis

```bash
cd analysis
pip install -r requirements.txt
python analyze_primes.py --data-dir ../data/primes/
```

This produces all statistics reported in the paper:
- π_Q(N) vs. Bateman–Horn prediction (Table 3)
- Gap distribution and normalized gaps (Tables 5–6)
- TVD and KL divergence for exponential vs. mod-11 model
- k-tuplet counts and Hardy–Littlewood predictions (Tables 7–8)
- Residue class uniformity (Table 4)

## Citation

```bibtex
@article{chen2026q5primes,
  author  = {Chen, Ruqing},
  title   = {Prime values and consecutive-prime clusters of {$n^5-(n-1)^5$}: 
             Computation, heuristics, and large probable prime generation},
  year    = {2026},
  note    = {Preprint, submitted to Mathematics of Computation}
}
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## Contact

Ruqing Chen — ruqing@hotmail.com  
GUT Geoservice Inc., Montréal, QC, Canada
