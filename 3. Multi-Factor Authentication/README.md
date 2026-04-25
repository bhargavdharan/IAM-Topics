# 3. Multi-Factor Authentication (MFA)

## 🏠 Real-World Analogy: The Bank Vault

Imagine a bank vault that requires **two different keys** to open:
1. A **physical key** that the bank manager carries
2. A **combination code** that only the treasurer knows

Neither person can open the vault alone. Even if a thief steals the manager's key, they don't know the combination. Even if they kidnap the treasurer (horrible thought!), they don't have the physical key.

**MFA is exactly this:** requiring multiple *different types* of proof before granting access.

---

## 📋 Overview

Multi-Factor Authentication (MFA) requires users to provide **two or more verification factors** to gain access. According to Microsoft, MFA blocks **99.9%** of automated credential-based attacks.

Even if your password is stolen in a data breach, MFA prevents the attacker from logging in — because they don't have your second factor.

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain why MFA is one of the most effective security controls
- Describe TOTP, HOTP, push notifications, and hardware tokens
- Understand MFA bypass techniques and how to prevent them
- Recognize and defend against MFA fatigue attacks
- Explain how TOTP works under the hood

---

## 📚 Key Concepts

### Why Passwords Alone Are Not Enough

Even "strong" passwords can be compromised:

| Attack Method | How It Works | Real Example |
|--------------|--------------|--------------|
| **Phishing** | Fake login page tricks you into entering credentials | "Your Amazon order has issues" email |
| **Keylogger** | Malware records every keystroke | Infected software download |
| **Data Breach** | Company database leaked with passwords | HaveIBeenPwned lists billions |
| **Password Guessing** | Automated tools try common passwords | "123456" still top password in 2024 |
| **Credential Stuffing** | Try leaked username/password combos on other sites | Same password for LinkedIn and bank |

**MFA adds layers so that compromised credentials alone are insufficient.**

### MFA Methods Compared

| Method | Security | Usability | How It Works | Best For |
|--------|----------|-----------|--------------|----------|
| **SMS OTP** | ⚠️ Medium | ✅ Easy | Code texted to your phone | Beginners, quick deployment |
| **TOTP (App)** | ✅ Good | ✅ Easy | 6-digit code changes every 30 seconds | Most users (Google Auth, Authy) |
| **Push Notification** | ✅ Good | ✅ Easy | Tap "Approve" on your phone | Convenience-focused |
| **Hardware Token** | ✅ Strong | ⚠️ Moderate | Physical USB device (YubiKey) | High-security users |
| **Biometric** | ✅ Strong | ✅ Easy | Fingerprint or face scan | Mobile devices |
| **WebAuthn/FIDO2** | ✅ Strongest | ✅ Easy | Cryptographic key pair | Passwordless future |

> ⚠️ **Why SMS is less secure:** SMS messages can be intercepted through SIM swapping, SS7 attacks, or phone malware. App-based TOTP and hardware tokens are safer.

### TOTP (Time-based One-Time Password)

TOTP is the most common MFA method (used by Google Authenticator, Authy, Microsoft Authenticator).

**How it feels:** You open an app, see a 6-digit code like `739284`, and type it before it expires.

---

## 🔧 Under the Hood

### How TOTP Actually Works

