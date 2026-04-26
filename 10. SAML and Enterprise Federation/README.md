# 10. SAML and Enterprise Federation

## What Is SAML?

**SAML (Security Assertion Markup Language)** is an XML-based open standard for exchanging authentication and authorization data between an Identity Provider (IdP) and a Service Provider (SP). It is the dominant protocol for enterprise single sign-on and cross-organizational identity federation.

While OAuth 2.0 and OpenID Connect power consumer and mobile applications, SAML remains the backbone of B2B integrations, enterprise SaaS deployments, and regulated industry authentication.

---

## Why Learn This?

SAML has been the enterprise standard since 2005. It is supported by virtually every enterprise application, from Salesforce and Workday to custom internal systems. Understanding SAML is essential for:
- Integrating with enterprise identity providers
- Configuring SSO for SaaS applications
- Working in regulated industries (finance, healthcare, government)
- Understanding legacy and hybrid federation architectures
- Troubleshooting authentication issues in enterprise environments

---

## Core Concepts

### SAML Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Identity Provider (IdP)** | System that authenticates users and issues SAML assertions | Company's Active Directory Federation Services (AD FS), Okta, Ping Identity |
| **Service Provider (SP)** | Application that trusts the IdP and consumes assertions | Salesforce, Workday, ServiceNow, custom applications |
| **Assertion** | XML document containing authentication statement and user attributes | "Alice authenticated at 10:00 AM using password + MFA. She is in Engineering with Manager role." |
| **Subject** | The authenticated user identified in the assertion | `alice@company.com` |
| **Attribute** | Additional information about the user transmitted in the assertion | Department=Engineering, Role=Manager, EmployeeID=12345 |

### Types of SAML Assertions

| Type | Purpose | Contents |
|------|---------|----------|
| **Authentication Assertion** | States that the user authenticated successfully | Authentication time, method used, subject identifier |
| **Attribute Assertion** | Transmits user attributes to the SP | Department, role, email, groups, custom attributes |
| **Authorization Decision Assertion** | States whether the user is permitted to access a specific resource | Decision (Permit/Deny), resource identifier, justification |

### SAML Bindings

Bindings define how SAML messages are transported between parties:

| Binding | Transport Mechanism | Use Case | Security Notes |
|---------|-------------------|----------|---------------|
| **HTTP Redirect** | SAML message in URL query parameters | IdP-initiated SSO | Limited by URL length; signed to prevent tampering |
| **HTTP POST** | SAML message in HTML form POST body | SP-initiated SSO | Most common; no URL length limits |
| **HTTP Artifact** | Small reference sent; assertion retrieved via back-channel SOAP call | High-security environments | Prevents assertion exposure in browser |
| **SOAP** | Direct server-to-server communication | Attribute queries, identity queries | Not used for browser SSO |

### SAML Profiles

Profiles define specific use cases built on SAML bindings:

| Profile | Purpose | Typical Flow |
|---------|---------|-------------|
| **Web Browser SSO** | User logs in via web browser | Most common SAML use case |
| **Single Logout (SLO)** | Logging out of one service logs out of all | Requires coordination between IdP and all SPs |
| **Name Identifier Management** | Linking or unlinking user accounts across systems | Used when accounts are merged or split |
| **Artifact Resolution** | Secure retrieval of assertions | Back-channel fetch using artifact reference |

---

## How It Works

### SAML Assertion Structure

A SAML 2.0 assertion is a signed XML document with these key sections:

**1. Issuer**
Identifies the IdP that issued the assertion. The SP validates that this matches the expected trusted IdP.

**2. Digital Signature**
The entire assertion is digitally signed by the IdP's private key. The SP verifies this signature using the IdP's public certificate from metadata. Signature verification ensures:
- The assertion genuinely came from the IdP
- The assertion has not been modified in transit
- The assertion is authentic

**3. Subject**
Identifies the authenticated user, typically by NameID (email, employee ID, or transient identifier).

