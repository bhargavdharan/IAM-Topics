#!/usr/bin/env python3
"""
SAML Assertion Generator and Validator
======================================
Generates and validates SAML 2.0 assertions:
- Creates signed SAML assertions
- Validates signatures and conditions
- Demonstrates XML structure

Run: python saml_assertion_gen.py
"""

import base64
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, tostring


class SAMLAssertion:
    """Represents a SAML 2.0 Assertion."""
    
    def __init__(self, issuer: str, subject: str, audience: str,
                 attributes: dict = None):
        self.id = f"_{secrets.token_hex(16)}"
        self.issuer = issuer
        self.subject = subject
        self.audience = audience
        self.attributes = attributes or {}
        self.issue_instant = datetime.utcnow()
        self.not_before = self.issue_instant - timedelta(minutes=5)
        self.not_on_or_after = self.issue_instant + timedelta(minutes=5)
        self.authn_instant = self.issue_instant
        
        # Simulated private/public key pair
        self.private_key = secrets.token_hex(32)
        self.public_key = self.private_key  # Simplified
    
    def to_xml(self) -> str:
        """Generate SAML assertion XML."""
        # Root element
        assertion = Element("saml:Assertion")
        assertion.set("xmlns:saml", "urn:oasis:names:tc:SAML:2.0:assertion")
        assertion.set("ID", self.id)
        assertion.set("IssueInstant", self.issue_instant.isoformat() + "Z")
        assertion.set("Version", "2.0")
        
        # Issuer
        issuer_elem = SubElement(assertion, "saml:Issuer")
        issuer_elem.text = self.issuer
        
        # Signature (simplified)
        signature = SubElement(assertion, "ds:Signature")
        sig_info = SubElement(signature, "ds:SignedInfo")
        sig_value = SubElement(signature, "ds:SignatureValue")
        sig_value.text = self._generate_signature()
        
        # Subject
        subject = SubElement(assertion, "saml:Subject")
        name_id = SubElement(subject, "saml:NameID")
        name_id.set("Format", "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress")
        name_id.text = self.subject
        
        subject_confirm = SubElement(subject, "saml:SubjectConfirmation")
        subject_confirm.set("Method", "urn:oasis:names:tc:SAML:2.0:cm:bearer")
        confirm_data = SubElement(subject_confirm, "saml:SubjectConfirmationData")
        confirm_data.set("NotOnOrAfter", self.not_on_or_after.isoformat() + "Z")
        confirm_data.set("Recipient", self.audience)
        
        # Conditions
        conditions = SubElement(assertion, "saml:Conditions")
        conditions.set("NotBefore", self.not_before.isoformat() + "Z")
        conditions.set("NotOnOrAfter", self.not_on_or_after.isoformat() + "Z")
        
        audience_restrict = SubElement(conditions, "saml:AudienceRestriction")
        audience_elem = SubElement(audience_restrict, "saml:Audience")
        audience_elem.text = self.audience
        
        # AuthnStatement
        authn = SubElement(assertion, "saml:AuthnStatement")
        authn.set("AuthnInstant", self.authn_instant.isoformat() + "Z")
        authn_context = SubElement(authn, "saml:AuthnContext")
        authn_context_class = SubElement(authn_context, "saml:AuthnContextClassRef")
        authn_context_class.text = "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport"
        
        # AttributeStatement
        if self.attributes:
            attr_statement = SubElement(assertion, "saml:AttributeStatement")
            for attr_name, attr_value in self.attributes.items():
                attr = SubElement(attr_statement, "saml:Attribute")
                attr.set("Name", attr_name)
                attr_val = SubElement(attr, "saml:AttributeValue")
                attr_val.text = str(attr_value)
        
        return tostring(assertion, encoding="unicode")
    
    def _generate_signature(self) -> str:
        """Generate a simplified digital signature."""
        data = f"{self.issuer}{self.subject}{self.audience}{self.id}"
        return hashlib.sha256((data + self.private_key).encode()).hexdigest()
    
    def validate(self, public_key: str, expected_audience: str) -> dict:
        """Validate the assertion."""
        results = {
            "valid": True,
            "checks": []
        }
        
        # Check signature
        expected_sig = hashlib.sha256(
            (f"{self.issuer}{self.subject}{self.audience}{self.id}" + public_key).encode()
        ).hexdigest()
        
        if expected_sig != self._generate_signature():
            results["valid"] = False
            results["checks"].append("❌ Signature invalid")
        else:
            results["checks"].append("✅ Signature valid")
        
        # Check audience
        if self.audience != expected_audience:
            results["valid"] = False
            results["checks"].append(f"❌ Wrong audience: {self.audience} (expected {expected_audience})")
        else:
            results["checks"].append("✅ Audience correct")
        
        # Check expiration
        now = datetime.utcnow()
        if now > self.not_on_or_after:
            results["valid"] = False
            results["checks"].append("❌ Assertion expired")
        else:
            results["checks"].append("✅ Not expired")
        
        if now < self.not_before:
            results["valid"] = False
            results["checks"].append("❌ Assertion not yet valid")
        else:
            results["checks"].append("✅ Within valid time window")
        
        return results
    
    def encode(self) -> str:
        """Base64 encode the assertion for transport."""
        xml = self.to_xml()
        return base64.b64encode(xml.encode()).decode()


