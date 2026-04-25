# 1. Introduction to Identity and Access Management (IAM)

## 🏠 Real-World Analogy: The Hotel Security System

Imagine checking into a luxury hotel:

1. **At the front desk**, you show your passport. The clerk verifies your face matches the photo. → This is **Authentication**
2. **You receive a key card** that opens your room (101), the gym, and the lobby — but NOT the staff kitchen or other guests' rooms. → This is **Authorization**
3. **Security cameras** record that you entered the gym at 7 PM. → This is **Audit/Accounting**
4. **When you check out**, your key card is deactivated. → This is **Deprovisioning**

**IAM is exactly this — but for every digital system you use.**

---

## 📋 Overview

Identity and Access Management (IAM) is the security discipline that makes sure the **right people** can access the **right resources** at the **right times** for the **right reasons**.

Without IAM, it's like a hotel where:
- Anyone can claim any room
- Master keys are left on the front desk
- There are no cameras or logs
- Former employees still have working key cards

> 🔑 **IAM answers two fundamental questions:**
> 1. **Who are you?** (Identity)
> 2. **What can you do?** (Access)

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain IAM using real-world analogies
- Describe the five stages of the IAM lifecycle
- Understand the CIA Triad and how IAM supports it
- Differentiate between identity management and access management
- Explain the Principle of Least Privilege and Separation of Duties
- Name common IAM standards and frameworks

---

## 📚 Key Concepts

### The IAM Lifecycle

Every identity goes through a journey:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. Create  │───→│  2. Verify  │───→│  3. Permit  │
│  Provision  │    │Authenticate │    │ Authorize   │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
┌─────────────┐    ┌─────────────┐           │
│  5. Remove  │←───│  4. Watch   │←──────────┘
│Deprovision  │    │   Monitor   │
└─────────────┘    └─────────────┘
```

| Stage | Hotel Example | Digital Example |
|-------|--------------|-----------------|
| **Provision** | Guest checks in, gets key card | HR creates new employee account |
| **Authenticate** | Clerk checks ID | User enters username + password |
| **Authorize** | Key card opens allowed doors | System checks permissions |
| **Monitor** | Security cameras and logs | Audit logs track all actions |
| **Deprovision** | Key card deactivated at checkout | Account disabled when employee leaves |

### Core Components

| Component | Simple Definition | Hotel Equivalent | Digital Example |
|-----------|-------------------|------------------|-----------------|
| **Identity** | A unique digital representation | Guest registration record | `jdoe@company.com` |
| **Credential** | Proof of who you are | Passport, driver's license | Password, fingerprint, security key |
| **Authentication** | Verifying your identity | Matching face to passport | Logging in with username + password |
| **Authorization** | Deciding what you can do | Key card access levels | Permission to view `finance-reports` |
| **Accounting** | Recording what you did | Security camera footage | Audit log: "jdoe downloaded Q4-report.pdf at 14:32" |

### Identity Types

| Type | Examples | Why They Matter |
|------|----------|----------------|
| **Human Identities** | Employees, contractors, customers, partners | Most visible, but also most vulnerable to phishing |
| **Machine Identities** | Servers, applications, APIs, IoT devices | Often over-permissioned and forgotten |
| **Privileged Identities** | Administrators, root accounts | "Keys to the kingdom" — highest risk if compromised |

### The CIA Triad

IAM protects information through three pillars:

| Pillar | What It Means | IAM's Role |
|--------|--------------|-----------|
| **Confidentiality** | Only authorized users see data | Authentication + Authorization prevent unauthorized access |
| **Integrity** | Data cannot be tampered with | Audit logs detect unauthorized changes |
| **Availability** | Systems work when needed | Proper provisioning ensures users can do their jobs |

### Principle of Least Privilege (PoLP)

> **Simple rule:** Give people the *minimum* access they need to do their job — nothing more.

**Hotel analogy:** A housekeeper gets a key that opens guest rooms (for cleaning) but NOT the hotel safe or manager's office.

**Why it matters:** If a housekeeper's key is stolen, the thief can only enter rooms — not steal the hotel's money.

**Digital example:** A marketing employee can access the CMS but NOT the production database.

### Separation of Duties (SoD)

> **Simple rule:** No single person should control an entire sensitive process.

**Real-world analogy:** At a bank, the person who approves a loan is different from the person who disburses the money.

**Digital example:** In IAM, the person who can create user accounts should NOT be the same person who can approve access to financial systems.

---

## 🔧 Under the Hood

### How Identity Stores Actually Work

Behind every IAM system is a **directory service** — essentially a specialized database optimized for looking up users and their attributes.

**LDAP (Lightweight Directory Access Protocol)** is the most common standard. Think of it like a phonebook that stores:
- Usernames and passwords (hashed, never plain text!)
- Group memberships
- Email addresses, phone numbers
- Organizational hierarchy

```
Directory Tree Structure (like a family tree):

