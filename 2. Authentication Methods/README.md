# 2. Authentication Methods and Password Security

## 🏠 Real-World Analogy: Proving You're a Club Member

Imagine an exclusive private club. To enter, you need to prove your identity. The club offers several ways:

1. **Password** = Secret handshake only members know
2. **Security token** = Physical membership card with a chip
3. **Biometric** = Fingerprint scanner at the door
4. **Behavioral** = The bouncer recognizes your walk and voice
5. **Risk-based** = If you're a regular coming at your usual time, they wave you through. If it's your first time or you're visiting at 3 AM, they ask for extra ID.

**Authentication is simply: proving you are who you claim to be.**

---

## 📋 Overview

Authentication is the **first line of defense** in cybersecurity. Every time you log in — whether it's your email, bank, or social media — authentication is happening behind the scenes. 

Understanding how it works (and how it fails) is essential for both users and security professionals.

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain the five types of authentication factors with real-world examples
- Describe why password complexity matters and how passwords are stored securely
- Compare modern authentication methods (FIDO2, WebAuthn, biometrics)
- Understand risk-based and adaptive authentication
- Name common authentication attacks and how to prevent them

---

## 📚 Key Concepts

### Authentication Factors

| Factor Type | Simple Name | Examples | Security Level |
|-------------|-------------|----------|---------------|
| **Knowledge** | Something you **know** | Password, PIN, security question | ⚠️ Can be guessed or phished |
| **Possession** | Something you **have** | Phone, smart card, YubiKey | ✅ Harder to steal remotely |
| **Inherence** | Something you **are** | Fingerprint, face, voice | ✅ Very hard to fake |
| **Location** | Somewhere you **are** | GPS, IP address | ⚠️ Can be spoofed |
| **Behavior** | Something you **do** | Typing rhythm, mouse movements | ✅ Hard to imitate |

> 💡 **The more factors you use, the stronger the authentication.** This is why MFA (Module 3) is so important.

### Password Security

**Why passwords are still everywhere:**
- Cheap to implement
- Everyone understands them
- Work on every device

**Why passwords are problematic:**
- People reuse them across sites
- Common passwords are easily guessed
- Data breaches expose millions at once
- Phishing tricks people into revealing them

**Strong Password Principles:**

| Rule | Why It Matters | Example |
|------|---------------|---------|
| Minimum 12-16 characters | Each character exponentially increases cracking time | `correct-horse-battery-staple` |
| Mix of character types | Prevents dictionary attacks | `Tr0ub4dor&3` |
| No personal information | Social media makes this easy to guess | NOT `John1990!` |
| Unique per account | One breach doesn't compromise everything | Use a password manager |
| Changed only when compromised | Frequent changes lead to predictable patterns | NIST 2020 guidance |

### Password Hashing: Why Companies Should NEVER Store Your Actual Password

**The golden rule:** If a company can email you your password, they are storing it insecurely. Proper systems store a **hash** — a one-way mathematical fingerprint.

---

## 🔧 Under the Hood

### How Password Hashing Actually Works

