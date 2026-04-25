#!/usr/bin/env python3
"""
Decentralized Identity Demonstration
====================================
Demonstrates decentralized identity concepts:
- DID generation
- Verifiable credential creation and signing
- Credential presentation and verification
- Revocation checking

Run: python decentralized_id_demo.py
"""

import hashlib
import secrets
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class DID:
    """Decentralized Identifier."""
    did: str
    public_key: str
    controller: str
    
    @classmethod
    def create(cls, method: str = "example") -> "DID":
        public_key = secrets.token_hex(32)
        did_id = hashlib.sha256(public_key.encode()).hexdigest()[:32]
        return cls(
            did=f"did:{method}:{did_id}",
            public_key=public_key,
            controller=f"did:{method}:{did_id}"
        )


@dataclass
class VerifiableCredential:
    """A cryptographically signed credential."""
    id: str
    issuer: str
    subject: str
    claims: Dict
    issuance_date: float
    expiration_date: float
    proof: Dict = field(default_factory=dict)
    revoked: bool = False
    
    def sign(self, issuer_private_key: str):
        """Sign the credential."""
        data = f"{self.issuer}{self.subject}{self.claims}{self.issuance_date}"
        signature = hashlib.sha256((data + issuer_private_key).encode()).hexdigest()
        self.proof = {
            "type": "SimpleSignature2024",
            "created": time.time(),
            "proofValue": signature
        }


@dataclass
class VerifiablePresentation:
    """A presentation of credentials to a verifier."""
    holder: str
    credentials: List[VerifiableCredential]
    challenge: str
    domain: str
    proof: Dict = field(default_factory=dict)
    
    def sign(self, holder_private_key: str):
        """Sign the presentation."""
        data = f"{self.holder}{self.challenge}{self.domain}"
        signature = hashlib.sha256((data + holder_private_key).encode()).hexdigest()
        self.proof = {
            "type": "SimpleSignature2024",
            "created": time.time(),
            "proofValue": signature
        }


class DecentralizedIdentitySystem:
    """Simulates a decentralized identity ecosystem."""
    
    def __init__(self):
        self.dids: Dict[str, DID] = {}
        self.credentials: Dict[str, VerifiableCredential] = {}
        self.revocation_list: set = set()
        self.private_keys: Dict[str, str] = {}  # In reality, never stored centrally!
    
    def create_identity(self, name: str) -> DID:
        """Create a new decentralized identity."""
        did = DID.create()
        self.dids[did.did] = did
        # Store "private key" (simulated - in reality in user's wallet)
        self.private_keys[did.did] = secrets.token_hex(32)
        
        print(f"\n🆔 Created identity for {name}:")
        print(f"   DID: {did.did}")
        print(f"   Public Key: {did.public_key[:20]}...")
        return did
    
    def issue_credential(self, issuer_did: str, subject_did: str, 
                        claims: Dict) -> VerifiableCredential:
        """Issue a verifiable credential."""
        if issuer_did not in self.dids:
            raise ValueError("Invalid issuer DID")
        
        vc = VerifiableCredential(
            id=f"urn:uuid:{secrets.token_hex(16)}",
            issuer=issuer_did,
            subject=subject_did,
            claims=claims,
            issuance_date=time.time(),
            expiration_date=time.time() + 31536000  # 1 year
        )
        
        # Sign with issuer's private key
        issuer_key = self.private_keys[issuer_did]
        vc.sign(issuer_key)
        
        self.credentials[vc.id] = vc
        
        print(f"\n📜 Issued credential:")
        print(f"   ID: {vc.id}")
        print(f"   Issuer: {vc.issuer}")
        print(f"   Subject: {vc.subject}")
        print(f"   Claims: {vc.claims}")
        print(f"   Signature: {vc.proof['proofValue'][:20]}...")
        return vc
    
    def verify_credential(self, vc: VerifiableCredential) -> bool:
        """Verify a credential's signature and status."""
        if vc.id in self.revocation_list:
            print(f"   ❌ Credential {vc.id} has been revoked")
            return False
        
        # Verify signature
        issuer_key = self.dids[vc.issuer].public_key
        data = f"{vc.issuer}{vc.subject}{vc.claims}{vc.issuance_date}"
        expected_sig = hashlib.sha256((data + self.private_keys[vc.issuer]).encode()).hexdigest()
        
        if vc.proof.get("proofValue") == expected_sig:
            print(f"   ✅ Credential signature valid")
            return True
        else:
            print(f"   ❌ Invalid signature")
            return False
    
    def create_presentation(self, holder_did: str, 
                           credential_ids: List[str],
                           challenge: str,
                           domain: str) -> VerifiablePresentation:
        """Create a verifiable presentation."""
        credentials = [self.credentials[cid] for cid in credential_ids if cid in self.credentials]
        
        vp = VerifiablePresentation(
            holder=holder_did,
            credentials=credentials,
            challenge=challenge,
            domain=domain
        )
        
        # Sign with holder's private key
        vp.sign(self.private_keys[holder_did])
        
        print(f"\n📨 Created presentation:")
        print(f"   Holder: {vp.holder}")
        print(f"   Credentials: {len(vp.credentials)}")
        print(f"   Challenge: {vp.challenge}")
        print(f"   Domain: {vp.domain}")
        return vp
    
    def verify_presentation(self, vp: VerifiablePresentation) -> bool:
        """Verify a presentation and all contained credentials."""
        print(f"\n🔍 Verifying presentation from {vp.holder}...")
        
        # Verify holder signature
        holder_key = self.private_keys[vp.holder]
        data = f"{vp.holder}{vp.challenge}{vp.domain}"
        expected_sig = hashlib.sha256((data + holder_key).encode()).hexdigest()
        
        if vp.proof.get("proofValue") != expected_sig:
            print("   ❌ Holder signature invalid")
            return False
        print("   ✅ Holder signature valid")
        
        # Verify each credential
        for vc in vp.credentials:
            if not self.verify_credential(vc):
                return False
        
        print("   ✅ All credentials verified")
        return True
    
    def revoke_credential(self, credential_id: str):
        """Revoke a credential."""
        self.revocation_list.add(credential_id)
        if credential_id in self.credentials:
            self.credentials[credential_id].revoked = True
        print(f"\n🚫 Revoked credential: {credential_id}")


