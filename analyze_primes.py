#!/usr/bin/env python3
"""
analyze_primes.py — Statistical analysis of Q(n) = n^5 - (n-1)^5 prime data.

Reproduces all tables and statistics in:
  R. Chen, "Prime values and consecutive-prime clusters of n^5-(n-1)^5"

Usage:
  python analyze_primes.py --data-dir ../data/primes/

Requires the four CSV files (primes_Q5_part_{1..4}.csv) in the data directory.
Download from Zenodo if not present locally.
"""

import argparse
import math
import bisect
from collections import Counter
from pathlib import Path


# ============================================================
# Constants
# ============================================================

C_Q = 3.678113109  # Bateman-Horn constant (9 significant digits)
SAFE_MOD11 = {0, 1, 2, 3, 6, 9, 10}
FORBIDDEN_MOD11 = {4, 5, 7, 8}


def load_n_values(data_dir: Path) -> list:
    """Load all n values from the four CSV files."""
    n_values = []
    for i in range(1, 5):
        fpath = data_dir / f"primes_Q5_part_{i}.csv"
        if not fpath.exists():
            raise FileNotFoundError(
                f"{fpath} not found. Download from Zenodo and place in {data_dir}/"
            )
        print(f"  Loading {fpath.name}...")
        with open(fpath) as f:
            header = f.readline()
            for line in f:
                line = line.strip()
                if line:
                    n = int(line.split(",")[0])
                    n_values.append(n)
    n_values.sort()
    return n_values


def bateman_horn_integral(N: float, steps: int = 200000) -> float:
    """Compute ∫_2^N dt / ln(Q(t)) where Q(t) = 5t^4 - 10t^3 + 10t^2 - 5t + 1."""
    if N <= 2:
        return 0.0
    h = (math.log(N) - math.log(2)) / steps
    total = 0.0
    for i in range(steps):
        t = 2 * math.exp((i + 0.5) * h)
        dt = 2 * math.exp((i + 1) * h) - 2 * math.exp(i * h)
        Q = 5 * t**4 - 10 * t**3 + 10 * t**2 - 5 * t + 1
        if Q > 1:
            total += dt / math.log(Q)
    return total


def weight_mod11(g: int) -> float:
    """Transition weight w(g) = fraction of safe residues r where r+g is also safe."""
    return sum(1 for r in SAFE_MOD11 if (r + g) % 11 in SAFE_MOD11) / 7.0


# ============================================================
# Table 3: π_Q(N) vs Bateman-Horn prediction
# ============================================================

def table3_bateman_horn(n_values: list):
    print("\n" + "=" * 70)
    print("TABLE 3: π_Q(N) vs Bateman-Horn prediction (C_Q = {:.9f})".format(C_Q))
    print("=" * 70)

    milestones = [
        1e3, 1e4, 1e5, 1e6, 2e6, 5e6, 1e7, 2e7, 5e7,
    ]

    print(f"{'N':>12} | {'π_Q(N)':>10} | {'C_Q·∫dt/lnQ':>14} | {'Ratio':>8}")
    print("-" * 55)
    for m in milestones:
        count = bisect.bisect_right(n_values, int(m))
        integral = bateman_horn_integral(m)
        pred = C_Q * integral
        ratio = count / pred if pred > 0 else 0
        print(f"{m:>12,.0f} | {count:>10,} | {pred:>14,.1f} | {ratio:>8.4f}")


# ============================================================
# Table 4: Residue class uniformity mod 11
# ============================================================

def table4_residue_uniformity(n_values: list):
    print("\n" + "=" * 70)
    print("TABLE 4: Distribution of n (mod 11)")
    print("=" * 70)

    mod11_counts = Counter(n % 11 for n in n_values)
    total = len(n_values)
    expected = total / 7

    for r in range(11):
        c = mod11_counts.get(r, 0)
        status = "root" if r in FORBIDDEN_MOD11 else "safe"
        dev = abs(c - expected) / expected * 100 if status == "safe" else 0
        print(f"  n ≡ {r:>2} (mod 11): {c:>10,}  [{status}]  dev={dev:.2f}%")
    print(f"  Expected per safe class: {expected:,.0f}")


# ============================================================
# Tables 5-6: Gap distribution
# ============================================================

