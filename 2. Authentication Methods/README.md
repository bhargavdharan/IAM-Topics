# 2. Authentication Methods and Password Security

## What Is Authentication?

**Authentication** is the security process of verifying that an identity is genuine — that someone or something is who or what they claim to be.

When you enter a username and password, swipe an access badge, scan your fingerprint, or approve a push notification on your phone, you are performing authentication. It is the first and most critical gatekeeper in any security system.

Authentication is distinct from authorization (which decides what you can do after you have proven your identity). Confusing these two concepts is one of the most common mistakes in security discussions.

---

## Why Learn This?

Passwords remain the most common authentication method and also the most commonly compromised. According to industry reports, stolen or weak credentials are involved in the vast majority of data breaches.

Understanding authentication enables you to:
- Build secure login systems that protect user data
- Evaluate and select appropriate authentication methods for different risk levels
- Protect your own personal and professional accounts
- Investigate authentication-related security incidents
- Design systems that balance security with usability

---

## Core Concepts

### Authentication Factors

A **factor** is a category of evidence used to prove identity. The strength of authentication depends on how many distinct factors you use and how difficult each factor is to forge, steal, or replicate.

| Factor | Category | Examples | Strengths | Weaknesses |
|--------|----------|----------|-----------|------------|
| **Knowledge** | Something you know | Password, PIN, security question | Cheap, universal, no hardware needed | Can be guessed, phished, written down, or forgotten |
| **Possession** | Something you have | Phone, smart card, hardware token, YubiKey | Requires physical access; hard to steal remotely | Can be lost, stolen, or left behind |
| **Inherence** | Something you are | Fingerprint, face, iris, voice | Cannot be forgotten; always with you | Can be spoofed; privacy concerns; cannot be changed if compromised |
| **Location** | Somewhere you are | GPS, IP address | Adds context | Can be spoofed with VPNs or proxies |
| **Behavior** | Something you do | Typing rhythm, mouse movements, gait | Passive; hard to imitate | Requires baselining; can change due to injury or context |

**The principle of multi-factor authentication:** Combining factors from different categories creates defense in depth. A password (knowledge) combined with a phone (possession) is significantly stronger than either alone. However, two passwords (knowledge + knowledge) is NOT multi-factor authentication — it is still single-factor.

**Authenticator Assurance Levels (NIST SP 800-63B):**
- **AAL1:** Single-factor authentication (password only)
- **AAL2:** Two-factor authentication (password + OTP, or password + biometric)
- **AAL3:** Two-factor authentication with hardware-backed cryptographic authenticator (password + hardware security key)

### Password Security

Passwords persist because they are universally understood, require no special hardware, and work across every device and platform. But they are also the weakest link in most security architectures.

**How passwords are compromised:**

| Attack Method | How It Works | Real-World Example |
|--------------|--------------|-------------------|
| **Phishing** | Fake login page tricks user into entering credentials | Email: "Your Amazon order has issues. Click here to resolve." |
| **Credential stuffing** | Try username/password combinations leaked from one site on another site | Same password used for LinkedIn and corporate VPN |
| **Brute force** | Try every possible password systematically | Automated tools trying millions of passwords per second against weak hashes |
| **Dictionary attack** | Try common words and variations | Tools like Hashcat with wordlists containing millions of common passwords |
| **Keylogger** | Malware records every keystroke | Infected software download that silently captures login pages |
| **Social engineering** | Manipulate person into revealing password | Phone call pretending to be IT support asking for password to "fix an issue" |
| **Data breach** | Attackers steal database containing password hashes | Have I Been Pwned catalogs billions of compromised accounts |

**What makes a password strong:**

The mathematics of password strength comes down to **entropy** — the measure of unpredictability. A password's entropy is calculated as:

```
Entropy = Length × log2(Character Set Size)
```

For example:
- 8-character password using lowercase letters only: 8 × log2(26) = 37.6 bits
- 12-character password using mixed case, numbers, and symbols: 12 × log2(94) = 78.4 bits
- 20-character passphrase using words from a 7,776-word dictionary: 20 is misleading — it's actually 4 words × log2(7776) = 51.7 bits

**Key insight from the math:** Length is the dominant factor. Adding one character to a password increases its strength exponentially, while adding more character types increases it linearly. A 16-character passphrase of common words is stronger than an 8-character complex password.

**NIST SP 800-63B modern password guidelines:**
- Minimum 8 characters (but encourage longer)
- Check against known-bad password lists (dictionary words, leaked passwords)
- Do not require arbitrary complexity rules (one uppercase, one symbol, etc.)
- Do not force periodic changes unless compromise is suspected
- Support paste functionality (enables password managers)

### Modern Authentication Standards

**FIDO2 / WebAuthn:**
FIDO2 is a passwordless authentication standard that uses public key cryptography. During registration, your device generates a unique key pair for each website. The public key goes to the server. The private key never leaves your device. During authentication, the server sends a challenge; your device signs it with the private key; the server verifies with the public key.

**Why FIDO2 is phishing-resistant:** The private key is cryptographically bound to the website's domain. A fake "gmail.com" site at "gmail-security-update.com" cannot use your real Gmail credentials because the keys do not match.

