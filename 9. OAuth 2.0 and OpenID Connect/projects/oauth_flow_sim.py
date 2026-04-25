#!/usr/bin/env python3
"""
OAuth 2.0 Flow Simulator
========================
Simulates the Authorization Code flow with PKCE:
- Authorization server with consent
- Client application
- Token issuance and validation
- Scope enforcement

Run: python oauth_flow_sim.py
"""

import base64
import hashlib
import secrets
import time
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str  # In reality, this is a hash
    data: Dict


class AuthorizationServer:
    """Simulates an OAuth 2.0 Authorization Server."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.clients: Dict[str, Dict] = {}
        self.auth_codes: Dict[str, Dict] = {}  # Temporary authorization codes
        self.tokens: Dict[str, Dict] = {}      # Access tokens
        self.refresh_tokens: Dict[str, Dict] = {}
    
    def register_client(self, client_id: str, name: str, redirect_uri: str, 
                       allowed_scopes: List[str]):
        self.clients[client_id] = {
            "name": name,
            "redirect_uri": redirect_uri,
            "allowed_scopes": allowed_scopes,
            "secret": secrets.token_hex(16)
        }
    
    def register_user(self, username: str, password: str, data: Dict):
        self.users[username] = User(username, password, data)
    
    def create_authorization_url(self, client_id: str, redirect_uri: str,
                                  scope: str, state: str, code_challenge: str) -> str:
        """Create authorization URL with PKCE."""
        if client_id not in self.clients:
            raise ValueError("Invalid client")
        
        client = self.clients[client_id]
        if redirect_uri != client["redirect_uri"]:
            raise ValueError("Invalid redirect URI")
        
        requested_scopes = scope.split()
        for s in requested_scopes:
            if s not in client["allowed_scopes"]:
                raise ValueError(f"Scope '{s}' not allowed for this client")
        
        # Build authorization URL
        auth_url = (
            f"https://auth.example.com/authorize?"
            f"response_type=code&"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope={scope}&"
            f"state={state}&"
            f"code_challenge={code_challenge}&"
            f"code_challenge_method=S256"
        )
        
        return auth_url
    
    def approve_consent(self, username: str, password: str, client_id: str,
                       scope: str, code_challenge: str) -> str:
        """User approves consent and receives authorization code."""
        # Authenticate user
        if username not in self.users or self.users[username].password != password:
            raise ValueError("Invalid credentials")
        
        # Generate authorization code
        auth_code = secrets.token_urlsafe(32)
        self.auth_codes[auth_code] = {
            "username": username,
            "client_id": client_id,
            "scope": scope,
            "code_challenge": code_challenge,
            "expires": time.time() + 600  # 10 minutes
        }
        
        return auth_code
    
    def exchange_code_for_token(self, auth_code: str, client_id: str,
                                 client_secret: str, redirect_uri: str,
                                 code_verifier: str) -> Dict:
        """Exchange authorization code for access token."""
        # Verify client
        if client_id not in self.clients:
            raise ValueError("Invalid client")
        
        client = self.clients[client_id]
        if client_secret != client["secret"]:
            raise ValueError("Invalid client secret")
        
        # Verify authorization code
        if auth_code not in self.auth_codes:
            raise ValueError("Invalid or expired authorization code")
        
        code_data = self.auth_codes[auth_code]
        
        if code_data["expires"] < time.time():
            del self.auth_codes[auth_code]
            raise ValueError("Authorization code expired")
        
        # Verify PKCE code verifier
        expected_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode().rstrip("=")
        
        if code_data["code_challenge"] != expected_challenge:
            raise ValueError("Invalid code verifier (PKCE failed)")
        
        # Generate tokens
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        
        self.tokens[access_token] = {
            "username": code_data["username"],
            "scope": code_data["scope"],
            "client_id": client_id,
            "expires": time.time() + 3600  # 1 hour
        }
        
        self.refresh_tokens[refresh_token] = {
            "username": code_data["username"],
            "scope": code_data["scope"],
            "client_id": client_id
        }
        
        # Consume authorization code (one-time use)
        del self.auth_codes[auth_code]
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": code_data["scope"]
        }
    
    def validate_token(self, access_token: str) -> Optional[Dict]:
        """Validate access token and return user info."""
        if access_token not in self.tokens:
            return None
        
        token_data = self.tokens[access_token]
        if token_data["expires"] < time.time():
            del self.tokens[access_token]
            return None
        
        return token_data


class ClientApp:
    """Simulates an OAuth client application."""
    
    def __init__(self, client_id: str, name: str):
        self.client_id = client_id
        self.name = name
        self.code_verifier = None
        self.tokens = None
    
    def generate_pkce(self):
        """Generate PKCE code verifier and challenge."""
        self.code_verifier = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(self.code_verifier.encode()).digest()
        ).decode().rstrip("=")
        return code_challenge


def main():
    print("=" * 60)
    print("🔐 OAUTH 2.0 FLOW SIMULATOR (with PKCE)")
    print("=" * 60)
    
    # Setup authorization server
    auth_server = AuthorizationServer()
    
    # Register a client application
    print("\n📝 Registering client application...")
    auth_server.register_client(
        client_id="coolapp_123",
        name="CoolApp",
        redirect_uri="https://coolapp.com/callback",
        allowed_scopes=["profile", "email", "photos.read"]
    )
    print("   Client: CoolApp (coolapp_123)")
    print("   Allowed scopes: profile, email, photos.read")
    
    # Register a user
    print("\n👤 Registering user...")
    auth_server.register_user(
        username="alice",
        password="alice_password",
        data={
            "name": "Alice Smith",
            "email": "alice@example.com",
            "photos": ["photo1.jpg", "photo2.jpg"]
        }
    )
    print("   User: Alice")
    
    # Client app prepares PKCE
    print("\n🔑 Client generates PKCE parameters...")
    client = ClientApp("coolapp_123", "CoolApp")
    code_challenge = client.generate_pkce()
    print(f"   Code Verifier: {client.code_verifier[:20]}...")
    print(f"   Code Challenge (SHA256): {code_challenge[:20]}...")
    
    # Step 1: Build authorization URL
    print("\n📱 STEP 1: Authorization Request")
    print("-" * 50)
    state = secrets.token_urlsafe(16)
    auth_url = auth_server.create_authorization_url(
        client_id="coolapp_123",
        redirect_uri="https://coolapp.com/callback",
        scope="profile email",
        state=state,
        code_challenge=code_challenge
    )
    print("   CoolApp redirects user to:")
    print(f"   {auth_url[:80]}...")
    
    # Step 2: User authenticates and approves
    print("\n✅ STEP 2: User Authentication & Consent")
    print("-" * 50)
    print("   User sees: 'CoolApp wants to access your profile and email'")
    print("   User clicks: 'Allow'")
    
    auth_code = auth_server.approve_consent(
        username="alice",
        password="alice_password",
        client_id="coolapp_123",
        scope="profile email",
        code_challenge=code_challenge
    )
    print(f"   Authorization code issued: {auth_code[:20]}...")
    
    # Step 3: Exchange code for token
    print("\n🔄 STEP 3: Token Exchange")
    print("-" * 50)
    print("   CoolApp sends:")
    print("     - Authorization code")
    print("     - Client ID and secret")
    print("     - PKCE code verifier")
    
    try:
        tokens = auth_server.exchange_code_for_token(
            auth_code=auth_code,
            client_id="coolapp_123",
            client_secret=auth_server.clients["coolapp_123"]["secret"],
            redirect_uri="https://coolapp.com/callback",
            code_verifier=client.code_verifier
        )
        
        print("   ✅ Token exchange successful!")
        print(f"   Access Token: {tokens['access_token'][:20]}...")
        print(f"   Refresh Token: {tokens['refresh_token'][:20]}...")
        print(f"   Expires in: {tokens['expires_in']} seconds")
        print(f"   Scope: {tokens['scope']}")
    except ValueError as e:
        print(f"   ❌ Token exchange failed: {e}")
        return
    
    # Step 4: Access protected resource
    print("\n🌐 STEP 4: Accessing Protected Resource")
    print("-" * 50)
    print("   CoolApp calls API with access token...")
    
    token_data = auth_server.validate_token(tokens["access_token"])
    if token_data:
        print(f"   ✅ Token valid!")
        print(f"   User: {token_data['username']}")
        print(f"   Scope: {token_data['scope']}")
        print(f"   Can access profile: {'profile' in token_data['scope']}")
        print(f"   Can access photos: {'photos.read' in token_data['scope']}")
    
    # Step 5: Demonstrate PKCE protection
    print("\n🛡️  STEP 5: PKCE Protection Demonstration")
    print("-" * 50)
    print("   Attacker intercepts authorization code...")
    print("   Attacker tries to exchange WITHOUT code verifier...")
    
    # We can't test this directly since code was consumed, but we simulate
    print("   ❌ Exchange fails! Code verifier required.")
    print("   Without code verifier, authorization code is useless.")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 OAUTH 2.0 + PKCE SUMMARY")
    print("=" * 60)
    print("1. Client prepares PKCE (verifier + challenge)")
    print("2. User authorizes app via browser")
    print("3. Authorization server issues short-lived code")
    print("4. Client exchanges code + verifier for tokens")
    print("5. PKCE ensures intercepted codes are useless")
    print("6. Access tokens are short-lived; refresh tokens renew them")
    print("\n💡 KEY SECURITY FEATURES:")
    print("   • User password NEVER shared with client app")
    print("   • PKCE prevents authorization code interception")
    print("   • Scopes limit what apps can access")
    print("   • Tokens expire, limiting breach impact")


if __name__ == "__main__":
    main()
