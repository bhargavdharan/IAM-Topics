# 11. Identity Providers and Directory Services

## 🏠 Real-World Analogy: The Phone Company

Imagine the world before mobile phones:

- Everyone had a landline connected to a central phone company
- The phone company maintained a **massive directory** of all customers
- When you wanted to call someone, the directory helped route your call
- The phone company knew your name, address, phone number, and service plan
- They could add new customers, disconnect service, or update your address
- Other companies (like emergency services) could query the directory for legitimate purposes

**Directory services are the "phone company" of enterprise IT — the central source of truth for who everyone is.**

---

## 📋 Overview

Identity Providers (IdPs) and Directory Services are the foundation of enterprise IAM. They store user identities, credentials, group memberships, and attributes — then make this information available to applications and services.

**Why directories matter:**
- Centralized user management (create once, use everywhere)
- Single source of truth for identity data
- Standardized access for applications
- Foundation for SSO, RBAC, and ABAC

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- Explain directory services with real-world analogies
- Understand LDAP, Active Directory, and cloud directories
- Describe how IdPs authenticate users and issue tokens
- Compare on-premises and cloud identity providers
- Implement a basic LDAP simulator

---

## 📚 Key Concepts

### Directory Service Types

| Service | Vendor | Deployment | Best For |
|---------|--------|-----------|----------|
| **Active Directory (AD)** | Microsoft | On-premises | Windows-centric enterprises |
| **Azure AD / Entra ID** | Microsoft | Cloud | Microsoft 365, hybrid organizations |
| **LDAP (OpenLDAP)** | Open Source | On-premises | Unix/Linux environments |
| **Google Cloud Identity** | Google | Cloud | Google Workspace organizations |
| **Okta** | Okta | Cloud | SaaS application integration |
| **Ping Identity** | Ping | Cloud/Hybrid | Enterprise federation |

### Directory Structure

Directories use a **hierarchical tree** structure (like a family tree or file system):

```
dc=example,dc=com                    ← Root (domain)
├── ou=Users                         ← Organizational Unit: Users
│   ├── uid=alice                    ← User Alice
│   │   ├── cn=Alice Smith
│   │   ├── mail=alice@example.com
│   │   ├── userPassword={SSHA}...
│   │   └── memberOf=cn=Engineering,ou=Groups,dc=example,dc=com
│   ├── uid=bob
│   └── uid=charlie
├── ou=Groups                        ← Organizational Unit: Groups
│   ├── cn=Engineering               ← Group: Engineering
│   │   └── member=uid=alice,ou=Users,dc=example,dc=com
│   ├── cn=Finance
│   └── cn=Admins
├── ou=Computers                     ← Organizational Unit: Computers
│   ├── cn=workstation-alice
│   └── cn=server-prod-01
└── ou=ServiceAccounts               ← Organizational Unit: Service Accounts
    └── cn=backup-service
```

**Key terms:**
- **DN (Distinguished Name):** Unique identifier: `uid=alice,ou=Users,dc=example,dc=com`
- **OU (Organizational Unit):** Folder for grouping objects
- **DC (Domain Component):** Part of the domain name
- **CN (Common Name):** Display name

### LDAP Operations

LDAP (Lightweight Directory Access Protocol) is the standard for querying directories:

| Operation | Description | Example |
|-----------|-------------|---------|
| **Bind** | Authenticate to directory | Log in with username/password |
| **Search** | Query for entries | "Find all users in Engineering" |
| **Compare** | Check attribute value | "Is Alice's department Finance?" |
| **Add** | Create new entry | Add new employee |
| **Modify** | Update existing entry | Change user's phone number |
| **Delete** | Remove entry | Remove departed employee |

### Identity Provider Functions

An IdP does more than just store identities:

```
┌─────────────────────────────────────────┐
│           Identity Provider             │
├─────────────────────────────────────────┤
│  1. Authentication Engine               │
│     - Verify passwords                  │
│     - Handle MFA                        │
│     - Support federated login           │
├─────────────────────────────────────────┤
│  2. Token Service                       │
│     - Issue SAML assertions             │
│     - Issue JWT/OAuth tokens            │
│     - Manage token lifecycle            │
├─────────────────────────────────────────┤
│  3. User Store / Directory              │
│     - Store identities and attributes   │
│     - Manage group memberships          │
│     - Sync with HR systems              │
├─────────────────────────────────────────┤
│  4. Policy Engine                       │
│     - Password policies                 │
│     - Access policies                   │
│     - MFA requirements                  │
├─────────────────────────────────────────┤
│  5. Audit & Reporting                   │
│     - Log all authentication events     │
│     - Generate compliance reports       │
│     - Detect anomalies                  │
└─────────────────────────────────────────┘
```

