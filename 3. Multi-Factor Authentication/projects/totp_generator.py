#!/usr/bin/env python3
"""
TOTP Generator and Validator
============================
Implements RFC 6238 TOTP algorithm from scratch:
- Generates time-based one-time passwords
- Demonstrates HMAC-SHA1 calculation
- Validates codes with drift tolerance
- Shows Base32 encoding of secrets

Run: python totp_generator.py
"""

import base64
import hashlib
import hmac
import struct
import time
from typing import Tuple


class TOTP:
    """
    Time-based One-Time Password (RFC 6238) implementation.
    
    This is the algorithm used by Google Authenticator, Authy, 
    Microsoft Authenticator, and other MFA apps.
    """
    
    def __init__(self, secret: bytes, digits: int = 6, interval: int = 30):
        """
        Args:
            secret: Shared secret key (Base32 decoded)
            digits: Number of digits in OTP (default 6)
            interval: Time step in seconds (default 30)
        """
        self.secret = secret
        self.digits = digits
        self.interval = interval
    
    @classmethod
    def from_base32(cls, secret_b32: str, **kwargs) -> "TOTP":
        """Create TOTP from Base32-encoded secret (like QR codes)."""
        # Remove spaces and convert to uppercase
        secret_b32 = secret_b32.replace(" ", "").upper()
        # Add padding if needed
        padding = 8 - (len(secret_b32) % 8)
        if padding != 8:
            secret_b32 += "=" * padding
        secret = base64.b32decode(secret_b32)
        return cls(secret, **kwargs)
    
    def _get_counter(self, timestamp: float = None) -> int:
        """Calculate time counter (changes every interval seconds)."""
        if timestamp is None:
            timestamp = time.time()
        return int(timestamp) // self.interval
    
    def _hmac_sha1(self, counter: int) -> bytes:
        """Generate HMAC-SHA1 of counter using secret."""
        # Counter must be 8 bytes, big-endian
        counter_bytes = struct.pack(">Q", counter)
        return hmac.new(self.secret, counter_bytes, hashlib.sha1).digest()
    
    def _truncate(self, hmac_result: bytes) -> int:
        """
        Dynamic truncation per RFC 4226.
        
        1. Take last 4 bits of HMAC as offset
        2. Extract 4 bytes starting at offset
        3. Mask most significant bit to avoid sign issues
        4. Convert to integer
        """
        # Get offset from last byte (last 4 bits)
        offset = hmac_result[-1] & 0x0F
        
        # Extract 4 bytes starting at offset
        code = struct.unpack(">I", hmac_result[offset:offset+4])[0]
        
        # Mask most significant bit (0x7FFFFFFF = 0111 1111...)
        code = code & 0x7FFFFFFF
        
        return code
    
    def generate(self, timestamp: float = None) -> str:
        """Generate TOTP code for given timestamp."""
        counter = self._get_counter(timestamp)
        hmac_result = self._hmac_sha1(counter)
        code = self._truncate(hmac_result)
        
        # Modulo to get desired number of digits
        otp = code % (10 ** self.digits)
        
        # Zero-pad to ensure correct length
        return str(otp).zfill(self.digits)
    
    def verify(self, code: str, timestamp: float = None, 
               drift_windows: int = 1) -> Tuple[bool, str]:
        """
        Verify TOTP code with drift tolerance.
        
        Args:
            code: The code to verify
            timestamp: Current time (default: now)
            drift_windows: Number of past/future windows to check
        
        Returns:
            (is_valid, message)
        """
        if timestamp is None:
            timestamp = time.time()
        
        current_counter = self._get_counter(timestamp)
        
        # Check current window and adjacent windows (for clock drift)
        for offset in range(-drift_windows, drift_windows + 1):
            check_counter = current_counter + offset
            
            # Temporarily use this counter
            hmac_result = self._hmac_sha1(check_counter)
            check_code = str(self._truncate(hmac_result) % (10 ** self.digits)).zfill(self.digits)
            
            if check_code == code:
                if offset == 0:
                    return True, "Valid (current window)"
                elif offset < 0:
                    return True, f"Valid (behind by {abs(offset)} window(s) - clock drift)"
                else:
                    return True, f"Valid (ahead by {offset} window(s) - clock drift)"
        
        return False, "Invalid code"
    
    def get_remaining_seconds(self) -> int:
        """Get seconds remaining in current time window."""
        return self.interval - (int(time.time()) % self.interval)
    
    def explain(self, timestamp: float = None):
        """Show step-by-step calculation for educational purposes."""
        if timestamp is None:
            timestamp = time.time()
        
        counter = self._get_counter(timestamp)
        counter_bytes = struct.pack(">Q", counter)
        hmac_result = self._hmac_sha1(counter)
        offset = hmac_result[-1] & 0x0F
        code = struct.unpack(">I", hmac_result[offset:offset+4])[0]
        masked = code & 0x7FFFFFFF
        otp = masked % (10 ** self.digits)
        
        print(f"\n🔬 UNDER THE HOOD: TOTP Calculation")
        print(f"   Timestamp:       {timestamp}")
        print(f"   Time step:       {self.interval}s")
        print(f"   Counter:         {counter} (timestamp // {self.interval})")
        print(f"   Counter bytes:   {counter_bytes.hex()}")
        print(f"   Secret (hex):    {self.secret.hex()}")
        print(f"   HMAC-SHA1:       {hmac_result.hex()}")
        print(f"   Offset (last 4 bits): {offset}")
        print(f"   4-byte extract:  {hmac_result[offset:offset+4].hex()}")
        print(f"   As integer:      {code}")
        print(f"   Masked (0x7F):   {masked}")
        print(f"   Mod 10^{self.digits}:         {otp}")
        print(f"   Final OTP:       {str(otp).zfill(self.digits)}")


