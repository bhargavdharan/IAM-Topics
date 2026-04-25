# 9. OAuth 2.0 and OpenID Connect

## 🏠 Real-World Analogy: The Valet Parking Key

Imagine going to a fancy hotel:

1. You drive up and a **valet** offers to park your car
2. You give the valet a **special valet key** (not your full keychain)
3. This valet key **only opens the driver's door and starts the engine**
4. It **does NOT** open the trunk, glove box, or your home
5. The valet parks your car safely
6. When you leave, you get your car back
7. The valet never had access to your personal belongings

**OAuth 2.0 is exactly this — but for your digital data.**

You can let one app (the valet) access specific parts of your data on another service (your car) WITHOUT giving away your password (full keychain).

---

## 📋 Overview

OAuth 2.0 is the industry-standard protocol for **authorization**. It allows users to grant applications access to their information without sharing passwords.

OpenID Connect (OIDC) is built on top of OAuth 2.0 and adds **authentication** — proving who you are.

**Where you use OAuth every day:**
- "Log in with Google" on random websites
- "Connect to Spotify" in a fitness app
- "Share to Twitter" from a news app
- "Import contacts from Gmail" in a CRM

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain OAuth 2.0 with real-world analogies
- Describe the four OAuth flows and when to use each
- Understand access tokens, refresh tokens, and ID tokens
- Explain the difference between OAuth (authorization) and OIDC (authentication)
- Identify common OAuth vulnerabilities
- Implement a basic OAuth flow simulator

---

## 📚 Key Concepts

### OAuth 2.0 Roles

| Role | Analogy | Description |
|------|---------|-------------|
| **Resource Owner** | You (the car owner) | The user who owns the data |
| **Client** | The valet | The application requesting access |
| **Authorization Server** | Hotel front desk | Issues tokens after user consent |
| **Resource Server** | The parking garage | Holds and serves the protected data |
| **Protected Resource** | Your car | The data being accessed (photos, contacts, etc.) |

### OAuth 2.0 Flows (Grant Types)

| Flow | Use Case | Security Level | Complexity |
|------|----------|---------------|------------|
| **Authorization Code** | Web apps with backend | ✅ Highest | Medium |
| **PKCE** | Mobile/SPA apps | ✅ High | Medium |
| **Client Credentials** | Server-to-server APIs | ✅ High (no user) | Low |
| **Device Code** | Smart TVs, IoT devices | ✅ Medium | Low |
| **Implicit** | Legacy SPAs | ⚠️ Deprecated | Low |
| **Password** | Legacy/trusted apps | ⚠️ Discouraged | Low |

### The Authorization Code Flow (Most Common)

```
1. User clicks "Log in with Google" on CoolApp
2. CoolApp redirects user to Google Authorization Server
3. Google asks: "CoolApp wants to read your email. Allow?"
4. User clicks "Allow"
5. Google redirects back to CoolApp with an authorization code
6. CoolApp sends the code + client secret to Google
7. Google verifies and returns an access token
8. CoolApp uses the access token to fetch user's email from Gmail API
```

**Key insight:** The user NEVER enters their Google password on CoolApp's website.

### Scopes: Fine-Grained Permissions

Scopes define WHAT the app can access:

| Scope | What It Allows | Example |
|-------|---------------|---------|
| `profile` | Read basic profile info | Name, photo |
| `email` | Read email address | alice@gmail.com |
| `calendar.read` | Read calendar events | View your meetings |
| `calendar.write` | Create/modify events | Add meetings |
| `drive.read` | Read files | View your documents |
| `drive.write` | Upload/modify files | Save backups |

**Best practice:** Apps should request the MINIMUM scopes needed (least privilege).

### OAuth vs OpenID Connect

| | OAuth 2.0 | OpenID Connect |
|--|-----------|---------------|
| **Purpose** | Authorization (access data) | Authentication (prove identity) |
| **Question answered** | "Can this app access my data?" | "Who is this user?" |
| **Token type** | Access Token | ID Token (JWT) |
| **Example** | "Let this app post to my Facebook" | "Log in to this site with Facebook" |
| **Built on** | Standalone protocol | OAuth 2.0 + extras |

**Relationship:** OIDC uses OAuth 2.0 to get an access token, then adds an ID Token containing user identity information.

---

## 🔧 Under the Hood

### Access Tokens

An access token is like a temporary hotel room key:
- Issued by the authorization server
- Contains scopes (what you can access)
- Has an expiration time (usually 15-60 minutes)
- Presented to the resource server with every API request

