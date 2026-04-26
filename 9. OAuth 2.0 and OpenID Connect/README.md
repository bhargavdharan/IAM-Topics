# 9. OAuth 2.0 and OpenID Connect

## What Is OAuth 2.0?

**OAuth 2.0** is an authorization framework that enables a user to grant a third-party application limited access to their resources without sharing their password.

**OpenID Connect (OIDC)** is an identity layer built on top of OAuth 2.0 that adds authentication — the ability to verify the user's identity.

When you click "Log in with Google," "Connect to Spotify," or "Share to Twitter," you are using OAuth and OIDC. These protocols power much of the modern web's integration and interoperability.

---

## Why Learn This?

OAuth 2.0 is one of the most widely deployed authorization protocols on the internet. It enables:
- Social login ("Log in with Google")
- API access (fitness app reading your health data)
- Integration (CRM importing contacts from email)
- Mobile app authentication without passwords

Understanding OAuth is essential for:
- Building applications that integrate with third-party services
- Securing APIs against unauthorized access
- Understanding the security boundaries of delegated authorization
- Implementing secure authentication flows

---

## Core Concepts

### OAuth 2.0 Roles

| Role | Definition | Example |
|------|-----------|---------|
| **Resource Owner** | The user who owns the data and grants access | You, the user |
| **Client** | The application requesting access | A fitness tracking app |
| **Authorization Server** | Server that authenticates the user and issues tokens | Google Accounts, Okta, Auth0 |
| **Resource Server** | Server hosting the protected resources | Gmail API, Spotify API |
| **Protected Resource** | The specific data being accessed | Your emails, playlists, calendar events |

### Authorization Flows (Grant Types)

OAuth 2.0 defines multiple flows for different scenarios:

| Flow | Use Case | Security Level | Notes |
|------|----------|---------------|-------|
| **Authorization Code + PKCE** | Web apps, mobile apps, SPAs | Highest | Recommended for all client types |
| **Client Credentials** | Server-to-server APIs | High | No user involved; machine-to-machine |
| **Device Code** | Smart TVs, IoT devices, CLI tools | Medium | User authorizes on separate device |
| **Implicit** | Legacy SPAs | Low | Deprecated; tokens exposed in URLs |
| **Password** | Legacy trusted applications | Low | Discouraged; shares user password with client |

**Authorization Code Flow with PKCE (detailed):**
1. User clicks "Log in with Google" on CoolApp
2. CoolApp generates a PKCE code verifier and code challenge
3. CoolApp redirects user to Google Authorization Server with: client_id, redirect_uri, scope, state, code_challenge
4. Google authenticates user (password, MFA)
5. Google asks: "CoolApp wants to read your email. Allow?"
6. User clicks "Allow"
7. Google redirects back to CoolApp with authorization code
8. CoolApp sends: authorization code + client_secret + code_verifier
9. Google verifies everything and returns access token + refresh token
10. CoolApp uses access token to call Gmail API

**Critical security point:** The user NEVER enters their Google password on CoolApp's website.

### Scopes: Fine-Grained Permissions

Scopes define WHAT the client application can access:

| Scope | Allows | Risk If Over-Granted |
|-------|--------|---------------------|
| `openid` | Authenticate user (OIDC) | N/A — required for OIDC |
| `profile` | Read basic profile info | Low |
| `email` | Read email address | Low |
| `calendar.read` | Read calendar events | Medium — reveals schedule |
| `calendar.write` | Create/modify events | Medium — could disrupt schedule |
| `drive.read` | Read files | High — accesses documents |
| `drive.write` | Upload/modify files | High — could delete or modify |
| `gmail.read` | Read emails | Very High — accesses private communication |
| `gmail.send` | Send emails | Very High — could send as user |

**Best practice:** Request the minimum scopes needed. If your app only needs to read profile information, do not request email or calendar access.

### OAuth vs OpenID Connect