dc=company,dc=com
├── ou=Users
│   ├── uid=jdoe (cn=John Doe, mail=jdoe@company.com)
│   ├── uid=asmith
│   └── uid=badmin
├── ou=Groups
│   ├── cn=Finance (member: jdoe, asmith)
│   └── cn=Admins (member: badmin)
└── ou=Devices
    └── cn=laptop-jdoe-001
```

**Under the hood:** When you log in, the system:
1. Receives your username
2. Searches the directory for that user
3. Retrieves your stored password hash
4. Hashes the password you just entered
5. Compares the two hashes (never the raw passwords!)
6. If they match, looks up your group memberships
7. Determines your permissions based on those groups

### How Session Tokens Work

After you authenticate, the system doesn't ask for your password on every click. Instead, it gives you a **session token** — like a temporary wristband at a concert.

**Under the hood:**
1. After successful login, the server generates a unique random string (e.g., `sess_abc123xyz`)
2. It stores this in a database with your user ID and expiration time
3. It sends this token to your browser as a **cookie**
4. On every subsequent request, your browser automatically sends this cookie
5. The server looks up the token, finds your user ID, and knows who you are

```python
# Simplified session token logic
def create_session(user_id):
    token = generate_random_string(32)  # e.g., "a3f7b2..."
    expiration = now() + 2_hours
    save_to_database(token, user_id, expiration)
    return token

def check_session(token):
    session = lookup_database(token)
    if session and session.expiration > now():
        return session.user_id
    return None  # Token expired or invalid
```

### Audit Logs: The Digital Security Camera

Every IAM system logs actions for compliance and forensics. A typical audit log entry contains:

```json
{
  "timestamp": "2024-01-15T14:32:18Z",
  "user_id": "jdoe",
  "action": "FILE_DOWNLOAD",
  "resource": "finance/Q4-report.pdf",
  "result": "ALLOWED",
  "ip_address": "192.168.1.45",
  "user_agent": "Mozilla/5.0...",
  "session_id": "sess_abc123"
}
```

**Why this matters:** If a breach occurs, audit logs answer:
- WHO did it?
- WHAT did they do?
- WHEN did it happen?
- WHERE were they logging in from?

---

## 🔧 Standards and Frameworks

| Standard | What It Covers | Why It Matters |
|----------|---------------|----------------|
| **NIST SP 800-63** | Digital Identity Guidelines | US federal standard for authentication strength |
| **ISO/IEC 27001** | Information Security Management | International certification standard |
| **COBIT** | IT Governance Framework | Helps align IAM with business goals |
| **CSA CCM** | Cloud Security Controls | Specifically for cloud IAM implementations |

---

## 🛠️ Projects in This Module

### `identity_lifecycle_sim.py`
Simulates the complete IAM lifecycle for an organization:
- Onboards new employees with role-based provisioning
- Simulates role changes and access modifications
- Handles offboarding with complete access revocation
- Generates audit reports for compliance

**Run it:** `python "1. Introduction to IAM/projects/identity_lifecycle_sim.py"`

### `iam_maturity_assessment.py`
Evaluates an organization's IAM maturity across dimensions:
- Identity governance
- Access management
- Privileged access
- Authentication strength
- Monitoring and analytics

---

## 📝 Quiz Questions

1. **What are the two fundamental questions IAM answers?**
2. **Name the five stages of the IAM lifecycle and give a real-world example for each.**
3. **What is the Principle of Least Privilege? Why is it like giving a housekeeper only a room key?**
4. **How does Separation of Duties prevent fraud?**
5. **What is the difference between authentication and authorization?**
6. **What information does an audit log typically capture?**

---

## 🔗 Further Reading

- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)
- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001)
- [IAM Architecture Guide - Gartner](https://www.gartner.com)

---

## 🏷️ Tags
`#IAM` `#IdentityManagement` `#AccessManagement` `#Cybersecurity` `#LeastPrivilege` `#CIA-Triad`
