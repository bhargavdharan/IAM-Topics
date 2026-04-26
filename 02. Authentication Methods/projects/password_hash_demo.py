#!/usr/bin/env python3
"""
Password Hashing Demonstration
==============================
Demonstrates modern password hashing algorithms:
- Implements bcrypt, scrypt, and Argon2
- Shows salt generation and verification
- Compares hash computation times
- Demonstrates why older algorithms fail

Run: python password_hash_demo.py
"""

import time
import hashlib
import secrets
import string
from typing import Callable, Tuple

# Try to import modern hashing libraries
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("⚠️  bcrypt not installed. Run: pip install bcrypt")

try:
    import argon2
    from argon2 import PasswordHasher
    ARGON2_AVAILABLE = True
except ImportError:
    ARGON2_AVAILABLE = False
    print("⚠️  argon2-cffi not installed. Run: pip install argon2-cffi")


def simple_hash(password: str) -> str:
    """DANGEROUS: Simple MD5 hash (for demonstration only!)."""
    return hashlib.md5(password.encode()).hexdigest()


def simple_hash_with_salt(password: str, salt: str = None) -> Tuple[str, str]:
    """Better: Hash with salt, but still using fast MD5."""
    if salt is None:
        salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest(), salt


def benchmark_hash(func: Callable, password: str, iterations: int = 100) -> float:
    """Benchmark hash function over N iterations."""
    start = time.perf_counter()
    for _ in range(iterations):
        func(password)
    elapsed = time.perf_counter() - start
    return elapsed


def demonstrate_rainbow_table():
    """Show why simple hashing fails against rainbow tables."""
    print("\n🌈 RAINBOW TABLE ATTACK DEMONSTRATION")
    print("-" * 50)
    
    # Common passwords
    common_passwords = ["password", "123456", "qwerty", "admin", "welcome"]
    
    # Pre-computed "rainbow table" (what attackers store)
    rainbow_table = {simple_hash(p): p for p in common_passwords}
    
    # User's "hashed" password (leaked from a breach)
    leaked_hash = simple_hash("password")
    
    print("Attacker's rainbow table (pre-computed hashes):")
    for h, p in rainbow_table.items():
        print(f"   {p:10s} → {h}")
    
    print(f"\nLeaked hash from breach: {leaked_hash}")
    print("Attacker looks up hash in rainbow table...")
    
    if leaked_hash in rainbow_table:
        cracked = rainbow_table[leaked_hash]
        print(f"🚨 CRACKED! Password is: '{cracked}'")
        print("   This took milliseconds because the hash was pre-computed.")
    
    print("\n💡 SOLUTION: Use a unique salt for every password.")
    print("   With salt, pre-computed tables become useless.")


def demonstrate_salting():
    """Show how salting defeats rainbow tables."""
    print("\n🧂 SALTING DEMONSTRATION")
    print("-" * 50)
    
    password = "password"
    
    # Without salt - same hash every time
    hash1 = simple_hash(password)
    hash2 = simple_hash(password)
    print(f"Without salt:")
    print(f"   Hash 1: {hash1}")
    print(f"   Hash 2: {hash2}")
    print(f"   Same hash? {hash1 == hash2} ← Attackers love this!")
    
    # With salt - different hash every time
    hash1, salt1 = simple_hash_with_salt(password)
    hash2, salt2 = simple_hash_with_salt(password)
    print(f"\nWith salt:")
    print(f"   Hash 1: {hash1} (salt: {salt1})")
    print(f"   Hash 2: {hash2} (salt: {salt2})")
    print(f"   Same hash? {hash1 == hash2} ← Attackers can't pre-compute!")


def demonstrate_bcrypt():
    """Demonstrate bcrypt adaptive hashing."""
    if not BCRYPT_AVAILABLE:
        return
    
    print("\n🔐 BCRYPT DEMONSTRATION")
    print("-" * 50)
    
    password = b"super_secret_password"
    
    # Different work factors (rounds)
    for rounds in [8, 10, 12]:
        start = time.perf_counter()
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password, salt)
        elapsed = time.perf_counter() - start
        
        print(f"\nWork factor (2^{rounds} rounds):")
        print(f"   Salt:     {salt.decode()}")
        print(f"   Hash:     {hashed.decode()}")
        print(f"   Time:     {elapsed:.4f} seconds")
        print(f"   Adaptive: As computers get faster, increase rounds to maintain time")
    
    # Verify
    print("\n✅ Verification:")
    print(f"   Correct password: {bcrypt.checkpw(password, hashed)}")
    print(f"   Wrong password:   {bcrypt.checkpw(b'wrong', hashed)}")