def tables5_6_gap_analysis(n_values: list):
    total = len(n_values)
    gaps = [n_values[i + 1] - n_values[i] for i in range(total - 1)]

    print("\n" + "=" * 70)
    print("TABLE 5: Raw gap frequencies")
    print("=" * 70)
    print(f"Total gaps: {len(gaps):,}")
    print(f"Mean gap: {sum(gaps)/len(gaps):.2f}")
    print(f"Max gap: {max(gaps)}")

    gap_counter = Counter(gaps)
    print(f"\n{'Gap':>5} | {'Count':>10} | {'Freq':>7}")
    print("-" * 30)
    for g in list(range(1, 12)) + [22]:
        c = gap_counter.get(g, 0)
        print(f"{g:>5} | {c:>10,} | {c/len(gaps)*100:>6.2f}%")

    # Normalized gaps
    print("\n" + "=" * 70)
    print("TABLE 6: Normalized gap distribution")
    print("=" * 70)

    bins = [
        (0, 0.25), (0.25, 0.50), (0.50, 0.75), (0.75, 1.00),
        (1.00, 1.50), (1.50, 2.00), (2.00, 3.00), (3.00, 4.00),
        (4.00, 6.00), (6.00, float("inf")),
    ]

    normalized = []
    for i in range(len(gaps)):
        n = n_values[i]
        if n > 100:
            E = 4 * math.log(n) / C_Q
            normalized.append(gaps[i] / E)

    observed = [0] * len(bins)
    for g in normalized:
        for j, (a, b) in enumerate(bins):
            if a <= g < b:
                observed[j] += 1
                break

    N_total = sum(observed)
    E_avg = sum(gaps) / len(gaps)

    def exp_prob(a, b):
        return math.exp(-a) if b == float("inf") else math.exp(-a) - math.exp(-b)

    def mod11_prob(a, b, E=E_avg, max_g=600):
        g_min = max(1, int(math.ceil(a * E)))
        g_max = int(math.floor(b * E)) if b < 100 else max_g
        return sum(weight_mod11(g) * math.exp(-g / E) / E for g in range(g_min, g_max + 1))

    mod11_raw = [mod11_prob(a, b) for a, b in bins]
    Z = sum(mod11_raw)
    mod11_norm = [p / Z for p in mod11_raw]

    print(f"{'Bin':>15} | {'Observed':>10} | {'Frac':>6} | {'Exp':>6} | {'Mod-11':>6}")
    print("-" * 60)
    for j, (a, b) in enumerate(bins):
        label = f"[{a:.2f}, {'inf' if b == float('inf') else f'{b:.2f}'})"
        frac = observed[j] / N_total
        ep = exp_prob(a, b)
        mp = mod11_norm[j]
        print(f"{label:>15} | {observed[j]:>10,} | {frac:>6.3f} | {ep:>6.3f} | {mp:>6.3f}")

    # Effect-size metrics
    obs_frac = [o / N_total for o in observed]
    exp_frac = [exp_prob(a, b) for a, b in bins]

    tvd_exp = 0.5 * sum(abs(o - e) for o, e in zip(obs_frac, exp_frac))
    tvd_mod = 0.5 * sum(abs(o - m) for o, m in zip(obs_frac, mod11_norm))
    kl_exp = sum(o * math.log(o / e) for o, e in zip(obs_frac, exp_frac) if o > 0)
    kl_mod = sum(o * math.log(o / m) for o, m in zip(obs_frac, mod11_norm) if o > 0)

    print(f"\nEffect-size metrics:")
    print(f"  TVD (exponential): {tvd_exp:.4f}")
    print(f"  TVD (mod-11):      {tvd_mod:.4f}  (improvement: {tvd_exp/tvd_mod:.1f}×)")
    print(f"  KL  (exponential): {kl_exp:.6f}")
    print(f"  KL  (mod-11):      {kl_mod:.6f}  (improvement: {kl_exp/kl_mod:.1f}×)")


# ============================================================
# Tables 7-8: k-tuplet counts and Hardy-Littlewood heuristics
# ============================================================

