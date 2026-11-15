"""
Comprehensive Test Suite for Number Theory & Applied Cryptography
Author: Mahfuzur Rahman (ID: IT-23005)
Course: Cryptography and Cyber Law
"""

import sys
from number_theory import (
    extended_gcd, lcm, diophantine, modInverse, divide,
    FastModularExponentiation, ChineseRemainderTheorem,
    repunit, is_even_perfect_number, is_fermat_pseudoprime
)
from cryptosystems import (
    ConvertToInt, ConvertToStr, toHex, toStr, Xor,
    otp_encrypt, otp_decrypt, TryGuessingSubstring,
    DiffieHellmanParty, rsa_keygen, Encrypt, Decrypt,
    shors_classical_reduction
)
from rsa_attacks import (
    IntSqrt, DecipherSimple, DecipherSmallPrime,
    DecipherSmallDiff, DecipherCommonDivisor, DecipherHastad
)


def run_tests():
    print("=" * 70)
    print("CT-1: NUMBER THEORY & APPLIED CRYPTOGRAPHY TEST SUITE")
    print("Student: Mahfuzur Rahman | ID: IT-23005")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Number Theory Tests
    # ---------------------------------------------------------
    print("\n[+] Testing Number Theory Core Algorithms...")

    # Extended GCD
    d, x, y = extended_gcd(8, 4)
    assert d == 4 and 8 * x + 4 * y == 4, "Extended GCD failed on (8, 4)"
    d, x, y = extended_gcd(27, 15)
    assert d == 3 and 27 * x + 15 * y == 3, "Extended GCD failed on (27, 15)"
    print("  ✓ extended_gcd passed.")

    # LCM
    assert lcm(9, 3) == 9, "lcm(9, 3) failed"
    assert lcm(17, 37) == 629, "lcm(17, 37) failed"
    print("  ✓ lcm passed.")

    # Linear Diophantine
    x, y = diophantine(34, 51, 170)
    assert 34 * x + 51 * y == 170, "diophantine(34, 51, 170) failed"
    x, y = diophantine(91, 117, 65)
    assert 91 * x + 117 * y == 65, "diophantine(91, 117, 65) failed"
    print("  ✓ diophantine passed.")

    # Modular Inverse & Division
    assert divide(9, 5, 3) == 0, "divide(9, 5, 3) failed"
    assert divide(223, 67, 54) == 13, "divide(223, 67, 54) failed"
    print("  ✓ modInverse and divide passed.")

    # Fast Modular Exponentiation
    assert FastModularExponentiation(4, 5, 3) == pow(4, 5, 3), "FastModularExponentiation failed"
    assert FastModularExponentiation(7, 256, 13) == pow(7, 256, 13)
    print("  ✓ FastModularExponentiation passed.")

    # Chinese Remainder Theorem
    assert ChineseRemainderTheorem(13, 7, 6, 5) == 59, "CRT(13, 7, 6, 5) failed"
    assert ChineseRemainderTheorem(28, 20, 19, 3) == 440, "CRT(28, 20, 19, 3) failed"
    print("  ✓ ChineseRemainderTheorem passed.")

    # Repunits & Even Perfect Numbers
    assert repunit(3) == 111
    assert repunit(5) == 11111
    is_perf, p_val = is_even_perfect_number(28)
    assert is_perf and p_val == 3, "28 is even perfect number with p=3"
    is_perf, p_val = is_even_perfect_number(496)
    assert is_perf and p_val == 5, "496 is even perfect number with p=5"
    print("  ✓ Repunits and Perfect Number validations passed.")

    # Fermat Pseudoprimes
    # 341 = 11 * 31 is the smallest Fermat pseudoprime to base 2
    assert is_fermat_pseudoprime(341, base=2), "341 must be pseudoprime base 2"
    assert is_fermat_pseudoprime(561, base=2), "561 is a Carmichael number"
    print("  ✓ Fermat Pseudoprime check passed.")

    # ---------------------------------------------------------
    # 2. Cryptosystem Tests
    # ---------------------------------------------------------
    print("\n[+] Testing Cryptosystem Implementations...")

    # String <-> Int conversion
    msg = "Cryptography and Cyber Law"
    encoded_int = ConvertToInt(msg)
    decoded_str = ConvertToStr(encoded_int)
    assert decoded_str == msg, "String-to-Int encoding roundtrip failed"
    print("  ✓ String <-> Base-256 Integer encoding passed.")

    # OTP
    key = "A" * len(msg)
    otp_c = otp_encrypt(msg, key)
    otp_dec = otp_decrypt(otp_c, key)
    assert otp_dec == msg, "OTP roundtrip failed"
    print("  ✓ One-Time Pad roundtrip passed.")

    # Many-Time Pad Crib Dragging
    m1 = "steal the secret"
    m2 = "the cat the bird"
    k_pad = "supersecretverys"
    c1 = otp_encrypt(m1, k_pad)
    c2 = otp_encrypt(m2, k_pad)
    xor_c = Xor(c1, c2)
    guesses = TryGuessingSubstring(" the ", len(m1), xor_c)
    assert len(guesses) > 0, "Crib dragging failed to detect matches"
    print("  ✓ Many-Time Pad crib dragging passed.")

    # Diffie-Hellman Protocol
    N_dh = 23
    g_dh = 5
    alice = DiffieHellmanParty("Alice", N_dh, g_dh, private_key=6)
    bob = DiffieHellmanParty("Bob", N_dh, g_dh, private_key=15)
    alice_shared = alice.compute_shared_key(bob.public_value)
    bob_shared = bob.compute_shared_key(alice.public_value)
    assert alice_shared == bob_shared == 2, f"Diffie-Hellman key derivation mismatch: {alice_shared} != {bob_shared}"
    print(f"  ✓ Diffie-Hellman Protocol verified (Shared synthesized key = {alice_shared}).")

    # RSA Keygen, Encryption & Decryption
    # Certified primes p and q
    p_rsa = 1000000000039
    q_rsa = 1000000000061
    keys = rsa_keygen(p_rsa, q_rsa, e=65537)
    rsa_c = Encrypt("attack", keys["N"], keys["e"])
    rsa_m = Decrypt(rsa_c, keys["p"], keys["q"], keys["e"])
    assert rsa_m == "attack", "RSA encryption/decryption failed"
    print("  ✓ RSA Keygen, Encryption, and Decryption verified.")

    # Shor's Algorithm Classical Reduction
    p_shor, q_shor = shors_classical_reduction(N=35, a=8, r=4)
    assert (p_shor, q_shor) == (5, 7), f"Shor reduction failed on N=35: got ({p_shor}, {q_shor})"
    print(f"  ✓ Shor's Algorithm reduction verified (Factors of 35: {p_shor}, {q_shor}).")

    # ---------------------------------------------------------
    # 3. RSA Cryptanalysis Tests (The 7 Assignment Questions)
    # ---------------------------------------------------------
    print("\n[+] Testing Practical RSA Cryptanalytic Attacks...")

    # Q3: DecipherSimple
    mod_simple = 1000000007 * 1000000009
    exp_simple = 65537
    c_simple = Encrypt("attack", mod_simple, exp_simple)
    guessed = DecipherSimple(c_simple, mod_simple, exp_simple, ["retreat", "wait", "attack", "surrender"])
    assert guessed == "attack", "DecipherSimple failed"
    print("  ✓ Attack 1 (DecipherSimple / Dictionary Search) passed.")

    # Q4: DecipherSmallPrime
    p_small = 999983
    q_large = 10000000000000000051
    n_small = p_small * q_large
    c_small = Encrypt("attack", n_small, 65537)
    dec_small = DecipherSmallPrime(c_small, n_small, 65537)
    assert dec_small == "attack", "DecipherSmallPrime failed"
    print("  ✓ Attack 2 (DecipherSmallPrime / Small Factor) passed.")

    # Q5: DecipherSmallDiff (Fermat's Factorization)
    p_close = 1000000007
    q_close = 1000000009
    n_close = p_close * q_close
    c_close = Encrypt("attack", n_close, 239)
    dec_close = DecipherSmallDiff(c_close, n_close, 239)
    assert dec_close == "attack", "DecipherSmallDiff failed"
    print("  ✓ Attack 3 (DecipherSmallDiff / Fermat Factorization) passed.")

    # Q6: DecipherCommonDivisor (Shared Prime Factor)
    p_common = 101
    q1 = 18298970732541109011012304219376080251334480295537316123696052970419466495220522723330315111017831737980079504337868198011077274303193766040393009648852841770668239779097280026631944319501437547002412556176186750790476901358334138818777298389724049250700606462316428106882097210008142941838672676714188593227684360287806974345181893018133710957167334490627178666071809992955566020058374505477745993383434501768887090900283569055646901291270870833498474402084748161755197005050874785474707550376333429671113753137201128897550014524209754619355308207537703754006699795711188492048286436285518105948050401762394690148387
    q2 = 10000000000000000051
    n1_comm = p_common * q1
    n2_comm = p_common * q2
    c1_comm = Encrypt("attack", n1_comm, 239)
    c2_comm = Encrypt("wait", n2_comm, 17)
    m1_res, m2_res = DecipherCommonDivisor(c1_comm, n1_comm, 239, c2_comm, n2_comm, 17)
    assert m1_res == "attack" and m2_res == "wait", "DecipherCommonDivisor failed"
    print("  ✓ Attack 4 (DecipherCommonDivisor / Shared Prime) passed.")

    # Q7: DecipherHastad (Broadcast Attack with e=2)
    p1 = 790383132652258876190399065097
    q1 = 662503581792812531719955475509
    p2 = 656917682542437675078478868539
    q2 = 1263581691331332127259083713503
    n1_h = p1 * q1
    n2_h = p2 * q2
    c1_h = Encrypt("attack", n1_h, 2)
    c2_h = Encrypt("attack", n2_h, 2)
    m_hastad = DecipherHastad(c1_h, n1_h, c2_h, n2_h)
    assert m_hastad == "attack", "DecipherHastad failed"
    print("  ✓ Attack 5 (DecipherHastad / Broadcast Attack) passed.")

    print("\n" + "=" * 70)
    print("ALL TEST SUITES PASSED FLAWLESSLY! 100% VERIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
