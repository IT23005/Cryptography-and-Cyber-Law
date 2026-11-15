"""
Number Theory Foundations for Cryptography
Author: Mahfuzur Rahman (ID: IT-23005)
Course: Cryptography and Cyber Law
Workshop Ref: https://github.com/mnp-club/Number_Theory_and_Cryptography_Workshop
"""

import math
from typing import Tuple, List, Optional


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Computes gcd(a, b) and Bezout coefficients (x, y) such that:
        gcd(a, b) = a * x + b * y
    Requires: a >= b and b >= 0 and a + b > 0.
    Complexity: O(log(min(a, b)))
    """
    assert a >= b and b >= 0 and a + b > 0, "Invalid inputs for extended_gcd"
    
    if b == 0:
        return (a, 1, 0)
    
    d, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    assert a % d == 0 and b % d == 0
    assert d == a * x + b * y
    return (d, x, y)


def lcm(a: int, b: int) -> int:
    """
    Computes the Least Common Multiple (LCM) of two positive integers.
    Uses the identity: a * b = gcd(a, b) * lcm(a, b)
    """
    assert a > 0 and b > 0, "Inputs must be positive integers"
    g = extended_gcd(max(a, b), min(a, b))[0]
    return (a * b) // g


def diophantine(a: int, b: int, c: int) -> Tuple[int, int]:
    """
    Finds a particular integer solution (x, y) to the linear Diophantine equation:
        a * x + b * y = c
    A solution exists if and only if gcd(a, b) divides c.
    """
    assert a > 0 and b > 0, "Coefficients a and b must be positive"
    
    swapped = False
    if a < b:
        a_orig, b_orig = a, b
        a_val, b_val = b, a
        swapped = True
    else:
        a_orig, b_orig = a, b
        a_val, b_val = a, b
        
    gcd_val, x0, y0 = extended_gcd(a_val, b_val)
    assert c % gcd_val == 0, f"No integer solution exists: gcd({a_orig}, {b_orig}) = {gcd_val} does not divide {c}"
    
    factor = c // gcd_val
    x0 *= factor
    y0 *= factor
    
    if swapped:
        x, y = y0, x0
    else:
        x, y = x0, y0
        
    assert a_orig * x + b_orig * y == c, "Diophantine solution verification failed"
    return (x, y)


def modInverse(a: int, n: int) -> int:
    """
    Calculates the multiplicative inverse of a modulo n:
        a * x = 1 (mod n)
    Requires gcd(a, n) == 1 and n > 1.
    """
    assert n > 1, "Modulus n must be greater than 1"
    a_reduced = a % n
    assert a_reduced > 0, "a cannot be divisible by n"
    
    if a_reduced >= n:
        d, x, y = extended_gcd(a_reduced, n)
        inv = x % n
    else:
        d, x, y = extended_gcd(n, a_reduced)
        inv = y % n
        
    assert d == 1, f"Modular inverse does not exist: gcd({a}, {n}) = {d} != 1"
    return (inv + n) % n


def divide(b: int, a: int, n: int) -> int:
    """
    Computes modular division b / a mod n, i.e., finds x in [0, n-1] such that:
        a * x = b (mod n)
    Requires gcd(a, n) == 1 and n > 1.
    """
    assert n > 1 and a > 0
    a_inv = modInverse(a, n)
    assert (a * a_inv) % n == 1
    return (a_inv * b) % n


def FastModularExponentiation(b: int, e: int, m: int) -> int:
    """
    Computes (b^e) mod m using the Square-and-Multiply algorithm.
    Takes ~ 2 * log2(e) modular multiplications.
    """
    assert m > 0, "Modulus m must be positive"
    result = 1
    base = b % m
    exp = e
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % m
        base = (base * base) % m
        exp //= 2
    return result


def ChineseRemainderTheorem(n1: int, r1: int, n2: int, r2: int) -> int:
    """
    Constructs the unique integer r modulo (n1 * n2) such that:
        r = r1 (mod n1)
        r = r2 (mod n2)
    Requires: gcd(n1, n2) == 1, 0 <= r1 < n1, 0 <= r2 < n2.
    """
    assert n1 > 0 and n2 > 0
    swapped = False
    if n1 < n2:
        d, x, y = extended_gcd(n2, n1)
        # n2 * x + n1 * y = 1 => n1 * y = 1 mod n2, n2 * x = 1 mod n1
        swapped = True
    else:
        d, x, y = extended_gcd(n1, n2)
        # n1 * x + n2 * y = 1 => n2 * y = 1 mod n1, n1 * x = 1 mod n2
        
    assert d == 1, f"Moduli must be coprime: gcd({n1}, {n2}) = {d}"
    
    N = n1 * n2
    if swapped:
        r = (r2 * n1 * y + r1 * n2 * x) % N
    else:
        r = (r1 * n2 * y + r2 * n1 * x) % N
        
    r = (r + N) % N
    assert r % n1 == r1
    assert r % n2 == r2
    return r


# Day 2 Theoretical Helpers: Repunits, Perfect Numbers, Pseudoprimes

def repunit(n: int) -> int:
    """Generates the n-th Repunit R_n = 111...1 (n digits) = (10^n - 1) / 9."""
    assert n >= 1
    return (10**n - 1) // 9


def is_even_perfect_number(n: int) -> Tuple[bool, Optional[int]]:
    """
    Checks if n is an even perfect number by Euclid-Euler theorem:
    n = 2^(p-1) * (2^p - 1), where (2^p - 1) is a Mersenne prime.
    """
    if n <= 0 or n % 2 != 0:
        return False, None
    # Extract powers of 2
    p_minus_1 = 0
    temp = n
    while temp % 2 == 0:
        temp //= 2
        p_minus_1 += 1
    p = p_minus_1 + 1
    mersenne_candidate = temp
    if mersenne_candidate == (1 << p) - 1:
        # Check if mersenne_candidate is prime
        m = mersenne_candidate
        if m < 2:
            return False, None
        for i in range(2, int(math.isqrt(m)) + 1):
            if m % i == 0:
                return False, None
        return True, p
    return False, None


def is_fermat_pseudoprime(n: int, base: int = 2) -> bool:
    """
    Checks whether composite n is a Fermat pseudoprime to base a:
    composite n > 1 and a^(n-1) == 1 (mod n) with gcd(a, n) == 1.
    """
    if n < 4:
        return False
    # Check if composite
    is_composite = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            is_composite = True
            break
    if not is_composite:
        return False
    if math.gcd(base, n) != 1:
        return False
    return FastModularExponentiation(base, n - 1, n) == 1
