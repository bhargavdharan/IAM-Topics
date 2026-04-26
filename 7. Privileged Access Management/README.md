# 7. Privileged Access Management (PAM)

## What Is PAM?

**Privileged Access Management (PAM)** is the discipline of securing, monitoring, and governing accounts that have elevated permissions. These accounts — administrators, root users, service accounts — are the most valuable targets for attackers because they provide unrestricted access to systems and data.

PAM does not ask "Should this person have access?" It asks "How do we protect the accounts that already have the most power?"

---

## Why Learn This?

According to industry research, the vast majority of breaches involve compromised privileged credentials. A single admin account breach can expose an entire organization. PAM is essential for:
- Protecting the "keys to the kingdom"
- Meeting compliance requirements (SOX, PCI-DSS, HIPAA)
- Preventing insider threats
- Enabling forensic investigation

---

## Core Concepts

### Types of Privileged Accounts

| Account Type | Examples | Risk Level |
|-------------|----------|------------|
| **Domain/Enterprise Admin** | Active Directory admin, Azure AD Global Admin | Critical |
| **Local Administrator** | Windows Admin, Linux root | Critical |
| **Service accounts** | Database service, backup account | High |
| **Application accounts** | API keys, application secrets | High |
| **Cloud admin** | AWS Root, Azure Subscription Owner | Critical |
| **Emergency/Break-glass** | "In case of emergency" accounts | Medium |

### The PAM Lifecycle

PAM governs privileged accounts through four stages:

| Stage | What Happens | Goal |
|-------|-------------|------|
| **Discover** | Find all privileged accounts | You cannot protect what you do not know exists |
| **Protect** | Vault credentials, enforce MFA | Prevent credential theft |
| **Monitor** | Record sessions, log access | Detect misuse and enable forensics |
| **Control** | Just-in-time access, approval workflows | Minimize standing privileges |

### Core PAM Capabilities

| Capability | What It Does | Why It Matters |
|-----------|-------------|--------------|
| **Credential vaulting** | Store passwords/keys in encrypted vault | Prevents hardcoded credentials and spreadsheet-based password management |
| **Session recording** | Record screen and keystrokes during privileged sessions | Provides forensic evidence and deters misuse |
| **Just-in-Time (JIT) access** | Grant elevated rights only when needed, then revoke | Reduces the attack window |
| **Password rotation** | Automatically change passwords on schedule | Limits exposure if credentials are stolen |
| **Workflow approval** | Require manager approval for sensitive access | Enforces oversight |
| **Privilege elevation** | Allow standard users to temporarily elevate | Eliminates permanent admin rights |

### Just-in-Time Access

Instead of administrators having permanent elevated access:

1. Admin requests access to production server
2. Manager approves the request
3. System creates temporary credentials valid for 2 hours
4. Admin performs necessary work
5. Credentials automatically expire
6. Session is recorded and audited

**Benefits:**
- No standing privileges = smaller attack surface
- Every elevation is logged and approved
- If credentials leak, they are useless after expiration

---

## How It Works

### How Credential Vaults Work

A PAM vault is a specialized encrypted database:
1. All credentials encrypted at rest using AES-256
2. Access controlled through RBAC (only authorized PAM admins)
3. APIs allow applications to retrieve credentials programmatically
4. Old passwords invalidated, new passwords generated and distributed

### Session Recording

Privileged sessions are recorded for forensics:
- **Video recording:** Screen capture of the entire session
- **Keystroke logging:** Every command typed
- **Command filtering:** Dangerous commands blocked in real-time
- **Real-time monitoring:** Security teams watch live sessions

**Why this matters:** If an admin accidentally runs `rm -rf /`, the recording proves whether it was accidental or malicious.

### Privilege Escalation Mechanisms

**Linux sudo:**
```bash
# /etc/sudoers
alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
# Alice can restart nginx as root without password
```

**Windows UAC:**
- Standard users get a standard token
- Admin users get two tokens: standard and elevated
- UAC prompt switches from standard to elevated token

**Kerberos Constrained Delegation:**
- Service A can act on behalf of User B
- But ONLY for specific services
- Prevents unlimited privilege escalation

### Password Rotation Strategies

| Strategy | How It Works | Use Case |
|----------|-------------|----------|
| **Automatic** | Changed every 30 days by system | Service accounts |
| **On-demand** | Changed after each use | Highly sensitive accounts |
| **Triggered** | Changed when user leaves or breach suspected | Human admin accounts |
| **Session-based** | Temporary password for single session | Contractor access |

---

## Where You See It

| Product | PAM Feature | Example |
|---------|------------|---------|
| **CyberArk** | Enterprise PAM vault | Vault privileged credentials |
| **HashiCorp Vault** | Secrets management | Dynamic secrets for applications |
| **Microsoft PIM** | Privileged Identity Management | Just-in-time Azure AD role activation |
| **AWS Secrets Manager** | Cloud credential vault | Rotate database credentials automatically |
| **Linux sudo** | Privilege elevation | Controlled root access |
| **Windows LAPS** | Local admin password solution | Unique local admin passwords per machine |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "PAM is only for large enterprises" | Any organization with admin accounts needs PAM |
| "Shared admin accounts are fine" | Shared accounts eliminate accountability |
| "Session recording violates privacy" | Privileged access is not private; it is organizational |
| "PAM replaces IAM" | PAM is a subset of IAM focused on elevated privileges |
| "JIT access is too slow" | Modern PAM approves access in seconds |

---

## How to Practice

1. **Audit privileged accounts in your environment**
   - List all accounts with admin/root access
   - Check how many are service accounts vs human accounts
   - Identify accounts that have not been used in 90 days

2. **Design a JIT access workflow**
   - Who can request elevated access?
   - Who approves it?
   - How long should access last?
   - What is logged?

3. **Run the simulations**
   - `pam_vault_sim.py` demonstrates credential vaulting
   - `session_monitor.py` shows forensics and anomaly detection
   - `jit_access_sim.py` models just-in-time workflows

---

## Projects

### `pam_vault_sim.py`
Simulates a privileged credential vault:
- Secure credential storage with encryption
- Role-based access to vault contents
- Audit logging of all retrievals
- Automatic password generation

### `session_monitor.py`
Records and analyzes privileged sessions:
- Command logging with timestamps
- Real-time anomaly detection
- Session playback for forensics
- Alerting on suspicious commands

### `jit_access_sim.py`
Simulates just-in-time access workflows:
- Access request submission
- Manager approval workflow
- Time-limited credential issuance
- Automatic revocation and cleanup

### `privilege_escalation_detector.py`
Analyzes logs for unauthorized escalation:
- Detects sudo abuse
- Identifies token impersonation
- Flags unauthorized role assignments

---

## Check Your Understanding

1. Why are privileged accounts the most valuable targets for attackers?
2. What is Just-in-Time (JIT) access and how does it reduce risk?
3. How does credential vaulting protect passwords better than a spreadsheet?
4. Why is session recording important for privileged accounts?
5. What is the difference between automatic and on-demand password rotation?
