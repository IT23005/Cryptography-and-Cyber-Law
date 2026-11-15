"""
RSA Cryptanalysis & Vulnerability Exploitations
Author: Mahfuzur Rahman (ID: IT-23005)
Course: Cryptography and Cyber Law
Workshop Ref: https://github.com/mnp-club/Number_Theory_and_Cryptography_Workshop
"""

import math
from typing import List, Tuple
from cryptosystems import Encrypt, Decrypt, ConvertToStr, ExtendedEuclid, InvertModulo


def IntSqrt(n: int) -> int:
    """
    Computes floor(sqrt(n)) using binary search.
    Handles arbitrarily large integers without precision loss.
    """
    if n < 0:
        raise ValueError("Cannot take square root of negative integer")
    if n == 0:
        return 0
    low = 1
    high = n
    ans = 1
    while low <= high:
        mid = (low + high) // 2
        if mid * mid <= n:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    return ans


def GCD(a: int, b: int) -> int:
    """Euclidean greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


# -------------------------------------------------------------
# Attack 1: Known-Plaintext / Dictionary Attack on Small Message Space
# -------------------------------------------------------------

def DecipherSimple(ciphertext: int, modulo: int, exponent: int, potential_messages: List[str]) -> str:
    """
    When RSA is used without randomized padding (textbook RSA) and the message
    comes from a small predictable set (e.g., 'attack', 'wait', 'retreat'),
    an attacker encrypts all candidates with the public key and checks for a match.
    """
    for msg in potential_messages:
        if Encrypt(msg, modulo, exponent) == ciphertext:
            return msg
    return "don't know"


# -------------------------------------------------------------
# Attack 2: Small Prime Factorization Attack (p < 1,000,000)
# -------------------------------------------------------------

def DecipherSmallPrime(ciphertext: int, modulo: int, exponent: int, search_bound: int = 1000000) -> str:
    """
    If one of the prime factors of N = p * q is small (p < search_bound),
    trial division rapidly factors N, computing d and decrypting C.
    """
    found_p = None
    # 2 is the only even prime
    if modulo % 2 == 0:
        found_p = 2
    else:
        for i in range(3, search_bound, 2):
            if modulo % i == 0:
                found_p = i
                break
                
    assert found_p is not None, f"Prime factor below {search_bound} not found"
    q = modulo // found_p
    return Decrypt(ciphertext, found_p, q, exponent)


# -------------------------------------------------------------
# Attack 3: Fermat's Factorization Attack (|p - q| is Small)
# -------------------------------------------------------------

def DecipherSmallDiff(ciphertext: int, modulo: int, exponent: int, max_steps: int = 50000) -> str:
    """
    Fermat's Factorization Method breaks RSA when |p - q| is small:
        N = a^2 - b^2 = (a - b)(a + b)
    where a = (p + q) / 2 and b = |p - q| / 2.
    Starting from a0 = ceil(sqrt(N)), iterating a quickly finds integer b.
    """
    a = IntSqrt(modulo)
    if a * a < modulo:
        a += 1
        
    for step in range(max_steps):
        t2 = a * a - modulo
        b = IntSqrt(t2)
        if b * b == t2:
            p = a - b
            q = a + b
            assert p * q == modulo, "Fermat factor product check failed"
            return Decrypt(ciphertext, p, q, exponent)
        a += 1
        
    raise ValueError(f"Fermat factorization failed within {max_steps} iterations")


# -------------------------------------------------------------
# Attack 4: Shared Prime Factor / Common Modulus Attack
# -------------------------------------------------------------

def DecipherCommonDivisor(first_ciphertext: int, first_modulo: int, first_exponent: int,
                           second_ciphertext: int, second_modulo: int, second_exponent: int) -> Tuple[str, str]:
    """
    If two independent RSA key pairs share a common prime p (due to poor RNG or collision):
        N1 = p * q1  and  N2 = p * q2
    Then gcd(N1, N2) = p instantly in logarithmic time, factoring both keys!
    """
    common_p = GCD(first_modulo, second_modulo)
    assert common_p > 1, "Moduli are coprime; no shared factor exists"
    
    q1 = first_modulo // common_p
    q2 = second_modulo // common_p
    
    msg1 = Decrypt(first_ciphertext, common_p, q1, first_exponent)
    msg2 = Decrypt(second_ciphertext, common_p, q2, second_exponent)
    return (msg1, msg2)


# -------------------------------------------------------------
# Attack 5: Håstad's Broadcast Attack via Chinese Remainder Theorem
# -------------------------------------------------------------

def ChineseRemainderTheoremHelper(n1: int, r1: int, n2: int, r2: int) -> int:
    """Reconstructs r modulo n1*n2 using Extended Euclidean Algorithm."""
    (x, y) = ExtendedEuclid(n1, n2)
    # n1*x + n2*y = 1
    N = n1 * n2
    r = (r1 * n2 * y + r2 * n1 * x) % N
    return (r + N) % N


def DecipherHastad(first_ciphertext: int, first_modulo: int,
                   second_ciphertext: int, second_modulo: int) -> str:
    """
    Håstad's Broadcast Attack:
    When the same message M is broadcast to 2 recipients with public exponent e = 2:
        C1 = M^2 mod N1
        C2 = M^2 mod N2
    By CRT, we reconstruct x = M^2 mod (N1 * N2).
    Since M < N1 and M < N2, M^2 < N1 * N2, so x = M^2 exactly over integers!
    Taking the standard integer square root reveals M without factoring N1 or N2.
    """
    m2 = ChineseRemainderTheoremHelper(first_modulo, first_ciphertext, second_modulo, second_ciphertext)
    m = IntSqrt(m2)
    assert m * m == m2, "Reconstructed CRT value is not a perfect square!"
    return ConvertToStr(m)
