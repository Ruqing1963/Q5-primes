# Data Files

## `pfgw/` — Probable Prime Results

| File | Description | Count |
|------|-------------|-------|
| `pfgw_10k_expressions.log` | All 175 PRPs with ~10,000 digits in PFGW expression form `(10^2499+k)^5-(10^2499+k-1)^5` | 133 entries (offsets 203,823–1,162,743) |
| `pfgw_10k_raw_values.log` | Additional PRPs as raw 9,997-digit decimal numbers | 42 entries (offsets 3,469–190,434) |
| `pfgw_50k.log` | Two ~50,000-digit PRPs: offsets 5,730 and 29,658 from base 10^12499 | 2 |
| `pfgw_100k.log` | One ~100,000-digit PRP: offset 25,098 from base 10^24999 | 1 |

**Combined unique 10k-digit PRPs:** 175 (42 + 133, zero overlap)

The 42 raw-value entries correspond to offsets:
3469, 6073, 14791, 15367, 20398, 26943, 44759, 48337, 49436, 50368,
60716, 61899, 64870, 65769, 71174, 73025, 87603, 88183, 91080, 93129,
94912, 100905, 105403, 106459, 106520, 109353, 115504, 117292, 131871,
135981, 137534, 138028, 139571, 142308, 155852, 156578, 162669, 179711,
182412, 185742, 187007, 190434

## `tuplets/` — Prime Tuplet Data

| File | Description |
|------|-------------|
| `5-tuplets_6-tuplets.txt` | All 458 quintuplets and 25 sextuplets for n ≤ 1.9×10⁹ |

## `ecpp/` — Primality Certificate

| File | Description |
|------|-------------|
| `primo-Q5_3469.cert` | ECPP certificate proving Q(10²⁴⁹⁹ + 3469) is prime |

**Certificate details:**
- Software: Primo 4.3.3 (LX64)
- Status: **Candidate certified prime**
- Number: (10^2499+3469)^5 - (10^2499+3468)^5
- Decimal size: 9,997 digits
- Certificate chain: 887 steps
- Wall-clock time: 286,269 seconds (~3.3 days)
- Total CPU time: 3,753,821 seconds (~43.4 CPU-days)

## `primes/` — Exhaustive Prime Tables (NOT included in Git)

The four CSV files containing all 5,179,467 primes Q(n) for n ≤ 10⁸ are too large
for GitHub (~50 MB each, ~200 MB total compressed). They are hosted on Zenodo:

**Zenodo DOI:** [10.5281/zenodo.xxxxxxx](https://zenodo.org/)

| File | Range | Primes | Size |
|------|-------|--------|------|
| `primes_Q5_part_1.csv` | n = 2 to ~22.9M | 1,294,867 | ~50 MB |
| `primes_Q5_part_2.csv` | n = ~22.9M to ~47.9M | 1,294,868 | ~55 MB |
| `primes_Q5_part_3.csv` | n = ~47.9M to ~73.7M | 1,294,868 | ~56 MB |
| `primes_Q5_part_4.csv` | n = ~73.7M to 10⁸ | 1,294,867 | ~57 MB |

Each CSV has columns: `n, Q(n)` with header row.

To download and place:
```bash
mkdir -p data/primes
# Download from Zenodo and unzip into data/primes/
```
