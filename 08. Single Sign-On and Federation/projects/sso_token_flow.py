#!/usr/bin/env python3
"""
SSO Token Flow Simulator
========================
Simulates Single Sign-On token exchange between Identity Provider
and Service Provider with trust validation.

Run: python sso_token_flow.py
"""

import base64
import hashlib
import json
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, Optional


class IdentityProvider:
    """Simulates an Identity Provider (IdP)."""
    
    def __init__(self, name: str):
        self.name = name
        self.users: Dict[str, Dict] = {}
        self.private_key = secrets.token_hex(32)  # Simulated private key
        self.public_key = self.private_key  # In reality, derived from private
        self.issued_tokens: Dict[str, Dict] = {}
    
    def register_user(self, username: str, attributes: Dict):
        self.users[username] = {
            "password": secrets.token_hex(8),  # Simulated password hash
            "attributes": attributes
        }
    
    def authenticate(self, username: str, password: str) -> bool:
        """Simulate user authentication."""
        if username not in self.users:
            return False
        # In reality, compare password hashes
        return True
    
    def issue_token(self, username: str, audience: str) -> str:
        """Issue a signed token (simulated JWT/SAML)."""
        if username not in self.users:
            raise ValueError("User not found")
        
        user = self.users[username]
        now = int(time.time())
        
        token_data = {
            "iss": self.name,  # Issuer
            "sub": username,   # Subject
            "aud": audience,   # Audience (who this is for)
            "iat": now,        # Issued at
            "exp": now + 3600, # Expires in 1 hour
            "jti": secrets.token_hex(16),  # Unique token ID
            "attributes": user["attributes"]
        }
        
        # Simulate signing (in reality, use RSA/ECDSA)
        signature = hashlib.sha256(
            (json.dumps(token_data, sort_keys=True) + self.private_key).encode()
        ).hexdigest()
        
        token = {
            "data": token_data,
            "signature": signature
        }
        
        # Store issued token
        self.issued_tokens[token_data["jti"]] = token
        
        return base64.b64encode(json.dumps(token).encode()).decode()
    
    def get_public_key(self) -> str:
        return self.public_key


class ServiceProvider:
    """Simulates a Service Provider (SP)."""
    
    def __init__(self, name: str, idp: IdentityProvider):
        self.name = name
        self.idp = idp
        self.trusted_idps: Dict[str, str] = {}  # name -> public_key
        self.consumed_tokens: set = set()  # Prevent replay attacks
        
        # Establish trust
        self.trusted_idps[idp.name] = idp.get_public_key()
    
    def verify_token(self, token_b64: str) -> Optional[Dict]:
        """Verify an incoming token."""
        try:
            token_json = base64.b64decode(token_b64).decode()
            token = json.loads(token_json)
        except Exception:
            print("   ❌ Invalid token format")
            return None
        
        data = token["data"]
        signature = token["signature"]
        
        # 1. Check issuer is trusted
        issuer = data.get("iss")
        if issuer not in self.trusted_idps:
            print(f"   ❌ Untrusted issuer: {issuer}")
            return None
        
        # 2. Check audience
        audience = data.get("aud")
        if audience != self.name:
            print(f"   ❌ Wrong audience: {audience} (expected {self.name})")
            return None
        
        # 3. Verify signature
        expected_sig = hashlib.sha256(
            (json.dumps(data, sort_keys=True) + self.trusted_idps[issuer]).encode()
        ).hexdigest()
        
        if signature != expected_sig:
            print("   ❌ Invalid signature")
            return None
        
        # 4. Check expiration
        if data.get("exp", 0) < time.time():
            print("   ❌ Token expired")
            return None
        
        # 5. Check for replay
        jti = data.get("jti")
        if jti in self.consumed_tokens:
            print("   ❌ Token replay detected")
            return None
        
        self.consumed_tokens.add(jti)
        
        print("   ✅ Token verified successfully")
        return data
    
    def process_login(self, token_b64: str):
        """Process SSO login with token."""
        print(f"\n🔑 {self.name} processing login...")
        user_data = self.verify_token(token_b64)
        
        if user_data:
            print(f"   Welcome, {user_data['sub']}!")
            print(f"   Attributes: {user_data['attributes']}")
            return user_data
        else:
            print("   Access denied.")
            return None