---

## 🔧 Under the Hood

### How LDAP Authentication Works

1. **Bind Request:** Client sends username (DN) and password
2. **Password Retrieval:** Directory retrieves stored password hash
3. **Comparison:** Directory hashes the submitted password and compares
4. **Result:** Success (bind succeeds) or InvalidCredentials

```python
# Conceptual LDAP authentication
def ldap_authenticate(user_dn, password):
    # Search for user
    user_entry = directory.search(base_dn, filter=f"(dn={user_dn})")
    
    if not user_entry:
        return False  # User not found
    
    stored_hash = user_entry.userPassword
    submitted_hash = hash_password(password)
    
    return stored_hash == submitted_hash
```

### Active Directory Under the Hood

AD is more than just LDAP — it's a comprehensive identity platform:

**Core Components:**
- **Domain Controllers (DCs):** Servers that authenticate users and replicate data
- **Global Catalog:** Index of all objects across the forest (for fast searches)
- **Sites:** Physical network locations for optimized replication
- **Replication:** Changes on one DC propagate to all others

**Authentication Protocols:**
- **Kerberos:** Primary protocol for Windows domain authentication
- **NTLM:** Legacy protocol (less secure, being deprecated)
- **LDAP/S:** LDAP over TLS for secure directory queries

**Kerberos in AD:**
1. User enters password on Windows login
2. Client requests Ticket Granting Ticket (TGT) from Key Distribution Center (KDC)
3. KDC verifies password hash and issues TGT (valid for ~10 hours)
4. When accessing a file server, client presents TGT and requests Service Ticket
5. File server validates Service Ticket and grants access

**Group Policy:**
- Centralized configuration management
- Apply settings based on OU membership
- Example: "All computers in Engineering OU require BitLocker encryption"

### Cloud Directory Architecture

Modern cloud directories (Azure AD, Okta) differ from on-prem AD:

| Feature | On-Prem AD | Cloud Directory |
|---------|-----------|-----------------|
| **Protocol** | Kerberos + LDAP | SAML + OIDC + OAuth |
| **Topology** | Domain controllers in data centers | Globally distributed cloud servers |
| **Scaling** | Add more DCs | Auto-scaling |
| **Integration** | Windows-centric | Cross-platform, API-first |
| **Password** | Hash stored in AD | Can be passwordless |

### Directory Synchronization

Most enterprises use **hybrid identity** — both on-prem AD and cloud directory:

```
On-Prem AD ──→ Azure AD Connect ──→ Azure AD / Entra ID
     │                │                    │
     │           Sync engine          Cloud apps
     │           (password hash       (Office 365,
     │            sync or SSO)         Salesforce, etc.)
```

**Sync options:**
- **Password Hash Sync:** Copies password hashes to cloud (allows cloud auth)
- **Pass-through Authentication:** Cloud forwards auth to on-prem AD
- **Federation (AD FS):** On-prem AD FS handles all authentication

---

## 🛠️ Projects in This Module

### `ldap_simulator.py`
Simulates LDAP directory operations:
- Directory tree with users, groups, and OUs
- Bind authentication with password verification
- Search with filters and attribute selection
- Add, modify, and delete operations
- Group membership queries

### `identity_sync_engine.py`
Simulates directory synchronization:
- Source directory (on-prem AD)
- Target directory (cloud IdP)
- Detects changes (adds, updates, deletes)
- Syncs with conflict resolution
- Generates sync reports

### `idp_token_issuer.py`
Simulates an Identity Provider token service:
- User authentication
- SAML assertion generation
- JWT/ID token issuance
- Token validation endpoint
- Session management

### `directory_audit_tool.py`
Audits directory configurations:
- Identifies stale accounts (no login for 90 days)
- Finds privileged group memberships
- Detects weak password policies
- Reports on group nesting depth
- Exports user access reports

---

## 📝 Quiz Questions

1. **What is the difference between a directory service and an identity provider?**
2. **In LDAP, what is a Distinguished Name (DN)? Why is it important?**
3. **How does Kerberos authentication work in Active Directory? What is a TGT?**
4. **What are the three directory synchronization options in a hybrid identity setup?**
5. **Why might an organization choose a cloud directory over on-premises Active Directory?**

---

## 🔗 Further Reading

- [LDAP Wiki](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol)
- [Active Directory Documentation](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview)
- [Azure AD Architecture](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-architecture)

---

## 🏷️ Tags
`#DirectoryServices` `#LDAP` `#ActiveDirectory` `#IdentityProvider` `#AzureAD` `#Kerberos` `#HybridIdentity`