**4. Conditions**
Defines when and where the assertion is valid:
- `NotBefore`: Assertion is not valid before this time
- `NotOnOrAfter`: Assertion expires after this time (typically 5 minutes)
- `AudienceRestriction`: Assertion is only valid for specific SPs

**5. AuthnStatement**
Describes how the user authenticated:
- `AuthnInstant`: When authentication occurred
- `AuthnContext`: Method used (password, MFA, Kerberos, etc.)
- `SessionIndex`: Identifier for the user's session at the IdP

**6. AttributeStatement**
Contains user attributes the SP needs:
```xml
<saml:AttributeStatement>
  <saml:Attribute Name="Role">
    <saml:AttributeValue>Manager</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="Department">
    <saml:AttributeValue>Engineering</saml:AttributeValue>
  </saml:Attribute>
</saml:AttributeStatement>
```

### SP-Initiated vs IdP-Initiated SSO

**SP-initiated (preferred for security):**
```
1. User visits SP (e.g., Salesforce) and clicks "Company Login"
2. SP generates SAML AuthnRequest with unique ID
3. SP redirects browser to IdP with AuthnRequest
4. IdP authenticates user (password, MFA)
5. IdP generates SAML Response referencing the AuthnRequest ID
6. IdP sends Response back to SP via browser POST
7. SP verifies: signature valid, ID matches request, not expired, audience correct
8. SP establishes session and logs user in
```

**Security advantage:** The `InResponseTo` attribute in the SAML Response must match the `ID` of the original AuthnRequest. This correlation prevents replay attacks where an attacker captures and resends a valid assertion.

**IdP-initiated:**
```
1. User logs into IdP portal (e.g., company intranet)
2. User clicks icon for Salesforce
3. IdP generates SAML Response without corresponding request
4. IdP sends Response to SP via browser POST
5. SP verifies: signature valid, not expired, audience correct
6. SP establishes session and logs user in
```

**Risk:** Without a correlated request, replay attacks are theoretically possible. Mitigations include very short assertion lifetimes (minutes), strict audience restrictions, and one-time-use identifiers.

### Trust Metadata

IdPs and SPs exchange metadata XML files to establish trust:

**IdP Metadata contains:**
- Entity ID (unique identifier)
- SSO service URL (where to send AuthnRequests)
- SLO service URL (where to send logout requests)
- X.509 certificate for signature verification
- Supported bindings and protocols

**SP Metadata contains:**
- Entity ID
- Assertion Consumer Service (ACS) URL (where to send Responses)
- SLO service URL
- Supported bindings
- Requested attributes

**The X.509 certificate is the trust anchor.** The SP uses this certificate to verify that SAML assertions were actually signed by the IdP. If the certificate is expired or mismatched, SSO fails.

### SAML vs OIDC

| Aspect | SAML | OIDC |
|--------|------|------|
| **Data format** | XML | JSON (JWT) |
| **Complexity** | Higher (verbose XML, multiple bindings) | Lower (compact JSON, REST-based) |
| **Mobile support** | Poorer (designed for browser POST/redirect) | Better (native app support via AppAuth) |
| **Enterprise adoption** | Dominant (most enterprise apps support SAML) | Growing (especially for cloud-native apps) |
| **Token size** | Larger (XML verbosity) | Smaller (compact JWT) |
| **Best for** | Enterprise SSO, B2B federation | Modern web apps, mobile apps, APIs |

**Practical reality:** Many organizations use both. SAML for legacy enterprise applications, OIDC for modern web and mobile apps.

---

## Where You See It

