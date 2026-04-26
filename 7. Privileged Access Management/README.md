# 7. Privileged Access Management (PAM)

## What Is PAM?

**Privileged Access Management (PAM)** is the security discipline focused on protecting, monitoring, and governing accounts that have elevated or administrative permissions. These privileged accounts — including system administrators, root users, database administrators, and service accounts — are the most valuable targets for attackers because they provide broad, often unrestricted access to critical systems and data.

While standard IAM manages everyday user access, PAM specifically addresses the unique risks and requirements of high-powered accounts. A compromised standard user account might expose one person's emails. A compromised domain admin account can expose an entire organization's infrastructure.

---

## Why Learn This?

Privileged accounts represent the highest concentration of risk in any organization:
- They have the broadest access
- They are often shared among teams
- They are frequently targeted by attackers
- Their compromise has the most severe impact
- They are subject to the strictest compliance requirements

Understanding PAM is essential for:
- Protecting critical infrastructure
- Meeting compliance requirements (SOX, PCI-DSS, HIPAA)
- Preventing insider threats
- Enabling forensic investigation
- Implementing least privilege for administrative functions

---

## Core Concepts

### Types of Privileged Accounts

| Account Type | Examples | Risk Level | Why It's Targeted |
|-------------|----------|------------|-------------------|
| **Domain/Enterprise Admin** | Active Directory admin, Azure AD Global Admin | Critical | Controls all user accounts, group policies, domain resources |
| **Local Administrator** | Windows local admin, Linux root | Critical | Full control over individual servers and workstations |
| **Database Administrator** | Oracle DBA, SQL Server sysadmin, MongoDB root | High | Access to all data, ability to modify or delete records |
| **Cloud Admin** | AWS Root, Azure Subscription Owner, GCP Organization Admin | Critical | Controls cloud infrastructure, billing, all resources |
| **Service Accounts** | Database service account, backup account, application identity | High | Often over-permissioned; credentials hard-coded in applications |
| **Application Accounts** | API keys, application secrets, OAuth client credentials | High | Used by applications to authenticate; often long-lived |
| **Emergency/Break-glass** | "In case of emergency" accounts, firefighter accounts | Medium-High | Powerful access for emergencies; often poorly monitored |

### The PAM Lifecycle

PAM implements a specialized lifecycle for privileged accounts:

| Stage | Action | Goal |
|-------|--------|------|
| **Discover** | Find all privileged accounts across all systems | You cannot protect what you do not know exists |
| **Protect** | Vault credentials, enforce MFA, implement isolation | Prevent credential theft and unauthorized use |
| **Monitor** | Record sessions, log all access, analyze behavior | Detect misuse and enable investigation |
| **Control** | Just-in-time access, approval workflows, time limits | Minimize standing privileges and attack windows |

### Core PAM Capabilities

**Credential Vaulting**
Privileged passwords and keys are stored in an encrypted vault rather than spreadsheets, code repositories, or sticky notes. The vault:
- Encrypts all credentials at rest (AES-256 or stronger)
- Controls access through strict RBAC
- Rotates passwords automatically
- Provides APIs for application retrieval
- Logs every access for audit

**Session Recording and Monitoring**
Every action taken during a privileged session is recorded:
- Video recording of the screen
- Keystroke logging
- Command history
- File transfers
- Clipboard activity

This provides forensic evidence, deters misuse, and enables real-time anomaly detection.

**Just-in-Time (JIT) Access**
Instead of administrators having permanent elevated privileges, access is:
1. Requested for a specific purpose and time window
2. Approved by a manager or through automated policy
3. Granted temporarily (e.g., 2 hours)
4. Automatically revoked when time expires
5. Fully logged and recorded

**Benefits of JIT:**
- No standing privileges = smaller attack surface
- Every elevation is justified and audited
- Compromised temporary credentials expire automatically
- Administrators use standard accounts for daily work

**Privilege Elevation**
Standard users can temporarily elevate their privileges for specific tasks:
- Linux: `sudo` for command-level elevation
- Windows: User Account Control (UAC) prompts
- macOS: Admin password for system changes
- Cloud: AssumeRole / service account impersonation

**Password Rotation**
Privileged credentials are changed automatically according to policy:
- **Time-based:** Every 30, 60, or 90 days
- **Event-based:** After each use (for highly sensitive accounts)
- **Triggered:** On employee departure, suspected breach, or policy violation

---

## How It Works

### How Credential Vaults Work

A PAM vault is a hardened, encrypted database with strict access controls:

```
┌─────────────────────────────────────────┐
│           PAM Credential Vault          │
├─────────────────────────────────────────┤
│  Encryption Layer                       │
│  - AES-256-GCM at rest                  │
│  - TLS 1.3 in transit                   │
├─────────────────────────────────────────┤
│  Access Control Layer                   │
│  - Multi-factor authentication required │
│  - Role-based vault access              │
│  - Approval workflows for sensitive creds│
├─────────────────────────────────────────┤
│  Credential Storage                     │
│  - Passwords (hashed + encrypted)       │
│  - SSH keys                             │
│  - API tokens                           │
│  - Certificates                         │
├─────────────────────────────────────────┤
│  Automation Layer                       │
│  - Automatic password rotation          │
│  - API access for applications          │
│  - Discovery of new privileged accounts │
└─────────────────────────────────────────┘
```

