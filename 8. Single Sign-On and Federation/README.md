# 8. Single Sign-On (SSO) and Federation

## 🏠 Real-World Analogy: The Theme Park Wristband

Imagine visiting a massive theme park resort:

- At the entrance, you show your ID and ticket → They verify you're a paying guest
- They put a **special wristband** on your arm
- For the rest of the day, you simply tap your wristband to:
  - Enter rides
  - Buy food
  - Open your hotel room
  - Access the water park

**You never have to show your ID or wallet again.** The wristband proves who you are to every service in the resort.

**SSO is the digital wristband.** Log in once, access everything.

---

## 📋 Overview

Single Sign-On (SSO) allows users to authenticate once and gain access to multiple applications without logging in again. Federation extends this concept across organizational boundaries.

**Why SSO matters:**
- Users hate remembering 50 passwords
- Password fatigue leads to weak passwords and reuse
- IT spends enormous resources on password resets
- Centralized authentication = centralized security control

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain SSO with real-world analogies
- Describe the difference between SSO and Federation
- Understand identity tokens (SAML, OIDC)
- Explain trust relationships between identity providers and service providers
- Identify SSO security risks and mitigations

---

## 📚 Key Concepts

### SSO vs Federation

| Aspect | SSO | Federation |
|--------|-----|------------|
| **Scope** | Within one organization | Across multiple organizations |
| **Example** | Company apps share one login | University library access for students |
| **Trust** | Internal trust | External trust agreement |
| **Protocols** | Kerberos, SAML, OIDC | SAML, OIDC, WS-Federation |

### Key Players

| Term | Definition | Theme Park Analogy |
|------|-----------|-------------------|
| **Identity Provider (IdP)** | Verifies who you are | Entrance gate that checks your ticket |
| **Service Provider (SP)** | Application you want to use | Individual rides and restaurants |
| **User/Principal** | The person logging in | You, the guest |
| **Token/Assertion** | Proof of identity | The wristband |

### How SSO Works (Simplified)

```
1. User opens Gmail (SP)
2. Gmail: "I don't know who you are. Go ask Google Identity (IdP)."
3. User goes to Google Identity
4. Google Identity: "Enter your password"
5. User enters password
6. Google Identity creates a signed token: "This is Alice, authenticated at 10:00 AM"
7. User brings token back to Gmail
8. Gmail verifies Google's signature on the token
9. Gmail: "Welcome, Alice!"
```

**The magic:** Gmail NEVER sees your password. It trusts Google's say-so.

### SSO Protocols

| Protocol | Data Format | Best For | Complexity |
|----------|------------|----------|------------|
| **SAML 2.0** | XML | Enterprise, B2B | High |
| **OpenID Connect** | JSON (JWT) | Web apps, mobile | Medium |
| **Kerberos** | Binary tickets | Windows networks | Medium |
| **CAS** | XML/JSON | Education | Low |

### Trust Establishment

Before SSO works, the IdP and SP must establish trust:

1. **Exchange metadata:** Share URLs, certificates, endpoints
2. **Certificate trust:** SP trusts IdP's digital signature
3. **User mapping:** Agree on how to identify users (email, employee ID)

**Analogy:** The theme park resort and the nearby water park sign a contract. The wristband from the resort is accepted at the water park because they trust each other.

---

## 🔧 Under the Hood

### SAML Assertions

SAML (Security Assertion Markup Language) is the enterprise standard for SSO. The core artifact is the **SAML Assertion** — an XML document that says "I vouch for this user."

```xml
<saml:Assertion>
  <saml:Issuer>https://company-idp.com</saml:Issuer>
  <saml:Subject>
    <saml:NameID>alice@company.com</saml:NameID>
  </saml:Subject>
  <saml:Conditions NotBefore="2024-01-15T10:00:00Z" 
                   NotOnOrAfter="2024-01-15T10:05:00Z"/>
  <saml:AttributeStatement>
    <saml:Attribute Name="Role">
      <saml:AttributeValue>Manager</saml:AttributeValue>
    </saml:Attribute>
    <saml:Attribute Name="Department">
      <saml:AttributeValue>Engineering</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
</saml:Assertion>
```

**Key elements:**
- **Issuer:** Who vouches for this (the IdP)
- **Subject:** Who this is about (the user)
- **Conditions:** When this assertion is valid (prevents replay attacks)
- **Attributes:** Extra information about the user (roles, department)

**Digital Signature:** The assertion is digitally signed by the IdP. The SP verifies this signature using the IdP's public certificate. If the signature doesn't match, the assertion is rejected.

### SAML Flow (SP-Initiated)

```
User ──→ SP (app) ──→ "Redirect to IdP"
  │                       │
  │←────── Redirect ──────┘
  │
  └────→ IdP ──→ "Enter credentials"
            │
            └──→ "Create signed SAML Assertion"
            │
  │←────── POST Assertion ───┘
  │
  └────→ SP ──→ Verify signature ──→ "Access granted"
```

### OpenID Connect (OIDC) for SSO

OIDC is built on OAuth 2.0 and uses JSON Web Tokens (JWT) instead of XML:

```json
{
  "iss": "https://accounts.google.com",
  "sub": "1234567890",
  "name": "Alice Smith",
  "email": "alice@company.com",
  "iat": 1516239022,
  "exp": 1516239322,
  "roles": ["Manager", "Engineering"]
}
```

**Why OIDC is popular:**
- JSON is easier to parse than XML
- Works natively with JavaScript/web apps
- Supports mobile apps better
- Simpler protocol

### SSO Security Risks

| Risk | How It Happens | Prevention |
|------|---------------|------------|
| **Token theft** | Session cookie stolen via XSS | HttpOnly cookies, short expiration |
| **Replay attacks** | Intercepted assertion reused | Short validity windows, unique IDs |
| **IdP compromise** | Attacker controls identity provider | Strong IdP security, MFA on admin accounts |
| **SP misconfiguration** | Accepts assertions from wrong IdP | Strict certificate validation |
| **Logout issues** | User logs out of one app, others stay open | Single Logout (SLO) protocols |

---

## 🛠️ Projects in This Module

### `sso_token_flow.py`
Simulates SSO token exchange:
- Generates SAML-style assertions
- Signs and verifies tokens
- Simulates IdP-SP trust validation
- Demonstrates token expiration and replay prevention

### `federation_trust_sim.py`
Models trust relationships between organizations:
- Creates identity provider metadata
- Establishes trust through certificate exchange
- Simulates cross-organizational authentication
- Demonstrates attribute mapping

### `saml_assertion_inspector.py`
Parses and validates SAML assertions:
- Extracts issuer, subject, attributes
- Verifies digital signatures
- Checks time validity
- Identifies security issues

---

## 📝 Quiz Questions

1. **What is the difference between SSO and Federation? Give a real-world example of each.**
2. **In SSO, why does the Service Provider never see the user's password?**
3. **What is a SAML Assertion and what key information does it contain?**
4. **How does digital signature verification prevent fake assertions?**
5. **Why is OpenID Connect often preferred over SAML for modern web applications?**

---

## 🔗 Further Reading

- [SAML 2.0 Technical Overview](https://wiki.shibboleth.net/confluence/display/CONCEPT/SAML2Intro)
- [OpenID Connect Core Specification](https://openid.net/specs/openid-connect-core-1_0.html)
- [SSO Security Best Practices - CISA](https://www.cisa.gov)

---

## 🏷️ Tags
`#SSO` `#SingleSignOn` `#Federation` `#SAML` `#OpenIDConnect` `#IdentityProvider` `#ServiceProvider`