def demonstrate_totp():
    """Demonstrate TOTP generation and verification."""
    print("=" * 60)
    print("🔢 TOTP GENERATOR (RFC 6238)")
    print("=" * 60)
    
    # Example secret (Base32 encoded, like you'd scan from a QR code)
    secret_b32 = "JBSWY3DPEHPK3PXP"  # Base32 for "Hello!"
    
    print(f"\n📱 Setting up authenticator...")
    print(f"   Secret (Base32): {secret_b32}")
    
    totp = TOTP.from_base32(secret_b32)
    
    # Show the underlying secret bytes
    print(f"   Secret (hex):    {totp.secret.hex()}")
    print(f"   Secret (ascii):  {totp.secret.decode('ascii', errors='replace')}")
    
    # Generate codes for current and adjacent windows
    now = time.time()
    current_counter = totp._get_counter(now)
    
    print(f"\n⏱️  Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Time window:  {totp.interval}s (changes every {totp.interval} seconds)")
    print(f"   Current counter: {current_counter}")
    print(f"   Time remaining in window: {totp.get_remaining_seconds()}s")
    
    print(f"\n🔑 Generated codes:")
    for offset in range(-2, 3):
        ts = now + (offset * totp.interval)
        code = totp.generate(ts)
        marker = " ← CURRENT" if offset == 0 else ""
        time_str = time.strftime('%H:%M:%S', time.localtime(ts))
        print(f"   Counter {current_counter + offset:3d} ({time_str}): {code}{marker}")
    
    # Show detailed calculation
    totp.explain(now)
    
    # Interactive verification
    print(f"\n🧪 VERIFICATION TEST")
    print("-" * 50)
    current_code = totp.generate()
    print(f"Current valid code: {current_code}")
    
    # Verify correct code
    valid, msg = totp.verify(current_code)
    print(f"Verify '{current_code}': {msg}")
    
    # Verify wrong code
    wrong_code = "000000"
    valid, msg = totp.verify(wrong_code)
    print(f"Verify '{wrong_code}': {msg}")
    
    # Verify with drift
    past_code = totp.generate(now - 30)
    valid, msg = totp.verify(past_code, drift_windows=1)
    print(f"Verify previous code '{past_code}': {msg}")


def main():
    demonstrate_totp()
    
    print("\n" + "=" * 60)
    print("📋 KEY TAKEAWAYS")
    print("=" * 60)
    print("• TOTP uses shared secret + current time + HMAC-SHA1")
    print("• Codes change every 30 seconds (configurable)")
    print("• Both device and server must know the same secret")
    print("• Time drift is handled by checking adjacent windows")
    print("• The secret is NEVER transmitted after initial setup")
    print("• QR codes contain the Base32-encoded secret")
    print("=" * 60)


if __name__ == "__main__":
    main()
