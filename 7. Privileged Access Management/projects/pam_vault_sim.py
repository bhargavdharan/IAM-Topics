#!/usr/bin/env python3
"""
PAM Vault Simulator
===================
Simulates a privileged credential vault with:
- Encrypted credential storage
- Role-based vault access
- Audit logging of all retrievals
- Automatic password generation

Run: python pam_vault_sim.py
"""

import secrets
import string
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class VaultEntry:
    account_name: str
    password_hash: str
    salt: str
    allowed_roles: List[str]
    created_at: datetime
    last_rotated: datetime
    access_count: int = 0
    
    def check_access(self, user_roles: List[str]) -> bool:
        return any(role in self.allowed_roles for role in user_roles)


class PAMVault:
    """Simulates a Privileged Access Management vault."""
    
    def __init__(self):
        self.entries: Dict[str, VaultEntry] = {}
        self.audit_log: List[Dict] = []
        self.access_log: Dict[str, List[datetime]] = {}  # Track who accessed what
    
    def log(self, event_type: str, user: str, account: str, details: str):
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "user": user,
            "account": account,
            "details": details
        }
        self.audit_log.append(event)
        print(f"   [AUDIT] {event_type}: {user} → {account} ({details})")
    
    def _generate_password(self, length: int = 20) -> str:
        """Generate a cryptographically strong password."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password with salt using SHA-256 (simplified for demo)."""
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def store_credential(self, account_name: str, allowed_roles: List[str]):
        """Store a new privileged credential in the vault."""
        password = self._generate_password()
        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password, salt)
        
        entry = VaultEntry(
            account_name=account_name,
            password_hash=password_hash,
            salt=salt,
            allowed_roles=allowed_roles,
            created_at=datetime.now(),
            last_rotated=datetime.now()
        )
        
        self.entries[account_name] = entry
        self.log("STORE", "vault_admin", account_name, "Credential stored")
        
        # Return plaintext password ONCE for setup (in reality, this would be
        # injected directly to the target system)
        return password
    
    def retrieve_credential(self, account_name: str, user: str, 
                           user_roles: List[str]) -> Optional[str]:
        """Retrieve a credential from the vault (with authorization check)."""
        if account_name not in self.entries:
            self.log("RETRIEVE_FAILED", user, account_name, "Account not found")
            return None
        
        entry = self.entries[account_name]
        
        # Authorization check
        if not entry.check_access(user_roles):
            self.log("RETRIEVE_DENIED", user, account_name, 
                    f"Unauthorized roles: {user_roles}")
            return None
        
        # Log successful access
        entry.access_count += 1
        self.log("RETRIEVE", user, account_name, 
                f"Access #{entry.access_count}")
        
        # Track access pattern
        if account_name not in self.access_log:
            self.access_log[account_name] = []
        self.access_log[account_name].append(datetime.now())
        
        # In real vault, we'd decrypt and return
        # Here we simulate by returning a placeholder
        return f"[DECRYPTED_PASSWORD_FOR_{account_name}]"
    
    def rotate_password(self, account_name: str, admin_user: str):
        """Rotate (change) a stored password."""
        if account_name not in self.entries:
            return
        
        new_password = self._generate_password()
        salt = secrets.token_hex(16)
        self.entries[account_name].password_hash = self._hash_password(new_password, salt)
        self.entries[account_name].salt = salt
        self.entries[account_name].last_rotated = datetime.now()
        
        self.log("ROTATE", admin_user, account_name, "Password rotated")
        return new_password
    
    def audit_report(self):
        """Generate vault audit report."""
        print("\n" + "=" * 60)
        print("🔐 PAM VAULT AUDIT REPORT")
        print("=" * 60)
        print(f"Generated: {datetime.now().isoformat()}")
        print(f"Total credentials: {len(self.entries)}")
        
        print("\n📋 Stored Credentials:")
        for name, entry in self.entries.items():
            age = (datetime.now() - entry.last_rotated).days
            status = "🟢" if age < 90 else "🟡" if age < 180 else "🔴"
            print(f"   {status} {name}")
            print(f"      Roles: {entry.allowed_roles}")
            print(f"      Access count: {entry.access_count}")
            print(f"      Last rotated: {entry.last_rotated.strftime('%Y-%m-%d')} ({age} days ago)")
        
        print("\n📊 Recent Audit Events:")
        for event in self.audit_log[-10:]:
            print(f"   [{event['timestamp']}] {event['type']}: "
                  f"{event['user']} → {event['account']}")
        
        print("=" * 60)


def main():
    print("=" * 60)
    print("🔐 PAM VAULT SIMULATOR")
    print("=" * 60)
    
    vault = PAMVault()
    
    # Store privileged credentials
    print("\n💾 Storing privileged credentials...")
    pw1 = vault.store_credential("prod_db_admin", ["DBA", "Senior_Admin"])
    pw2 = vault.store_credential("domain_admin", ["Domain_Admin"])
    pw3 = vault.store_credential("backup_service", ["Backup_Operator", "Admin"])
    
    print(f"   Generated strong passwords (shown once for setup)")
    
    # Simulate access attempts
    print("\n🔑 Simulating credential retrievals...")
    
    # Authorized access
    result = vault.retrieve_credential("prod_db_admin", "alice", ["DBA"])
    print(f"   Result: {'✅ Success' if result else '❌ Denied'}")
    
    # Unauthorized access
    result = vault.retrieve_credential("domain_admin", "bob", ["DBA"])
    print(f"   Result: {'✅ Success' if result else '❌ Denied'}")
    
    # Another authorized access
    result = vault.retrieve_credential("prod_db_admin", "charlie", ["Senior_Admin"])
    print(f"   Result: {'✅ Success' if result else '❌ Denied'}")
    
    # Password rotation
    print("\n🔄 Rotating domain_admin password...")
    vault.rotate_password("domain_admin", "vault_admin")
    
    # Generate audit report
    vault.audit_report()
    
    print("\n💡 KEY CONCEPTS:")
    print("   • Credentials are NEVER stored in plaintext")
    print("   • Access is logged for every retrieval")
    print("   • Role-based authorization controls vault access")
    print("   • Regular rotation limits exposure window")


if __name__ == "__main__":
    main()