class SAMLIdentityProvider:
    """Simulates a SAML Identity Provider."""
    
    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self.users = {}
        self.assertions = {}
    
    def register_user(self, email: str, attributes: dict):
        self.users[email] = attributes
    
    def create_assertion(self, user_email: str, sp_entity_id: str) -> SAMLAssertion:
        if user_email not in self.users:
            raise ValueError("User not found")
        
        assertion = SAMLAssertion(
            issuer=self.entity_id,
            subject=user_email,
            audience=sp_entity_id,
            attributes=self.users[user_email]
        )
        
        self.assertions[assertion.id] = assertion
        return assertion


class SAMLServiceProvider:
    """Simulates a SAML Service Provider."""
    
    def __init__(self, entity_id: str, idp_entity_id: str, idp_public_key: str):
        self.entity_id = entity_id
        self.idp_entity_id = idp_entity_id
        self.idp_public_key = idp_public_key
        self.consumed_assertions = set()
    
    def process_assertion(self, encoded_assertion: str) -> dict:
        """Process and validate a SAML assertion."""
        print(f"\n🔑 {self.entity_id} processing SAML assertion...")
        
        # Decode
        try:
            xml = base64.b64decode(encoded_assertion).decode()
        except Exception:
            return {"valid": False, "error": "Invalid encoding"}
        
        # In a real implementation, we'd parse the XML
        # For simulation, we'd need to reconstruct the assertion
        # This is simplified
        
        print("   Decoded assertion (first 200 chars):")
        print(f"   {xml[:200]}...")
        
        return {"valid": True, "message": "Assertion processed (simulated)"}


def main():
    print("=" * 60)
    print("📜 SAML ASSERTION GENERATOR & VALIDATOR")
    print("=" * 60)
    
    # Setup IdP and SP
    idp = SAMLIdentityProvider("https://idp.company.com")
    idp.register_user("alice@company.com", {
        "Role": "Manager",
        "Department": "Engineering",
        "EmployeeID": "E12345"
    })
    
    # Create assertion
    print("\n🏢 Creating SAML assertion for alice@company.com...")
    assertion = idp.create_assertion("alice@company.com", "https://app.salesforce.com")
    
    print(f"\n📄 Assertion Details:")
    print(f"   ID: {assertion.id}")
    print(f"   Issuer: {assertion.issuer}")
    print(f"   Subject: {assertion.subject}")
    print(f"   Audience: {assertion.audience}")
    print(f"   Issued: {assertion.issue_instant}")
    print(f"   Expires: {assertion.not_on_or_after}")
    print(f"   Attributes: {assertion.attributes}")
    
    # Show XML structure
    print(f"\n🔍 SAML Assertion XML Structure:")
    xml = assertion.to_xml()
    print(xml[:800] + "..." if len(xml) > 800 else xml)
    
    # Validate
    print(f"\n✅ Validating assertion...")
    results = assertion.validate(assertion.public_key, "https://app.salesforce.com")
    for check in results["checks"]:
        print(f"   {check}")
    print(f"   Overall: {'VALID' if results['valid'] else 'INVALID'}")
    
    # Try wrong audience
    print(f"\n🧪 Testing with wrong audience...")
    bad_results = assertion.validate(assertion.public_key, "https://evil.com")
    for check in bad_results["checks"]:
        print(f"   {check}")
    
    # Encode for transport
    encoded = assertion.encode()
    print(f"\n📤 Base64-encoded for transport:")
    print(f"   {encoded[:100]}...")
    
    print("\n" + "=" * 60)
    print("📋 SAML KEY CONCEPTS")
    print("=" * 60)
    print("• Assertions are XML documents signed by the IdP")
    print("• Subject contains the user's identifier")
    print("• Audience restriction prevents token misuse")
    print("• Time conditions prevent replay attacks")
    print("• Attributes carry user information (roles, department)")
    print("• Digital signature ensures authenticity and integrity")


if __name__ == "__main__":
    main()
