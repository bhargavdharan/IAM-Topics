# 10. SAML and Enterprise Federation

## 🏠 Real-World Analogy: The Diplomatic Passport

Imagine a United Nations conference:

- Each country has its own passport system (identity provider)
- The UN doesn't verify your identity directly
- Instead, your country issues you a **diplomatic passport** with your credentials
- The UN trusts your country's government (trust relationship)
- When you arrive, you show your diplomatic passport
- The UN accepts it because they trust your country's signing authority
- The passport also lists your delegation role: "Ambassador", "Advisor", "Observer"
- Based on your role, the UN grants access to specific meeting rooms

**SAML federation is exactly this — but for enterprise software.**

---

## 📋 Overview

SAML (Security Assertion Markup Language) is the dominant standard for enterprise single sign-on and federation. While OAuth/OIDC dominate consumer applications, SAML remains the backbone of B2B and enterprise identity federation.

**Why SAML persists in enterprise:**
- Mature, well-understood standard (since 2005)
- Strong security through XML signatures
- Comprehensive attribute exchange
- Supported by virtually every enterprise application

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain SAML with real-world analogies
- Describe SAML assertions, protocols, and bindings
- Understand Identity Provider (IdP) and Service Provider (SP) roles
- Compare SAML vs OAuth/OIDC for different use cases
- Implement SAML assertion generation and validation

---

## 📚 Key Concepts

### SAML Components

| Component | Description | Diplomatic Analogy |
|-----------|-------------|-------------------|
| **Identity Provider (IdP)** | Authenticates users and issues assertions | Your home country's passport office |
| **Service Provider (SP)** | Application that trusts the IdP | The UN conference center |
| **Assertion** | XML document vouching for the user | Diplomatic passport |
| **Subject** | The user being authenticated | You, the diplomat |
| **Attribute** | Additional info about the user (roles, department) | Your title and delegation |

### Types of SAML Assertions

| Type | Purpose | Example |
|------|---------|---------|
| **Authentication Assertion** | "This user authenticated at 10:00 AM using MFA" | Passport proving identity |
| **Attribute Assertion** | "This user is in the Engineering department with Manager role" | Passport listing your title |
| **Authorization Decision Assertion** | "This user is permitted to access Resource X" | Visa stamp for a specific country |

### SAML Bindings

Bindings define HOW SAML messages are transported:

| Binding | How It Works | Use Case |
|---------|-------------|----------|
| **HTTP Redirect** | IdP redirects browser to SP with SAMLResponse in URL | IdP-initiated SSO |
| **HTTP POST** | SAMLResponse in HTML form POST | SP-initiated SSO (most common) |
| **HTTP Artifact** | Send small reference, retrieve assertion via back-channel | High-security environments |
| **SOAP** | Direct server-to-server communication | Attribute queries |

### SAML Profiles

Profiles define specific use cases:

| Profile | What It Does |
|---------|-------------|
| **Web Browser SSO** | User logs in via browser (most common) |
| **Single Logout** | Logging out of one app logs out of all |
| **Name Identifier Management** | Linking/unlinking accounts across systems |
| **Artifact Resolution** | Secure assertion retrieval |

---

## 🔧 Under the Hood

### SAML Assertion Structure

A SAML assertion is a signed XML document with three main parts:

