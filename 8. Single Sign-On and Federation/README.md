# 8. Single Sign-On (SSO) and Federation

## What Is SSO?

**Single Sign-On (SSO)** is an authentication mechanism that allows a user to log in once and gain access to multiple applications and systems without being prompted to log in again for each one.

**Federation** extends SSO across organizational boundaries, enabling users from one organization to access resources in another organization using their home organization's credentials.

The fundamental principle of both is **delegated authentication**: instead of each application verifying your identity itself, applications trust an external identity provider to vouch for you.

---

## Why Learn This?

Password fatigue is one of the most significant security challenges in modern organizations:
- Users with dozens of accounts reuse passwords across sites
- Weak passwords are chosen for convenience
- Password resets consume enormous IT resources
- Each application that stores passwords becomes a breach target

SSO addresses these problems by:
- Reducing the number of passwords users must remember
- Centralizing authentication for stronger security controls
- Enabling consistent MFA deployment across all applications
- Simplifying user onboarding and offboarding

Understanding SSO and Federation is essential for:
- Designing login architectures
- Integrating applications with identity providers
- Evaluating SSO security risks
- Implementing SAML and OIDC connections

---

## Core Concepts

### Key Players

| Term | Definition | Example |
|------|-----------|---------|
| **Identity Provider (IdP)** | System that authenticates users and issues identity tokens | Google, Okta, Azure AD, ADFS, Ping Identity |
| **Service Provider (SP)** | Application that relies on the IdP for authentication | Gmail, Salesforce, Workday, internal applications |
| **User/Principal** | The person or system authenticating | Alice, a contractor logging into a client system |
| **Token/Assertion** | Cryptographic proof of authentication issued by the IdP | SAML Assertion, JWT ID Token, Kerberos ticket |

### How SSO Works

The SSO flow follows a consistent pattern across protocols:

```
1. User attempts to access an application (Service Provider)
2. SP: "I don't know who you are. Go to the Identity Provider."
3. User is redirected to the Identity Provider
4. IdP authenticates the user (password, MFA, etc.)
5. IdP creates a signed token/assertion: "This is Alice, authenticated at 10:00 AM"
6. User presents this token to the SP
7. SP verifies the token's signature and validity
8. SP: "Welcome, Alice!" — access granted
```

**Critical security point:** The Service Provider NEVER sees the user's password. The SP trusts the IdP's cryptographic signature.

### SSO vs Federation

| Aspect | SSO | Federation |
|--------|-----|------------|
| Scope | Within one organization or trust domain | Across multiple independent organizations |
| Trust relationship | Internal, managed by one organization | External, established through agreements and metadata exchange |
| Example | Employee logs into company email, CRM, and HR with one password | University student accesses library databases at partner institutions |
| Protocols | Kerberos, SAML, OIDC | SAML, OIDC, WS-Federation |
| Setup complexity | Medium | Higher (requires legal agreements, metadata exchange, attribute mapping) |

### Trust Establishment

Before SSO can function, the IdP and SP must establish a trust relationship:

1. **Metadata exchange:** Both parties share XML or JSON metadata containing:
   - Entity ID (unique identifier)
   - Endpoint URLs (where to send requests and responses)
   - Supported bindings and protocols
   - X.509 certificates for signature verification

2. **Certificate trust:** The SP trusts the IdP's public certificate. The IdP signs tokens with its private key; the SP verifies with the public key.

3. **Attribute mapping:** Both parties agree on how user attributes are represented:
   - IdP might send `mail=alice@company.com`
   - SP might expect `email=alice@company.com`
   - Mapping ensures correct interpretation

---

## How It Works

### SAML Assertions

SAML (Security Assertion Markup Language) is the dominant enterprise SSO standard. The core artifact is the **SAML Assertion** — a digitally signed XML document.

**Assertion components:**
- **Issuer:** The IdP that vouches for the assertion (e.g., `https://idp.company.com`)
- **Subject:** The authenticated user (e.g., `alice@company.com`)
- **Conditions:** Validity window (`NotBefore`, `NotOnOrAfter`)
- **AuthnStatement:** How and when the user authenticated
- **AttributeStatement:** User attributes (roles, department, email)
- **Digital Signature:** Cryptographic proof the assertion came from the IdP

**Signature verification:** The assertion is signed by the IdP's private key. The SP verifies this signature using the IdP's public certificate from metadata. If verification fails, the assertion is rejected.

### SP-Initiated vs IdP-Initiated SSO

**SP-initiated (preferred for security):**
1. User clicks login on the SP
2. SP generates a SAML `AuthnRequest` with a unique ID
3. User redirected to IdP with the request
4. IdP authenticates user
5. IdP sends SAML `Response` back to SP
6. SP verifies the Response matches the Request ID

**Security benefit:** The `InResponseTo` attribute in the SAML Response must match the original Request ID, preventing replay attacks.

**IdP-initiated:**
1. User logs into IdP portal first
2. User clicks an application icon
3. IdP sends SAML Response to SP
4. SP verifies and logs user in

**Risk:** Without a correlated request, replay attacks are possible if the assertion is intercepted. Shorter validity windows and strict audience restrictions mitigate this.

### OpenID Connect (OIDC)

OIDC is built on OAuth 2.0 and uses JSON Web Tokens (JWT) instead of XML:

```json
{
  "iss": "https://accounts.google.com",
  "sub": "1234567890",
  "name": "Alice Smith",
  "email": "alice@company.com",
  "iat": 1516239022,
  "exp": 1516239322,
  "aud": "my-app-client-id"
}
```