TOTP is defined in [RFC 6238](https://tools.ietf.org/html/rfc6238). Here's what happens behind the scenes:

#### Step 1: Secret Sharing (One-Time Setup)

When you enable MFA on a website:
1. The server generates a **random secret** (e.g., `JBSWY3DPEHPK3PXP`)
2. It encodes this secret as a **QR code** for easy scanning
3. Your authenticator app scans the QR code and stores the secret
4. The server also stores the secret linked to your account

**Critical:** The secret is the same on both sides, but it's never transmitted again after setup.

#### Step 2: Code Generation (Every 30 Seconds)

```
TOTP = Truncate(HMAC-SHA1(secret_key, current_time / 30))
```

Breaking this down:

1. **Current time / 30**: The current Unix timestamp is divided by 30 (the time window). This gives a number that changes every 30 seconds.
   - Example: If timestamp is `1705312085`, then `1705312085 / 30 = 56843739`

2. **HMAC-SHA1**: A cryptographic function that mixes the secret key with the time counter.
   - Think of HMAC as a "secure blender" — you put in the secret and the time, and you get a fixed-length output that looks random.

3. **Truncate**: Take the last 4 bytes of the HMAC output, convert to a number, and take the last 6 digits.

```python
# Conceptual TOTP implementation
import hmac, hashlib, struct, time, base64

def generate_totp(secret_b32):
    secret = base64.b32decode(secret_b32)
    counter = int(time.time()) // 30  # Changes every 30 seconds
    
    # Create HMAC-SHA1
    msg = struct.pack(">Q", counter)  # 8-byte big-endian counter
    hmac_result = hmac.new(secret, msg, hashlib.sha1).digest()
    
    # Dynamic truncation
    offset = hmac_result[-1] & 0x0F
    code = struct.unpack(">I", hmac_result[offset:offset+4])[0]
    code = code & 0x7FFFFFFF  # Clear highest bit
    return code % 1000000  # Last 6 digits
```

**Why 30 seconds?** 
- Shorter = more secure but harder to type in time
- Longer = more convenient but more vulnerable to replay attacks
- 30 seconds is the sweet spot defined in the standard

**Time synchronization:** Both your phone and the server need roughly correct time. A drift of a few seconds is handled by checking the previous and next windows.

### HOTP vs TOTP

| Feature | HOTP | TOTP |
|---------|------|------|
| Full name | HMAC-based One-Time Password | Time-based One-Time Password |
| Counter | Event-based (incrementing number) | Time-based (clock) |
| Example | Press button on hardware token | Google Authenticator codes |
| Advantage | Works offline forever | Synchronizes automatically |
| Disadvantage | Can get out of sync | Requires reasonably accurate time |

### Push Notification MFA Under the Hood

1. You enter your password on the website
2. The website sends a push request to your phone via Apple Push Notification Service (APNS) or Firebase Cloud Messaging (FCM)
3. Your authenticator app receives the push and shows "Approve login to Gmail?"
4. You tap "Approve"
5. Your phone cryptographically signs an approval message
6. The website verifies the signature and completes login

### Numbered Challenge Verification

Modern push MFA uses **numbered challenges** to prevent MFA fatigue attacks:

```
Website shows:  "Enter code 7392 on your phone"
Phone shows:    "Are you logging in to Gmail? Code: 7392 [Approve] [Deny]"
```

This prevents attackers from flooding you with approvals — you must match the number.

### MFA Bypass Techniques

| Technique | How It Works | Prevention |
|-----------|--------------|------------|
| **MFA Fatigue** | Flood user with push notifications until they approve | Numbered matching, rate limiting |
| **SIM Swapping** | Transfer victim's phone number to attacker's SIM | Avoid SMS MFA; use app-based |
| **Real-time Phishing** | Proxy login session to victim; victim completes MFA for attacker | Numbered verification, FIDO2 |
| **Token Theft** | Steal session cookies after legitimate MFA | Device binding, continuous auth |
| **SS7 Attacks** | Intercept SMS messages via phone network | Avoid SMS-based MFA |

---

## 🛠️ Projects in This Module

### `totp_generator.py`
Implements RFC 6238 TOTP algorithm:
- Generates QR codes for secret setup
- Creates 6-digit codes with 30-second windows
- Validates codes with drift tolerance
- Demonstrates secret key generation and Base32 encoding

### `mfa_flow_simulator.py`
Simulates complete MFA enrollment and login flows:
- User registration with MFA setup
- Login with primary and secondary factor
- Backup code generation and recovery
- Device trust and remembered devices
- Account lockout on repeated failures

### `mfa_bypass_detector.py`
Analyzes authentication logs for MFA bypass attempts:
- Detects push notification flooding
- Identifies suspicious MFA disable requests
- Flags unusual device or location patterns
- Alerts on repeated failed MFA attempts

### `hardware_token_sim.py`
Simulates FIDO2/WebAuthn hardware token behavior:
- Challenge-response authentication
- Public key credential creation
- Origin binding and anti-phishing
- Resident key and discoverable credentials

---

## 📝 Quiz Questions

1. **Why is SMS-based MFA considered less secure than app-based TOTP? Name two attacks.**
2. **How does TOTP prevent replay attacks? Why can't an attacker reuse a code?**
3. **What is an MFA fatigue attack and how can numbered challenges prevent it?**
4. **Explain the difference between HOTP and TOTP. When would you use each?**
5. **Why is FIDO2 considered phishing-resistant? What makes it different from TOTP?**
6. **What happens if your phone's clock is wrong by 2 minutes? Will TOTP still work?**

---

## 🔗 Further Reading

- [RFC 6238 - TOTP](https://tools.ietf.org/html/rfc6238)
- [Microsoft: MFA blocks 99.9% of attacks](https://www.microsoft.com/security/blog/2019/08/20/one-simple-action-you-can-take-to-prevent-99-9-percent-of-account-attacks/)
- [OWASP MFA Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)

---

## 🏷️ Tags
`#MFA` `#TOTP` `#TwoFactorAuth` `#FIDO2` `#WebAuthn` `#PushNotification` `#Authentication`
