# 10. SAML and Enterprise Federation

## What Is SAML?

**SAML (Security Assertion Markup Language)** is an XML-based standard for exchanging authentication and authorization data between an Identity Provider (IdP) and a Service Provider (SP). It is the dominant protocol for enterprise single sign-on.

While OAuth/OIDC power consumer applications, SAML remains the backbone of B2B and enterprise identity federation.

---

## Why Learn This?

SAML has been the enterprise standard since 2005. It is supported by virtually every enterprise application. Understanding SAML is essential for:
- Integrating with enterprise identity providers
- Configuring SSO for SaaS applications
- Understanding legacy federation architectures
- Working in regulated industries

---

## Core Concepts

### SAML Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Identity Provider (IdP)** | Authenticates users and issues assertions | Company's Active Directory Federation Services |
| **Service Provider (SP)** | Application that trusts the IdP | Salesforce, Workday, internal apps |
| **Assertion** | XML document vouching for the user | "Alice authenticated at 10:00 AM with Manager role" |
| **Subject** | The user being authenticated | alice@company.com |
| **Attribute** | Additional information about the user | Department=Engineering, Role=Manager |

### Types of SAML Assertions

| Type | Purpose |
|------|---------|
| **Authentication Assertion** | States that the user authenticated at a specific time, using a specific method |
| **Attribute Assertion** | Transmits user attributes like department, role, or email |
| **Authorization Decision Assertion** | States whether the user is permitted to access a specific resource |

### SAML Bindings

Bindings define HOW SAML messages are transported:

| Binding | Transport | Use Case |
|---------|-----------|----------|
| **HTTP Redirect** | URL parameters | IdP-initiated SSO |
| **HTTP POST** | HTML form | SP-initiated SSO (most common) |
| **HTTP Artifact** | Small reference + back-channel retrieval | High-security environments |

### SAML Profiles

| Profile | Purpose |
|---------|---------|
| **Web Browser SSO** | User logs in via browser |
| **Single Logout** | Logging out of one app logs out of all |
| **Artifact Resolution** | Secure assertion retrieval |

---

## How It Works

### SAML Assertion Structure

A SAML assertion contains:
- **Issuer:** Who vouches for this
- **Digital Signature:** Proves authenticity
- **Subject:** Who this is about
- **Conditions:** Validity window (NotBefore, NotOnOrAfter)
- **AuthnStatement:** How and when the user authenticated
- **AttributeStatement:** User attributes like roles and department

**Digital signatures are critical:** The assertion is signed by the IdP. The SP verifies this signature using the IdP's public certificate. If the signature does not match, the assertion is rejected.

### SP-Initiated vs IdP-Initiated SSO

**SP-initiated (preferred):**
1. User clicks "Company Login" on Salesforce
2. Salesforce generates a SAML Request and redirects to IdP
3. IdP authenticates user
4. IdP sends SAML Response back to Salesforce
5. Salesforce validates Response (matches Request ID)

**IdP-initiated:**
1. User logs into Company Portal
2. User clicks "Salesforce" icon
3. IdP sends SAML Response to Salesforce

**Why SP-initiated is preferred:** The SAML Request contains a unique ID that must match the SAML Response, preventing replay attacks.

### Trust Metadata

IdPs and SPs exchange metadata XML files containing:
- Entity IDs
- Endpoint URLs
- X.509 certificates for signature verification

**The X.509 certificate is the trust anchor.** The SP uses this certificate to verify that SAML assertions were actually signed by the IdP.

### SAML vs OIDC

| Aspect | SAML | OIDC |
|--------|------|------|
| Data format | XML | JSON (JWT) |
| Complexity | Higher | Lower |
| Mobile support | Poorer | Better |
| Enterprise adoption | Dominant | Growing |
| Best for | Enterprise SSO | Modern web/mobile apps |

---

## Where You See It

| Product | SAML Use |
|---------|----------|
| **Salesforce** | Enterprise SSO via SAML |
| **Workday** | HR system federation |
| **ServiceNow** | IT service management SSO |
| **Shibboleth** | Academic federation |
| **AD FS** | Windows-based federation |
| **Okta** | SAML provider for thousands of apps |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "SAML is outdated" | SAML is mature and widely supported; it is not going away in enterprise |
| "SAML assertions are encrypted by default" | Assertions are signed by default; encryption is optional |
| "IdP-initiated is as secure as SP-initiated" | SP-initiated includes request/response correlation that prevents replay |
| "SAML and OIDC are competitors" | They serve different use cases; many organizations use both |

---

## How to Practice

1. **Read a SAML assertion**
   - If your organization uses SAML, use a browser extension or proxy to capture the SAMLResponse
   - Decode it (Base64) and examine the XML structure
   - Identify the issuer, subject, attributes, and conditions

2. **Compare SAML and OIDC for your use case**
   - Building a mobile app? OIDC is likely better.
   - Integrating with an enterprise HR system? SAML is likely required.

3. **Run the simulations**
   - `saml_assertion_gen.py` generates and signs assertions
   - `saml_validator.py` validates signatures and conditions

---

## Projects

### `saml_assertion_gen.py`
Generates and signs SAML assertions:
- Creates SAML 2.0 assertions
- Signs with X.509 certificates
- Includes authentication, attribute, and condition statements

### `saml_validator.py`
Validates SAML assertions:
- Verifies XML signatures
- Checks time conditions
- Validates audience restrictions
- Detects replay attacks

### `federation_metadata_manager.py`
Manages SAML federation metadata:
- Parses IdP and SP metadata
- Extracts endpoints and certificates
- Validates metadata signatures

---

## Check Your Understanding

1. What is the difference between an Authentication Assertion and an Attribute Assertion?
2. Why is the digital signature on a SAML assertion critical?
3. What is the difference between SP-initiated and IdP-initiated SSO?
4. How does SAML prevent replay attacks through the `InResponseTo` attribute?
5. When would an organization choose SAML over OpenID Connect?