def tables7_8_tuplets(n_values: list):
    print("\n" + "=" * 70)
    print("TABLES 7-8: k-tuplet analysis")
    print("=" * 70)

    n_set = set(n_values)
    total = len(n_values)

    # Find maximal runs
    runs = []
    start = n_values[0]
    length = 1
    for i in range(1, total):
        if n_values[i] == n_values[i - 1] + 1:
            length += 1
        else:
            if length >= 2:
                runs.append((start, length))
            start = n_values[i]
            length = 1
    if length >= 2:
        runs.append((start, length))

    run_counts = Counter(r[1] for r in runs)

    print("\nMaximal run counts:")
    print(f"{'k':>5} | {'Count':>10} | {'Smallest n':>15}")
    print("-" * 40)
    for k in sorted(run_counts.keys()):
        example = min(r[0] for r in runs if r[1] == k)
        print(f"{k:>5} | {run_counts[k]:>10,} | {example:>15,}")

    # Overlapping counts
    print("\nOverlapping counts T_k:")
    for target_k in [2, 3, 4, 5, 6]:
        count = sum(max(0, length - target_k + 1) for _, length in runs)
        print(f"  T_{target_k} = {count:,}")

    # Singular series computation (using primes up to 5000)
    print("\nHardy-Littlewood singular series (primes ≤ 5000):")
    sieve_lim = 5000
    is_prime = [True] * (sieve_lim + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sieve_lim**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, sieve_lim + 1, i):
                is_prime[j] = False

    def roots_mod_p(p):
        return [n for n in range(p) if (pow(n, 5, p) - pow((n - 1) % p, 5, p)) % p == 0]

    def safe_starts(p, roots, k):
        root_set = set(roots)
        return sum(
            1 for n in range(p) if all((n + j) % p not in root_set for j in range(k))
        )

    N = n_values[-1]
    for k in [2, 3, 4, 5, 6]:
        S = 1.0
        for p in range(2, sieve_lim + 1):
            if not is_prime[p]:
                continue
            roots = roots_mod_p(p)
            safe = safe_starts(p, roots, k)
            omega_k = p - safe
            factor = (1 - omega_k / p) / (1 - 1 / p) ** k
            S *= factor

        # Integral
        h = (math.log(N) - math.log(2)) / 200000
        integral = 0
        for i in range(200000):
            t = 2 * math.exp((i + 0.5) * h)
            dt = 2 * math.exp((i + 1) * h) - 2 * math.exp(i * h)
            Q = 5 * t**4 - 10 * t**3 + 10 * t**2 - 5 * t + 1
            if Q > 1:
                integral += dt / math.log(Q) ** k

        predicted = S * integral
        overlap = sum(max(0, length - k + 1) for _, length in runs)
        print(f"  k={k}: S_k={S:>12.4f}, predicted={predicted:>10.1f}, observed={overlap:>8}")


# ============================================================
# Euler product convergence (Table 2)
# ============================================================

def table2_euler_product():
    print("\n" + "=" * 70)
    print("TABLE 2: Bateman-Horn constant convergence")
    print("=" * 70)

    SIEVE_LIM = 10_000_000
    is_prime = bytearray([1]) * (SIEVE_LIM + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(SIEVE_LIM**0.5) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = bytearray(len(is_prime[i * i :: i]))

    C = 1.0
    checkpoints = [10**k for k in range(2, 8)]
    cp_idx = 0

    for p in range(2, SIEVE_LIM + 1):
        if not is_prime[p]:
            continue
        if p == 5:
            C *= 5.0 / 4.0
        elif p % 5 == 1:
            C *= (1 - 4.0 / p) / (1 - 1.0 / p)
        else:
            C *= 1.0 / (1 - 1.0 / p)

        if cp_idx < len(checkpoints) and p >= checkpoints[cp_idx]:
            print(f"  C_Q (p ≤ {checkpoints[cp_idx]:>10,}) = {C:.10f}")
            cp_idx += 1


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Q(n)=n^5-(n-1)^5 prime data"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("../data/primes"),
        help="Directory containing primes_Q5_part_{1..4}.csv",
    )
    parser.add_argument(
        "--skip-data",
        action="store_true",
        help="Skip analyses requiring the large CSV files (run Table 2 only)",
    )
    args = parser.parse_args()

    print("Q5-primes analysis pipeline")
    print("=" * 70)

    # Table 2 (no data files needed)
    table2_euler_product()

    if args.skip_data:
        print("\n[--skip-data] Skipping data-dependent analyses.")
        return

    print("\nLoading prime data...")
    n_values = load_n_values(args.data_dir)
    print(f"Loaded {len(n_values):,} primes, range [{n_values[0]}, {n_values[-1]}]")

    table3_bateman_horn(n_values)
    table4_residue_uniformity(n_values)
    tables5_6_gap_analysis(n_values)
    tables7_8_tuplets(n_values)

    print("\n" + "=" * 70)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
