# 11. Identity Providers and Directory Services

## What Are Directory Services?

A **directory service** is a specialized database designed for storing and organizing information about users, computers, applications, and other resources in a hierarchical structure. It serves as the central repository for identity and access information in an organization.

An **Identity Provider (IdP)** is a system that authenticates users and issues security tokens (SAML assertions, JWTs, Kerberos tickets) that other systems can trust. The IdP relies on a directory service as its authoritative identity source.

Together, directory services and identity providers form the backbone of enterprise identity management.

---

## Why Learn This?

Every organization's identity infrastructure depends on directory services. Whether you work with:
- **Microsoft Active Directory** — 90%+ of enterprises
- **LDAP** — Unix systems, applications, network equipment
- **Cloud directories** — Azure AD, Google Cloud Identity, AWS Directory Service
- **Modern platforms** — Okta, Ping, ForgeRock

Understanding these systems is essential for:
- User provisioning and deprovisioning
- Authentication architecture
- Group and organizational management
- Integration with applications
- Troubleshooting login issues

---

## Core Concepts

### Directory Service Architecture

Directory services use a hierarchical tree structure:

```
                    dc=company,dc=com
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    ou=People       ou=Groups       ou=Computers
          │               │               │
    uid=alice         cn=Engineering    cn=SERVER01
    uid=bob           cn=Finance        cn=SERVER02
    uid=charlie       cn=Admins
```

**Key concepts:**
- **DIT (Directory Information Tree):** The hierarchical structure
- **DN (Distinguished Name):** Unique identifier for an entry (e.g., `uid=alice,ou=People,dc=company,dc=com`)
- **Entry:** A record in the directory representing a user, group, or resource
- **Attribute:** A property of an entry (e.g., `cn` = common name, `mail` = email, `uid` = user ID)
- **ObjectClass:** Defines what type of object an entry is and what attributes it can have

### Active Directory (AD)

Active Directory is Microsoft's directory service and the most widely deployed enterprise identity platform.

**AD Components:**

| Component | Description | Example |
|-----------|-------------|---------|
| **Domain** | Logical grouping of objects with common policies | `company.com` |
| **Forest** | Collection of one or more domains sharing a schema | All `company.com` and `subsidiary.company.com` |
| **Tree** | Hierarchy of domains within a forest | `us.company.com`, `eu.company.com` |
| **Organizational Unit (OU)** | Container for organizing objects | `OU=Engineering,DC=company,DC=com` |
| **Domain Controller (DC)** | Server running AD services | Authenticates users, enforces policies |
| **Global Catalog** | Partial replica of all objects in the forest | Enables cross-domain queries |

**AD Authentication Protocols:**
- **Kerberos:** Primary protocol for domain authentication (tickets, not passwords)
- **NTLM:** Legacy challenge-response protocol (being deprecated)
- **LDAP:** Directory query protocol (for applications)

**Group Policy:** AD can enforce security policies across all domain-joined computers:
- Password complexity requirements
- Account lockout thresholds
- Firewall settings
- Software installation
- Registry settings

### LDAP (Lightweight Directory Access Protocol)

LDAP is the protocol used to query and modify directory services.

**Common LDAP Operations:**

| Operation | Purpose | Example |
|-----------|---------|---------|
| **Bind** | Authenticate to the directory | `ldap_bind(dn, password)` |
| **Search** | Query for entries | Find all users in Engineering |
| **Compare** | Check if an attribute matches | Verify user is in a group |
| **Add** | Create a new entry | Add a new user account |
| **Modify** | Update an existing entry | Change a user's department |
| **Delete** | Remove an entry | Delete a terminated user's account |

**LDAP Filter Examples:**
```
(objectClass=user)                    → All user accounts
(&(objectClass=user)(department=Engineering))  → Engineering users
(|(department=Sales)(department=Marketing))     → Sales OR Marketing
(!(userAccountControl:1.2.840.113556.1.4.803:=2))  → Enabled accounts only
```

### Azure Active Directory (Azure AD / Entra ID)

Azure AD is Microsoft's cloud-based identity platform:

| Feature | On-Premises AD | Azure AD |
|---------|---------------|----------|
| Protocol | Kerberos, LDAP | SAML, OIDC, OAuth 2.0 |
| Authentication | Domain-joined | Cloud-based, any device |
| Structure | Domains, forests, OUs | Tenants, subscriptions |
| Group Policy | Extensive | Intune, Conditional Access |
| Federation | AD FS | Built-in SaaS app gallery |
| MFA | Third-party | Built-in |
| Conditional Access | Limited | Rich (location, device, risk) |

**Azure AD Concepts:**
- **Tenant:** An organization's instance of Azure AD
- **Subscription:** Billing boundary for Azure resources
- **Conditional Access:** Dynamic access policies based on signals
- **Identity Protection:** Risk-based detection and remediation

### Hybrid Identity

Most enterprises operate both on-premises AD and cloud identity:

**Synchronization:**
- **Azure AD Connect:** Syncs on-premises AD users/groups to Azure AD
- **Password Hash Synchronization (PHS):** Hashes synced to cloud; users can authenticate with same password
- **Pass-through Authentication (PTA):** Password validation sent back to on-premises AD
- **Federation (AD FS):** Authentication redirected to on-premises AD FS

**When each is used:**
- PHS: Most common, simple, provides seamless SSO
- PTA: Preferred when password policies must be enforced on-premises
- Federation: When additional authentication requirements or third-party MFA

---

## How It Works

### Kerberos Authentication

Kerberos is the primary authentication protocol in Active Directory:

```
Phase 1: Authentication Service Exchange (AS-REQ / AS-REP)
┌────────┐                              ┌──────────────┐
│ Client │  "I am Alice"               │ Kerberos KDC │
│        │─────────────────────────────→│ (Key Dist.   │
│        │  Receive: TGT (Ticket       │   Center)    │
│        │←─────────────────────────────│              │
│        │    Granting Ticket)          │              │
└────────┘                              └──────────────┘

Phase 2: Ticket Granting Service Exchange (TGS-REQ / TGS-REP)
┌────────┐                              ┌──────────────┐
│ Client │  "TGT + I want FileServer"  │ Kerberos KDC │
│        │─────────────────────────────→│              │
│        │  Receive: Service Ticket     │              │
│        │←─────────────────────────────│              │
└────────┘                              └──────────────┘

Phase 3: Application Request (AP-REQ / AP-REP)
┌────────┐                              ┌────────────┐
│ Client │  "Service Ticket"            │ FileServer │
│        │─────────────────────────────→│            │
│        │  Authenticated! Access       │            │
│        │←─────────────────────────────│            │
└────────┘                              └────────────┘
```

**Why Kerberos is secure:**
- Passwords are NEVER transmitted over the network
- Tickets have limited lifetime (typically 10 hours)
- Mutual authentication (client verifies server, server verifies client)
- Forwardable tickets enable delegation with restrictions

### LDAP Query Flow

```
Application needs to verify user membership
           │
           ▼
    LDAP Search Request
    Base: dc=company,dc=com
    Filter: (&(uid=alice)(memberOf=cn=Engineering,ou=Groups,dc=company,dc=com))
           │
           ▼
    ┌─────────────┐
    │ LDAP Server │
    │ (OpenLDAP,  │
    │  AD, etc.)  │
    └─────────────┘
           │
           ▼
    LDAP Search Result:
    - Entry found / not found
    - Attributes requested
```

### Directory Replication

In multi-domain-controller environments, directory changes must replicate:
- **Intra-site replication:** Within a site (LAN), frequent (seconds)
- **Inter-site replication:** Between sites (WAN), scheduled (minutes to hours)
- **Conflict resolution:** Last-writer-wins or attribute-specific rules
- **Replication topology:** Ring-based with shortcuts for efficiency

---

## Where You See It