def main():
    print("=" * 60)
    print("🔗 DECENTRALIZED IDENTITY DEMONSTRATION")
    print("=" * 60)
    
    system = DecentralizedIdentitySystem()
    
    # Create identities
    print("\n🏢 Creating identities...")
    alice = system.create_identity("Alice (Job Seeker)")
    university = system.create_identity("State University (Issuer)")
    employer = system.create_identity("TechCorp (Verifier)")
    
    # University issues degree credential to Alice
    print("\n🎓 University issues degree credential to Alice...")
    degree_vc = system.issue_credential(
        issuer_did=university.did,
        subject_did=alice.did,
        claims={
            "type": "BachelorDegree",
            "field": "Computer Science",
            "graduationDate": "2023-05-15",
            "gpa": "3.8"
        }
    )
    
    # Alice creates a presentation for TechCorp
    print("\n👩‍💼 Alice creates presentation for job application...")
    # She selectively discloses (in real SSI, she could hide GPA)
    vp = system.create_presentation(
        holder_did=alice.did,
        credential_ids=[degree_vc.id],
        challenge="login_challenge_12345",
        domain="techcorp.com"
    )
    
    # TechCorp verifies
    print("\n🏢 TechCorp verifies Alice's credentials...")
    is_valid = system.verify_presentation(vp)
    
    if is_valid:
        print("\n✅ Alice's degree is verified! She's hired!")
    
    # Scenario: Credential revocation
    print("\n" + "=" * 60)
    print("📋 SCENARIO: Credential Revocation")
    print("=" * 60)
    
    print("\nOh no! University discovers Alice's degree was fraudulent...")
    system.revoke_credential(degree_vc.id)
    
    print("\nTechCorp re-verifies Alice's application...")
    is_valid = system.verify_presentation(vp)
    
    if not is_valid:
        print("\n❌ Alice's degree is revoked. Application rejected.")
    
    # Summary
    print("\n" + "=" * 60)
    print("💡 DECENTRALIZED IDENTITY CONCEPTS")
    print("=" * 60)
    print("• DIDs are self-controlled identifiers (no central authority)")
    print("• Verifiable Credentials are cryptographically signed")
    print("• Holders store credentials in their digital wallet")
    print("• Presentations prove ownership without revealing everything")
    print("• Revocation is tracked without centralized databases")
    print("• Privacy: Selective disclosure possible (show degree, hide GPA)")


if __name__ == "__main__":
    main()
