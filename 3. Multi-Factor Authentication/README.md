# 3. Multi-Factor Authentication (MFA)

## What Is MFA?

**Multi-Factor Authentication (MFA)** requires users to provide two or more verification factors from different categories before granting access. It is one of the most effective security controls available, blocking the vast majority of automated and credential-based attacks.

The principle is simple: even if one factor is compromised, the attacker still lacks the other factor(s) and cannot gain access.

---

## Why Learn This?

Passwords are compromised constantly through phishing, data breaches, and malware. MFA is the single most impactful control an organization or individual can deploy to protect accounts. Microsoft reports that MFA blocks over 99.9% of automated attacks.

Understanding how MFA works — and how it can be bypassed — is essential for:
- Implementing secure systems
- Choosing appropriate MFA methods
- Defending against MFA-targeted attacks
- Educating users on proper MFA hygiene

---

## Core Concepts

### Why Passwords Alone Are Insufficient

Even strong passwords can be compromised:

| Attack | How It Works | Real Example |
|--------|-------------|--------------|
| **Phishing** | Fake login page harvests credentials | "Your package delivery failed" email |
| **Keylogger** | Malware records keystrokes | Infected software installer |
| **Data breach** | Database leaked with passwords | Have I Been Pwned catalogs billions |
| **Credential stuffing** | Try leaked combos on other sites | Same password for LinkedIn and bank |
| **Password guessing** | Automated tools try common passwords | "123456" still most common password |

MFA addresses these by ensuring that knowing the password is necessary but not sufficient.

### MFA Methods Compared

Not all MFA methods provide equal security:

| Method | Security | Usability | How It Works |
|--------|----------|-----------|--------------|
| **SMS OTP** | Medium | Easy | Code texted to phone |
| **TOTP (app)** | Good | Easy | Time-based code from authenticator app |
| **Push notification** | Good | Easy | Approve login via mobile app |
| **Hardware token** | Strong | Moderate | Physical USB device (YubiKey) |
| **Biometric** | Strong | Easy | Fingerprint or face scan |
| **WebAuthn/FIDO2** | Strongest | Easy | Cryptographic key pair, phishing-resistant |

**Critical distinction:** SMS-based MFA is significantly less secure than app-based or hardware-based MFA because SMS messages can be intercepted through SIM swapping, SS7 attacks, or phone malware. App-based TOTP and hardware tokens are strongly preferred.

### TOTP (Time-based One-Time Password)

TOTP is the most widely deployed MFA method, used by Google Authenticator, Authy, and Microsoft Authenticator.

**How it works at a high level:**
1. During setup, the server generates a random secret and shares it with your authenticator app (typically via QR code)
2. Both the server and your app store this secret
3. Every 30 seconds, both sides independently compute a 6-digit code using the secret and the current time
4. During login, you enter the code shown on your app
5. The server computes what the code should be and compares

**Why the code changes:** The 30-second window means each code is valid only briefly, preventing replay attacks where an attacker reuses an intercepted code.

### MFA Bypass Techniques

Understanding how MFA fails is as important as understanding how it works:

| Technique | How It Works | Prevention |
|-----------|--------------|------------|
| **MFA fatigue** | Flood user with push notifications until they approve | Numbered challenge verification |
| **SIM swapping** | Transfer victim's phone number to attacker's SIM | Avoid SMS; use app-based MFA |
| **Real-time phishing** | Proxy login session to victim who completes MFA | FIDO2/WebAuthn with origin binding |
| **Token theft** | Steal session cookies after legitimate MFA | Device binding, short session lifetimes |
| **SS7 attacks** | Intercept SMS at the phone network level | Avoid SMS-based MFA |

**Numbered challenge verification:** Modern push MFA shows a matching number on both the login screen and the phone. The user must verify the numbers match before approving. This prevents users from blindly approving push floods.

---

## How It Works

### TOTP Under the Hood (RFC 6238)

The TOTP algorithm combines three ingredients:
1. A **shared secret** (randomly generated during setup)
2. The **current timestamp** divided by the time window (usually 30 seconds)
3. **HMAC-SHA1** — a cryptographic function that mixes the secret with the time counter

The result is truncated to produce a 6-digit code.

```python
# Conceptual implementation
counter = int(current_time) // 30
hmac_result = HMAC-SHA1(secret, counter)
code = truncate_to_6_digits(hmac_result)
```