| Aspect | OAuth 2.0 | OpenID Connect |
|--------|-----------|---------------|
| **Purpose** | Authorization (can this app access my data?) | Authentication (who is this user?) |
| **Token type** | Access Token | ID Token (JWT) |
| **What it proves** | User granted permission to app | User's identity verified |
| **Example** | "Let this app post to my Facebook" | "Log in to this site with Facebook" |
| **Relationship** | Base protocol | Extension built on OAuth 2.0 |

**Key insight:** OAuth 2.0 alone does not tell you WHO the user is — only that they granted permission. OIDC adds the ID Token which contains identity claims (name, email, subject identifier).

---

## How It Works

### Access Tokens

An access token is a temporary credential that represents the authorization granted:
- Issued by the authorization server
- Contains or references the granted scopes
- Has an expiration time (typically 15-60 minutes)
- Presented to the resource server with every API request

```http
GET /api/v1/user/emails HTTP/1.1
Host: api.google.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**Bearer token security:** Whoever holds the token can use it. This is why HTTPS is mandatory — tokens must be encrypted in transit. Tokens should also be stored securely on the client (not in localStorage for web apps — use httpOnly cookies instead).

### JWT (JSON Web Tokens)

Modern access tokens and ID tokens are often JWTs — self-contained, signed JSON objects:

```
eyJhbGciOiJSUzI1NiIs...   // Header: algorithm, token type
.                           // Separator
eyJpc3MiOiJodHRwczovL2Fj...  // Payload: claims (issuer, subject, audience, expiration)
.                           // Separator
SflKxwRJSMeKKF2QT4fwpMe...   // Signature: cryptographic proof of integrity
```

**Header contains:** Algorithm (RS256, ES256) and token type (JWT)
**Payload contains:** Issuer, subject, audience, issued at, expiration, scopes, custom claims
**Signature ensures:** The token was issued by the claimed authority and has not been tampered with

**Why JWTs are useful:**
- Self-contained — resource server can verify without database lookup
- Signed — integrity is cryptographically guaranteed
- Compact — Base64Url encoded for easy transport

**JWT limitation:** Once issued, a JWT cannot be revoked before its expiration (unless the resource server checks a revocation list). This is why access tokens are short-lived.

### Refresh Tokens

Access tokens are short-lived for security. But asking users to re-authenticate every 15 minutes would be terrible UX.

**Solution: Refresh tokens**
- Long-lived (days, weeks, or months)
- Stored securely by the client
- Used to obtain new access tokens when old ones expire
- Can be revoked independently (if stolen or user logs out)
- Typically rotated with each use (new refresh token issued)

**Flow:**
```
Access Token (15 min) ──expires──→ 
  Use Refresh Token → Get new Access Token + new Refresh Token