**Risk-Based Authentication (RBA):**
RBA adjusts authentication requirements based on real-time risk signals:
- Low risk (known device, normal time, familiar location) → Allow with minimal friction
- Medium risk (new device, unusual time) → Require additional factor
- High risk (impossible travel, known attacker IP, automated behavior) → Block or require step-up

**Biometric Authentication:**
Biometric systems extract mathematical templates from physical characteristics. They do NOT store raw images (which would be a privacy nightmare and easily stolen). The template is a set of measurements (minutiae points for fingerprints, feature vectors for faces) that can be compared but not reversed into the original image.

---

## How It Works

### Password Hashing: From Storage to Verification

When you create an account, the system must store something to verify future passwords. **Storing the password itself is never acceptable.** If the database is breached, attackers gain every password immediately.

**Step 1: Hashing**
A hash function transforms input into a fixed-length output:
- Same input → Same output (deterministic)
- Different input → Drastically different output (avalanche effect)
- Output cannot be reversed to find input (one-way)

```python
import hashlib
password = "hello123"
hash_md5 = hashlib.md5(password.encode()).hexdigest()
# Result: 203... (fixed length, looks random)
```

**Step 2: Why simple hashing fails — Rainbow Tables**
Attackers pre-compute hashes for millions of common passwords:
```
Password    MD5 Hash
--------    ---------
123456      e10adc3949ba59abbe56e057f20f883e
password    5f4dcc3b5aa765d61d8327deb882cf99
hello123    203... ( lookup instantly )
```
To check if your password is "hello123", the attacker just looks up its hash. This takes milliseconds.

**Step 3: Salting — defeating rainbow tables**
A **salt** is a random string unique to each password. The system hashes `password + salt` instead of just `password`.

```python
import bcrypt
password = b"hello123"
salt = bcrypt.gensalt()  # Random: b'$2b$12$N9qo8uLOickgx2ZMRZoMy...'
hashed = bcrypt.hashpw(password, salt)
```

Even if two users have the same password, their salts are different, so their hashes are completely different. Rainbow tables become useless because the attacker would need a separate table for every possible salt.

**Step 4: Adaptive hashing — staying ahead of hardware**
As computers get faster, attackers can compute more hashes per second. **Adaptive hashing algorithms** intentionally take time to compute:

| Algorithm | Key Feature | Work Factor |
|-----------|-------------|-------------|
| **bcrypt** | Adaptive cost factor | Configurable rounds (e.g., 2^12 = 4096 iterations) |
| **scrypt** | Memory-hard | Requires significant RAM, defeating GPU crackers |
| **Argon2** | Memory-hard + GPU-resistant | Winner of Password Hashing Competition; most secure |

**Why "memory-hard" matters:** GPUs and specialized cracking hardware (ASICs) excel at parallel computation but have limited memory. An algorithm that requires 64 MB of RAM per hash operation cannot be efficiently parallelized on GPUs.

**Step 5: Peppering — the secret ingredient**
A **pepper** is a secret value shared across all passwords, stored separately from the database (often in application configuration or a hardware security module). Even if the database is stolen, attackers lack the pepper.

```
Stored in DB:    hash(password + salt)
Stored in app:   PEPPER = "secret_value_123"
Actual verify:   hash(password + salt + pepper)
```

### How Biometric Authentication Works Under the Hood

**Enrollment:**
1. User places finger on scanner / looks at camera
2. Sensor captures raw biometric data (image, video, or signal)
3. Feature extraction algorithm identifies key characteristics:
   - For fingerprints: ridge endings, bifurcations, ridge flow
   - For faces: distance between eyes, nose shape, jawline
   - For iris: furrows, rings, freckles
4. Algorithm creates a mathematical template (NOT the raw image)
5. Template is encrypted and stored
6. Raw biometric data is discarded

**Authentication:**
1. User presents biometric
2. Sensor captures new sample
3. Feature extraction creates a new template
4. System compares new template against stored template
5. Similarity score is calculated
6. If score exceeds threshold → Accept; else → Reject

**Two critical metrics:**
- **FAR (False Acceptance Rate):** Probability that an impostor is accepted. Lower = more secure.
- **FRR (False Rejection Rate):** Probability that a legitimate user is rejected. Lower = more convenient.

These trade off: Making the system very strict (low FAR) increases false rejections (high FRR). Applications choose their balance based on risk tolerance.

### How FIDO2/WebAuthn Prevents Phishing

**Traditional password authentication:**
1. User types password on attacker-controlled fake site
2. Attacker captures password
3. Attacker uses password on real site

**FIDO2 authentication:**
1. Real site registers a key pair bound to its domain (e.g., `accounts.google.com`)
2. User tries to authenticate on fake site (`accounts-google-verify.com`)
3. Fake site sends challenge
4. User's device looks up private key for the requesting domain
5. Device finds no key for `accounts-google-verify.com` (key was created for `accounts.google.com`)
6. Authentication fails — even if the user is tricked, the cryptography prevents the attack