**Vault access flow:**
1. Administrator authenticates to vault with MFA
2. Vault verifies identity and authorization
3. Administrator requests credential for target system
4. Vault logs the access with timestamp, user, and target
5. Vault decrypts and displays credential (or injects it directly)
6. Administrator uses credential
7. Vault optionally rotates credential after session

### Session Recording for Forensics

Privileged sessions are recorded at multiple levels:

| Recording Type | What Is Captured | Use Case |
|---------------|------------------|----------|
| **Video** | Screen capture | Visual evidence of what was done |
| **Keystrokes** | Every key pressed | Exact commands entered |
| **Commands** | Structured command logs | Automated analysis and alerting |
| **Metadata** | Start/end time, user, target | Session timeline reconstruction |

**Real-time monitoring:**
- Dangerous commands (rm -rf, DROP TABLE) trigger immediate alerts
- Unusual patterns (large data exports, privilege escalation attempts) flag sessions
- Security analysts can watch live sessions and terminate if suspicious

### Privilege Escalation Mechanisms

**Linux sudo:**
```bash
# /etc/sudoers
# Alice can restart nginx without password
alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx

# Bob can run any command as root (with password)
bob ALL=(ALL) ALL

# Developers can run commands as deploy user
%developers ALL=(deploy) ALL
```

**Windows User Account Control (UAC):**
- Standard users receive standard tokens
- Administrators receive two tokens: standard and elevated
- UAC prompt requires explicit elevation for admin actions
- Applications can request specific privilege levels in their manifests

**Kerberos Constrained Delegation:**
- Service A can act on behalf of User B
- But ONLY for specific services (constrained)
- Prevents unlimited privilege escalation through service chaining

### Password Rotation Strategies

| Strategy | Mechanism | Best For | Trade-off |
|----------|-----------|----------|-----------|
| **Automatic periodic** | System changes password every N days | Service accounts, standard admin accounts | Brief windows of exposure between rotation and update |
| **On-demand** | Password changed after each checkout | Highly sensitive accounts (domain admin, root) | Requires immediate distribution to dependent systems |
| **Triggered** | Changed on event (departure, breach) | Human admin accounts | Requires event detection and rapid response |
| **Session-based** | Temporary password for single session | Contractor access, emergency access | Most secure; highest operational overhead |

---

## Where You See It

| Product | PAM Capability | Use Case |
|---------|---------------|----------|
| **CyberArk** | Enterprise PAM vault | Privileged credential management, session isolation |
| **HashiCorp Vault** | Secrets management | Dynamic secrets, encryption as a service |
| **Microsoft PIM** | Privileged Identity Management | Just-in-time Azure AD role activation |
| **AWS Secrets Manager** | Cloud credential vault | Automatic rotation of database credentials |
| **BeyondTrust** | Privileged remote access | Secure vendor and contractor access |
| **Linux sudo** | Privilege elevation | Controlled root access |
| **Windows LAPS** | Local admin password | Unique passwords per machine |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "PAM is only for large enterprises" | Any organization with admin accounts needs PAM. A 10-person company with shared admin credentials has a critical gap. |
| "Shared admin accounts are fine if we trust the team" | Shared accounts eliminate accountability. You cannot determine who performed an action. |
| "Session recording violates employee privacy" | Privileged access to organizational systems is not private. Recording is standard security practice. |
| "PAM replaces general IAM" | PAM is a specialized subset of IAM focused on elevated privileges. Both are needed. |
| "JIT access is too slow for emergencies" | Modern PAM approves access in seconds. Emergency break-glass procedures provide immediate access with full logging. |
| "Service accounts don't need PAM" | Service accounts often have excessive permissions and are frequently hard-coded. They require the same governance as human accounts. |

---

## How to Practice

### Exercise 1: Audit Privileged Accounts
1. List all accounts with admin/root/domain admin access in your environment
2. Categorize them: human accounts, service accounts, shared accounts, emergency accounts
3. Identify accounts that have not been used in 90 days
4. Check which credentials are stored in vaults vs. spreadsheets/code/config files
5. Document your findings and recommend priorities

### Exercise 2: Design a JIT Access Workflow
Design a just-in-time access process for production database access:
- Who can request access?
- Who approves it?
- How long should access last?
- What is recorded during the session?
- How are credentials handled after the session?
- What happens in a true emergency when approvers are unavailable?

### Exercise 3: Evaluate sudo Configuration
On a Linux system (or virtual machine):
1. Run `sudo -l` to list your sudo privileges
2. Read `/etc/sudoers` and files in `/etc/sudoers.d/`
3. Identify any overly broad permissions (e.g., `ALL=(ALL) NOPASSWD: ALL`)
4. Propose more restrictive sudo rules

### Exercise 4: Run the Simulations
- `pam_vault_sim.py` — Experience credential vaulting
- `session_monitor.py` — Observe session forensics
- `jit_access_sim.py` — Model just-in-time workflows

