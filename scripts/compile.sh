#!/bin/bash
# Compile the C++ modular sieve for Q(n) = n^5 - (n-1)^5
# Requires: g++ with C++17 support and 128-bit integer support

set -e

SRCDIR="$(cd "$(dirname "$0")/../src" && pwd)"
OUTDIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Compiling fast_sieve.cpp..."
g++ -O3 -std=c++17 -march=native -o "${OUTDIR}/fast_sieve" "${SRCDIR}/fast_sieve.cpp" -lm

echo "Build successful: ${OUTDIR}/fast_sieve"
echo ""
echo "Usage: ./fast_sieve"
echo "  Generates survivor_offsets.txt in the current directory"
echo "  Sieve depth: B = 10^9, Range: R = 1,200,000 offsets"
echo "  Expected runtime: ~1 hour on a modern CPU"
