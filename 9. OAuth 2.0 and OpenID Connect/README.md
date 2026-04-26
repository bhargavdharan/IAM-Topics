# 9. OAuth 2.0 and OpenID Connect

## What Is OAuth 2.0?

**OAuth 2.0** is an authorization framework that allows a user to grant a third-party application access to their resources without sharing their password.

**OpenID Connect (OIDC)** builds on OAuth 2.0 to add authentication — proving who the user is.

When you click "Log in with Google" or "Connect to Spotify," you are using OAuth and OIDC.

---

## Why Learn This?

OAuth 2.0 powers much of the modern web. It enables:
- Social login ("Log in with Google")
- API access (fitness app reading your health data)
- Integration (CRM importing contacts from email)
- Mobile app authentication

Understanding OAuth is essential for:
- Building applications that integrate with third-party services
- Securing APIs
- Understanding the security boundaries of delegated access

---

## Core Concepts

### OAuth 2.0 Roles

| Role | Definition | Example |
|------|-----------|---------|
| **Resource Owner** | The user who owns the data | You |
| **Client** | Application requesting access | A fitness tracking app |
| **Authorization Server** | Issues tokens after user consent | Google Accounts, Okta |
| **Resource Server** | Holds the protected data | Gmail API, Spotify API |
| **Protected Resource** | The data being accessed | Your emails, playlists |

### Authorization Flows

| Flow | Use Case | Security |
|------|----------|----------|
| **Authorization Code + PKCE** | Web apps, mobile apps | Highest |
| **Client Credentials** | Server-to-server APIs | High |
| **Device Code** | Smart TVs, IoT devices | Medium |
| **Implicit** | Legacy SPAs | Deprecated |
| **Password** | Legacy trusted apps | Discouraged |

**Authorization Code Flow (most common):**
1. User clicks "Log in with Google" on CoolApp
2. CoolApp redirects user to Google Authorization Server
3. Google asks: "CoolApp wants to read your email. Allow?"
4. User clicks "Allow"
5. Google redirects back to CoolApp with an authorization code
6. CoolApp sends the code + client secret to Google
7. Google verifies and returns an access token
8. CoolApp uses the token to fetch data from Gmail API

**The user NEVER enters their Google password on CoolApp's website.**

### Scopes: Fine-Grained Permissions

Scopes define WHAT the app can access:

| Scope | Allows | Risk If Over-Granted |
|-------|--------|---------------------|
| `profile` | Read basic profile | Low |
| `email` | Read email address | Low |
| `calendar.read` | Read calendar events | Medium |
| `calendar.write` | Create/modify events | Medium |
| `drive.read` | Read files | High |
| `drive.write` | Upload/modify files | High |

**Best practice:** Apps should request the minimum scopes needed.

### OAuth vs OpenID Connect

| | OAuth 2.0 | OpenID Connect |
|--|-----------|---------------|
| **Purpose** | Authorization (access data) | Authentication (prove identity) |
| **Question** | "Can this app access my data?" | "Who is this user?" |
| **Token** | Access Token | ID Token (JWT) |
| **Example** | "Let this app post to my Facebook" | "Log in to this site with Facebook" |

**Relationship:** OIDC uses OAuth 2.0 to get an access token, then adds an ID Token containing identity information.

---

## How It Works

### Access Tokens

An access token is a temporary credential:
- Issued by the authorization server
- Contains scopes (permissions)
- Has an expiration time (usually 15-60 minutes)
- Presented to the resource server with every API request

```http
GET /api/user/profile HTTP/1.1
Host: api.google.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**Bearer token security:** Whoever holds the token can use it. This is why HTTPS is mandatory.

### JWT (JSON Web Tokens)

Modern tokens are often JWTs — self-contained, signed JSON:

```
header.payload.signature
```

**Why JWTs are useful:**
- Self-contained (all info in the token)
- Digitally signed (cannot be tampered with)
- Can be verified without database lookup (if using asymmetric signatures)

### PKCE (Proof Key for Code Exchange)

Mobile apps and SPAs cannot securely store client secrets. PKCE solves this:
1. App generates a random "code verifier"
2. App hashes it to create "code challenge"
3. App sends challenge to authorization server
4. Later, app sends original verifier to exchange code for token
5. Server verifies: hash(verifier) == challenge

**Why it works:** Even if an attacker intercepts the authorization code, they lack the verifier and cannot exchange it.

---

## Where You See It

| Integration | OAuth Use | OIDC Use |
|------------|-----------|----------|
| **Google Sign-In** | Access Google APIs | Prove user identity |
| **GitHub Apps** | Access repositories | Identify the user |
| **Slack apps** | Post messages | Identify team members |
| **Stripe Connect** | Process payments on behalf of users | Account linking |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "OAuth is for authentication" | OAuth is for authorization; OIDC adds authentication on top |
| "Access tokens are encrypted" | Access tokens are signed, not necessarily encrypted. Do not put sensitive data in them |
| "Refresh tokens last forever" | Refresh tokens should be rotatable and revocable |
| "The client secret is a password" | The client secret identifies the application, not the user |

---

## How to Practice

1. **Inspect an OAuth flow in your browser**
   - Open Developer Tools → Network tab
   - Log in with Google on a third-party site
   - Watch the redirects, authorization code, and token exchange

2. **Evaluate scopes an app requests**
   - Next time you authorize an app, read the scope list carefully
   - Ask: Does this app need ALL of these permissions?

3. **Run the simulations**
   - `oauth_flow_sim.py` demonstrates the complete authorization code flow
   - `jwt_inspector.py` decodes and validates JSON Web Tokens

---

## Projects

### `oauth_flow_sim.py`
Simulates the complete OAuth 2.0 authorization code flow:
- Authorization server with consent screen
- Client application requesting tokens
- Token issuance and validation
- Resource server verifying access tokens

### `jwt_inspector.py`
Decodes and validates JSON Web Tokens:
- Parses header, payload, and signature
- Verifies token signatures
- Checks expiration and issuer

### `oidc_auth_sim.py`
Simulates OpenID Connect authentication:
- ID token generation
- UserInfo endpoint simulation
- Claims validation

### `oauth_vulnerability_scanner.py`
Tests OAuth implementations for common flaws:
- Redirect URI validation
- State parameter usage
- Scope escalation checks

---

## Check Your Understanding

1. What is the difference between OAuth 2.0 and OpenID Connect? What does each provide?
2. Why is the Authorization Code flow with PKCE recommended for mobile apps?
3. What is the purpose of a refresh token? Why not just make access tokens last forever?
4. How does the `state` parameter prevent CSRF attacks in OAuth?
5. Why should an app request the minimum scopes it needs?
