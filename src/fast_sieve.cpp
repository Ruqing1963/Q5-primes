#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <chrono>

typedef unsigned long long uint64;

// Fast Modular Exponentiation: (base^exp) % mod
uint64 power(uint64 base, uint64 exp, uint64 mod) {
    uint64 res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) res = (__int128)res * base % mod;
        base = (__int128)base * base % mod;
        exp /= 2;
    }
    return res;
}

// Modular Multiplicative Inverse (Extended Euclidean Algorithm)
uint64 modInverse(uint64 n, uint64 m) {
    long long m0 = m, t, q;
    long long x0 = 0, x1 = 1;
    if (m == 1) return 0;
    while (n > 1) {
        q = n / m;
        t = m;
        m = n % m, n = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }
    return (x1 < 0) ? x1 + m0 : x1;
}

// Calculate modulo of a giant string for the starting offset
uint64 mod_large_string(const std::string& num_str, uint64 p) {
    uint64 res = 0;
    for (char c : num_str) {
        res = (res * 10 + (c - '0')) % p;
    }
    return res;
}

int main() {
    // --- DIAMOND-GRADE PARAMETERS ---
    // Start point for n (2500 digits for a 10,000-digit Q(n))
    std::string base_n_str = "1" + std::string(2499, '0'); 
    
    // Search range: 200,000 points
    uint64 search_range = 200000; 
    
    // Ultra-deep sieve: 1 Billion (10^9)
    uint64 p_max = 1000000000;       
    
    auto start_time = std::chrono::high_resolution_clock::now();

    std::cout << "[1/4] Crushing: Generating Prime Table up to 1B (bitset)..." << std::endl;
    std::vector<bool> is_p(p_max + 1, true);
    is_p[0] = is_p[1] = false;
    for (uint64 p = 2; p * p <= p_max; p++) {
        if (is_p[p]) {
            for (uint64 i = p * p; i <= p_max; i += p) is_p[i] = false;
        }
    }

    std::cout << "[2/4] Initializing High-Grade Flotation Array..." << std::endl;
    std::vector<uint8_t> is_composite(search_range, 0);

    std::cout << "[3/4] Deep Chemical Extraction (p_max = 1B)..." << std::endl;
    uint64 active_agents = 0;

    for (uint64 p = 11; p <= p_max; p++) {
        if (!is_p[p] || p % 5 != 1) continue;

        active_agents++;
        uint64 s_mod = mod_large_string(base_n_str, p);

        uint64 g = 0;
        for (uint64 a = 2; a < p; a++) {
            uint64 r = power(a, (p - 1) / 5, p);
            if (r != 1) { g = r; break; }
        }

        uint64 roots[4];
        roots[0] = g;
        roots[1] = (__int128)g * g % p;
        roots[2] = (__int128)roots[1] * g % p;
        roots[3] = (__int128)roots[2] * g % p;

        for (int j = 0; j < 4; j++) {
            uint64 x = roots[j];
            uint64 x_minus_1_inv = modInverse((p + x - 1) % p, p);
            uint64 n_target = (__int128)x * x_minus_1_inv % p;
            
            uint64 first_i = (p + n_target - s_mod) % p;
            for (uint64 i = first_i; i < search_range; i += p) {
                is_composite[i] = 1;
            }
        }
        
        if (active_agents % 1000000 == 0) 
            std::cout << "  > Applied " << active_agents << " Million agents..." << std::endl;
    }

    std::cout << "[4/4] Collecting Diamond-Grade Survivors..." << std::endl;
    std::ofstream out_file("survivor_offsets.txt");
    uint64 count = 0;
    for (uint64 i = 0; i < search_range; ++i) {
        if (is_composite[i] == 0) {
            out_file << i << "\n";
            count++;
        }
    }
    out_file.close();

    auto end_time = std::chrono::high_resolution_clock::now();
    std::cout << "----------------------------------------\n";
    std::cout << "Extraction Depth : " << p_max << "\n";
    std::cout << "Survivors Found  : " << count << " (Ready for PFGW)\n";
    std::cout << "Total Sieve Time : " << std::chrono::duration<double>(end_time - start_time).count() << "s\n";
    std::cout << "----------------------------------------\n";

    return 0;
}
