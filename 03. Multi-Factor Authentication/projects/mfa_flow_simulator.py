#!/usr/bin/env python3
"""
MFA Flow Simulator
==================
Interactive simulation of MFA enrollment and login:
- User registration with MFA setup
- Login with primary and secondary factor
- Backup code generation and recovery
- Device trust and remembered devices
- MFA fatigue attack simulation

Run: python mfa_flow_simulator.py
"""

import secrets
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class User:
    username: str
    password: str
    mfa_enabled: bool = False
    mfa_secret: str = ""
    backup_codes: List[str] = field(default_factory=list)
    trusted_devices: List[str] = field(default_factory=list)
    failed_mfa_attempts: int = 0
    locked_until: float = 0


class MFASystem:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.used_codes: set = set()
        self.audit_log: List[Dict] = []
    
    def log(self, event: str, username: str, details: str):
        self.audit_log.append({
            "time": time.strftime("%H:%M:%S"),
            "event": event,
            "user": username,
            "details": details
        })
        print(f"   [LOG] {event}: {details}")
    
    def register(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        self.users[username] = user
        self.log("REGISTER", username, "Account created")
        return user
    
    def setup_mfa(self, username: str) -> str:
        """Simulate MFA setup (like scanning a QR code)."""
        if username not in self.users:
            raise ValueError("User not found")
        
        user = self.users[username]
        user.mfa_secret = secrets.token_hex(20)
        user.mfa_enabled = True
        
        # Generate backup codes
        user.backup_codes = [secrets.token_hex(4).upper() for _ in range(8)]
        
        self.log("MFA_SETUP", username, "MFA enabled with TOTP")
        
        print(f"\n   📱 MFA Setup Complete for {username}")
        print(f"   Secret Key: {user.mfa_secret[:20]}...")
        print(f"   (In real life, this would be a QR code)")
        print(f"\n   🔑 Backup Codes (save these!):")
        for i, code in enumerate(user.backup_codes, 1):
            print(f"      {i}. {code[:4]}-{code[4:]}")
        
        return user.mfa_secret
    
    def generate_totp(self, username: str) -> str:
        """Simulate TOTP code generation."""
        if username not in self.users:
            return ""
        
        user = self.users[username]
        if not user.mfa_secret:
            return ""
        
        # Simulate 6-digit TOTP
        counter = int(time.time()) // 30
        code = str(int(hash(user.mfa_secret + str(counter))) % 1000000).zfill(6)
        return code
    
    def login(self, username: str, password: str, device_id: str,
              mfa_code: str = None, use_backup: bool = False) -> bool:
        """Simulate login with MFA."""
        print(f"\n🔐 Login attempt: {username} from {device_id}")
        
        if username not in self.users:
            print("   ❌ User not found")
            return False
        
        user = self.users[username]
        
        # Check lockout
        if time.time() < user.locked_until:
            remaining = int(user.locked_until - time.time())
            print(f"   ❌ Account locked. Try again in {remaining} seconds.")
            return False
        
        # Step 1: Password check
        if user.password != password:
            self.log("LOGIN_FAIL", username, "Invalid password")
            print("   ❌ Invalid password")
            return False
        
        print("   ✅ Password correct")
        
        # Step 2: Check if device is trusted
        if device_id in user.trusted_devices and not mfa_code:
            self.log("LOGIN_SUCCESS", username, f"Trusted device: {device_id}")
            print("   ✅ Trusted device - MFA skipped")
            return True
        
        # Step 3: MFA check
        if not user.mfa_enabled:
            self.log("LOGIN_SUCCESS", username, "No MFA configured")
            print("   ⚠️  MFA not enabled (less secure)")
            return True
        
        if mfa_code is None:
            print("   ⏳ MFA required. Waiting for code...")
            return False
        
        # Check backup codes
        if use_backup:
            if mfa_code in user.backup_codes:
                user.backup_codes.remove(mfa_code)
                self.log("LOGIN_SUCCESS", username, "Used backup code")
                print("   ✅ Backup code accepted")
                return True
            else:
                print("   ❌ Invalid backup code")
                user.failed_mfa_attempts += 1
        else:
            # Check TOTP
            expected = self.generate_totp(username)
            if mfa_code == expected:
                user.failed_mfa_attempts = 0
                
                # Offer to trust device
                print("   ✅ MFA code correct")
                trust = input(f"   Trust this device ({device_id}) for 30 days? (y/n): ").lower()
                if trust == 'y':
                    user.trusted_devices.append(device_id)
                    print("   📱 Device trusted for 30 days")
                
                self.log("LOGIN_SUCCESS", username, f"MFA verified on {device_id}")
                return True
            else:
                print(f"   ❌ Invalid MFA code (expected: {expected})")
                user.failed_mfa_attempts += 1
        
        # Lockout after 3 failed MFA attempts
        if user.failed_mfa_attempts >= 3:
            user.locked_until = time.time() + 300  # 5 minutes
            self.log("LOCKOUT", username, "3 failed MFA attempts")
            print("   🚫 Account locked for 5 minutes due to failed attempts")
        
        return False
    
    def simulate_fatigue_attack(self, username: str):
        """Simulate MFA fatigue/push bombing attack."""
        print(f"\n🚨 SIMULATING MFA FATIGUE ATTACK on {username}")
        print("   Attacker repeatedly sends push notifications...")
        
        for i in range(1, 6):
            print(f"\n   Push notification #{i}")
            if i >= 3:
                print("   🛡️  Numbered challenge required!")
                print(f"   Screen shows: 'Enter code 7392 on your phone'")
                print(f"   Phone shows: 'Login? Code: 7392'")
                print("   ✅ User MUST match the number - prevents blind approval")
                break
        
        self.log("FATIGUE_BLOCKED", username, "Numbered challenge prevented attack")


def main():
    print("=" * 60)
    print("🔐 MFA FLOW SIMULATOR")
    print("=" * 60)
    
    mfa = MFASystem()
    
    # Register user
    print("\n👤 Step 1: Register new user 'alice'")
    mfa.register("alice", "password123")
    
    # Setup MFA
    print("\n📱 Step 2: Setup MFA")
    mfa.setup_mfa("alice")
    
    # First login (untrusted device)
    print("\n🔐 Step 3: Login from new laptop")
    current_totp = mfa.generate_totp("alice")
    print(f"   (For demo, current TOTP is: {current_totp})")
    mfa.login("alice", "password123", "laptop_001", current_totp)
    
    # Second login (trusted device)
    print("\n🔐 Step 4: Login again from same laptop")
    mfa.login("alice", "password123", "laptop_001")
    
    # Login from phone
    print("\n🔐 Step 5: Login from phone (new device)")
    current_totp = mfa.generate_totp("alice")
    print(f"   (For demo, current TOTP is: {current_totp})")
    mfa.login("alice", "password123", "phone_001", current_totp)
    
    # Failed login attempts
    print("\n🔐 Step 6: Attacker tries wrong codes")
    mfa.login("alice", "password123", "attacker_pc", "000000")
    mfa.login("alice", "password123", "attacker_pc", "111111")
    mfa.login("alice", "password123", "attacker_pc", "222222")
    
    # Show lockout
    print("\n🔐 Step 7: Another attempt (account locked)")
    mfa.login("alice", "password123", "attacker_pc", "333333")
    
    # MFA fatigue
    mfa.simulate_fatigue_attack("alice")
    
    # Show audit log
    print("\n📊 AUDIT LOG:")
    for entry in mfa.audit_log:
        print(f"   [{entry['time']}] {entry['event']}: {entry['details']}")
    
    print("\n💡 KEY TAKEAWAYS:")
    print("   • Trusted devices improve UX without sacrificing security")
    print("   • Failed attempts trigger lockouts (rate limiting)")
    print("   • Backup codes are essential for account recovery")
    print("   • Numbered challenges prevent MFA fatigue attacks")


if __name__ == "__main__":
    main()
