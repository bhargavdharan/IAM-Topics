# 8. Single Sign-On (SSO) and Federation

## What Is SSO?

**Single Sign-On (SSO)** allows a user to authenticate once and gain access to multiple applications without entering credentials again.

**Federation** extends this concept across organizational boundaries — allowing users from one organization to access resources in another using their home organization's credentials.

---

## Why Learn This?

Password fatigue is real. Users with dozens of accounts reuse passwords, write them down, or forget them. IT departments spend enormous resources on password resets. SSO addresses these problems while centralizing security control.

Understanding SSO and Federation enables you to:
- Design login architectures for multi-application environments
- Integrate with identity providers
- Evaluate SSO security risks
- Implement SAML and OIDC connections

---

## Core Concepts

### Key Players

| Term | Definition | Example |
|------|-----------|---------|
| **Identity Provider (IdP)** | Authenticates users and issues identity tokens | Google, Okta, Azure AD, your company's login server |
| **Service Provider (SP)** | Application that trusts the IdP | Gmail, Salesforce, your internal app |
| **User/Principal** | The person logging in | You |
| **Token/Assertion** | Cryptographic proof of authentication | SAML Assertion, JWT ID Token |

### How SSO Works

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

**Critical point:** Gmail NEVER sees your password. It trusts Google's say-so.

### SSO vs Federation

| Aspect | SSO | Federation |
|--------|-----|------------|
| Scope | Within one organization | Across multiple organizations |
| Example | Company apps share one login | University students access library databases |
| Trust | Internal trust | External trust agreement |
| Protocols | Kerberos, SAML, OIDC | SAML, OIDC, WS-Federation |

### Trust Establishment

Before SSO works, the IdP and SP must establish trust:
1. **Exchange metadata:** Share URLs, certificates, endpoints
2. **Certificate trust:** SP trusts IdP's digital signature
3. **User mapping:** Agree on how to identify users (email, employee ID)

---

## How It Works

### SAML Assertions

SAML (Security Assertion Markup Language) is the enterprise standard for SSO. The core artifact is the **SAML Assertion** — a digitally signed XML document stating "I vouch for this user."

**Key elements:**
- **Issuer:** Who vouches for this (the IdP)
- **Subject:** Who this is about (the user)
- **Conditions:** When this assertion is valid (prevents replay)
- **Attributes:** Extra information (roles, department)
- **Digital Signature:** Proves the assertion came from the IdP and was not tampered with

**SP-initiated vs IdP-initiated:**
- **SP-initiated:** User starts at the application. More secure because the request and response are correlated.
- **IdP-initiated:** User starts at the identity portal. Slightly less secure but more convenient.

### OpenID Connect (OIDC)

OIDC is built on OAuth 2.0 and uses JSON Web Tokens (JWT) instead of XML:

```json
{
  "iss": "https://accounts.google.com",
  "sub": "1234567890",
  "name": "Alice Smith",
  "email": "alice@company.com",
  "iat": 1516239022,
  "exp": 1516239322
}
```

**Why OIDC is popular:**
- JSON is easier to parse than XML
- Works natively with web and mobile applications
- Simpler protocol than SAML

### SSO Security Risks

| Risk | How It Happens | Prevention |
|------|---------------|------------|
| **Token theft** | Session cookie stolen via XSS | HttpOnly cookies, short expiration |
| **Replay attacks** | Intercepted assertion reused | Short validity windows, unique IDs |
| **IdP compromise** | Attacker controls identity provider | Strong IdP security, MFA on admin accounts |
| **SP misconfiguration** | Accepts assertions from wrong IdP | Strict certificate validation |
| **Logout issues** | User logs out of one app, others stay open | Single Logout (SLO) protocols |

---

## Where You See It

| Product | Protocol | Use Case |
|---------|----------|----------|
| **Okta** | SAML, OIDC | Enterprise SSO for hundreds of apps |
| **Azure AD** | SAML, OIDC | Microsoft 365 and cloud app integration |
| **Google Workspace** | OIDC | Consumer and business login |
| **Shibboleth** | SAML | Academic federation |
| **Active Directory FS** | SAML, WS-Fed | On-premises Windows federation |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "SSO means one password for everything" | You authenticate once, but each app gets a token, not your password |
| "SSO is less secure" | Centralized authentication enables stronger MFA and monitoring |
| "SAML and OIDC do the same thing" | SAML is enterprise-focused; OIDC is modern web/mobile-focused |
| "Federation means trusting everyone" | Federation requires explicit trust agreements and certificate exchange |

---

## How to Practice

1. **Examine SSO on a website you use**
   - Click "Log in with Google" on a third-party site
   - Notice the redirect to Google
   - Notice you do not enter your password on the third-party site
   - Observe the redirect back with a token

2. **Compare SAML and OIDC**
   - List three differences in data format, transport, and use cases
   - Determine which your organization uses

3. **Run the simulations**
   - `sso_token_flow.py` demonstrates token exchange
   - `federation_trust_sim.py` models trust relationships
   - `saml_assertion_inspector.py` parses SAML assertions

---

## Projects

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

### `saml_assertion_inspector.py`
Parses and validates SAML assertions:
- Extracts issuer, subject, attributes
- Verifies digital signatures
- Checks time validity

---

## Check Your Understanding

1. What is the difference between SSO and Federation? Give a real-world example of each.
2. In SSO, why does the Service Provider never see the user's password?
3. What is a SAML Assertion and what key information does it contain?
4. How does digital signature verification prevent fake assertions?
5. Why is OpenID Connect often preferred over SAML for modern web applications?