---

## Projects

### `pam_vault_sim.py`
Simulates a privileged credential vault:
- Secure credential storage with encryption
- Role-based access to vault contents
- Audit logging of all retrievals
- Automatic password generation
- Integration with session recording

### `session_monitor.py`
Records and analyzes privileged sessions:
- Command logging with timestamps
- Real-time anomaly detection (dangerous commands flagged)
- Session playback for forensics
- Alerting on suspicious activity patterns

### `jit_access_sim.py`
Simulates just-in-time access workflows:
- Access request submission with justification
- Manager approval workflow
- Time-limited credential issuance
- Automatic revocation and cleanup
- Emergency break-glass procedures

### `privilege_escalation_detector.py`
Analyzes logs for unauthorized privilege escalation:
- Detects sudo abuse patterns
- Identifies token impersonation attempts
- Flags unauthorized role assignments
- Alerts on break-glass account usage

---

## PAM in Practice: COTS Products and Career Roles

### PAM COTS Products and What They Do

Organizations do not build PAM solutions from scratch. They buy specialized products:

| Product | Type | Best For | Key Differentiator |
|---------|------|----------|-------------------|
| **CyberArk** | Enterprise PAM | Large organizations; strict compliance | Most comprehensive; highest security certifications; expensive |
| **Delinea (formerly Thycotic)** | Enterprise PAM | Mid-to-large organizations | Strong Windows integration; easier deployment than CyberArk |
| **BeyondTrust** | PAM + Remote Access | Organizations with many vendors/contractors | Strong privileged remote access; session management |
| **HashiCorp Vault** | Secrets Management | Cloud-native; DevOps environments | Dynamic secrets; API-first; developer-friendly |
| **Microsoft Privileged Identity Management (PIM)** | Cloud PAM | Microsoft-heavy environments | Native Azure AD integration; no extra licensing for E5 customers |
| **AWS Secrets Manager** | Cloud Secrets | AWS-centric organizations | Automatic rotation; tight AWS service integration |
| **Linux sudo + LAPS** | Built-in OS | Small-to-mid organizations; cost-constrained | Free; built into operating systems; limited features |

**Product selection reality:**
- A 50-person startup uses **sudo + password manager** — no budget for CyberArk
- A 5,000-person bank uses **CyberArk** — regulatory requirements demand it
- A cloud-native company uses **HashiCorp Vault** — developers need API access to secrets
- A Microsoft shop uses **Azure AD PIM** — already paying for E5 licenses

### PAM Support vs Implementation

| Aspect | PAM Support | PAM Implementation |
|--------|------------|-------------------|
| **Daily work** | Unlock vault access, troubleshoot session recording, investigate failed logins, rotate passwords on demand | Deploy vault infrastructure, configure safes/folders, integrate with AD, set up session recording, design JIT workflows |
| **Skills needed** | Product-specific admin (CyberArk PVWA, Delinea Secret Server), Active Directory, scripting for automation | Product architecture, AD/LDAP integration, API development, policy design, project management |
| **Tools** | Vault admin console, session replay, audit logs | Installation media, configuration wizards, API documentation, test plans |
| **Typical ticket** | "I cannot access the production database vault" | "Deploy PAM for 500 administrators across 3 data centers" |

**Implementation project example:**
A hospital implements CyberArk for HIPAA compliance:
- **Phase 1 (2 weeks):** Install vault servers, configure high availability
- **Phase 2 (4 weeks):** Integrate with Active Directory, import existing admin accounts
- **Phase 3 (6 weeks):** Configure safes (folders) for each system type, set access policies
- **Phase 4 (4 weeks):** Deploy session recording agents to jump servers
- **Phase 5 (4 weeks):** Configure automatic password rotation for service accounts
- **Phase 6 (ongoing):** Train administrators, hand over to Support team

**Total: 20 weeks for initial deployment + ongoing support**

---

## Check Your Understanding

1. Why are privileged accounts the most valuable targets for attackers? Describe three specific risks of privileged account compromise.
2. What is Just-in-Time (JIT) access? Draw the complete workflow from request to revocation and explain how each step reduces risk.
3. How does credential vaulting protect passwords better than a spreadsheet or shared document? Compare security controls.
4. Why is session recording important for privileged accounts? What would happen if a privileged action caused an outage without recording?
5. What is the difference between automatic, on-demand, and triggered password rotation? When would you use each strategy?
6. Design a PAM strategy for a mid-sized company with: 5 domain admins, 20 local admins, 50 service accounts, and 5 emergency accounts.
7. Compare Linux sudo, Windows UAC, and Kerberos Constrained Delegation as privilege elevation mechanisms. What are their strengths and weaknesses?
8. A developer asks why they cannot have permanent local admin rights on their laptop. How would you explain the risk and propose alternatives?
9. An auditor asks "Who accessed the production database on March 15?" What evidence would a properly implemented PAM system provide?
10. Describe how you would migrate an organization from shared admin passwords to a PAM vault with JIT access. What are the phases and risks?