This is called **origin binding** and is the fundamental reason FIDO2 is phishing-resistant.

---

## Where You See It

| Product / Protocol | Factor Type | Use Case | Security Level |
|-------------------|-------------|----------|---------------|
| **Password login** | Knowledge | Universal default | Low alone; Medium with MFA |
| **Google Authenticator** | Possession | TOTP time-based codes | Medium |
| **Apple Face ID** | Inherence | Mobile device unlock | High |
| **YubiKey 5** | Possession | Hardware FIDO2 token | Very High |
| **Windows Hello** | Inherence + Possession | Biometric + TPM-backed key | Very High |
| **Banking apps** | Multiple | Password + SMS/hardware token | High |
| ** risk-based login** | Behavior/Context | Adjust requirements dynamically | Adaptive |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Complex passwords are always better" | Length beats complexity. `correct-horse-battery-staple` is stronger and more memorable than `Tr0ub4dor&3` |
| "Biometrics are stored as images" | Only mathematical templates are stored. Raw images are discarded after feature extraction |
| "MFA with SMS is as secure as an app" | SMS is vulnerable to SIM swapping and SS7 interception. App-based TOTP or hardware tokens are significantly safer |
| "Hashing alone protects passwords" | Salting is mandatory. Adaptive algorithms (bcrypt/Argon2) are recommended. Pepper adds another layer |
| "FIDO2 is only for enterprises" | Passkeys (consumer FIDO2) are now built into Apple, Google, and Microsoft ecosystems |
| "Biometrics can be changed like passwords" | You cannot change your fingerprint if the template is compromised. Biometrics are identifiers, not secrets |
| "Password managers are unsafe" | Password managers are significantly safer than password reuse or weak passwords. Use a reputable one |

---

## How to Practice

### Exercise 1: Observe Real Authentication Flows
1. Log into your email account from a new browser
2. Notice: password entry, possible MFA prompt, session creation
3. Open browser DevTools → Application → Cookies
4. Find the session cookie. Observe its flags (HttpOnly, Secure, SameSite)
5. Log out and observe if the cookie is deleted or invalidated

### Exercise 2: Calculate Password Entropy
1. Take three passwords you currently use (or hypothetical ones)
2. Calculate approximate entropy using the formula: Length × log2(Character Set Size)
3. Estimate crack time assuming 10 billion guesses/second (modern GPU cluster)
4. Determine which passwords need improvement

### Exercise 3: Evaluate MFA on Your Critical Accounts
1. List your 10 most important accounts (email, bank, password manager, etc.)
2. Check if MFA is enabled on each
3. Identify which use SMS (upgrade to app or hardware key if possible)
4. Save backup codes in a secure offline location

### Exercise 4: Run the Simulations
- `password_hash_demo.py` — See MD5 vs bcrypt vs Argon2 computation times
- `password_policy_enforcer.py` — Test password strength interactively
- `risk_based_auth_sim.py` — Experience adaptive authentication

---

## Projects

### `password_hash_demo.py`
Comprehensive password hashing demonstration:
- Shows MD5, SHA-256, bcrypt, scrypt, and Argon2
- Demonstrates rainbow table vulnerability
- Shows salting in action
- Benchmarks computation times across algorithms
- Explains memory-hard properties

### `password_policy_enforcer.py`
Interactive password strength analyzer:
- Calculates Shannon entropy
- Detects common passwords and keyboard patterns
- Checks against breached password lists
- Visual strength meter with time-to-crack estimates
- Provides specific improvement suggestions

### `risk_based_auth_sim.py`
Risk-based authentication simulator:
- Evaluates login attempts from multiple risk signals
- Demonstrates step-up authentication
- Shows how low-risk users get streamlined access
- Simulates device trust, location anomaly, and time-based risk

### `biometric_auth_sim.py`
Biometric authentication simulator:
- Demonstrates template matching
- Shows FAR vs FRR tradeoffs
- Simulates multi-modal biometric fusion
- Demonstrates liveness detection concepts

---

## Check Your Understanding

1. Name the three classic authentication factors. For each, give a real-world example and explain how it could be compromised.
2. Why is salting necessary for password hashes? Describe step by step what happens with and without salting when two users have the same password.
3. What makes Argon2 superior to SHA-256 for password storage? Explain "memory-hard" and why it matters for resisting GPU attacks.
4. How does risk-based authentication improve both security and user experience? Give a specific example of each risk signal and its effect.
5. Explain the difference between FAR and FRR. Why can both not be zero simultaneously, and how do different applications balance them?
6. How does FIDO2/WebAuthn prevent phishing attacks in a way that passwords and TOTP codes cannot? Explain origin binding.
7. Describe the complete process of biometric authentication, from enrollment to verification. Why are raw biometric images not stored?
8. According to NIST SP 800-63B, what modern password guidelines should organizations follow? Which legacy rules should they abandon?
9. An attacker steals a database containing password hashes but no salts. What attack can they perform? How would salts have prevented this?
10. Your organization is choosing between SMS MFA and hardware key MFA. Compare the security, cost, and usability of each for a 500-person company.