```http
GET /api/user/profile HTTP/1.1
Host: api.google.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**Bearer token:** Whoever "bears" (holds) the token can use it. This is why HTTPS is mandatory — tokens must be encrypted in transit.

### JWT (JSON Web Tokens)

Modern access tokens and ID tokens are often JWTs — self-contained, signed JSON objects:

```
eyJhbGciOiJSUzI1NiIs...  ← Header (algorithm, token type)
   .
eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJzdWIiOiIxMT...  ← Payload (claims)
   .
SflKxwRJSMeKKF2QT4fwpMe...  ← Signature (verifies integrity)
```

**Decoded payload:**
```json
{
  "iss": "https://accounts.google.com",
  "sub": "1234567890",
  "aud": "my-app-client-id",
  "exp": 1516239322,
  "iat": 1516239022,
  "scope": "email profile",
  "email": "alice@gmail.com"
}
```

**Why JWTs are useful:**
- Self-contained (all info in the token itself)
- Digitally signed (can't be tampered with)
- Can be verified without database lookup (if using asymmetric signatures)

### Refresh Tokens

Access tokens are short-lived for security. But asking users to re-authenticate every 15 minutes is terrible UX.

**Solution: Refresh tokens**
- Long-lived (days, weeks, or months)
- Stored securely by the client
- Used to get new access tokens when old ones expire
- Can be revoked independently

```
Access Token (15 min) ──expires──→ Use Refresh Token → Get new Access Token
```

### PKCE (Proof Key for Code Exchange)

Mobile apps and SPAs cannot securely store client secrets. PKCE solves this:

1. App generates a random "code verifier" (a secret string)
2. App hashes it to create "code challenge"
3. App sends code challenge to authorization server
4. Later, app sends original code verifier to exchange code for token
5. Authorization server verifies: hash(verifier) == challenge

**Why it works:** Even if an attacker intercepts the authorization code, they don't have the code verifier, so they can't exchange it for a token.

### Common OAuth Vulnerabilities

| Vulnerability | How It Happens | Prevention |
|--------------|---------------|------------|
| **Redirect URI manipulation** | Attacker tricks app into sending token to malicious site | Strict redirect URI validation |
| **Token leakage in logs** | Access token logged in URL or server logs | Never put tokens in URLs |
| **Scope escalation** | App requests more permissions than needed | User reviews scopes; least privilege |
| **CSRF on authorization** | Attacker forces user to authorize attacker's account | Use `state` parameter |
| **Implicit flow in SPAs** | Token exposed in browser history/URL | Use PKCE authorization code flow |

---

## 🛠️ Projects in This Module

### `oauth_flow_sim.py`
Simulates the complete OAuth 2.0 authorization code flow:
- Authorization server with consent screen
- Client application requesting tokens
- Token issuance and validation
- Resource server verifying access tokens
- Scope enforcement

### `jwt_inspector.py`
Decodes and validates JSON Web Tokens:
- Parses header, payload, and signature
- Verifies token signatures
- Checks expiration and issuer
- Identifies security misconfigurations

### `oidc_auth_sim.py`
Simulates OpenID Connect authentication:
- ID token generation
- UserInfo endpoint simulation
- Claims validation
- Session management

### `oauth_vulnerability_scanner.py`
Tests OAuth implementations for common flaws:
- Redirect URI validation
- State parameter usage
- Scope escalation checks
- Token storage analysis

---

## 📝 Quiz Questions

1. **What is the difference between OAuth 2.0 and OpenID Connect? What does each provide?**
2. **In the valet parking analogy, what is the resource owner, client, authorization server, and protected resource?**
3. **Why is the Authorization Code flow with PKCE recommended for mobile apps?**
4. **What is the purpose of a refresh token? Why not just make access tokens last forever?**
5. **How does the `state` parameter prevent CSRF attacks in OAuth?**
6. **Why should an app request the minimum scopes it needs?**

---

## 🔗 Further Reading

- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [OAuth 2.0 Security Best Current Practice](https://tools.ietf.org/html/draft-ietf-oauth-security-topics)
- [PKCE RFC 7636](https://tools.ietf.org/html/rfc7636)

---

## 🏷️ Tags
`#OAuth2` `#OpenIDConnect` `#JWT` `#Authorization` `#Authentication` `#PKCE` `#AccessToken` `#RefreshToken`
