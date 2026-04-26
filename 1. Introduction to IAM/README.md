# 1. Introduction to Identity and Access Management

## What Is IAM?

**Identity and Access Management (IAM)** is the comprehensive framework of policies, processes, and technologies that organizations use to manage digital identities and control access to resources. It ensures that the right individuals and systems can access the right resources at the right times for the right reasons.

At its foundation, IAM addresses two fundamental security questions:
1. **Who are you?** — This is the realm of **identity** and **authentication**
2. **What can you do?** — This is the realm of **authorization** and **access control**

Every organization that operates digital systems — from a five-person startup to a multinational enterprise — needs IAM. Without it, there is no way to control who can access sensitive data, modify critical systems, or view confidential information.

---

## Why Learn This?

IAM is the **bedrock of cybersecurity**. No firewall, encryption scheme, or intrusion detection system can compensate for poor identity and access controls. Consider these scenarios:

- A former employee's account remains active for three months after departure, allowing them to access customer data
- A contractor accidentally gains admin privileges because roles were misconfigured
- An auditor asks "Who has access to financial systems?" and the organization cannot answer definitively
- A developer deploys code to production because there is no separation between development and deployment permissions

All of these are IAM failures. Understanding IAM enables you to:
- Design secure access architectures
- Pass compliance audits (SOX, HIPAA, PCI-DSS, ISO 27001)
- Prevent data breaches caused by identity mismanagement
- Build career expertise in one of the most in-demand security domains

**Career relevance:** See the root `README.md` for detailed IAM career paths including Support Engineer, Administrator, Analyst, Developer, Consultant, and Architect roles.

---

## Core Concepts

### The Five Stages of the IAM Lifecycle

The IAM lifecycle describes the complete journey of an identity from creation to removal. Gaps or delays at any stage create security vulnerabilities.

#### Stage 1: Provision
**What happens:** A new identity is created and assigned initial access based on role.

**Real-world process:**
- HR creates an employee record in the HRIS system
- The IAM system detects the new hire and triggers provisioning
- An account is created in Active Directory / Azure AD / Google Workspace
- The user is assigned to appropriate groups based on their department and role
- An email account is created
- Access to standard applications (email, intranet, collaboration tools) is granted automatically

**What goes wrong:** Manual provisioning delays leave new hires without access on day one. Over-provisioning gives excessive initial permissions. Inconsistent provisioning across systems creates access gaps.

**Automation best practice:** Use HR-driven provisioning with role-based templates. When HR marks someone as hired in the system of record, IAM should automatically create accounts, assign roles, and grant baseline access within minutes.

#### Stage 2: Authenticate
**What happens:** The system verifies that the user is who they claim to be.

**Real-world process:**
- User enters username and password
- System validates credentials against the directory service
- If MFA is enabled, user provides second factor (TOTP code, push approval, hardware key)
- System evaluates risk signals (location, device, time, behavior)
- Upon successful authentication, system issues a session token

**What goes wrong:** Weak password policies allow easily guessed credentials. MFA is not enforced for privileged accounts. Risk signals are ignored, allowing compromised credentials to be used from unusual locations.

#### Stage 3: Authorize
**What happens:** The system determines what resources the authenticated user can access and what operations they can perform.

**Real-world process:**
- User attempts to open a file, application, or API endpoint
- System checks the user's roles, groups, and direct permissions
- System evaluates policies (RBAC, ABAC, or both)
- System logs the access decision
- If allowed, access is granted; if denied, user sees "Access Denied"

**What goes wrong:** Over-permissioning (giving users more access than needed) is rampant. Role definitions are outdated. Temporary access grants become permanent. There is no regular review of who has what access.

#### Stage 4: Monitor
**What happens:** The system tracks and logs all identity-related activities for audit, compliance, and security detection.

**Real-world process:**
- Every login is logged with timestamp, IP address, device information, and result
- Every access decision (allowed or denied) is recorded
- Privileged operations are flagged for additional review
- Anomalies trigger alerts (impossible travel, unusual access patterns, after-hours admin activity)
- Logs are retained according to compliance requirements

**What goes wrong:** Logs are incomplete or missing. Alerts are not configured. No one reviews privileged activity. Log retention does not meet compliance requirements.

#### Stage 5: Deprovision
**What happens:** Access is completely removed when the identity is no longer needed.

