# 11. Identity Providers and Directory Services

## What Are Identity Providers and Directory Services?

An **Identity Provider (IdP)** is a system that creates, maintains, and manages identity information while providing authentication services to other applications.

A **Directory Service** is the underlying database that stores user identities, credentials, group memberships, and attributes. It is the source of truth for who everyone is in an organization.

Together, they form the backbone of enterprise IAM. Every login, every permission check, and every audit trail depends on these systems.

---

## Why Learn This?

Directory services are the foundation upon which all other IAM capabilities are built. Without a reliable directory, there is no SSO, no RBAC, no access governance. Understanding directories enables you to:
- Troubleshoot authentication issues
- Design identity architectures
- Integrate applications with enterprise identity
- Understand cloud migration challenges

---

## Core Concepts

### Directory Service Types

| Service | Vendor | Deployment | Best For |
|---------|--------|-----------|----------|
| **Active Directory (AD)** | Microsoft | On-premises | Windows-centric enterprises |
| **Azure AD / Entra ID** | Microsoft | Cloud | Microsoft 365, hybrid organizations |
| **LDAP (OpenLDAP)** | Open Source | On-premises | Unix/Linux environments |
| **Google Cloud Identity** | Google | Cloud | Google Workspace organizations |
| **Okta** | Okta | Cloud | SaaS application integration |

### Directory Structure

Directories use a **hierarchical tree** structure:

```
dc=example,dc=com                    ← Root (domain)
├── ou=Users                         ← Organizational Unit
│   ├── uid=alice
│   │   ├── cn=Alice Smith
│   │   ├── mail=alice@example.com
│   │   └── userPassword={SSHA}...
│   └── uid=bob
├── ou=Groups
│   ├── cn=Engineering
│   └── cn=Finance
└── ou=Computers
    └── cn=workstation-alice-001
```

**Key terms:**
- **DN (Distinguished Name):** Unique identifier: `uid=alice,ou=Users,dc=example,dc=com`
- **OU (Organizational Unit):** Container for grouping objects
- **DC (Domain Component):** Part of the domain name

### LDAP Operations

LDAP (Lightweight Directory Access Protocol) is the standard for querying directories:

| Operation | Purpose | Example |
|-----------|---------|---------|
| **Bind** | Authenticate | Log in with username/password |
| **Search** | Query entries | Find all users in Engineering |
| **Add** | Create entry | Add new employee |
| **Modify** | Update entry | Change phone number |
| **Delete** | Remove entry | Remove departed employee |

### Identity Provider Functions

An IdP does more than store identities:

1. **Authentication Engine:** Verifies passwords, handles MFA, supports federated login
2. **Token Service:** Issues SAML assertions, JWT/OAuth tokens
3. **User Store / Directory:** Stores identities, group memberships, attributes
4. **Policy Engine:** Enforces password policies, access policies, MFA requirements
5. **Audit & Reporting:** Logs authentication events, generates compliance reports

---

## How It Works

### How LDAP Authentication Works

1. Client sends username (DN) and password
2. Directory retrieves stored password hash
3. Directory hashes the submitted password
4. If hashes match, authentication succeeds
5. Directory returns user attributes and group memberships

### Active Directory Under the Hood

AD is more than LDAP — it is a comprehensive identity platform:

**Core Components:**
- **Domain Controllers:** Servers that authenticate users and replicate data
- **Global Catalog:** Index of all objects across the forest
- **Sites:** Physical network locations for optimized replication
- **Replication:** Changes on one DC propagate to all others

**Authentication Protocols:**
- **Kerberos:** Primary protocol for Windows domain authentication
- **NTLM:** Legacy protocol (being deprecated)
- **LDAP/S:** Secure directory queries

**Kerberos in AD:**
1. User enters password on Windows login
2. Client requests Ticket Granting Ticket (TGT) from KDC
3. KDC verifies password hash and issues TGT (valid ~10 hours)
4. When accessing a file server, client presents TGT and requests Service Ticket
5. File server validates Service Ticket and grants access

### Cloud Directory Architecture

Modern cloud directories differ from on-prem AD:

| Feature | On-Prem AD | Cloud Directory |
|---------|-----------|-----------------|
| Protocol | Kerberos + LDAP | SAML + OIDC + OAuth |
| Topology | Domain controllers | Globally distributed |
| Scaling | Add more DCs | Auto-scaling |
| Integration | Windows-centric | Cross-platform, API-first |

### Directory Synchronization

Most enterprises use **hybrid identity** — both on-prem AD and cloud directory:

```
On-Prem AD ──→ Azure AD Connect ──→ Azure AD / Entra ID
```

**Sync options:**
- **Password Hash Sync:** Copies password hashes to cloud
- **Pass-through Authentication:** Cloud forwards auth to on-prem
- **Federation:** On-prem AD FS handles all authentication

---

## Where You See It

| Product | Role | Notes |
|---------|------|-------|
| **Active Directory** | Directory + authentication | Windows domain controller |
| **Azure AD Connect** | Sync engine | Bridges on-prem and cloud |
| **Okta** | Cloud IdP | SaaS SSO and MFA |
| **FreeIPA** | Open source IdP | Linux-centric alternative to AD |
| **OpenLDAP** | Directory server | Lightweight, customizable |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "AD is just a user database" | AD includes Group Policy, DNS, certificates, and Kerberos |
| "Cloud directories replace AD completely" | Most enterprises use hybrid identity for years |
| "LDAP is outdated" | LDAP remains the standard for directory queries |
| "Identity Provider = Directory Service" | The IdP uses the directory but adds authentication, tokens, and policies |

---

## How to Practice

1. **Query a directory**
   - If you have access to AD or LDAP, run a search query
   - Look up your own user entry and identify your attributes
   - Find your group memberships

2. **Observe Kerberos authentication**
   - On Windows, run `klist` to see your tickets
   - Notice the TGT and Service Tickets
   - Understand why tickets expire

3. **Run the simulations**
   - `ldap_simulator.py` demonstrates directory operations
   - `identity_sync_engine.py` shows hybrid synchronization

---

## Projects

### `ldap_simulator.py`
Simulates LDAP directory operations:
- Directory tree with users, groups, and OUs
- Bind authentication with password verification
- Search with filters and attribute selection
- Add, modify, and delete operations

### `identity_sync_engine.py`
Simulates directory synchronization:
- Source directory (on-prem AD)
- Target directory (cloud IdP)
- Detects changes and syncs with conflict resolution

### `idp_token_issuer.py`
Simulates an Identity Provider token service:
- User authentication
- SAML assertion generation
- JWT/ID token issuance
- Token validation endpoint

### `directory_audit_tool.py`
Audits directory configurations:
- Identifies stale accounts
- Finds privileged group memberships
- Detects weak password policies

---

## Check Your Understanding

1. What is the difference between a directory service and an identity provider?
2. In LDAP, what is a Distinguished Name (DN)? Why is it important?
3. How does Kerberos authentication work in Active Directory? What is a TGT?
4. What are the three directory synchronization options in a hybrid identity setup?
5. Why might an organization choose a cloud directory over on-premises Active Directory?