def demonstrate_argon2():
    """Demonstrate Argon2 (memory-hard hashing)."""
    if not ARGON2_AVAILABLE:
        return
    
    print("\n🛡️  ARGON2 DEMONSTRATION (Winner of Password Hashing Competition)")
    print("-" * 50)
    
    ph = PasswordHasher(
        time_cost=3,      # Number of iterations
        memory_cost=65536, # 64 MB of RAM
        parallelism=1,    # Number of parallel threads
        hash_len=32,
        salt_len=16
    )
    
    password = "super_secret_password"
    
    print("Argon2 is MEMORY-HARD: it requires lots of RAM to compute.")
    print("This makes it resistant to GPU and ASIC attacks.\n")
    
    start = time.perf_counter()
    hash_value = ph.hash(password)
    elapsed = time.perf_counter() - start
    
    print(f"Hash generation:")
    print(f"   Time: {elapsed:.4f} seconds")
    print(f"   Hash: {hash_value}")
    
    print("\n✅ Verification:")
    try:
        ph.verify(hash_value, password)
        print("   Correct password: True")
    except argon2.exceptions.VerifyMismatchError:
        print("   Correct password: False")
    
    try:
        ph.verify(hash_value, "wrong_password")
        print("   Wrong password: True")
    except argon2.exceptions.VerifyMismatchError:
        print("   Wrong password: False")


def benchmark_comparison():
    """Compare hash algorithm speeds."""
    print("\n⏱️  PERFORMANCE COMPARISON")
    print("-" * 50)
    print("Algorithm          | Time per hash | Security")
    print("-" * 50)
    
    password = "benchmark_password"
    
    # MD5 (insecure, fast)
    md5_time = benchmark_hash(lambda p: hashlib.md5(p.encode()).hexdigest(), password, 10000)
    print(f"MD5 (broken)       | {md5_time/10000*1000:.4f} ms    | ❌ Trivial to crack")
    
    # SHA-256 (fast, needs iterations)
    sha_time = benchmark_hash(lambda p: hashlib.sha256(p.encode()).hexdigest(), password, 10000)
    print(f"SHA-256 (fast)     | {sha_time/10000*1000:.4f} ms    | ⚠️  Needs iterations")
    
    if BCRYPT_AVAILABLE:
        bpw = password.encode()
        bcrypt_time = benchmark_hash(lambda p: bcrypt.hashpw(p.encode(), bcrypt.gensalt()), password, 10)
        print(f"bcrypt (adaptive)  | {bcrypt_time/10:.4f} s      | ✅ Recommended")
    
    if ARGON2_AVAILABLE:
        ph = PasswordHasher(time_cost=2, memory_cost=65536)
        argon_time = benchmark_hash(ph.hash, password, 10)
        print(f"Argon2 (memory-hard)| {argon_time/10:.4f} s      | ✅ Best Practice")
    
    print("\n💡 KEY INSIGHT: Good password hashes are SLOW by design.")
    print("   If an attacker can compute billions per second, your hash is too fast.")


def main():
    print("=" * 60)
    print("🔐 PASSWORD HASHING DEMONSTRATION")
    print("=" * 60)
    print("\nThis demo shows why modern password hashing matters.")
    print("We'll explore: MD5 (broken) → Salting → bcrypt → Argon2\n")
    
    demonstrate_rainbow_table()
    demonstrate_salting()
    
    if BCRYPT_AVAILABLE:
        demonstrate_bcrypt()
    else:
        print("\n⚠️  Install bcrypt to see the bcrypt demo: pip install bcrypt")
    
    if ARGON2_AVAILABLE:
        demonstrate_argon2()
    else:
        print("\n⚠️  Install argon2-cffi to see the Argon2 demo: pip install argon2-cffi")
    
    benchmark_comparison()
    
    print("\n" + "=" * 60)
    print("📋 BEST PRACTICES SUMMARY")
    print("=" * 60)
    print("1. NEVER store passwords in plain text")
    print("2. NEVER use MD5 or SHA-1 for password storage")
    print("3. ALWAYS use a unique salt per password")
    print("4. USE adaptive algorithms: bcrypt, scrypt, or Argon2")
    print("5. ADJUST work factors as hardware improves")
    print("6. CONSIDER adding a pepper (application secret)")
    print("=" * 60)


if __name__ == "__main__":
    main()
