# 7. Privileged Access Management (PAM)

## 🏠 Real-World Analogy: The Bank Vault Master Key

Imagine a bank with hundreds of safety deposit boxes:
- Customers have keys to their own boxes (regular access)
- But there's a **master key** that opens ALL boxes
- The master key is kept in a secure vault
- To use it, two managers must insert their keys simultaneously
- Every use is logged on camera
- The master key is only checked out for specific tasks and must be returned immediately

**Privileged accounts are the "master keys" of the digital world.** PAM is the system that protects them.

---

## 📋 Overview

Privileged Access Management (PAM) focuses on securing, monitoring, and governing accounts with elevated permissions. These accounts — administrators, root users, service accounts — are the **most valuable targets** for attackers because they provide unrestricted access.

**Why PAM is critical:**
- 80% of breaches involve compromised privileged credentials (Forrester)
- One admin account breach can expose the entire organization
- Compliance standards (SOX, PCI-DSS, HIPAA) require PAM controls

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Identify privileged accounts in any organization
- Explain the PAM lifecycle: discover → protect → monitor → control
- Describe just-in-time (JIT) access and session recording
- Understand credential vaulting and rotation
- Implement a basic PAM vault simulator

---

## 📚 Key Concepts

### Types of Privileged Accounts

| Account Type | Examples | Risk Level |
|-------------|----------|------------|
| **Domain/Enterprise Admin** | Active Directory admin, Azure AD Global Admin | 🔴 Critical |
| **Local Administrator** | Windows Admin, Linux root | 🔴 Critical |
| **Service Accounts** | Database service account, backup account | 🟠 High |
| **Application Accounts** | API keys, application secrets | 🟠 High |
| **Cloud Admin** | AWS Root, Azure Subscription Owner | 🔴 Critical |
| **Emergency/Break-glass** | "In case of emergency" accounts | 🟡 Medium |

### The PAM Lifecycle

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Discover   │───→│   Protect   │───→│   Monitor   │───→│   Control   │
│  (Find all  │    │  (Vault and │    │  (Record and│    │  (Just-in-  │
│   privileged│    │   rotate)   │    │   alert)    │    │   time)     │
│   accounts) │    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Core PAM Capabilities

| Capability | What It Does | Real-World Analogy |
|-----------|-------------|-------------------|
| **Credential Vaulting** | Stores passwords/keys in encrypted vault | Bank vault for master keys |
| **Session Recording** | Records everything done during privileged session | Security camera in server room |
| **Just-in-Time (JIT) Access** | Grants elevated rights only when needed, then revokes | Temporary elevator pass |
| **Privilege Elevation** | Standard users can temporarily elevate | Borrowing the manager's key |
| **Password Rotation** | Automatically changes passwords periodically | Changing vault combination monthly |
| **Workflow Approval** | Requires manager approval for sensitive access | Two-signature requirement |
| **Session Isolation** | Privileged sessions run on isolated systems | Clean room for sensitive work |

### Just-in-Time (JIT) Access

Instead of administrators having permanent elevated access:

```
1. Admin requests access to production server
2. Manager approves the request
3. System creates temporary credentials (valid for 2 hours)
4. Admin performs necessary work
5. Credentials automatically expire
6. Session is recorded and audited
```

**Benefits:**
- No standing privileges = smaller attack surface
- Every elevation is logged and approved
- If credentials leak, they're useless after expiration

---

## 🔧 Under the Hood

### How Credential Vaults Work

A PAM vault is a specialized encrypted database:

1. **Encryption:** All credentials encrypted at rest using AES-256
2. **Access Control:** Only authorized PAM administrators can decrypt
3. **API Integration:** Applications retrieve credentials programmatically
4. **Rotation:** Old password invalidated, new password generated and distributed

```python
# Conceptual vault lookup
def get_credential(vault, account_name, requester):
    # Check if requester is authorized
    if not vault.is_authorized(requester, account_name):
        raise AccessDenied()
    
    # Log the access
    audit_log.record(requester, account_name, timestamp=now())
    
    # Decrypt and return
    credential = vault.decrypt(account_name)
    return credential
```

### Session Recording and Keystroke Logging

Privileged sessions are often recorded for forensics:

- **Video recording:** Screen capture of entire session
- **Keystroke logging:** Every command typed is logged
- **Command filtering:** Dangerous commands can be blocked in real-time
- **Real-time monitoring:** Security teams can watch live sessions

**Why it matters:** If an admin accidentally runs `rm -rf /`, the recording proves it was an accident (or not).

### Privilege Escalation Mechanisms

**Linux sudo:**
```bash
# /etc/sudoers
alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
# Alice can restart nginx as root without password
```

**Windows User Account Control (UAC):**
- Standard users get standard token
- Admin users get two tokens: standard AND elevated
- UAC prompt switches from standard to elevated token

**Kerberos Constrained Delegation:**
- Service A can act on behalf of User B
- But ONLY for specific services (constrained)
- Prevents unlimited privilege escalation

### Credential Rotation Strategies

| Strategy | How It Works | Use Case |
|----------|-------------|----------|
| **Automatic** | System changes password every 30 days | Service accounts |
| **On-demand** | Password changed after each use | Highly sensitive accounts |
| **Triggered** | Changed when user leaves or breach suspected | Human admin accounts |
| **Session-based** | Temporary password for single session | Contractor access |

---

## 🛠️ Projects in This Module

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
Analyzes logs for unauthorized privilege escalation:
- Detects sudo abuse
- Identifies token impersonation
- Flags unauthorized role assignments
- Alerts on break-glass account usage

---

## 📝 Quiz Questions

1. **Why are privileged accounts the most valuable targets for attackers?**
2. **What is Just-in-Time (JIT) access and how does it reduce risk?**
3. **How does credential vaulting protect passwords better than a spreadsheet?**
4. **Why is session recording important for privileged accounts?**
5. **What is the difference between automatic and on-demand password rotation?**

---

## 🔗 Further Reading

- [NIST SP 800-53 - Access Control](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [CyberArk PAM Best Practices](https://www.cyberark.com/resources)
- [Microsoft Privileged Access Workstations](https://docs.microsoft.com/en-us/security/compass/privileged-access-devices)

---

## 🏷️ Tags
`#PAM` `#PrivilegedAccess` `#CredentialVault` `#JIT` `#SessionRecording` `#LeastPrivilege`