**Key differences from SAML:**
- Data format: JSON vs XML
- Transport: Designed for REST APIs and mobile apps
- Simplicity: Easier to parse and implement
- Adoption: Growing rapidly; SAML still dominates enterprise

### SSO Security Risks and Mitigations

| Risk | How It Happens | Mitigation |
|------|---------------|------------|
| **Token theft** | XSS steals session cookie | HttpOnly, Secure, SameSite cookies; short session lifetimes |
| **Replay attacks** | Intercepted assertion reused | Short validity windows; unique request/response IDs |
| **IdP compromise** | Attacker gains control of IdP | Strong IdP security; MFA on admin accounts; monitoring |
| **SP misconfiguration** | Accepts assertions from wrong IdP | Strict certificate validation; audience restrictions |
| **Logout issues** | User logs out of one app, others stay open | Single Logout (SLO) protocols; short session timeouts |
| **Man-in-the-middle** | Attacker intercepts token exchange | HTTPS everywhere; certificate pinning |

---

## Where You See It

| Product | Protocol | Use Case |
|---------|----------|----------|
| **Okta** | SAML, OIDC | Enterprise SSO for hundreds of SaaS apps |
| **Azure AD** | SAML, OIDC | Microsoft 365 integration; cloud app SSO |
| **Google Workspace** | OIDC | Consumer and business login |
| **Shibboleth** | SAML | Academic and research federation |
| **AD FS** | SAML, WS-Fed | On-premises Windows federation |
| **OneLogin** | SAML, OIDC | Mid-market SSO and MFA |
| **Ping Identity** | SAML, OIDC | Large enterprise federation |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "SSO means one password for everything" | You authenticate once, but each app receives a token. Your password is never shared with applications. |
| "SSO reduces security" | Centralized authentication enables stronger MFA, better monitoring, and faster revocation than distributed passwords. |
| "SAML and OIDC are interchangeable" | SAML dominates enterprise B2B; OIDC is preferred for modern web and mobile apps. Many organizations use both. |
| "Federation means trusting everyone" | Federation requires explicit trust agreements, certificate exchange, and often legal contracts. |
| "SSO eliminates the need for MFA" | SSO should be combined with MFA at the IdP for strong authentication. |

---

## How to Practice

### Exercise 1: Observe an SSO Flow
1. Open browser Developer Tools → Network tab
2. Log into a website using "Sign in with Google"
3. Observe the redirects:
   - From the SP to accounts.google.com
   - Authentication at Google
   - Redirect back to SP with authorization code
   - SP exchanging code for tokens
4. Identify: client_id, redirect_uri, scope, state parameters

### Exercise 2: Compare SAML and OIDC
Create a comparison table with these dimensions:
- Data format (XML vs JSON)
- Token structure
- Mobile app support
- Enterprise adoption
- Implementation complexity
- Your organization's primary use case

### Exercise 3: Design SSO for a Company
A 200-person company uses:
- Google Workspace (email, docs)
- Salesforce (CRM)
- Slack (communication)
- Custom internal application (React + Node.js)
- GitHub (code repositories)

Design the SSO architecture:
- Which IdP? Why?
- Which protocol for each application?
- MFA requirements?
- Offboarding process?

### Exercise 4: Run the Simulations
- `sso_token_flow.py` — Token exchange demonstration
- `federation_trust_sim.py` — Trust relationship modeling
- `saml_assertion_inspector.py` — Assertion validation

---

## Projects

### `sso_token_flow.py`
Simulates SSO token exchange:
- Generates SAML-style assertions
- Signs and verifies tokens with certificates
- Simulates IdP-SP trust validation
- Demonstrates token expiration and replay prevention
- Shows both SP-initiated and IdP-initiated flows

### `federation_trust_sim.py`
Models trust relationships between organizations:
- Creates IdP and SP metadata
- Establishes trust through certificate exchange
- Simulates cross-organizational authentication
- Demonstrates attribute mapping
- Tests trust revocation

### `saml_assertion_inspector.py`
Parses and validates SAML assertions:
- Extracts issuer, subject, attributes, conditions
- Verifies XML digital signatures
- Checks time validity (NotBefore, NotOnOrAfter)
- Identifies security issues (missing signature, expired assertion)
- Matches InResponseTo for replay detection

---

## Check Your Understanding

1. What is the difference between SSO and Federation? Give a real-world example of each and explain the trust relationship involved.
2. In SSO, why does the Service Provider never see the user's password? Trace the authentication flow and identify where the password is entered.
3. What is a SAML Assertion? List its key components and explain the purpose of each.
4. How does digital signature verification prevent fake assertions? What would happen if an attacker forged an assertion without the IdP's private key?
5. Why is SP-initiated SSO considered more secure than IdP-initiated? Explain the role of InResponseTo.
6. Compare SAML and OpenID Connect across five dimensions: data format, complexity, mobile support, enterprise adoption, and token type.
7. Design an SSO architecture for a university with 10,000 students, 1,000 faculty, and 200 staff. The university uses Google Workspace, Canvas (LMS), a library system, and a financial aid portal.
8. An employee leaves the organization. In an SSO environment, what actions should be taken to ensure they lose access to all applications?
9. Describe three SSO security risks and their mitigations. Which risk do you consider most critical and why?
10. Your organization uses Okta for SSO. A new SaaS vendor supports SAML but not OIDC. Walk through the integration steps from metadata exchange to first login.