| Product | SAML Use | Typical Setup |
|---------|----------|--------------|
| **Salesforce** | Enterprise SSO | SAML for employee access; local auth for customers |
| **Workday** | HR system federation | SAML from corporate IdP for employee access |
| **ServiceNow** | IT service management SSO | SAML for agents and employees |
| **Google Workspace** | SSO from corporate IdP | SAML from Azure AD or Okta to Google |
| **AWS SSO** | AWS console access | SAML from corporate IdP to AWS |
| **Shibboleth** | Academic federation | SAML between universities for resource sharing |
| **AD FS** | Windows-based federation | SAML and WS-Federation for Microsoft ecosystem |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "SAML is outdated" | SAML is mature and stable. It is not going away in enterprise environments. Many organizations will use SAML for decades. |
| "SAML assertions are encrypted by default" | Assertions are digitally signed by default. Encryption is optional and less commonly used. Signature ensures authenticity; encryption ensures confidentiality. |
| "IdP-initiated is as secure as SP-initiated" | SP-initiated includes request/response correlation (InResponseTo) that prevents replay attacks. IdP-initiated lacks this protection. |
| "SAML and OIDC are competitors" | They serve different but overlapping use cases. Most enterprises use both. The trend is SAML for legacy, OIDC for new. |
| "SAML is too complex for small companies" | Cloud IdPs like Okta and Azure AD handle SAML complexity. Small companies configure SAML through GUIs without touching XML. |

---

## How to Practice

### Exercise 1: Read a SAML Assertion
If your organization uses SAML:
1. Use browser DevTools or a SAML tracer extension to capture a SAMLResponse
2. Base64-decode it
3. Examine the XML structure
4. Identify: Issuer, Subject, Conditions, AuthnStatement, AttributeStatement
5. Check the NotOnOrAfter time — how long is the assertion valid?
6. Verify the AudienceRestriction — which SP is it intended for?

### Exercise 2: Compare SAML and OIDC for Your Use Case
Document:
- Three applications your organization uses
- Which support SAML, which support OIDC
- Which protocol is used for each
- What would be required to migrate from SAML to OIDC

### Exercise 3: Troubleshoot a SAML Issue
Scenario: Users cannot log into Salesforce via SAML.
Possible causes to investigate:
- Certificate mismatch or expiration
- Clock skew (assertion expired before receipt)
- Audience restriction mismatch
- ACS URL incorrect
- Attribute mapping failure
- IdP metadata not updated

Create a troubleshooting checklist.

### Exercise 4: Run the Simulations
- `saml_assertion_gen.py` — Generate and sign assertions
- `saml_validator.py` — Validate signatures and conditions

---

## Projects

### `saml_assertion_gen.py`
Generates and signs SAML 2.0 assertions:
- Creates complete SAML Assertions with all sections
- Signs with X.509 certificates using XML-Sig
- Includes authentication, attribute, and condition statements
- Exports valid SAML XML for testing

### `saml_validator.py`
Validates SAML assertions comprehensively:
- Verifies XML digital signatures
- Checks time conditions (NotBefore, NotOnOrAfter)
- Validates audience restrictions
- Matches InResponseTo for replay detection
- Identifies security issues and misconfigurations

### `federation_metadata_manager.py`
Manages SAML federation metadata:
- Parses IdP and SP metadata XML
- Extracts endpoints, certificates, and capabilities
- Validates metadata signatures
- Detects configuration drift

---

## Check Your Understanding

1. What is the difference between an Authentication Assertion and an Attribute Assertion? What information does each contain?
2. Why is the digital signature on a SAML assertion critical? What attacks would be possible without signature verification?
3. What is the difference between SP-initiated and IdP-initiated SSO? Why is SP-initiated considered more secure?
4. How does SAML prevent replay attacks through the `InResponseTo` attribute? Describe a replay attack that would succeed without it.
5. When would an organization choose SAML over OpenID Connect? When would OIDC be preferred?
6. What information is contained in SAML metadata? Why is the X.509 certificate the trust anchor?
7. A SAML assertion has `NotOnOrAfter="2024-01-15T10:05:00Z"` but the SP's clock is 10 minutes slow. What happens? How should this be fixed?
8. Design a SAML federation between two companies: Company A (IdP) has 5,000 employees. Company B (SP) provides a procurement portal. What attributes need to be exchanged? What trust establishment is required?
9. Compare HTTP POST, HTTP Redirect, and HTTP Artifact bindings. When would you use each?
10. Your organization's SAML SSO to a critical vendor application suddenly stops working. Create a systematic troubleshooting plan with at least 8 checks.