**Real-world process:**
- HR terminates employee in HRIS
- IAM system detects termination and triggers deprovisioning workflow
- User account is disabled in all systems
- Access tokens and sessions are invalidated
- User is removed from all groups and roles
- Email forwarding or delegation is configured if needed
- Manager is notified of completion

**What goes wrong:** The most common IAM failure. Accounts remain active for days, weeks, or months after termination. Service accounts for completed projects are never cleaned up. Contractors retain access after contract end.

**Critical metric:** Time-to-deprovision. Best practice is within minutes of termination; many organizations take days or weeks.

### Core IAM Vocabulary

| Term | Definition | Example | Why It Matters |
|------|-----------|---------|---------------|
| **Identity** | A unique digital representation of a user, device, or service | `jdoe@company.com` | Without identity, there is nothing to authenticate or authorize |
| **Credential** | Proof that an identity is genuine | Password, fingerprint, certificate | Credentials are what attackers steal; protecting them is paramount |
| **Authentication** | The process of verifying identity | Entering username + password | First line of defense; determines if access proceeds |
| **Authorization** | The decision to grant or deny access | Checking if user can view a file | Second line of defense; enforces least privilege |
| **Accounting/Audit** | Tracking and logging actions | Recording who downloaded what file when | Provides forensic evidence and compliance proof |
| **Principal** | Any entity that can be authenticated | User, service account, computer | IAM policies apply to principals |
| **Subject** | The active principal in a session | Alice while logged in | Used in access control decisions |

### Identity Types

**Human Identities**
- Employees, contractors, customers, partners, vendors
- Most visible identity type
- Susceptible to social engineering and phishing
- Require lifecycle management from onboarding to offboarding

**Machine Identities**
- Servers, applications, APIs, microservices, IoT devices, containers
- Often created at machine speed (thousands in cloud environments)
- Frequently over-permissioned because developers grant broad access "just in case"
- Often forgotten during decommissioning
- Growing faster than human identities in cloud-native environments

**Privileged Identities**
- System administrators, domain admins, root accounts, database administrators
- Service accounts with elevated permissions
- Often shared among teams (which eliminates accountability)
- Highest-value targets for attackers
- Require enhanced protection: vaulting, JIT access, session recording

### The CIA Triad and IAM

IAM directly supports the three pillars of information security:

| Pillar | Definition | IAM Contribution |
|--------|-----------|-----------------|
| **Confidentiality** | Ensuring information is accessible only to authorized parties | Authentication prevents unauthorized access; authorization enforces need-to-know |
| **Integrity** | Ensuring information is accurate and unaltered | Audit logs detect unauthorized changes; SoD prevents single-actor tampering |
| **Availability** | Ensuring information is accessible when needed | Proper provisioning ensures legitimate users can work; access reviews prevent lockouts |

### Core Security Principles

**Principle of Least Privilege (PoLP)**
> Every identity should have the minimum access necessary to perform its function — no more, no less.

**Implementation:**
- Start with zero permissions
- Add only what is explicitly needed
- Review and revoke unused permissions regularly
- Use time-bound access for temporary needs

**Why it fails in practice:** Convenience often overrides security. Administrators grant broad permissions to avoid ticket volume. Developers use admin accounts for daily work. Role definitions become bloated over time.

**Separation of Duties (SoD)**
> Critical actions should require multiple people to complete, preventing any single individual from abusing privileges.

**Implementation:**
- The person who requests a purchase cannot approve it
- The developer who writes code cannot deploy it to production without review
- The database administrator who backs up data cannot also delete audit logs
- The person who creates user accounts cannot also assign admin privileges

**Types of SoD:**
- **Static SoD:** Mutually exclusive roles cannot be assigned to the same user
- **Dynamic SoD:** Mutually exclusive roles cannot be activated in the same session
- **Preventive SoD:** System blocks the conflicting assignment
- **Detective SoD:** System flags the conflict for remediation

---

## How It Works

### Directory Services: The Identity Database

Behind every IAM system is a **directory service** — a specialized database optimized for fast reads of user information.

**LDAP (Lightweight Directory Access Protocol)** is the most widely adopted standard. Directories store data hierarchically:

```
dc=company,dc=com                    [Root: the domain]
├── ou=Users                         [Organizational Unit: all users]
│   ├── uid=jdoe                     [User entry]
│   │   ├── cn: John Doe             [Common Name: display name]
│   │   ├── mail: jdoe@company.com   [Email address]
│   │   ├── userPassword: {SSHA}...  [Password hash — NEVER plaintext]
│   │   ├── title: Senior Developer  [Job title]
│   │   └── department: Engineering  [Department]
│   └── uid=asmith
├── ou=Groups                        [Organizational Unit: all groups]
│   ├── cn=Engineering               [Group entry]
│   │   └── member: uid=jdoe         [Group members]
│   └── cn=Finance
└── ou=ServiceAccounts               [Service accounts]
    └── cn=backup-service
```

**Key LDAP terms:**
- **DN (Distinguished Name):** Unique identifier for every entry. Example: `uid=jdoe,ou=Users,dc=company,dc=com`
- **RDN (Relative Distinguished Name):** The individual component. Example: `uid=jdoe`
- **OU (Organizational Unit):** Container for grouping entries
- **DC (Domain Component):** Part of the DNS domain name
- **CN (Common Name):** Display name or object name
- **Attribute:** A property of an entry (mail, title, telephoneNumber)
- **ObjectClass:** Schema definition for what attributes an entry can have

**How a login actually works behind the scenes:**
1. User submits username and password to the application
2. Application formats the username as a DN (or searches for it)
3. Application sends a **bind** request to the directory with the DN and password
4. Directory retrieves the stored password hash for that DN
5. Directory hashes the submitted password using the same algorithm and salt
6. Directory compares the hashes (never compares plaintext passwords)
7. If they match, bind succeeds; if not, `InvalidCredentials` is returned
8. On successful bind, the application searches for the user's group memberships
9. The application resolves permissions based on group memberships
10. The application creates a session and issues a token

**Why directories use specialized databases:**
- Optimized for read-heavy workloads (thousands of lookups per minute)
- Hierarchical structure maps naturally to organizational charts
- Standardized protocol (LDAP) allows any application to query
- Replication ensures availability across multiple servers

### Session Tokens and Cookies

After successful authentication, the system does not ask for your password on every click. Instead, it issues a **session token**.

**How session management works:**
1. After successful authentication, the server generates a cryptographically random token (e.g., 128 bits of entropy)
2. The server stores the token in a session database with: user ID, creation time, expiration time, IP address, user agent
3. The server sends the token to the browser in a **cookie**
4. The browser automatically includes this cookie in every subsequent request
5. The server looks up the token, validates it (not expired, not revoked), and identifies the user

**Session security measures:**
- **Short expiration:** Sessions expire after 15-60 minutes of inactivity
- **HttpOnly flag:** Cookie cannot be accessed by JavaScript (prevents XSS theft)
- **Secure flag:** Cookie is only sent over HTTPS
- **SameSite attribute:** Cookie is not sent in cross-site requests (prevents CSRF)
- **Rotation:** Session ID changes on privilege escalation or sensitive actions
- **Invalidation:** Server can immediately revoke sessions (on logout, password change, or security incident)

**Token-based alternatives (JWT):**
- Instead of server-side session storage, some systems use JSON Web Tokens
- JWT contains user identity and claims, cryptographically signed by the server
- Server verifies the signature instead of looking up a database
- Trade-off: JWTs cannot be easily revoked before expiration

### Audit Logs: The Security Camera

Every IAM system must log actions for compliance and forensics. A comprehensive audit log entry contains:

```json
{
  "timestamp": "2024-01-15T14:32:18Z",
  "event_type": "AUTHENTICATION",
  "event_subtype": "LOGIN_SUCCESS",
  "user_id": "jdoe",
  "user_type": "human",
  "source_ip": "192.168.1.45",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
  "authentication_method": "password+mfa",
  "mfa_type": "totp",
  "session_id": "sess_a3f7b2d9e8c1",
  "application": "corporate-portal",
  "resource": "N/A",
  "action": "N/A",
  "result": "SUCCESS",
  "risk_score": 15,
  "device_id": "device_abc123",
  "location": "New York, USA",
  "correlation_id": "req_789xyz"
}
```

**What security analysts look for in logs:**
- Failed login attempts followed by success (possible brute force)
- Logins from impossible locations (same user in NYC and Tokyo within minutes)
- After-hours admin activity
- MFA disable requests
- New device registrations for privileged accounts
- Bulk permission changes
- Access to sensitive resources by unusual users