**Why HMAC-SHA1?** HMAC (Hash-based Message Authentication Code) is a secure way to combine a key with a message. Even if an attacker observes many TOTP codes, they cannot reverse-engineer the secret because HMAC is computationally irreversible.

**Time synchronization:** Both your phone and the server need approximately correct time. A drift of a few minutes is handled by checking adjacent time windows.

### HOTP vs TOTP

| Feature | HOTP | TOTP |
|---------|------|------|
| Counter | Event-based (incrementing number) | Time-based (clock) |
| Example | Hardware token with physical button | Google Authenticator |
| Advantage | Works offline indefinitely | Self-synchronizing |
| Disadvantage | Can get out of sync | Requires reasonably accurate time |

### Push Notification MFA Under the Hood

1. You enter your password on the website
2. The website sends a push request to your phone via Apple Push Notification Service (APNS) or Firebase Cloud Messaging (FCM)
3. Your authenticator app receives the push and displays "Approve login to Gmail?"
4. You tap "Approve"
5. Your phone cryptographically signs an approval message
6. The website verifies the signature and completes login

**Key security feature:** The approval is cryptographically signed by your device. An attacker cannot forge an approval without your device's private key.

---

## Where You See It

| Product | MFA Method | Notes |
|---------|-----------|-------|
| **Google Account** | TOTP, Push, FIDO2 | Security key recommended for high-risk users |
| **Microsoft 365** | TOTP, Push, FIDO2 | Azure AD Conditional Access policies |
| **Banking apps** | SMS, Push, Hardware token | Regulations often require MFA |
| **GitHub** | TOTP, FIDO2, SMS | SSH keys + MFA for code repositories |
| **AWS IAM** | Hardware token, Virtual MFA | Root account must have MFA |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "MFA is unhackable" | MFA can be bypassed via real-time phishing, token theft, or MFA fatigue |
| "SMS is good enough" | SIM swapping and SS7 interception make SMS the weakest MFA method |
| "Backup codes are unnecessary" | Without backup codes, losing your phone means losing access to your account |
| "TOTP codes are sent from the server" | TOTP codes are generated locally on your device; nothing is transmitted during login |
| "Push notification is less secure" | Push with numbered challenges is significantly more secure than SMS |

---

## How to Practice

1. **Enable MFA on your critical accounts**
   - Start with email, banking, and password manager
   - Use an authenticator app (Authy, Google Authenticator, or Microsoft Authenticator)
   - Save backup codes in a secure location

2. **Observe TOTP generation**
   - Run `totp_generator.py` to see the algorithm in action
   - Notice how the code changes every 30 seconds
   - Understand why both sides must share the same secret

3. **Simulate MFA attacks and defenses**
   - Run `mfa_flow_simulator.py` to experience enrollment, login, and account lockout
   - Run `mfa_bypass_detector.py` to identify suspicious patterns in authentication logs

4. **Compare MFA methods for a real scenario**
   - You are choosing MFA for a 500-employee company
   - Compare cost, usability, and security of app-based TOTP vs hardware keys
   - Document your recommendation with justification

---

## Projects

### `totp_generator.py`
Implements RFC 6238 TOTP from scratch:
- Generates codes from a shared secret
- Shows the HMAC-SHA1 calculation step by step
- Validates codes with drift tolerance
- Demonstrates Base32 encoding

### `mfa_flow_simulator.py`
Complete MFA enrollment and login simulation:
- User registration with MFA setup
- Login with primary and secondary factors
- Backup code generation and recovery
- Device trust and remembered devices
- Account lockout on repeated failures
- MFA fatigue attack demonstration

### `mfa_bypass_detector.py`
Analyzes authentication logs:
- Detects push notification flooding
- Flags suspicious MFA disable requests
- Identifies unusual device or location patterns
- Alerts on repeated failed MFA attempts

### `hardware_token_sim.py`
Simulates FIDO2/WebAuthn token behavior:
- Challenge-response authentication
- Public key credential creation
- Origin binding and anti-phishing
- Resident key and discoverable credentials

---

## Check Your Understanding

1. Why is SMS-based MFA considered less secure than app-based TOTP? Name two specific attacks.
2. How does TOTP prevent replay attacks? Why can't an attacker reuse a code they intercepted?
3. What is an MFA fatigue attack and how does numbered challenge verification prevent it?
4. Explain the difference between HOTP and TOTP. When would you choose each?
5. Why is FIDO2 considered phishing-resistant? What makes it different from TOTP?
6. What happens if your phone's clock is wrong by 2 minutes? Will TOTP still work? Why or why not?
