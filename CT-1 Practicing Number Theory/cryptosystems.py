"""
Applied Cryptosystems: OTP, Many-Time Pad, Diffie-Hellman, RSA, and Shor's Algorithm
Author: Mahfuzur Rahman (ID: IT-23005)
Course: Cryptography and Cyber Law
Workshop Ref: https://github.com/mnp-club/Number_Theory_and_Cryptography_Workshop
"""

import math
import random
from typing import Tuple, List, Dict
from number_theory import extended_gcd, modInverse, FastModularExponentiation


# -------------------------------------------------------------
# Encoding Utilities: String <-> Large Integer <-> Hex
# -------------------------------------------------------------

def ConvertToInt(message_str: str) -> int:
    """Encodes an ASCII text string into a single large integer using base-256."""
    res = 0
    for ch in message_str:
        res = res * 256 + ord(ch)
    return res


def ConvertToStr(n: int) -> str:
    """Decodes a base-256 integer back into an ASCII string."""
    res = []
    while n > 0:
        res.append(chr(n % 256))
        n //= 256
    return "".join(reversed(res))


def toHex(s: str) -> str:
    """Converts an ASCII string to an even-length hexadecimal string."""
    return "".join(f"{ord(ch):02x}" for ch in s)


def toStr(hex_str: str) -> str:
    """Converts a hexadecimal string back to ASCII text."""
    if len(hex_str) % 2 != 0:
        hex_str = "0" + hex_str
    return bytes.fromhex(hex_str).decode("latin1")


def Xor(hex1: str, hex2: str) -> str:
    """Bitwise XOR between two equal-length hex strings."""
    assert len(hex1) == len(hex2), "Hex strings must have equal length for XOR"
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)
    return bytes(x ^ y for x, y in zip(b1, b2)).hex()


# -------------------------------------------------------------
# 1. One-Time Pad & Many-Time Pad Vulnerability Demo
# -------------------------------------------------------------

def otp_encrypt(message: str, key: str) -> str:
    """One-Time Pad encryption: C = M XOR K (hex strings)."""
    assert len(message) == len(key), "Key length must match message length"
    return Xor(toHex(message), toHex(key))


def otp_decrypt(ciphertext_hex: str, key: str) -> str:
    """One-Time Pad decryption: M = C XOR K."""
    return toStr(Xor(ciphertext_hex, toHex(key)))


def TryGuessingSubstring(substring: str, message_length: int, xor_messages_hex: str) -> List[Tuple[int, str, str]]:
    """
    Crib dragging: slides a guessed substring along the XOR of two ciphertexts.
    Reveals readable plaintext wherever the crib matches either message.
    """
    good_guesses = []
    sub_len = len(substring)
    for pos in range(message_length - sub_len + 1):
        # Pad guess with null bytes to align with position
        padded_guess = "\x00" * pos + substring + "\x00" * (message_length - sub_len - pos)
        guess_hex = toHex(padded_guess)
        revealed_raw = toStr(Xor(guess_hex, xor_messages_hex))
        revealed_part = revealed_raw[pos : pos + sub_len]
        
        # Heuristic: valid if all characters are alphabetic or space
        if all(ch.isalpha() or ch.isspace() or ch in ",.!?'\"-" for ch in revealed_part):
            good_guesses.append((pos, substring, revealed_part))
            
    return good_guesses


# -------------------------------------------------------------
# 2. Diffie-Hellman Key Exchange Protocol
# -------------------------------------------------------------

class DiffieHellmanParty:
    """Simulates a Diffie-Hellman protocol participant (Alice or Bob)."""
    
    def __init__(self, name: str, modulus_N: int, generator_g: int, private_key: Optional[int] = None):
        self.name = name
        self.N = modulus_N
        self.g = generator_g
        # Private key chosen from {2, ..., N-2}
        self.private_key = private_key if private_key is not None else random.randint(2, modulus_N - 2)
        # Compute public transmitted value A or B = g^x mod N
        self.public_value = FastModularExponentiation(self.g, self.private_key, self.N)
        self.shared_key = None

    def compute_shared_key(self, other_public_value: int) -> int:
        """Derives the shared secret: K = (other_public)^private mod N."""
        self.shared_key = FastModularExponentiation(other_public_value, self.private_key, self.N)
        return self.shared_key


# -------------------------------------------------------------
# 3. RSA Public-Key Cryptosystem
# -------------------------------------------------------------

def PowMod(a: int, n: int, mod: int) -> int:
    """Iterative square-and-multiply modular exponentiation."""
    return FastModularExponentiation(a, n, mod)


def ExtendedEuclid(a: int, b: int) -> Tuple[int, int]:
    """Helper for modular inversion: returns (x, y) such that a*x + b*y = gcd(a, b)."""
    if b == 0:
        return (1, 0)
    (x1, y1) = ExtendedEuclid(b, a % b)
    k = a // b
    return (y1, x1 - k * y1)


def InvertModulo(a: int, n: int) -> int:
    """Computes multiplicative inverse of a modulo n using Extended Euclid."""
    (b, x) = ExtendedEuclid(a, n)
    if b < 0:
        b = (b % n + n) % n
    return b


def rsa_keygen(p: int, q: int, e: int = 65537) -> Dict[str, any]:
    """Generates RSA key pair given primes p and q."""
    assert p != q, "Primes p and q must be distinct"
    N = p * q
    phiN = (p - 1) * (q - 1)
    assert math.gcd(e, phiN) == 1, f"Public exponent e={e} not coprime to phi(N)={phiN}"
    d = InvertModulo(e, phiN)
    return {
        "p": p,
        "q": q,
        "N": N,
        "phiN": phiN,
        "e": e,
        "d": d,
        "public_key": (e, N),
        "private_key": (d, N),
    }


def Encrypt(message: str, modulo: int, exponent: int) -> int:
    """RSA Encryption: C = M^e mod N."""
    m_int = ConvertToInt(message)
    assert m_int < modulo, f"Plaintext integer {m_int} exceeds modulus {modulo}! Split into blocks."
    return FastModularExponentiation(m_int, exponent, modulo)


def Decrypt(ciphertext: int, p: int, q: int, exponent: int) -> str:
    """RSA Decryption: M = C^d mod N, where d = e^(-1) mod phi(N)."""
    phiN = (p - 1) * (q - 1)
    d = InvertModulo(exponent, phiN)
    modulo = p * q
    m_int = FastModularExponentiation(ciphertext, d, modulo)
    return ConvertToStr(m_int)


# -------------------------------------------------------------
# 4. Shor's Algorithm: Quantum Order-Finding Reduction
# -------------------------------------------------------------

def shors_classical_reduction(N: int, a: int, r: int) -> Tuple[Optional[int], Optional[int]]:
    """
    Given an even period r of a modulo N such that a^(r/2) != -1 (mod N),
    computes the non-trivial prime factors of N via gcd(a^(r/2) - 1, N) and gcd(a^(r/2) + 1, N).
    """
    if r % 2 != 0:
        return None, None
    half_power = FastModularExponentiation(a, r // 2, N)
    if half_power == N - 1:  # a^(r/2) = -1 mod N
        return None, None
    p = math.gcd(half_power - 1, N)
    q = math.gcd(half_power + 1, N)
    if p > 1 and q > 1 and p * q == N:
        return min(p, q), max(p, q)
    return None, None