---

## Where You See It

| Product / Standard | Role in IAM | What You Interact With |
|-------------------|-------------|----------------------|
| **Active Directory** | Directory + authentication | Windows login, Group Policy, file shares |
| **Azure AD / Entra ID** | Cloud identity provider | Microsoft 365 login, SSO to SaaS apps |
| **Okta** | Cloud IAM platform | SSO dashboard, MFA prompts, lifecycle management |
| **AWS IAM** | Cloud resource authorization | IAM policies, roles, service accounts |
| **Linux PAM** | Authentication framework | sudo, login, password changes |
| **NIST SP 800-63** | Federal identity guidelines | Defines AAL (Authenticator Assurance Levels) |
| **ISO 27001** | Security management standard | Requires access control and audit procedures |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "IAM is just about passwords" | IAM covers the complete lifecycle: creation, authentication, authorization, monitoring, and removal. Passwords are just one authentication method. |
| "Authentication and authorization are the same thing" | Authentication proves identity. Authorization decides permissions. They are completely separate steps handled by different systems. |
| "Small companies don't need formal IAM" | Even a 5-person team needs to revoke access when someone leaves, review permissions quarterly, and protect admin accounts. |
| "IAM is only the IT department's responsibility" | HR triggers provisioning and deprovisioning. Legal requires audit trails. Compliance mandates access reviews. Managers certify their team's access. |
| "Cloud IAM is completely different from on-prem IAM" | The principles are identical. The implementation differs (APIs vs. GUIs, ephemeral resources vs. static servers), but the concepts translate directly. |
| "Service accounts don't need governance" | Machine identities often outnumber human identities and are frequently over-permissioned. They require the same governance as human accounts. |

---

## How to Practice

### Exercise 1: Map Your Organization's IAM Lifecycle
Pick an organization you know (your workplace, university, or a hypothetical company) and map:
- How does a new person get access? How long does it take?
- Who decides what they can access?
- How is access reviewed? How often?
- How is access removed when someone leaves? How quickly?
- Where are the gaps or risks?

### Exercise 2: Read Real Audit Logs
If you have access to any system logs:
- Locate authentication events (Windows Event Log, Linux auth.log, application logs)
- Identify: timestamp, user, IP address, action, result
- Look for patterns: repeated failures, after-hours access, new locations
- Write a one-page summary of what a security analyst would look for

### Exercise 3: Simulate the Lifecycle
Run the projects below to see the full lifecycle in action:

---

## Projects

### `identity_lifecycle_sim.py`
Simulates the complete IAM lifecycle for an organization:
- Onboards new employees with role-based provisioning
- Simulates role changes and promotions
- Handles offboarding with complete access revocation
- Generates compliance audit reports

**Run:** `python "1. Introduction to IAM/projects/identity_lifecycle_sim.py"`

### `iam_maturity_assessment.py`
Interactive assessment evaluating an organization's IAM maturity across:
- Identity governance and lifecycle management
- Access management and authorization
- Authentication strength
- Monitoring and analytics

Provides maturity scores and actionable recommendations.

**Run:** `python "1. Introduction to IAM/projects/iam_maturity_assessment.py"`

### `iam_concept_matcher.py`
Interactive quiz that tests whether you can match real-world scenarios to the correct IAM concept (authentication, authorization, provisioning, etc.).

**Run:** `python "1. Introduction to IAM/projects/iam_concept_matcher.py"`

---

## Check Your Understanding

1. Describe the five stages of the IAM lifecycle. For each stage, identify one common failure and its security impact.
2. Explain the difference between authentication and authorization. Give a real-world example where authentication succeeds but authorization fails.
3. What is the Principle of Least Privilege? Describe three ways it commonly fails in practice.
4. Compare and contrast Static SoD and Dynamic SoD. When would you use each?
5. What information does a comprehensive audit log capture? Explain why each field is important for security or compliance.
6. Name three types of identities and explain which is often the most overlooked in security programs. Why?
7. Describe the LDAP authentication process step by step, from username submission to session creation.
8. Why are session tokens used instead of asking for passwords on every request? What security measures protect session tokens?
9. What is the difference between an IAM Administrator and an IAM Analyst? Which role would be responsible for running quarterly access reviews?
10. Describe how an IAM Consultant differs from an IAM Developer in terms of responsibilities, skills, and deliverables.
