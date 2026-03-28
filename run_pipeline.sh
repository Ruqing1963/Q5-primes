#!/bin/bash
# Full pipeline for generating large probable primes of the form Q(n) = n^5 - (n-1)^5
#
# Prerequisites:
#   - fast_sieve compiled (run scripts/compile.sh first)
#   - Python 3.8+ with mpmath
#   - PFGW (pfgw64) in PATH
#
# The pipeline has three stages:
#   Stage 1: C++ modular sieve → survivor_offsets.txt
#   Stage 2: Python target builder → pfgw_targets.txt
#   Stage 3: PFGW PRP testing → results on stdout

set -e

BASEDIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "============================================"
echo "Q5-primes: Large Prime Generation Pipeline"
echo "============================================"
echo ""

# Stage 1: Sieve
echo "[Stage 1] Running modular sieve (C++)..."
echo "  This may take ~1 hour."
cd "${BASEDIR}"
./fast_sieve
SURVIVORS=$(wc -l < survivor_offsets.txt)
echo "  Done. ${SURVIVORS} survivors written to survivor_offsets.txt"
echo ""

# Stage 2: Build targets
echo "[Stage 2] Building PFGW targets (Python)..."
python3 scripts/build_targets.py
TARGETS=$(wc -l < pfgw_targets.txt)
echo "  Done. ${TARGETS} targets written to pfgw_targets.txt"
echo ""

# Stage 3: PRP testing
echo "[Stage 3] Running PFGW probable-prime tests..."
echo "  Each 10,000-digit test takes ~30 seconds."
if command -v pfgw64 &> /dev/null; then
    pfgw64 -t -h3 pfgw_targets.txt | tee pfgw_results.log
    echo ""
    echo "Results saved to pfgw_results.log"
else
    echo "  WARNING: pfgw64 not found in PATH."
    echo "  Download PFGW from: https://sourceforge.net/projects/openpfgw/"
    echo "  Then run: pfgw64 -t -h3 pfgw_targets.txt"
fi

echo ""
echo "Pipeline complete."