When you create a password, the system transforms it through a **hash function** — a mathematical operation that:
- Always produces the same output for the same input
- Cannot be reversed (you can't get the password from the hash)
- Produces drastically different output even if inputs are similar

**Analogy:** A hash is like a meat grinder. You can turn a steak into ground beef, but you can never turn ground beef back into a steak.

```python
# Simplified example (DO NOT use MD5 in production!)
import hashlib

password = "hello123"
hash_value = hashlib.md5(password.encode()).hexdigest()
print(hash_value)  # 203... (fixed length, looks random)
```

**The problem with simple hashing:** Attackers pre-compute hashes for millions of passwords and store them in "rainbow tables." To check if your password is "hello123", they just look up its hash.

### Salting: Adding Randomness

A **salt** is a random string added to your password before hashing. Even if two users have the same password, their hashes will be completely different.

```python
# With salting
import bcrypt

password = b"hello123"
salt = bcrypt.gensalt()  # Random salt: e.g., b'$2b$12$N9qo8uLOickgx2ZMRZoMy...'
hashed = bcrypt.hashpw(password, salt)

# Verification
bcrypt.checkpw(b"hello123", hashed)  # True
bcrypt.checkpw(b"wrongpass", hashed)  # False
```

**Why salting defeats rainbow tables:**
- Without salt: `hash("hello123")` is always the same → lookup in table
- With salt: `hash("hello123" + random_salt_1")` ≠ `hash("hello123" + random_salt_2")` → table useless

### Peppering: The Secret Ingredient

A **pepper** is a secret value added to ALL passwords, stored separately from the database (often in code or a hardware security module).

```
Stored in database:     hash(password + salt)
Stored in application:  PEPPER = "secret_value_123"
Actual verification:    hash(password + salt + pepper)
```

**Why it helps:** Even if the database is stolen, attackers lack the pepper, making offline cracking impossible.

### Modern Password Hashing Algorithms

| Algorithm | Status | Why |
|-----------|--------|-----|
| **MD5** | ❌ Broken | Cryptographically insecure, trivial to crack |
| **SHA-1** | ❌ Deprecated | Collision attacks demonstrated |
| **SHA-256** | ⚠️ Weak alone | Fast to compute = fast to crack; needs salt + stretching |
| **bcrypt** | ✅ Recommended | Adaptive cost factor — gets slower over time |
| **scrypt** | ✅ Recommended | Memory-hard — requires lots of RAM, defeating GPU crackers |
| **Argon2** | ✅ Best Practice | Winner of Password Hashing Competition; most secure |

**Adaptive cost factor (bcrypt):** You can configure bcrypt to take 100ms, 500ms, or 2 seconds to hash a password. As computers get faster, you increase the cost. Attackers must spend the same time per guess, making brute force impractical.

### How Biometric Authentication Works

Your fingerprint isn't stored as an image. That would be:
- Huge files
- Privacy nightmare
- Easy to fake with a photo

**Under the hood:** Biometric systems extract **minutiae points** — specific features like ridge endings and bifurcations — and store a mathematical template.

```
Fingerprint Image → Extract Features → Create Template → Store Template
                                         (not the image!)
```

| Metric | What It Means | Trade-off |
|--------|--------------|-----------|
| **FAR (False Acceptance Rate)** | Wrong person accepted | Lower = more secure, but... |
| **FRR (False Rejection Rate)** | Right person rejected | Lower = more convenient, but... |

**Balancing act:** Making the system very strict (low FAR) means you might be rejected often (high FRR). Banks prefer low FAR; phone unlocks prefer low FRR.

### FIDO2 / WebAuthn: The Future of Authentication

FIDO2 is a passwordless standard that uses **public key cryptography**:

1. **Registration:** Your device generates a unique key pair (public + private). The public key goes to the server; the private key NEVER leaves your device.
2. **Authentication:** The server sends a challenge. Your device signs it with the private key. The server verifies the signature with the public key.

**Why it's phishing-proof:** The private key is bound to the website's domain. A fake "gmail.com" site cannot use your real gmail.com credentials because the keys don't match.

### Risk-Based Authentication (RBA)

RBA adapts security requirements based on risk signals:

| Signal | Low Risk Example | High Risk Example | Result |
|--------|-----------------|-------------------|--------|
| **Location** | Logging in from home | Logging in from a new country | May require MFA |
| **Device** | Your known laptop | Unknown device | Step-up authentication |
| **Time** | 9 AM on a workday | 3 AM on a weekend | Additional verification |
| **Behavior** | Normal typing pattern | Automated/scripted input | Block or challenge |

---

## 🛠️ Projects in This Module

### `password_policy_enforcer.py`
Validates passwords against enterprise policy rules:
- Length, complexity, and entropy checks
- Dictionary and breached password detection
- NIST SP 800-63B compliance validation
- Generates strength scores and improvement suggestions

### `password_hash_demo.py`
Demonstrates modern password hashing:
- Implements bcrypt, scrypt, and Argon2
- Shows salt generation and verification
- Compares hash computation times
- Demonstrates why older algorithms fail

### `biometric_auth_sim.py`
Simulates biometric authentication systems:
- Fingerprint template matching with tolerance thresholds
- False Acceptance Rate (FAR) vs False Rejection Rate (FRR)
- Liveness detection simulation
- Multi-modal biometric fusion

### `risk_based_auth_sim.py`
Simulates adaptive authentication:
- Evaluates login risk from multiple signals
- Device trust scoring
- Location anomaly detection
- Behavior pattern analysis
- Dynamic step-up authentication

---

## 📝 Quiz Questions

1. **Name the three classic authentication factors and give a real-world example of each.**
2. **Why is salting necessary for password hashes? What problem does it solve?**
3. **What makes Argon2 superior to bcrypt? What does "memory-hard" mean?**
4. **How does risk-based authentication improve both security AND user experience?**
5. **What is the difference between FAR and FRR in biometrics? Why can't both be zero?**
6. **How does FIDO2/WebAuthn prevent phishing attacks?**

---

## 🔗 Further Reading

- [NIST SP 800-63B - Authentication and Lifecycle Management](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [FIDO Alliance Specifications](https://fidoalliance.org/specifications/)

---

## 🏷️ Tags
`#Authentication` `#PasswordSecurity` `#Biometrics` `#FIDO2` `#RiskBasedAuth` `#Hashing` `#Salting`