```

### PKCE (Proof Key for Code Exchange)

PKCE (pronounced "pixy") protects the authorization code flow:

**The problem:** Mobile apps and SPAs cannot securely store client secrets. An attacker who intercepts the authorization code could exchange it for tokens.

**PKCE solution:**
1. Client generates random `code_verifier` (43-128 characters)
2. Client hashes verifier to create `code_challenge`
3. Client sends challenge to authorization server
4. Later, client sends original verifier with authorization code
5. Server verifies: `hash(code_verifier) == code_challenge`

**Why it works:** Even if an attacker intercepts the authorization code, they do not have the code_verifier, so they cannot exchange it.

**RFC 7636:** PKCE was originally designed for mobile apps but is now recommended for ALL clients, including web apps.

---

## Where You See It

| Integration | OAuth Use | OIDC Use |
|------------|-----------|----------|
| **Google Sign-In** | Access Google APIs | Prove user identity |
| **GitHub Apps** | Access repositories, create issues | Identify the user |
| **Slack apps** | Post messages, read channels | Identify team members |
| **Stripe Connect** | Process payments on behalf of users | Link merchant accounts |
| **Salesforce** | Access CRM data | SSO login |
| **Spotify** | Read playlists, control playback | User identity |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "OAuth is for authentication" | OAuth is for authorization. OIDC adds authentication on top. They are related but distinct. |
| "Access tokens are encrypted" | Access tokens are signed, not necessarily encrypted. Do not put sensitive data in them. |
| "Refresh tokens last forever" | Refresh tokens should be rotatable and revocable. Good implementations issue new refresh tokens with each use. |
| "The client secret is a password" | The client secret identifies the application, not the user. It proves the request came from a registered application. |
| "OAuth is too complex for simple apps" | For simple use cases, libraries and services (Auth0, Firebase Auth) handle the complexity. |
| "State parameter is optional" | The `state` parameter is essential for CSRF protection. Omitting it creates a security vulnerability. |

---

## How to Practice

### Exercise 1: Inspect an OAuth Flow
1. Open browser Developer Tools → Network tab
2. Log into a website using "Sign in with Google"
3. Filter for requests to `accounts.google.com`
4. Observe the authorization request parameters:
   - `client_id`: Identifies the application
   - `redirect_uri`: Where to send the response
   - `scope`: What permissions are requested
   - `state`: CSRF protection token
   - `response_type`: "code" for authorization code flow
5. Observe the redirect back with `?code=...`
6. Observe the POST to exchange code for tokens

### Exercise 2: Decode a JWT
1. Go to jwt.io
2. Paste any JWT you have (from an API, a login, etc.)
3. Examine the header, payload, and signature
4. Identify: issuer, subject, audience, expiration, scopes
5. Understand what each claim means

### Exercise 3: Design OAuth Integration
Design OAuth integration for a task management app that:
- Needs to read user's Google Calendar (to show tasks alongside meetings)
- Needs to send email notifications via Gmail
- Should NOT be able to delete emails or calendars
- Should work on web and mobile

Specify: scopes, flow, token handling, security considerations.

### Exercise 4: Run the Simulations
- `oauth_flow_sim.py` — Complete authorization code flow with PKCE
- `jwt_inspector.py` — Decode and validate JWTs

---

## Projects

### `oauth_flow_sim.py`
Complete OAuth 2.0 authorization code flow simulation:
- Authorization server with consent screen
- Client application with PKCE generation
- Token exchange with verifier validation
- Resource server with scope enforcement
- Demonstrates state parameter for CSRF protection

### `jwt_inspector.py`
Decodes and validates JSON Web Tokens:
- Parses header, payload, and signature
- Verifies token signatures (HMAC, RSA)
- Checks expiration (exp), issuer (iss), audience (aud)
- Identifies security misconfigurations

### `oidc_auth_sim.py`
Simulates OpenID Connect authentication:
- ID token generation with claims
- UserInfo endpoint simulation
- Claims validation and verification
- Session management

### `oauth_vulnerability_scanner.py`
Tests OAuth implementations for common flaws:
- Redirect URI validation bypasses
- Missing state parameter
- Scope escalation attempts
- Insecure token storage detection

---

## Check Your Understanding

1. What is the difference between OAuth 2.0 and OpenID Connect? What does each protocol provide? Give an example of each.
2. Why is the Authorization Code flow with PKCE recommended for mobile apps? Describe the attack that PKCE prevents.
3. What is the purpose of a refresh token? Why not simply make access tokens last forever? Describe the security trade-off.
4. How does the `state` parameter prevent CSRF attacks in OAuth? Walk through an attack scenario that would succeed without `state`.
5. Why should an app request the minimum scopes it needs? Describe the risks of over-scoping.
6. Compare the Authorization Code flow, Client Credentials flow, and Device Code flow. When would you use each?
7. A JWT access token contains a user's roles and permissions. What are the advantages and disadvantages of this approach compared to opaque tokens that require database lookup?
8. Design an OAuth integration for a photo printing service that needs to access user's Google Photos. Specify scopes, flow, and security controls.
9. An attacker steals a refresh token from a mobile app's local storage. What can they do? How would you design the system to minimize damage?
10. Explain the complete OAuth flow from the user's perspective and from the developer's perspective. What does each party see and do?