```xml
<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
                ID="_a75adf55-01d7-40cc-929f-dbd8372ebdfc"
                IssueInstant="2024-01-15T10:00:00Z"
                Version="2.0">
    
    <!-- 1. ISSUER: Who vouches for this -->
    <saml:Issuer>https://company-idp.example.com</saml:Issuer>
    
    <!-- 2. SIGNATURE: Digital signature proving authenticity -->
    <ds:Signature>
        <ds:SignedInfo>...</ds:SignedInfo>
        <ds:SignatureValue>...</ds:SignatureValue>
        <ds:KeyInfo>...</ds:KeyInfo>
    </ds:Signature>
    
    <!-- 3. SUBJECT: Who this assertion is about -->
    <saml:Subject>
        <saml:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
            alice@company.com
        </saml:NameID>
        <saml:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
            <saml:SubjectConfirmationData 
                NotOnOrAfter="2024-01-15T10:05:00Z"
                Recipient="https://app.example.com/saml/acs"
                InResponseTo="_4fee3b046395c84e1662c8980b6b5a0b"/>
        </saml:SubjectConfirmation>
    </saml:Subject>
    
    <!-- 4. CONDITIONS: When and where this is valid -->
    <saml:Conditions NotBefore="2024-01-15T09:55:00Z" 
                     NotOnOrAfter="2024-01-15T10:05:00Z">
        <saml:AudienceRestriction>
            <saml:Audience>https://app.example.com</saml:Audience>
        </saml:AudienceRestriction>
    </saml:Conditions>
    
    <!-- 5. AUTHN STATEMENT: How the user authenticated -->
    <saml:AuthnStatement AuthnInstant="2024-01-15T10:00:00Z"
                         SessionIndex="_session123">
        <saml:AuthnContext>
            <saml:AuthnContextClassRef>
                urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport
            </saml:AuthnContextClassRef>
        </saml:AuthnContext>
    </saml:AuthnStatement>
    
    <!-- 6. ATTRIBUTE STATEMENT: User attributes -->
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

### SP-Initiated vs IdP-Initiated SSO

**SP-Initiated (most secure):**
```
1. User clicks "Company Login" on Salesforce (SP)
2. Salesforce generates SAML Request and redirects to IdP
3. IdP authenticates user
4. IdP sends SAML Response back to Salesforce
5. Salesforce validates Response (matches Request ID)
```

**IdP-Initiated:**
```
1. User logs into Company Portal (IdP)
2. User clicks "Salesforce" icon
3. IdP sends SAML Response to Salesforce
4. Salesforce validates Response
```

**Why SP-initiated is preferred:** The SAML Request contains a unique ID that must match the SAML Response, preventing replay attacks.

### Trust Metadata

IdPs and SPs exchange metadata XML files containing:

```xml
<EntityDescriptor entityID="https://company-idp.example.com">
    <IDPSSODescriptor>
        <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                             Location="https://company-idp.example.com/saml/sso"/>
        <KeyDescriptor use="signing">
            <KeyInfo>
                <X509Data>
                    <X509Certificate>MIIDXTCCAkWgAwIBAgIJAKoK/heBjcOu...</X509Certificate>
                </X509Data>
            </KeyInfo>
        </KeyDescriptor>
    </IDPSSODescriptor>
</EntityDescriptor>
```

**The X.509 certificate is the trust anchor.** The SP uses this certificate to verify that SAML assertions were actually signed by the IdP.

### SAML vs OIDC

| Aspect | SAML | OIDC |
|--------|------|------|
| **Data format** | XML | JSON (JWT) |
| **Complexity** | Higher | Lower |
| **Mobile support** | Poorer | Better |
| **Enterprise adoption** | Dominant | Growing |
| **Token structure** | Verbose, signed XML | Compact, signed JSON |
| **Best for** | Enterprise SSO | Modern web/mobile apps |

---

## 🛠️ Projects in This Module

### `saml_assertion_gen.py`
Generates and signs SAML assertions:
- Creates SAML 2.0 assertions
- Signs with X.509 certificates
- Includes authentication, attribute, and condition statements
- Exports valid SAML XML

### `saml_validator.py`
Validates SAML assertions:
- Verifies XML signatures
- Checks time conditions (NotBefore, NotOnOrAfter)
- Validates audience restrictions
- Detects replay attacks via InResponseTo matching

### `federation_metadata_manager.py`
Manages SAML federation metadata:
- Parses IdP and SP metadata
- Extracts endpoints and certificates
- Validates metadata signatures
- Detects configuration drift

---

## 📝 Quiz Questions

1. **What is the difference between an Authentication Assertion and an Attribute Assertion?**
2. **Why is the digital signature on a SAML assertion critical? What happens if it's missing or invalid?**
3. **What is the difference between SP-initiated and IdP-initiated SSO? Which is more secure and why?**
4. **How does SAML prevent replay attacks through the `InResponseTo` attribute?**
5. **When would an organization choose SAML over OpenID Connect?**

---

## 🔗 Further Reading

- [SAML 2.0 Specification](https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf)
- [SAML Technical Overview](https://wiki.shibboleth.net/confluence/display/CONCEPT/SAML2Intro)
- [OASIS SAML Standards](https://www.oasis-open.org/standard/saml/)

---

## 🏷️ Tags
`#SAML` `#EnterpriseFederation` `#SSO` `#XML` `#IdentityProvider` `#ServiceProvider` `#Assertion`