def main():
    print("=" * 60)
    print("🔐 SSO TOKEN FLOW SIMULATOR")
    print("=" * 60)
    
    # Setup IdP
    print("\n🏢 Setting up Identity Provider...")
    idp = IdentityProvider("Company-IdP")
    idp.register_user("alice", {
        "role": "Senior Developer",
        "department": "Engineering",
        "email": "alice@company.com"
    })
    idp.register_user("bob", {
        "role": "Manager",
        "department": "Finance",
        "email": "bob@company.com"
    })
    print(f"   IdP '{idp.name}' ready with {len(idp.users)} users")
    
    # Setup SPs
    print("\n🌐 Setting up Service Providers...")
    gmail = ServiceProvider("Gmail", idp)
    drive = ServiceProvider("GoogleDrive", idp)
    salesforce = ServiceProvider("Salesforce", idp)
    
    # Malicious SP (not trusted)
    malicious = ServiceProvider("FakeSite", IdentityProvider("Fake-IdP"))
    
    # Scenario 1: Normal SSO flow
    print("\n" + "=" * 60)
    print("📋 SCENARIO 1: Alice logs into Gmail via SSO")
    print("=" * 60)
    
    print("\n1️⃣  Alice authenticates with IdP")
    print("   Username: alice, Password: ********")
    if idp.authenticate("alice", "password"):
        print("   ✅ Authentication successful")
    
    print("\n2️⃣  IdP issues token for Gmail")
    token = idp.issue_token("alice", "Gmail")
    print(f"   Token issued (base64 encoded)")
    
    print("\n3️⃣  Alice sends token to Gmail")
    gmail.process_login(token)
    
    # Scenario 2: Same token to different SP (should fail audience check)
    print("\n" + "=" * 60)
    print("📋 SCENARIO 2: Reusing Gmail token for Google Drive")
    print("=" * 60)
    print("\n   (Token was issued for 'Gmail', not 'GoogleDrive')")
    drive.process_login(token)
    
    # Scenario 3: Fresh token for Google Drive
    print("\n" + "=" * 60)
    print("📋 SCENARIO 3: Proper token for Google Drive")
    print("=" * 60)
    token2 = idp.issue_token("alice", "GoogleDrive")
    drive.process_login(token2)
    
    # Scenario 4: Expired token simulation
    print("\n" + "=" * 60)
    print("📋 SCENARIO 4: Expired token attack")
    print("=" * 60)
    print("\n   Creating an expired token...")
    expired_data = {
        "iss": idp.name,
        "sub": "alice",
        "aud": "Gmail",
        "iat": int(time.time()) - 7200,  # 2 hours ago
        "exp": int(time.time()) - 3600,   # Expired 1 hour ago
        "jti": secrets.token_hex(16),
        "attributes": {}
    }
    expired_sig = hashlib.sha256(
        (json.dumps(expired_data, sort_keys=True) + idp.private_key).encode()
    ).hexdigest()
    expired_token = base64.b64encode(json.dumps({
        "data": expired_data, "signature": expired_sig
    }).encode()).decode()
    
    gmail.process_login(expired_token)
    
    # Scenario 5: Replay attack
    print("\n" + "=" * 60)
    print("📋 SCENARIO 5: Token replay attack")
    print("=" * 60)
    print("\n   Reusing the valid Gmail token from Scenario 1...")
    gmail.process_login(token)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print("✅ Valid token for correct audience: ALLOWED")
    print("❌ Wrong audience: DENIED (prevents token misuse)")
    print("❌ Expired token: DENIED (prevents replay of old tokens)")
    print("❌ Replayed token: DENIED (JTI tracking prevents reuse)")
    print("\n💡 SSO Security relies on:")
    print("   • Digital signatures (authenticity)")
    print("   • Audience restrictions (scope)")
    print("   • Expiration (time limits)")
    print("   • Unique token IDs (replay prevention)")


if __name__ == "__main__":
    main()
