# 1. Introduction to Identity and Access Management

## What Is IAM?

**Identity and Access Management (IAM)** is the framework that organizations use to ensure the right people and systems can access the right resources at the right times — and for the right reasons.

At its core, IAM answers two questions:
1. **Who are you?** → Identity
2. **What can you do?** → Access

Think of it as the digital equivalent of a building's security system: badges identify people, door readers verify them, and access levels determine which floors they can enter.

---

## Why Learn This?

Every organization that uses technology needs IAM. Whether you are:
- A **developer** building login systems
- A **manager** auditing who has access to financial data
- A **student** entering cybersecurity
- A **professional** transitioning into tech

Understanding IAM gives you the vocabulary and mental models to discuss security intelligently. It is the foundation upon which every other security concept rests.

---

## Core Concepts

### The Five Stages of the IAM Lifecycle

Every identity in an organization goes through a predictable lifecycle. Understanding this prevents security holes.

| Stage | What Happens | Example |
|-------|-------------|---------|
| **Provision** | Create identity and grant initial access | HR creates account for new hire |
| **Authenticate** | Verify the identity is genuine | User enters username + password |
| **Authorize** | Decide what resources they can use | System checks permissions |
| **Monitor** | Track what they do | Audit logs record file downloads |
| **Deprovision** | Remove access when no longer needed | IT disables account on last day |

**Why the lifecycle matters:** Most security incidents happen because of gaps in this lifecycle. A departing employee whose account stays active for weeks is a classic example of failed deprovisioning.

### Identity vs. Credential vs. Authentication vs. Authorization

These four terms are often confused. Here is the distinction:

| Term | Definition | Example |
|------|-----------|---------|
| **Identity** | The digital representation of a user or system | `jdoe@company.com` |
| **Credential** | Proof that an identity is genuine | Password, fingerprint, smart card |
| **Authentication** | The process of verifying credentials | Checking password against stored hash |
| **Authorization** | The decision to grant or deny access | "Alice can read but not delete" |

**Key distinction:** Authentication proves *who you are*. Authorization decides *what you can do*. They are separate steps.

### Types of Identities

| Type | Description | Risk Profile |
|------|-------------|--------------|
| **Human identities** | Employees, contractors, customers, partners | High — susceptible to phishing |
| **Machine identities** | Servers, applications, APIs, IoT devices | High — often over-permissioned and forgotten |
| **Privileged identities** | Administrators, root accounts, service accounts | Critical — compromise = full system access |

### Core Security Principles

**Principle of Least Privilege**
> Give every identity the minimum access necessary to perform its function.

In practice: A marketing employee should be able to publish blog posts, but not access the production database. A developer should be able to deploy to staging, but not production without approval.

**Separation of Duties (SoD)**
> No single person should be able to complete a sensitive process alone.

In practice: The person who requests a software purchase should not be the same person who approves the budget. The developer who writes code should not be the same person who deploys it to production without review.

---

## How It Works

### Behind the Scenes: Directory Services

At the heart of most IAM systems is a **directory service** — a specialized database optimized for reading user information.

The most common standard is **LDAP** (Lightweight Directory Access Protocol). Directories store information hierarchically, like a family tree:

```
dc=company,dc=com
├── ou=Users
│   ├── uid=jdoe
│   └── uid=asmith
├── ou=Groups
│   ├── cn=Engineering
│   └── cn=Finance
└── ou=Devices
    └── cn=laptop-jdoe-001
```

**How a login actually works:**
1. You submit your username and password
2. The system looks up your username in the directory
3. It retrieves your stored password hash (never the raw password)
4. It hashes the password you just submitted using the same algorithm
5. If the hashes match, authentication succeeds
6. The system looks up your group memberships
7. It resolves your permissions based on those groups
8. It creates a session token so you do not have to re-enter your password on every click

### Session Tokens

After authentication, the server generates a **session token** — a cryptographically random string like `sess_a3f7b2d9e8c1`. This token is stored in your browser as a cookie and sent with every subsequent request. The server looks up the token, finds your identity, and knows who you are without asking for your password again.

**Why this matters:** Session tokens can be stolen (via XSS attacks), which is why modern systems use:
- Short expiration times (15-60 minutes)
- HttpOnly cookies (inaccessible to JavaScript)
- Secure flags (HTTPS only)
- Rotation on privilege changes

---

## Where You See It

| Product / Standard | What It Does |
|-------------------|-------------|
| **Active Directory** | Microsoft's directory service for Windows networks |
| **Okta / Azure AD** | Cloud identity providers for SSO and MFA |
| **AWS IAM** | Controls access to Amazon Web Services resources |
| **Linux PAM** | Pluggable Authentication Modules for Unix systems |
| **NIST SP 800-63** | US federal guidelines for digital identity |
| **ISO 27001** | International standard requiring IAM controls |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "IAM is just passwords" | IAM covers the entire lifecycle: creation, authentication, authorization, monitoring, and removal |
| "Authentication = Authorization" | Authentication proves identity. Authorization decides permissions. They are separate |
| "Small companies don't need IAM" | Even a 5-person team needs to revoke access when someone leaves |
| "IAM is only for IT" | HR, legal, compliance, and finance all depend on IAM for audits and access control |

---

## How to Practice

1. **Map the lifecycle at your organization (or a hypothetical one)**
   - How does a new employee get access?
   - Who decides what they can access?
   - How is access removed when they leave?
   - Where are the gaps?

2. **Read an audit log**
   - If you have access to any system logs, look at authentication events
   - Notice the timestamp, user, IP address, action, and result
   - Understand what a security analyst would look for

3. **Run the simulations**
   - `identity_lifecycle_sim.py` shows provisioning through deprovisioning
   - `iam_maturity_assessment.py` evaluates how mature an organization's IAM is

---

## Projects

### `identity_lifecycle_sim.py`
Simulates the complete IAM lifecycle:
- Onboards employees with role-based access
- Handles role changes and promotions
- Offboards employees and revokes all access
- Generates audit reports

**Run:** `python "1. Introduction to IAM/projects/identity_lifecycle_sim.py"`

### `iam_maturity_assessment.py`
Interactive assessment that evaluates an organization's IAM across four dimensions: identity governance, access management, authentication strength, and monitoring.

**Run:** `python "1. Introduction to IAM/projects/iam_maturity_assessment.py"`

### `iam_concept_matcher.py`
Interactive quiz that tests whether you can match real-world scenarios to the correct IAM concept.

**Run:** `python "1. Introduction to IAM/projects/iam_concept_matcher.py"`

---

## Check Your Understanding

1. What are the five stages of the IAM lifecycle? Give a real-world example for each.
2. Explain the difference between authentication and authorization in your own words.
3. What is the Principle of Least Privilege? Give an example from a job you have held or observed.
4. Why is Separation of Duties important? What could happen without it?
5. What information does a typical audit log capture? Why is each field important?
6. Name three types of identities and explain which is often the most overlooked in security.