| Product | Type | Use Case |
|---------|------|----------|
| **Active Directory** | On-premises directory | Windows domain authentication, Group Policy |
| **Azure AD (Entra ID)** | Cloud directory | Microsoft 365, Azure, SaaS SSO |
| **OpenLDAP** | Open-source directory | Unix systems, custom applications |
| **Okta** | Cloud IdP | Workforce and customer identity |
| **Ping Identity** | Enterprise IdP | Large-scale federation |
| **FreeIPA** | Open-source IdP/directory | Linux enterprise identity |
| **AWS Directory Service** | Managed AD | AWS workloads needing AD |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Active Directory is just for authentication" | AD is also used for authorization (group membership), device management (Group Policy), DNS, certificate services, and more. |
| "LDAP and Active Directory are the same" | LDAP is a protocol. Active Directory is Microsoft's directory service that uses LDAP as one of its protocols. |
| "Cloud directories replace on-premises AD" | Most organizations use hybrid identity. Azure AD Connect syncs on-premises AD to Azure AD. Full migration is rare. |
| "Directory services are just databases" | Directory services have specialized schemas, replication, hierarchical organization, and authentication protocols that general databases do not provide. |
| "Kerberos is outdated" | Kerberos remains the most secure authentication protocol for domain environments. NTLM is outdated; Kerberos is not. |

---

## How to Practice

### Exercise 1: Explore Active Directory
If you have access to an AD environment:
1. Open Active Directory Users and Computers
2. Explore the OU structure
3. Find a user and examine their attributes
4. Check group memberships
5. View Group Policy Objects (GPOs)
6. Run `gpresult /r` to see applied policies

### Exercise 2: LDAP Queries
Using an LDAP browser (Apache Directory Studio, JXplorer) or command line:
1. Connect to a directory server
2. Search for all users
3. Search for users in a specific department
4. Search for disabled accounts
5. Compare filter results with different operators (&, |, !)

### Exercise 3: Design Hybrid Identity
An organization has:
- 5,000 on-premises AD users
- Microsoft 365 tenant
- 3 SaaS applications
- VPN for remote access

Design the hybrid identity architecture:
- Which sync method? (PHS, PTA, Federation)
- MFA implementation?
- Conditional Access policies?
- What stays on-premises vs. moves to cloud?

### Exercise 4: Run the Simulations
- `ldap_simulator.py` — Directory queries and authentication
- `ad_group_policy_analyzer.py` — Group Policy evaluation
- `identity_sync_engine.py` — Cross-directory synchronization

---

## Projects

### `ldap_simulator.py`
Simulates LDAP directory operations:
- Directory tree with hierarchical structure
- LDAP search with filter parsing
- Bind authentication simulation
- Add, modify, and delete operations
- OU and group membership queries

### `ad_group_policy_analyzer.py`
Analyzes Active Directory Group Policy:
- Parses GPO settings
- Detects security policy conflicts
- Maps policy to organizational units
- Identifies weak password policies
- Recommends hardening

### `identity_sync_engine.py`
Simulates cross-directory synchronization:
- Source directory (on-premises AD)
- Target directory (cloud IdP)
- Synchronization rules and attribute mapping
- Conflict detection and resolution
- Delta sync simulation

---

## Check Your Understanding

1. What is the difference between a directory service and an identity provider? How do they work together?
2. Draw the Active Directory hierarchy showing: forest, tree, domain, organizational unit, and domain controller. How do objects flow between these containers?
3. What are the three phases of Kerberos authentication? What is exchanged in each phase and why is no password sent over the network?
4. Compare Password Hash Synchronization, Pass-through Authentication, and Federation as hybrid identity methods. When would you use each?
5. Write LDAP filters for: (a) all users in the Engineering department, (b) all disabled accounts, (c) users who are members of either the Admin or Manager group.
6. Why is Kerberos considered more secure than NTLM? Describe the specific weaknesses of NTLM that Kerberos addresses.
7. An organization is migrating from on-premises AD to Azure AD. What objects and configurations must be considered? What cannot be directly migrated?
8. Explain how Group Policy works. How does a domain-joined computer know which policies to apply? What happens if policies conflict?
9. What is the purpose of the Global Catalog in Active Directory? When would a query use the Global Catalog instead of a local domain controller?
10. Design a directory service architecture for a multinational corporation with 50,000 employees across 20 countries. Consider replication, authentication, and administration.
